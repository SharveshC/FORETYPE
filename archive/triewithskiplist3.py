import curses
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import random

# ------------------ SKIP LIST ------------------
class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key  # negative frequency for max behavior
        self.value = value  # encrypted word
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):
        self.header = SkipListNode(None, None, SkipList.MAX_LEVEL)
        self.level = 0

    def random_level(self):
        lvl = 0
        while random.random() < SkipList.P and lvl < SkipList.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key, value):
        update = [None] * (SkipList.MAX_LEVEL + 1)
        current = self.header

        # FIX APPLIED HERE: Changed '>' to '<'
        # We want a MIN-list for the negative keys (-10, -5), so -10 (highest freq) comes first.
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl

        node = SkipListNode(key, value, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def top_k(self, k):
        result = []
        current = self.header.forward[0]
        while current and len(result) < k:
            result.append(current.value)
            current = current.forward[0]
        return result

# ------------------ TRIE CLASSES ------------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.encrypted_word = None
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, encrypted_word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.encrypted_word = encrypted_word
        node.frequency = 0

    def search_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def dfs_collect(self, node, collector):
        if node.is_end_of_word:
            collector.append((node.encrypted_word, node.frequency))
        for child in node.children.values():
            self.dfs_collect(child, collector)

# ------------------ ENCRYPTED TRIE ------------------
# Key generation outside the class remains fine
key = RSA.generate(2048)
public_key = key.publickey()
cipher = PKCS1_OAEP.new(public_key)
decipher = PKCS1_OAEP.new(key)

class EncryptedTrie:
    def __init__(self, public_key, decipher):
        self.trie = Trie()
        self.public_key = public_key
        self.decipher = decipher

    def encrypt_word(self, word):
        # NOTE: This assumes the word is short enough for the RSA key size.
        return cipher.encrypt(word.encode())

    def decrypt_word(self, encrypted_word):
        return self.decipher.decrypt(encrypted_word).decode()

    def insert_encrypted(self, word):
        encrypted_word = self.encrypt_word(word)
        self.trie.insert(word, encrypted_word)

    def autocomplete_encrypted(self, prefix, k=10):
        node = self.trie.search_node(prefix)
        if not node:
            return []

        # Collect all words under this prefix
        matches = []
        self.trie.dfs_collect(node, matches)

        # Build skiplist based on current frequencies
        temp_skip = SkipList()
        for encrypted_word, freq in matches:
            # Insert using negative frequency to get max-heap behavior
            temp_skip.insert(-freq, encrypted_word) 

        return temp_skip.top_k(k)

    def increase_word_frequency(self, word):
        node = self.trie.search_node(word)
        if node and node.is_end_of_word:
            node.frequency += 1

# ------------------ HELPER FUNCTIONS ------------------
def client_decrypt_suggestions(suggestions, decipher):
    return [decipher.decrypt(encrypted_word).decode() for encrypted_word in suggestions]

def menu_select(stdscr, items):
    curses.curs_set(0)
    current_row = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "--- Suggestions ---")
        for idx, item in enumerate(items):
            if idx == current_row:
                stdscr.addstr(idx + 1, 2, " " + item + " ", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 2, " " + item + " ")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(items) - 1:
            current_row += 1
        elif key in (ord('\n'), 10, 13):
            return items[current_row]
        elif key == 27:
            return None

def inputStr(stdscr, encrypted_trie, decipher):
    input_str = []
    cursor_x = 0
    
    while True:
        stdscr.clear()
        
        # Display the current input text
        current_text = "".join(input_str)
        stdscr.addstr(1, 2, "Enter text (Press Tab/Enter for autocomplete, ESC to exit):")
        stdscr.addstr(2, 2, "> " + current_text)
        
        # Display current suggestions
        prefix = current_text.split()[-1] if current_text else ""
        if prefix:
            encrypted_suggestions = encrypted_trie.autocomplete_encrypted(prefix)
            if encrypted_suggestions:
                decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
                stdscr.addstr(4, 2, "Suggestions (Type Tab to Select):")
                for i, suggestion in enumerate(decrypted_suggestions):
                    stdscr.addstr(5 + i, 2, f"  {suggestion}")
        
        stdscr.move(2, cursor_x + 4)
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:  # ESC
            return ""
        elif key in (curses.KEY_BACKSPACE, 127):
            if cursor_x > 0:
                cursor_x -= 1
                input_str.pop(cursor_x)
        elif key == curses.KEY_LEFT:
            if cursor_x > 0:
                cursor_x -= 1
        elif key == curses.KEY_RIGHT:
            if cursor_x < len(input_str):
                cursor_x += 1
        
        # Handle Autocomplete Selection
        elif key == ord('\t'):
            prefix = current_text.split()[-1] if current_text else ""
            encrypted_suggestions = encrypted_trie.autocomplete_encrypted(prefix)
            
            if encrypted_suggestions:
                decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
                
                # Show menu and get selection
                selected_word = menu_select(stdscr, decrypted_suggestions)
                
                if selected_word:
                    # Replace the current partial word with the selected word
                    if current_text.endswith(prefix):
                        new_text = current_text[:-len(prefix)] + selected_word
                    else:
                        new_text = selected_word # Should only happen if text is empty
                        
                    input_str = list(new_text)
                    cursor_x = len(input_str)
        
        elif 32 <= key <= 126:
            input_str.insert(cursor_x, chr(key))
            cursor_x += 1

        # Final input return
        if key in (10, 13):
            return "".join(input_str)

# ------------------ MAIN FUNCTION ------------------
def main(stdscr):
    # Setup curses environment
    curses.echo()
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)
    curses.curs_set(1)

    encrypted_trie = EncryptedTrie(public_key, decipher)

    predefined_words = ["the", "of", "and", "to", "in", "for", "is", "on", "that", "by",
                        "this", "with", "you", "it", "not", "or", "be", "are", "from", "at",
                        "cat", "case", "online", "only", "category", "apple", "app", "application"]

    for word in predefined_words:
        encrypted_trie.insert_encrypted(word)

    stdscr.addstr(1, 2, f"{len(predefined_words)} predefined words have been inserted into the Trie.")
    stdscr.addstr(2, 2, "Press any key to start typing...")
    stdscr.getch()

    while True:
        stdscr.clear()
        
        # CORRECTED LOGIC: inputStr handles all typing and selection.
        # It returns the final, complete word/string.
        final_input = inputStr(stdscr, encrypted_trie, decipher)

        if final_input == "":
            break # ESC was pressed

        # We assume the user finalized a single word for simplicity.
        # If the user typed a sentence, you might process the last word.
        # For this example, we'll try to increase frequency of the last word entered.
        words = final_input.split()
        word_to_update = words[-1] if words else None
        
        stdscr.clear()
        
        if word_to_update:
            # Increase the frequency of the word the user committed to.
            # This makes the ranking persistent for the next session.
            encrypted_trie.increase_word_frequency(word_to_update)
            stdscr.addstr(1, 2, f"Final Input: '{final_input}'")
            stdscr.addstr(2, 2, f"Frequency of '{word_to_update}' increased for future suggestions.")
        else:
            stdscr.addstr(1, 2, "Input finalized, but no word was entered.")

        stdscr.addstr(4, 2, "Press any key to continue to the next input or ESC to quit.")
        stdscr.getch()

# ------------------ RUN ------------------
if __name__ == "__main__":
    curses.wrapper(main)

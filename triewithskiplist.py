import curses
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import random

# ------------------ SKIP LIST ------------------
class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key  # frequency (negative for max behavior)
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

        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key > key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]
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

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

# ------------------ ENCRYPTED TRIE ------------------
key = RSA.generate(2048)
public_key = key.publickey()
cipher = PKCS1_OAEP.new(public_key)
decipher = PKCS1_OAEP.new(key)

class EncryptedTrie(Trie):
    def __init__(self, public_key, decipher):
        super().__init__()
        self.public_key = public_key
        self.decipher = decipher
        self.skiplist = SkipList()

    def encrypt_word(self, word):
        return cipher.encrypt(word.encode())

    def decrypt_word(self, encrypted_word):
        return self.decipher.decrypt(encrypted_word).decode()

    def insert_encrypted(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.encrypted_word = self.encrypt_word(word)
        node.frequency = 0

    def autocomplete_encrypted(self, prefix):
        node = self.search(prefix)
        if not node:
            return []
        suggestions = []
        self._dfs_encrypted(node, suggestions)
        # Insert into skip list based on frequency (negative for max behavior)
        for encrypted_word, freq in suggestions:
            self.skiplist.insert(-freq, encrypted_word)
        return self.skiplist.top_k(len(suggestions))

    def _dfs_encrypted(self, node, suggestions):
        if node.is_end_of_word:
            suggestions.append((node.encrypted_word, node.frequency))
        for child in node.children.values():
            self._dfs_encrypted(child, suggestions)

    def increase_word_frequency(self, word):
        node = self.search(word)
        if node and node.is_end_of_word:
            node.frequency += 1
            self.skiplist.insert(-node.frequency, node.encrypted_word)

# ------------------ HELPER FUNCTIONS ------------------
def client_decrypt_suggestions(suggestions, decipher):
    return [decipher.decrypt(encrypted_word).decode() for encrypted_word in suggestions]

def menu_select(stdscr, items):
    curses.curs_set(0)
    current_row = 0
    while True:
        stdscr.clear()
        for idx, item in enumerate(items):
            if idx == current_row:
                stdscr.addstr(idx + 1, 2, " "+item+" ", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 2, " "+item+" ")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(items) - 1:
            current_row += 1
        elif key == ord('\n'):
            return items[current_row]
        elif key == 27:
            return None

def inputStr(stdscr, encrypted_trie, decipher):
    input_str = []
    cursor_x = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Enter text (Press Enter or Tab for autocomplete, ESC to exit):")
        stdscr.addstr(2, 2, "> " + "".join(input_str) + " ")
        stdscr.move(2, cursor_x + 4)
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:
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
        elif key in (ord('\n'), ord('\t')):
            prefix = "".join(input_str)
            encrypted_suggestions = encrypted_trie.autocomplete_encrypted(prefix)
            if encrypted_suggestions:
                decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
                selected_word = menu_select(stdscr, decrypted_suggestions)
                if selected_word:
                    input_str = list(selected_word)
                    cursor_x = len(input_str)
        elif 32 <= key <= 126:
            input_str.insert(cursor_x, chr(key))
            cursor_x += 1

        if key == ord('\n'):
            return "".join(input_str)

# ------------------ MAIN FUNCTION ------------------
def main(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)

    encrypted_trie = EncryptedTrie(public_key, decipher)

    predefined_words = ["the", "of", "and", "to", "in", "for", "is", "on", "that", "by",
                        "this", "with", "you", "it", "not", "or", "be", "are", "from", "at",
                        "cat", "case", "online", "only", "category"]

    for word in predefined_words:
        encrypted_trie.insert_encrypted(word)

    stdscr.addstr(1, 2, f"{len(predefined_words)} predefined words have been inserted into the Trie.")
    stdscr.getch()

    while True:
        stdscr.clear()
        curses.curs_set(1)
        prefix = inputStr(stdscr, encrypted_trie, decipher)

        if prefix == "":
            break

        encrypted_suggestions = encrypted_trie.autocomplete_encrypted(prefix)
        if not encrypted_suggestions:
            stdscr.addstr(3, 2, f"No suggestions found for prefix '{prefix}'")
            stdscr.getch()
            continue

        decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
        selected_word = menu_select(stdscr, decrypted_suggestions)
        curses.curs_set(1)

        stdscr.clear()
        if selected_word in decrypted_suggestions:
            encrypted_trie.increase_word_frequency(selected_word)
            stdscr.addstr(1, 2, f"Frequency of '{selected_word}' increased.")
            stdscr.getch()

# ------------------ RUN ------------------
if __name__ == "__main__":
    curses.wrapper(main)

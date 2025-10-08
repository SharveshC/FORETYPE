import curses, heapq
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
        self.max_heap = []

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
        self.max_heap = []
        suggestions = []
        self._dfs_encrypted(node, suggestions)
        sorted_suggestions = heapq.nlargest(len(suggestions), self.max_heap, key=lambda x: -x[0])
        unique_encrypted_words = []
        seen_words = set()
        for _, encrypted_word in sorted_suggestions:
            if encrypted_word not in seen_words:
                unique_encrypted_words.append(encrypted_word)
                seen_words.add(encrypted_word)
        return unique_encrypted_words

    def _dfs_encrypted(self, node, suggestions):
        if node.is_end_of_word:
            suggestions.append((node.encrypted_word, node.frequency))
            heapq.heappush(self.max_heap, (-node.frequency, node.encrypted_word))
        for char, child in node.children.items():
            self._dfs_encrypted(child, suggestions)

    def increase_word_frequency(self, word):
        node = self.search(word)
        if node and node.is_end_of_word:
            node.frequency += 1
            heapq.heappush(self.max_heap, (-node.frequency, node.encrypted_word))

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
        elif key == 27:  # ESC cancels menu
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

        if key == 27:  # ESC exits
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
        elif key in (ord('\n'), ord('\t')):  # Enter or Tab triggers menu
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

        # Always return the typed input when user presses Enter after selection
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
                        "cat", "case", "online", "only", "category"]  # Add more words as needed

    for word in predefined_words:
        encrypted_trie.insert_encrypted(word)

    stdscr.addstr(1, 2, f"{len(predefined_words)} predefined words have been inserted into the Trie.")
    stdscr.getch()

    while True:
        stdscr.clear()
        curses.curs_set(1)
        prefix = inputStr(stdscr, encrypted_trie, decipher)

        if prefix == "":  # ESC pressed
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

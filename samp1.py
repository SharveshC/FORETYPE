import curses
import heapq
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# ------------------ BST Node ------------------
class BSTNode:
    def __init__(self, word, encrypted_word):
        self.word = word
        self.encrypted_word = encrypted_word
        self.frequency = 0
        self.left = None
        self.right = None


# ------------------ BST Class ------------------
class EncryptedBST:
    def __init__(self, public_key, decipher):
        self.root = None
        self.public_key = public_key
        self.decipher = decipher

    def encrypt_word(self, word):
        return cipher.encrypt(word.encode())

    def decrypt_word(self, encrypted_word):
        return self.decipher.decrypt(encrypted_word).decode()

    def insert(self, word):
        encrypted_word = self.encrypt_word(word)
        self.root = self._insert(self.root, word, encrypted_word)

    def _insert(self, node, word, encrypted_word):
        if not node:
            return BSTNode(word, encrypted_word)
        if word < node.word:
            node.left = self._insert(node.left, word, encrypted_word)
        elif word > node.word:
            node.right = self._insert(node.right, word, encrypted_word)
        return node

    def autocomplete_encrypted(self, prefix):
        results = []
        self._collect_with_prefix(self.root, prefix, results)
        # Sort by frequency (high first)
        results.sort(key=lambda x: -x[1])
        return [encrypted_word for encrypted_word, _ in results]

    def _collect_with_prefix(self, node, prefix, results):
        if not node:
            return
        if node.word.startswith(prefix):
            results.append((node.encrypted_word, node.frequency))
        self._collect_with_prefix(node.left, prefix, results)
        self._collect_with_prefix(node.right, prefix, results)

    def increase_frequency(self, word):
        node = self._search(self.root, word)
        if node:
            node.frequency += 1

    def _search(self, node, word):
        if not node:
            return None
        if word == node.word:
            return node
        elif word < node.word:
            return self._search(node.left, word)
        else:
            return self._search(node.right, word)


# ------------------ RSA Keys ------------------
key = RSA.generate(2048)
public_key = key.publickey()
cipher = PKCS1_OAEP.new(public_key)
decipher = PKCS1_OAEP.new(key)


# ------------------ Decryption ------------------
def client_decrypt_suggestions(suggestions, decipher):
    decrypted = []
    for encrypted_word in suggestions:
        word = decipher.decrypt(encrypted_word).decode()
        decrypted.append(word)
    return decrypted


# ------------------ Predefined Words ------------------
predefined_words = ["the", "of", "and", "to", "in", "for", "is", "on", "that", "by", "this", "with", "you", "it", "not",
    "or", "be", "are", "from", "at", "as", "your", "all", "have", "new", "more", "an", "was", "we", "will", "home",
    "can", "us", "about", "if", "page", "my", "has", "search", "free", "but", "our", "one", "other", "do", "no"]


# ------------------ Input Field ------------------
def inputStr(stdscr, bst, decipher):
    input_str = []
    cursor_x = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Enter text (Press Enter, ESC=cancel, Tab=autocomplete):")
        stdscr.addstr(2, 2, "> ")
        stdscr.addstr(2, 4, "".join(input_str) + " ")
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
        elif key == ord('\n'):
            return "".join(input_str)
        elif key == ord('\t'):  # Autocomplete
            prefix = "".join(input_str)
            encrypted_suggestions = bst.autocomplete_encrypted(prefix)
            if encrypted_suggestions:
                decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
                if decrypted_suggestions:
                    input_str = list(decrypted_suggestions[0])  # Most frequent
                    cursor_x = len(input_str)
        elif 32 <= key <= 126:  # Printable
            input_str.insert(cursor_x, chr(key))
            cursor_x += 1

    return ''.join(input_str)


# ------------------ Menu Selection ------------------
def menu_select(stdscr, items):
    curses.curs_set(0)
    current_row = 0
    while True:
        stdscr.clear()
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
        elif key == ord('\n'):
            return items[current_row]
        elif key == 27:
            break


# ------------------ Main ------------------
def main(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)

    bst = EncryptedBST(public_key, decipher)

    for word in predefined_words:
        bst.insert(word)

    stdscr.addstr(1, 2, f"{len(predefined_words)} predefined words inserted into BST.")
    stdscr.getch()

    while True:
        stdscr.clear()
        curses.curs_set(1)

        prefix = inputStr(stdscr, bst, decipher)
        if prefix.lower() == "exit":
            break

        encrypted_suggestions = bst.autocomplete_encrypted(prefix)
        if not encrypted_suggestions:
            stdscr.addstr(3, 2, f"No suggestions for prefix '{prefix}'")
            stdscr.getch()
            continue

        decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
        selected_word = menu_select(stdscr, decrypted_suggestions)

        stdscr.clear()
        if selected_word in decrypted_suggestions:
            bst.increase_frequency(selected_word)
            stdscr.addstr(1, 2, f"Frequency of '{selected_word}' increased.")
        else:
            stdscr.addstr(1, 2, "Word not found in suggestions or skipped.")
        stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)

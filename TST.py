import curses, heapq
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# ------------------ TST NODE ------------------
class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.eq = None
        self.right = None
        self.is_end_of_word = False
        self.encrypted_word = None
        self.frequency = 0

# ------------------ TST CLASS ------------------
class TernarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, word, encrypt_func):
        if not word:
            return
        self.root = self._insert(self.root, word, 0, encrypt_func)

    def _insert(self, node, word, index, encrypt_func):
        char = word[index]
        if not node:
            node = TSTNode(char)
        if char < node.char:
            node.left = self._insert(node.left, word, index, encrypt_func)
        elif char > node.char:
            node.right = self._insert(node.right, word, index, encrypt_func)
        else:
            if index + 1 < len(word):
                node.eq = self._insert(node.eq, word, index + 1, encrypt_func)
            else:
                node.is_end_of_word = True
                node.encrypted_word = encrypt_func(word)
                node.frequency = 0
        return node

    def search_prefix(self, prefix):
        return self._search(self.root, prefix, 0)

    def _search(self, node, prefix, index):
        if not node:
            return None
        char = prefix[index]
        if char < node.char:
            return self._search(node.left, prefix, index)
        elif char > node.char:
            return self._search(node.right, prefix, index)
        else:
            if index + 1 == len(prefix):
                return node
            return self._search(node.eq, prefix, index + 1)

# ------------------ ENCRYPTED TST ------------------
key = RSA.generate(2048)
public_key = key.publickey()
cipher = PKCS1_OAEP.new(public_key)
decipher = PKCS1_OAEP.new(key)

class EncryptedTST:
    def __init__(self, public_key, decipher):
        self.tst = TernarySearchTree()
        self.public_key = public_key
        self.decipher = decipher
        self.max_heap = []

    def encrypt_word(self, word):
        return cipher.encrypt(word.encode())

    def decrypt_word(self, encrypted_word):
        return self.decipher.decrypt(encrypted_word).decode()

    def insert_encrypted(self, word):
        self.tst.insert(word, self.encrypt_word)

    def autocomplete_encrypted(self, prefix):
        if not prefix:  # ✅ If prefix is empty, return nothing instead of crashing
            return []
        node = self.tst.search_prefix(prefix)
        if not node:
            return []
        self.max_heap = []
        suggestions = []
        if node.is_end_of_word:
            suggestions.append((node.encrypted_word, node.frequency))
            heapq.heappush(self.max_heap, (-node.frequency, node.encrypted_word))
        self._dfs_encrypted(node.eq, prefix, suggestions)
        sorted_suggestions = heapq.nlargest(len(suggestions), self.max_heap, key=lambda x: -x[0])
        unique_encrypted_words = []
        seen_words = set()
        for _, encrypted_word in sorted_suggestions:
            if encrypted_word not in seen_words:
                unique_encrypted_words.append(encrypted_word)
                seen_words.add(encrypted_word)
        return unique_encrypted_words

    def _dfs_encrypted(self, node, prefix, suggestions):
        if not node:
            return
        self._dfs_encrypted(node.left, prefix, suggestions)
        new_prefix = prefix + node.char
        if node.is_end_of_word:
            suggestions.append((node.encrypted_word, node.frequency))
            heapq.heappush(self.max_heap, (-node.frequency, node.encrypted_word))
        self._dfs_encrypted(node.eq, new_prefix, suggestions)
        self._dfs_encrypted(node.right, prefix, suggestions)

    def increase_word_frequency(self, word):
        node = self.tst.search_prefix(word)
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

def inputStr(stdscr, encrypted_tst, decipher):
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
        elif key in (curses.KEY_BACKSPACE, 127, 8):  # ✅ Universal backspace handling
            if cursor_x > 0:
                cursor_x -= 1
                input_str.pop(cursor_x)
        elif key == curses.KEY_LEFT:
            if cursor_x > 0:
                cursor_x -= 1
        elif key == curses.KEY_RIGHT:
            if cursor_x < len(input_str):
                cursor_x += 1
        elif key in (ord('\n'), ord('\t')):  # Enter or Tab triggers autocomplete
            prefix = "".join(input_str)
            encrypted_suggestions = encrypted_tst.autocomplete_encrypted(prefix)
            if encrypted_suggestions:
                decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
                selected_word = menu_select(stdscr, decrypted_suggestions)
                if selected_word:
                    input_str = list(selected_word)
                    cursor_x = len(input_str)
            if key == ord('\n'):  # Always return final word on Enter
                return "".join(input_str)
        elif 32 <= key <= 126:
            input_str.insert(cursor_x, chr(key))
            cursor_x += 1

# ------------------ MAIN FUNCTION ------------------
def main(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)

    encrypted_tst = EncryptedTST(public_key, decipher)

    predefined_words = [
        "the", "of", "and", "to", "in", "for", "is", "on", "that", "by",
        "this", "with", "you", "it", "not", "or", "be", "are", "from", "at",
        "cat", "case", "online", "only", "category"
    ]

    for word in predefined_words:
        encrypted_tst.insert_encrypted(word)

    stdscr.addstr(1, 2, f"{len(predefined_words)} predefined words have been inserted into the TST.")
    stdscr.getch()

    while True:
        stdscr.clear()
        curses.curs_set(1)
        prefix = inputStr(stdscr, encrypted_tst, decipher)

        if prefix == "":  # ESC pressed
            break

        encrypted_suggestions = encrypted_tst.autocomplete_encrypted(prefix)
        if not encrypted_suggestions:
            stdscr.addstr(3, 2, f"No suggestions found for prefix '{prefix}'")
            stdscr.getch()
            continue

        decrypted_suggestions = client_decrypt_suggestions(encrypted_suggestions, decipher)
        selected_word = menu_select(stdscr, decrypted_suggestions)
        curses.curs_set(1)

        stdscr.clear()
        if selected_word in decrypted_suggestions:
            encrypted_tst.increase_word_frequency(selected_word)
            stdscr.addstr(1, 2, f"Frequency of '{selected_word}' increased.")
            stdscr.getch()

# ------------------ RUN ------------------
if __name__ == "__main__":
    curses.wrapper(main)

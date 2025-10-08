import curses
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# ------------------ SKIP LIST ------------------
class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key        # ordering key (negative frequency -> larger freq first)
        self.value = value    # word string
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
        # Find place to insert (order by key desc, tie-break by value asc)
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and (
                current.forward[i].key > key or
                (current.forward[i].key == key and current.forward[i].value < value)
            ):
                current = current.forward[i]
            update[i] = current

        # Random level for new node
        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl

        node = SkipListNode(key, value, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def delete(self, key, value):
        update = [None] * (SkipList.MAX_LEVEL + 1)
        current = self.header
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and (
                current.forward[i].key > key or
                (current.forward[i].key == key and current.forward[i].value < value)
            ):
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]
        if current and current.key == key and current.value == value:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    continue
                update[i].forward[i] = current.forward[i]
            # Optionally lower self.level if top levels are empty
            while self.level > 0 and not self.header.forward[self.level]:
                self.level -= 1

    def top_k(self, k):
        result = []
        current = self.header.forward[0]
        while current and len(result) < k:
            result.append(current.value)
            current = current.forward[0]
        return result

# ------------------ TRIE ------------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None  # reference to the actual word string

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end_of_word = True
        node.word = word

    def search_node(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def dfs_collect(self, node, collector):
        if node is None:
            return
        if node.is_end_of_word and node.word is not None:
            collector.append(node.word)
        for child in node.children.values():
            self.dfs_collect(child, collector)

# ------------------ CRYPTO SETUP ------------------
key = RSA.generate(2048)
public_key = key.publickey()
cipher = PKCS1_OAEP.new(public_key)
decipher = PKCS1_OAEP.new(key)

# ------------------ ENCRYPTED AUTOCOMPLETE (Trie + SkipList) ------------------
class EncryptedTrie:
    def __init__(self, public_key, decipher):
        self.trie = Trie()
        self.public_key = public_key
        self.decipher = decipher
        self.encrypted_store = {}  # word -> encrypted bytes (single copy)
        self.frequency = {}        # word -> int

    def encrypt_word(self, word):
        # store single RSA-encrypted blob per word
        return cipher.encrypt(word.encode())

    def insert_encrypted(self, word):
        if word in self.encrypted_store:
            return
        self.trie.insert(word)
        self.encrypted_store[word] = self.encrypt_word(word)
        self.frequency[word] = 0

    def increase_word_frequency(self, word):
        if word in self.frequency:
            self.frequency[word] += 1

    def autocomplete_encrypted(self, prefix, k=10):
        node = self.trie.search_node(prefix)
        if not node:
            return []
        # collect words under prefix
        matches = []
        self.trie.dfs_collect(node, matches)
        if not matches:
            return []

        # Build a temporary skiplist only for matches to guarantee prefix-only suggestions
        temp_skip = SkipList()
        for w in matches:
            key = -self.frequency.get(w, 0)  # negative so larger freq appears first
            temp_skip.insert(key, w)

        top_words = temp_skip.top_k(k)
        # Return encrypted blobs in top order
        return [self.encrypted_store[w] for w in top_words]

# ------------------ HELPERS / UI ------------------
def client_decrypt_suggestions(suggestions, decipher):
    return [decipher.decrypt(enc).decode() for enc in suggestions]

def menu_select(stdscr, items):
    curses.curs_set(0)
    current_row = 0
    while True:
        stdscr.clear()
        for idx, item in enumerate(items):
            display = item
            if idx == current_row:
                stdscr.addstr(idx + 1, 2, " " + display + " ", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 2, " " + display + " ")
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
        elif key in (ord('\n'), ord('\t'), 10, 13):
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

        if key in (ord('\n'), 10, 13):
            return "".join(input_str)

# ------------------ MAIN ------------------
def main(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)

    encrypted_trie = EncryptedTrie(public_key, decipher)

    predefined_words = [
        "the", "of", "and", "to", "in", "for", "is", "on", "that", "by",
        "this", "with", "you", "it", "not", "or", "be", "are", "from", "at",
        "cat", "case", "online", "only", "category", "application", "app", "bat"
    ]

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
        if selected_word:
            encrypted_trie.increase_word_frequency(selected_word)
            stdscr.addstr(1, 2, f"Frequency of '{selected_word}' increased.")
            stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)

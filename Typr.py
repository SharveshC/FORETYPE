# CHANGE: Import 'pickle' for saving/loading the frequency dictionary
# and 'os' for checking if the file exists.
import pickle
import os

from pybloom_live import BloomFilter

# CHANGE: Define a constant for the filename to store frequencies.
# This makes it easy to change the filename later.
FREQUENCY_FILE = 'word_freq.pkl'

# ---------------- Trie Node ----------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None  # store full word

# ---------------- Trie ----------------
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.word = word

    def get_suggestions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        self._collect_words(node, results)
        return results

    def _collect_words(self, node, results):
        if node.is_end:
            results.append(node.word)
        for child in node.children.values():
            self._collect_words(child, results)

# ---------------- Autocomplete System ----------------
class AutoCompleteSystem:
    def __init__(self):
        self.trie = Trie()
        self.bloom = BloomFilter(capacity=1000, error_rate=0.01)
        self.load_frequencies()

        for word in self.word_freq.keys():
            self.trie.insert(word)
            for i in range(1, len(word) + 1):
                self.bloom.add(word[:i])

    def load_frequencies(self):
        """Loads the word frequency dictionary from a pickle file."""
        if os.path.exists(FREQUENCY_FILE):
            with open(FREQUENCY_FILE, 'rb') as f:
                self.word_freq = pickle.load(f)
        else:
            self.word_freq = {}

    def save_frequencies(self):
        """Saves the current word frequency dictionary to a pickle file."""
        with open(FREQUENCY_FILE, 'wb') as f:
            pickle.dump(self.word_freq, f)
            print(f"Word frequencies saved to '{FREQUENCY_FILE}'.")

    def add_word(self, word):
        if word not in self.word_freq:
            self.word_freq[word] = 0
        self.trie.insert(word)
        for i in range(1, len(word) + 1):
            self.bloom.add(word[:i])

    def get_suggestions(self, prefix):
        if prefix not in self.bloom:
            return []
        words = self.trie.get_suggestions(prefix)
        words.sort(key=lambda w: (-self.word_freq.get(w, 0), w))
        return words

    def select_word(self, word):
        if word in self.word_freq:
            self.word_freq[word] += 1

# ---------------- Main Program ----------------
def main():
    system = AutoCompleteSystem()

    # Preload dictionary
    words = ["cat", "car", "cart", "carbon", "case",
             "dog", "door", "dot", "dove", "data"]
    for w in words:
        # CHANGE: We only add a word from the default list if it's not
        # already in our loaded frequency dictionary. This prevents
        # resetting the frequency of these words every time the program runs.
        if w not in system.word_freq:
            system.add_word(w)

    print("Autocomplete system ready.")
    print("Type something and press Enter. Empty input exits.\n")

    # CHANGE: Use a try...finally block. The code in the 'finally'
    # part is guaranteed to run when the 'try' block is exited,
    # ensuring that we always save our data.
    try:
        while True:
            prefix = input("Enter prefix: ").strip()
            if prefix == "":
                break

            suggestions = system.get_suggestions(prefix)
            if not suggestions:
                print("No suggestions.")
                continue

            print("\nSuggestions (sorted by frequency):")
            for i, word in enumerate(suggestions, 1):
                # Use .get(w, 0) for safety in case a word exists in the trie
                # but somehow not in the frequency dict.
                freq = system.word_freq.get(word, 0)
                print(f"{i}. {word} (freq={freq})")

            choice = input("Select number to confirm word (Enter to skip): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(suggestions):
                    chosen = suggestions[idx]
                    system.select_word(chosen)
                    print(f"Selected: {chosen}, frequency now = {system.word_freq[chosen]}")
            print("")
    finally:
        # CHANGE: Call the save method when the program exits.
        system.save_frequencies()

if __name__ == "__main__":
    main()

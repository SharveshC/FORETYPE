import pickle
import os
from pybloom_live import BloomFilter

STATE_FILE = 'autocomplete_state.pkl'

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None

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

class AutoCompleteSystem:
    def __init__(self):
        self.trie = None
        self.bloom = None
        self.word_freq = None
        self.load_state()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'rb') as f:
                    state = pickle.load(f)
                    self.trie = state['trie']
                    self.bloom = state['bloom']
                    self.word_freq = state['freq']
                    print("Loaded saved state from file.")
                    return
            except Exception as e:
                print(f"Warning: Could not load state file. Starting fresh. Error: {e}")
        
        self.trie = Trie()
        self.bloom = BloomFilter(capacity=1000, error_rate=0.01)
        self.word_freq = {}
        print("No saved state found. Starting a new session.")


    def save_state(self):
        state = {
            'trie': self.trie,
            'bloom': self.bloom,
            'freq': self.word_freq
        }
        with open(STATE_FILE, 'wb') as f:
            pickle.dump(state, f)
            print(f"System state saved to '{STATE_FILE}'.")

    def add_word(self, word):
        if word not in self.word_freq:
            self.word_freq[word] = 0
            self.trie.insert(word)
            for i in range(1, len(word) + 1):
                self.bloom.add(word[:i])

    def get_suggestions(self, prefix):
        if not self.bloom or prefix not in self.bloom:
            return []
        words = self.trie.get_suggestions(prefix)
        words.sort(key=lambda w: (-self.word_freq.get(w, 0), w))
        return words

    def select_word(self, word):
        if word in self.word_freq:
            self.word_freq[word] += 1

def main():
    system = AutoCompleteSystem()

    if not system.word_freq:
        print("Preloading default dictionary...")
        words = ["cat", "car", "cart", "carbon", "case",
                 "dog", "door", "dot", "dove", "data"]
        for w in words:
            system.add_word(w)

    print("Autocomplete system ready.")
    print("Type something and press Enter. Empty input exits.\n")

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
        system.save_state()

if __name__ == "__main__":
    main()

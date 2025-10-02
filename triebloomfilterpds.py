from pybloom_live import BloomFilter

# ---------------- Persistent Counter ----------------
class PersistentCounter:
    def __init__(self, initial_value=0):
        self.value = initial_value

    def increment(self):
        return PersistentCounter(self.value + 1)

    def get(self):
        return self.value


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
        self._collect_words(node, prefix, results)
        return results

    def _collect_words(self, node, prefix, results):
        if node.is_end:
            results.append(node.word)
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)


# ---------------- Autocomplete System ----------------
class AutoCompleteSystem:
    def __init__(self):
        self.trie = Trie()
        self.word_freq = {}  # word -> PersistentCounter
        self.bloom = BloomFilter(capacity=1000, error_rate=0.01)

    def add_word(self, word):
        if word not in self.word_freq:
            self.word_freq[word] = PersistentCounter()
        self.trie.insert(word)
        for i in range(1, len(word) + 1):
            self.bloom.add(word[:i])

    def get_suggestions(self, prefix):
        if prefix not in self.bloom:
            return []
        words = self.trie.get_suggestions(prefix)
        # sort by frequency (descending), then alphabetically
        words.sort(key=lambda w: (-self.word_freq[w].get(), w))
        return words

    def select_word(self, word):
        if word in self.word_freq:
            self.word_freq[word] = self.word_freq[word].increment()


# ---------------- Main Program ----------------
def main():
    system = AutoCompleteSystem()

    # preload dictionary
    words = ["cat", "car", "cart", "carbon", "case",
             "dog", "door", "dot", "dove", "data"]
    for w in words:
        system.add_word(w)

    print("Autocomplete system ready.")
    print("Type something and press Enter. Empty input exits.\n")

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
            print(f"{i}. {word} (freq={system.word_freq[word].get()})")

        choice = input("Select number to confirm word (Enter to skip): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                chosen = suggestions[idx]
                system.select_word(chosen)
                print(f"Selected: {chosen}, frequency now = {system.word_freq[chosen].get()}")
        print("")


if __name__ == "__main__":
    main()

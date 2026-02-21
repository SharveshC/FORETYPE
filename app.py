import streamlit as st
import pickle
import os
from pybloom_live import BloomFilter

# Constants
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
            self.save_frequencies()

# ---------------- Streamlit UI ----------------
def main():
    st.set_page_config(
        page_title="Autocomplete Engine",
        page_icon="🔍",
        layout="centered"
    )
    
    st.title("🔍 Autocomplete Engine")
    st.markdown("Type a prefix and get intelligent suggestions based on frequency!")
    
    # Initialize the autocomplete system in session state
    if 'system' not in st.session_state:
        st.session_state.system = AutoCompleteSystem()
        
        # Preload dictionary
        words = ["cat", "car", "cart", "carbon", "case",
                 "dog", "door", "dot", "dove", "data",
                 "apple", "application", "apply", "approach", "appreciate",
                 "banana", "band", "bank", "base", "basic"]
        for w in words:
            if w not in st.session_state.system.word_freq:
                st.session_state.system.add_word(w)
    
    # Input section
    st.subheader("📝 Enter Prefix")
    prefix = st.text_input("Type your prefix here:", placeholder="Start typing...")
    
    # Suggestions section
    if prefix:
        suggestions = st.session_state.system.get_suggestions(prefix)
        
        if suggestions:
            st.subheader(f"💡 Suggestions for '{prefix}'")
            
            # Display suggestions as clickable buttons
            for i, word in enumerate(suggestions[:10], 1):  # Show top 10
                freq = st.session_state.system.word_freq.get(word, 0)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(f"{word}", key=f"word_{i}"):
                        st.session_state.system.select_word(word)
                        st.success(f"Selected: '{word}' (frequency: {st.session_state.system.word_freq[word]})")
                        st.rerun()
                
                with col2:
                    st.write(f"Freq: {freq}")
        else:
            st.info("No suggestions found for this prefix.")
    
    # Add new word section
    st.subheader("➕ Add New Word")
    new_word = st.text_input("Add a new word to the dictionary:", placeholder="Enter new word")
    
    if st.button("Add Word") and new_word:
        if new_word not in st.session_state.system.word_freq:
            st.session_state.system.add_word(new_word)
            st.success(f"Added '{new_word}' to the dictionary!")
            st.rerun()
        else:
            st.warning(f"'{new_word}' already exists in the dictionary.")
    
    # Statistics section
    st.subheader("📊 Statistics")
    total_words = len(st.session_state.system.word_freq)
    total_selections = sum(st.session_state.system.word_freq.values())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Words", total_words)
    with col2:
        st.metric("Total Selections", total_selections)
    
    # Show top words by frequency
    if st.session_state.system.word_freq:
        st.subheader("🏆 Most Popular Words")
        top_words = sorted(st.session_state.system.word_freq.items(), 
                          key=lambda x: x[1], reverse=True)[:5]
        
        for word, freq in top_words:
            st.write(f"• {word}: {freq} selections")
    
    # Reset button
    if st.button("🔄 Reset Frequencies", type="secondary"):
        st.session_state.system.word_freq = {word: 0 for word in st.session_state.system.word_freq}
        st.session_state.system.save_frequencies()
        st.success("All frequencies have been reset!")
        st.rerun()

if __name__ == "__main__":
    main()

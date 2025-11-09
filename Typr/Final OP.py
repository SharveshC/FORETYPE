import tkinter as tk
from tkinter import messagebox
import pickle
import os

# ---------------- Constants ----------------
FREQUENCY_FILE = 'word_freq.pkl'

# ---------------- Trie Node ----------------
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None

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
        self.load_frequencies()
        self.load_words()

    def load_frequencies(self):
        if os.path.exists(FREQUENCY_FILE):
            with open(FREQUENCY_FILE, 'rb') as f:
                self.word_freq = pickle.load(f)
        else:
            self.word_freq = {}

    def save_frequencies(self):
        with open(FREQUENCY_FILE, 'wb') as f:
            pickle.dump(self.word_freq, f)
            print(f"Word frequencies saved to '{FREQUENCY_FILE}'.")

    def add_word(self, word):
        word = word.lower()
        if word not in self.word_freq:
            self.word_freq[word] = 0
        self.trie.insert(word)

    def get_suggestions(self, prefix):
        prefix = prefix.lower()
        words = self.trie.get_suggestions(prefix)
        words.sort(key=lambda w: (-self.word_freq.get(w, 0), w))
        return words

    def select_word(self, word):
        word = word.lower()
        if word in self.word_freq:
            self.word_freq[word] += 1

    def load_words(self):
        words = [
    
    "apple", "ant", "anchor", "angle", "arrow", "art", "astronaut", "alarm", "adventure", "aviator",
    
    "ball", "bat", "banana", "boat", "book", "bridge", "butter", "bubble", "button", "brave",
    
    "cat", "car", "cup", "cake", "cloud", "circle", "candle", "cactus", "camera", "crayon",
    
    "dog", "door", "desk", "drum", "dance", "daisy", "diamond", "doll", "dolphin", "dragon",
    
    "egg", "ear", "earth", "engine", "energy", "eagle", "echo", "emerald", "exhibit", "escape",
    
    "fish", "fan", "frog", "fire", "forest", "feather", "flute", "frame", "flame", "festival",
    
    "goat", "game", "gold", "glass", "garden", "guitar", "globe", "gate", "ghost", "grape",
    
    "hat", "hand", "horse", "home", "honey", "hammer", "heart", "hill", "house", "helmet",
    
    "ice", "iron", "island", "idea", "image", "igloo", "ivy", "insect", "icon", "impact",
    
    "jam", "jar", "jungle", "juice", "jacket", "jewel", "jog", "jump", "jigsaw", "january",
    
    "kite", "king", "key", "kangaroo", "kitchen", "kettle", "knight", "koala", "kitten", "kingdom",
    
    "lion", "leaf", "lamp", "lake", "letter", "lamb", "ladder", "laser", "lemon", "library",
    
    "moon", "map", "mouse", "milk", "mountain", "mirror", "magnet", "mask", "mango", "machine",
    
    "nest", "nose", "name", "night", "needle", "nap", "net", "note", "nature", "nail",
    
    "orange", "owl", "ocean", "oil", "onion", "orbit", "octopus", "orchid", "opinion", "outdoor",
    
    "pen", "paper", "park", "plane", "phone", "pumpkin", "piano", "paint", "pearl", "pocket",
    
    "queen", "quick", "quiet", "quill", "quote", "quest", "quartz", "question", "quokka", "quality",
   
    "rain", "road", "river", "rock", "rose", "rocket", "ring", "ribbon", "room", "rope",
   
    "sun", "star", "snake", "sand", "song", "shoe", "shadow", "shell", "stone", "sock",
    
    "tree", "train", "toy", "table", "tiger", "tent", "ticket", "thread", "torch", "track",
    
    "umbrella", "unit", "user", "uniform", "unicorn", "utensil", "update", "ultra", "utility", "uplift",
    
    "van", "vase", "voice", "valley", "village", "violin", "vine", "vivid", "victory", "vacuum",
    
    "water", "wind", "wall", "wolf", "window", "wagon", "watch", "wave", "whale", "whistle",
    
    "xylophone", "xenon", "xerox", "xylem", "xenial", "xenophobia", "xenolith", "xiphoid", "xenograft", "xenagogue",
    
    "yarn", "yacht", "yard", "year", "yellow", "yogurt", "yodel", "yawn", "yield", "yoke",
    
    "zebra", "zero", "zone", "zip", "zoo", "zigzag", "zeal", "zenith", "zodiac", "zucchini"
]

        for w in words:
            self.add_word(w)

# ---------------- GUI ----------------
class AutoCompleteGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Autocomplete System")
        self.system = AutoCompleteSystem()

        # Entry box
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.on_type)

        # Listbox for suggestions
        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack(pady=10)

        # Buttons
        self.select_button = tk.Button(master, text="Select", command=self.on_select)
        self.select_button.pack(pady=5)

        self.clear_button = tk.Button(master, text="Clear", command=self.on_clear)
        self.clear_button.pack(pady=5)

        self.exit_button = tk.Button(master, text="Exit", command=self.on_exit)
        self.exit_button.pack(pady=5)

    def on_type(self, event):
        prefix = self.entry.get().strip().lower()
        suggestions = self.system.get_suggestions(prefix)
        self.listbox.delete(0, tk.END)
        for word in suggestions:
            freq = self.system.word_freq.get(word, 0)
            self.listbox.insert(tk.END, f"{word} (freq={freq})")

    def on_select(self):
        selection = self.listbox.curselection()
        if selection:
            word = self.listbox.get(selection[0]).split()[0]
            self.system.select_word(word)
            messagebox.showinfo("Selected", f"Selected {word}, freq={self.system.word_freq[word]}")
            self.on_type(None)  # Refresh suggestions

    def on_clear(self):
        self.entry.delete(0, tk.END)
        self.listbox.delete(0, tk.END)

    def on_exit(self):
        self.system.save_frequencies()
        self.master.destroy()

# ---------------- Main ----------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = AutoCompleteGUI(root)
    root.mainloop()

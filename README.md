# 🔤 Autocomplete System using Trie & Bloom Filter

An intelligent, adaptive **Autocomplete System** built in Python that efficiently suggests words based on user input.  
It combines **Trie** and **Bloom Filter** data structures for fast lookups and persistent learning through frequency tracking.

---

## 🧩 Overview

This project implements an **interactive command-line autocomplete engine**.  
It predicts possible word completions for a given prefix using:

- **Trie**: Efficient storage and retrieval of words based on prefixes  
- **Bloom Filter**: Fast probabilistic prefix membership test to skip unnecessary Trie traversals  
- **Persistent Frequency Learning**: Uses a pickle-based dictionary to remember how often each word is selected  

The system “learns” your preferences over time — words you select more frequently are prioritized in future suggestions.

---

## 🏗️ Architecture & Design

### Core Components

1. **Trie**
   - A tree-like structure for prefix-based word storage.
   - Each node represents a character.
   - Allows O(L) time for insertion and prefix search (L = length of word).

2. **Bloom Filter**
   - Space-efficient probabilistic set structure.
   - Used to test whether a prefix *may exist* in the dataset.
   - Greatly reduces unnecessary Trie traversals.
   - Has no false negatives (if it says “no,” it’s definitely not there) but may have rare false positives.

3. **Frequency Dictionary**
   - Tracks word usage frequency.
   - Stored in `word_freq.pkl` using Python’s `pickle` for persistence.
   - Updated every time a word is selected.
   - Ensures the system “remembers” user preferences across sessions.

4. **CLI Interface**
   - Simple and user-friendly command-line interaction.
   - Displays ranked suggestions, allows selection, and auto-saves progress.

---

## ⚙️ Implementation Details

- Written in **Python 3.8+**
- Uses `pybloom-live` for Bloom Filter implementation
- Uses built-in `pickle` and `os` modules for persistence
- Stores frequency data locally in `word_freq.pkl`
- Default dataset includes words like `cat`, `car`, `cart`, `case`, `dog`, etc.

---

## 📦 Installation

### 1️⃣ Clone the repository

bash
git clone https://github.com/yourusername/AutocompleteSystem.git
cd AutocompleteSystem


---

Autocomplete system ready.
Type something and press Enter.

Enter prefix: ca
Suggestions (sorted by frequency):
1. cat (freq=2)
2. car (freq=1)
3. cart (freq=0)

Select number to confirm word (Enter to skip): 1
Selected: cat, frequency now = 3

---
##User Input → Bloom Filter → Trie Lookup → Word Suggestions → Selection → Update Frequency → Save to Disk##
---


##⏱️ Time & Space Complexity
Operation	Time Complexity	Space Complexity	Description
Insert Word (Trie)	O(L)	O(L)	L = word length
Search Prefix (Trie)	O(P)	O(1)	P = prefix length
Bloom Filter Lookup	O(k)	O(m)	k = hash functions, m = bit array size
Add to Bloom Filter	O(k)	O(1)	Constant per insertion
Collect Suggestions	O(N)	O(N·L)	N = number of matched words
Sort Suggestions	O(N log N)	O(1)	Frequency + lex order
Save/Load Frequencies	O(W)	O(W)	W = number of stored words

---

##🔬 Future Enhancements

Feature	Description
Recency-based ranking	Prioritize recently used words
Limit displayed suggestions	Restrict output to top-k results
Dynamic resizing of Bloom Filter	Adapt capacity based on vocabulary size
File import/export support	Load external dictionaries
Web/GUI interface	Extend CLI into a web-based or Tkinter-based UI
Multilingual Support	Handle Unicode characters efficiently
---

##⚡ Performance Characteristics

Dataset Size	Trie Memory	Bloom Filter Memory	Average Lookup Time
1K words	~50 KB	~10 KB	< 1 ms
10K words	~400 KB	~80 KB	< 2 ms
100K words	~3.5 MB	~600 KB	~5–10 ms

---
##📄 Requirements

Python 3.8+
Dependencies:
pybloom-live
pickle (built-in)
os (built-in)
---
Example requirements.txt
pybloom-live

##📜 License
This project is released under the MIT License.

👥 Author
Your Name
📧 your.email@example.com
💻 GitHub Profile
🙏 Acknowledgement

Documentation format inspired by
LimitOrderBook by Arham Garg
,
a well-structured Python project demonstrating efficient data structures and strong documentation principles.

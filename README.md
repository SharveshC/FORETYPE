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



This project is released under the MIT License.

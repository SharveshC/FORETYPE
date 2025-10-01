# Encrypted Autocomplete Engine (DSA_PROJECT)

**Case Study for Data Structures & Algorithms** — an encrypted-autocomplete / suggestion engine using **Trie**, **TST**, **BST**, and **SkipList** with demo UI and RSA-based storage.

---

## Project Overview

This project implements a learning-focused autocomplete / suggestion engine. Users type a prefix, and the system returns suggestions ordered by frequency (how often each word was selected).  

It demonstrates:
- Multiple data structures (Trie, Ternary Search Tree, Binary Search Tree, SkipList).  
- Frequency-based ranking of suggestions.  
- RSA-based encryption of stored words (illustrating storing ciphertext and decrypting only for display).  
- A terminal-based interactive UI (using `curses`).  

> ⚠️ Note: The encryption here is **for demonstration only**. Keys are generated locally and decrypted in the same process — this is not a production-ready searchable encryption system.

---

## Why These Data Structures?

Autocomplete requires two essential operations:

1. **Prefix lookup** — find all words starting with a given prefix efficiently.  
2. **Ranking by frequency** — show the most commonly selected suggestions first.  

Chosen structures:
- **Trie** → O(L) prefix traversal, natural for autocomplete.  
- **Ternary Search Tree (TST)** → more space-efficient than Trie, still O(L).  
- **Binary Search Tree (BST)** → simple, but prefix searches can degrade in unbalanced cases.  
- **SkipList + Trie hybrid** → randomized structure with O(log n) operations, used to quickly fetch top-k suggestions.  

---

## Repository Structure

```
DSA_PROJECT/
├── BST.py                # BST + encryption + CLI UI
├── TRIE.py               # Trie + encryption + UI
├── TST.py                # Ternary Search Tree + encryption + UI
├── triewithskiplist.py   # Trie + SkipList integration for ranking
├── samp.py               # Simple Trie demo (no encryption) + UI
└── README.md             # (this file)
```

---

## Installation & Setup

### Requirements
- Python 3.8 or later  
- Required libraries:
```bash
pip install pycryptodome
pip install windows-curses   # only on Windows
```

### Run Examples
Run from a terminal (not an IDE console):

```bash
python TRIE.py
python TST.py
python BST.py
python triewithskiplist.py
python samp.py   # simpler demo without encryption
```

**Controls:**
- Type letters to build a prefix  
- Press **Tab / Enter** → generate suggestions  
- Use **Arrow Keys** to navigate, **Enter** to select  
- Press **ESC** to exit  

Selecting a suggestion increases its frequency count.

---

## High-Level Design

### Encryption Flow
- RSA keypair generated at runtime (`RSA.generate(2048)`)  
- Words are encrypted using the public key before insertion  
- Stored ciphertext is decrypted with the private key before display  
- Mimics client/server searchable-encryption (but runs locally)  

### Autocomplete Flow
1. **Insert / Build** → Insert word into chosen structure with encrypted storage + frequency counter  
2. **Prefix Traversal** → Traverse nodes matching user’s typed prefix  
3. **Candidate Collection** → DFS / traversal gathers possible completions  
4. **Ranking** → Use `heapq` or SkipList to return top-k results by frequency  
5. **Decryption & Display** → Ciphertext suggestions decrypted and shown in UI  

---

## Modules & Key Functions

### TRIE.py
- `TrieNode`, `Trie` (insert, search, autocomplete)  
- `autocomplete_encrypted(prefix, k)`  
- UI: `inputStr`, `menu_select`, `client_decrypt_suggestions`

### TST.py
- `TSTNode`, `TernarySearchTree`  
- `EncryptedTST` wrapper  
- Similar autocomplete flow adapted for TST  

### BST.py
- `BSTNode`, `EncryptedBST`  
- Stores encrypted words lexicographically  
- Autocomplete by scanning subtree prefixes  

### triewithskiplist.py
- `SkipListNode`, `SkipList` (probabilistic O(log n) structure)  
- Trie integrated with SkipList for frequency-based ranking  

---

## Complexity Summary

| Operation             | Trie / TST      | BST (balanced)    | SkipList ranking   |
|-----------------------|-----------------|------------------|-------------------|
| Insert / Search word  | O(L)            | O(log n)         | O(log n)          |
| Prefix traversal      | O(L)            | O(log n + range) | —                 |
| Gather completions    | O(M)            | O(M)             | O(k + log n)      |
| Ranking (top-k)       | O(M log k)      | O(M log k)       | O(k + log n)      |

- L = prefix length  
- n = number of words  
- M = number of matched completions  
- k = number of top results requested  

---

## Limitations

- RSA demo is **not secure** in production (keys generated and stored locally).  
- BST is unbalanced → worst case O(n).  
- No persistent storage — data resets on each run.  
- UI is terminal-based (`curses`) and may not work inside some IDEs.  

---

## Future Improvements

- Add unit tests with `pytest`  
- Use AVL / Red-Black tree instead of plain BST  
- Implement compressed trie (radix tree) for space efficiency  
- Persist vocabulary and frequency counts  
- Swap curses UI for a web-based or GUI interface  

---

## Contributors 

Sharvesh
Sachinkumar M
Sharmin 
Prawin

<a href="https://github.com/OWNER/REPO/graphs/contributors">
  <img src="https://github.com/sAcKy-14" />
</a>



---

---


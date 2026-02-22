import streamlit as st
import sqlite3
import time
import json
import pickle
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Try to import BloomFilter, fallback if not available
try:
    from pybloom_live import BloomFilter
    BLOOM_AVAILABLE = True
except ImportError:
    BLOOM_AVAILABLE = False
    print("BloomFilter not available, using fallback")

# Database setup
def init_database():
    conn = sqlite3.connect('autocomplete.db')
    cursor = conn.cursor()
    
    # Words table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            frequency INTEGER DEFAULT 0,
            category TEXT DEFAULT 'general',
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Search history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefix TEXT NOT NULL,
            suggestions TEXT NOT NULL,
            selected_word TEXT,
            algorithm TEXT NOT NULL,
            search_time REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Performance metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm TEXT NOT NULL,
            operation TEXT NOT NULL,
            execution_time REAL NOT NULL,
            memory_usage REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Database Manager
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('autocomplete.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def load_words(self):
        self.cursor.execute("SELECT word, frequency, category FROM words")
        return self.cursor.fetchall()
    
    def save_word(self, word, frequency=0, category='general'):
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO words (word, frequency, category) VALUES (?, ?, ?)",
                (word, frequency, category)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error saving word: {e}")
    
    def save_search_history(self, prefix, suggestions, selected_word, algorithm, search_time):
        self.cursor.execute(
            "INSERT INTO search_history (prefix, suggestions, selected_word, algorithm, search_time) VALUES (?, ?, ?, ?, ?)",
            (prefix, json.dumps(suggestions), selected_word, algorithm, search_time)
        )
        self.conn.commit()
    
    def get_search_history(self, limit=50):
        self.cursor.execute(
            "SELECT * FROM search_history ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()
    
    def get_performance_metrics(self):
        self.cursor.execute("""
            SELECT algorithm, AVG(execution_time) as avg_time, COUNT(*) as count
            FROM performance_metrics
            GROUP BY algorithm
        """)
        return self.cursor.fetchall()
    
    def get_word_stats(self):
        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_words,
                SUM(frequency) as total_searches,
                AVG(frequency) as avg_frequency,
                COUNT(DISTINCT category) as categories,
                COUNT(DISTINCT language) as languages
            FROM words
        """)
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

# Performance Monitor
class PerformanceMonitor:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def measure_operation(self, algorithm, operation, func):
        start_time = time.time()
        result = func()
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.db_manager.cursor.execute(
            "INSERT INTO performance_metrics (algorithm, operation, execution_time) VALUES (?, ?, ?)",
            (algorithm, operation, execution_time)
        )
        self.db_manager.conn.commit()
        
        return result, execution_time

# Trie Implementation
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

# TST Implementation
class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.eq = None
        self.right = None
        self.is_end_of_word = False
        self.word = None

class TernarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, word):
        self.root = self._insert_recursive(self.root, word, 0)
    
    def _insert_recursive(self, node, word, index):
        char = word[index]
        
        if node is None:
            node = TSTNode(char)
        
        if char < node.char:
            node.left = self._insert_recursive(node.left, word, index)
        elif char > node.char:
            node.right = self._insert_recursive(node.right, word, index)
        else:
            if index + 1 < len(word):
                node.eq = self._insert_recursive(node.eq, word, index + 1)
            else:
                node.is_end_of_word = True
                node.word = word
        
        return node
    
    def get_suggestions(self, prefix):
        node = self._search_node(self.root, prefix, 0)
        if not node:
            return []
        
        results = []
        self._collect_words_tst(node, results)
        return results
    
    def _search_node(self, node, word, index):
        if node is None:
            return None
        
        char = word[index]
        
        if char < node.char:
            return self._search_node(node.left, word, index)
        elif char > node.char:
            return self._search_node(node.right, word, index)
        else:
            if index + 1 < len(word):
                return self._search_node(node.eq, word, index + 1)
            else:
                return node
    
    def _collect_words_tst(self, node, results):
        if node is None:
            return
        
        if node.is_end_of_word:
            results.append(node.word)
        
        self._collect_words_tst(node.left, results)
        self._collect_words_tst(node.eq, results)
        self._collect_words_tst(node.right, results)

# BST Implementation
class BSTNode:
    def __init__(self, word):
        self.word = word
        self.frequency = 0
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.words = []
    
    def insert(self, word):
        self.words.append(word)
        if self.root is None:
            self.root = BSTNode(word)
        else:
            self._insert_recursive(self.root, word)
    
    def _insert_recursive(self, node, word):
        if word < node.word:
            if node.left is None:
                node.left = BSTNode(word)
            else:
                self._insert_recursive(node.left, word)
        else:
            if node.right is None:
                node.right = BSTNode(word)
            else:
                self._insert_recursive(node.right, word)
    
    def get_suggestions(self, prefix):
        return [word for word in self.words if word.startswith(prefix)]

# Enhanced Autocomplete System
class EnhancedAutoCompleteSystem:
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.db_manager = DatabaseManager()
        self.algorithms = {
            'Trie': Trie(),
            'TST': TernarySearchTree(),
            'BST': BinarySearchTree()
        }
        
        # Initialize Bloom Filter only if available
        if BLOOM_AVAILABLE:
            self.bloom_filter = BloomFilter(capacity=100000, error_rate=0.01)
        else:
            self.bloom_filter = None
            print("Running without Bloom Filter optimization")
        
        self.load_data()
    
    def load_data(self):
        words = self.db_manager.load_words()
        for word, frequency, category in words:
            for algorithm in self.algorithms.values():
                algorithm.insert(word)
            
            if self.bloom_filter:
                for i in range(1, len(word) + 1):
                    self.bloom_filter.add(word[:i])
    
    def get_suggestions(self, prefix, algorithm_name='Trie'):
        algorithm = self.algorithms.get(algorithm_name)
        if not algorithm:
            return [], 0
        
        # Bloom Filter check (only if available)
        if self.bloom_filter and prefix not in self.bloom_filter:
            return [], 0.001  # Fast return if no words start with prefix
        
        def search_operation():
            return algorithm.get_suggestions(prefix)
        
        suggestions, exec_time = self.monitor.measure_operation(
            algorithm_name, 'search', search_operation
        )
        
        # Sort by frequency
        word_freq = {word: freq for word, freq, _ in self.db_manager.load_words()}
        suggestions.sort(key=lambda w: -word_freq.get(w, 0))
        
        return suggestions[:10], exec_time
    
    def select_word(self, word, prefix, algorithm_name, search_time):
        self.db_manager.cursor.execute(
            "UPDATE words SET frequency = frequency + 1 WHERE word = ?",
            (word,)
        )
        self.db_manager.conn.commit()
        
        self.db_manager.save_search_history(
            prefix, [word], word, algorithm_name, search_time
        )

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="FORETYPE - Advanced Autocomplete",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize database
    init_database()
    
    # Initialize system
    if 'system' not in st.session_state:
        st.session_state.system = EnhancedAutoCompleteSystem()
        st.session_state.search_history = []
        st.session_state.current_prefix = ""
    
    system = st.session_state.system
    
    st.title("🚀 FORETYPE - Advanced Autocomplete Engine")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # Algorithm selection
    algorithm = st.sidebar.selectbox(
        "Select Algorithm",
        options=['Trie', 'TST', 'BST'],
        index=0
    )
    
    # Bloom Filter status
    if BLOOM_AVAILABLE:
        st.sidebar.success("✅ Bloom Filter: Active")
    else:
        st.sidebar.warning("⚠️ Bloom Filter: Not Available")
    
    # Main search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prefix = st.text_input(
            "🔍 Enter prefix:",
            value=st.session_state.current_prefix,
            key="search_input"
        )
    
    with col2:
        st.write("")
        search_button = st.button("🔎 Search", type="primary")
    
    # Real-time search
    if prefix != st.session_state.current_prefix:
        st.session_state.current_prefix = prefix
        if prefix:
            suggestions, search_time = system.get_suggestions(prefix, algorithm)
            st.session_state.current_suggestions = suggestions
            st.session_state.search_time = search_time
        else:
            st.session_state.current_suggestions = []
            st.session_state.search_time = 0
    
    # Display suggestions
    if st.session_state.get('current_suggestions'):
        suggestions = st.session_state.current_suggestions
        search_time = st.session_state.search_time
        
        st.subheader(f"💡 Suggestions ({len(suggestions)} found)")
        st.info(f"⏱️ Search time: {search_time:.6f} seconds using {algorithm}")
        
        if suggestions:
            cols = st.columns(min(5, len(suggestions)))
            for i, word in enumerate(suggestions):
                with cols[i % 5]:
                    if st.button(word, key=f"suggestion_{i}"):
                        system.select_word(word, prefix, algorithm, search_time)
                        st.success(f"✅ Selected: {word}")
                        st.rerun()
        else:
            st.warning("No suggestions found.")
    
    # Performance Analytics
    st.markdown("---")
    st.subheader("📊 Performance Analytics")
    
    # Get performance data
    performance_data = system.db_manager.get_performance_metrics()
    if performance_data:
        df_perf = pd.DataFrame(performance_data, columns=['Algorithm', 'Avg Time', 'Count'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_time = px.bar(df_perf, x='Algorithm', y='Avg Time', title='Average Search Time')
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            fig_count = px.bar(df_perf, x='Algorithm', y='Count', title='Search Count')
            st.plotly_chart(fig_count, use_container_width=True)
    
    # Search History
    st.subheader("📜 Search History")
    history = system.db_manager.get_search_history(20)
    if history:
        df_history = pd.DataFrame(history, columns=[
            'ID', 'Prefix', 'Suggestions', 'Selected', 'Algorithm', 'Time', 'Timestamp'
        ])
        st.dataframe(df_history[['Prefix', 'Selected', 'Algorithm', 'Time', 'Timestamp']])
    else:
        st.info("No search history yet.")
    
    # Footer
    st.markdown("---")
    st.markdown("🚀 **FORETYPE** - Advanced Autocomplete Engine | Built with ❤️ using Streamlit")

if __name__ == "__main__":
    main()

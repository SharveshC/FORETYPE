import streamlit as st
import sqlite3
import time
import json
import pickle
import os
from datetime import datetime
from pybloom_live import BloomFilter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Data Structures
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=0):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.word = word
        node.frequency = frequency

    def get_suggestions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        self._collect_words(node, results)
        results.sort(key=lambda w: w[1], reverse=True)  # Sort by frequency
        return [word for word, freq in results]

    def _collect_words(self, node, results):
        if node.is_end:
            results.append((node.word, node.frequency))
        for child in node.children.values():
            self._collect_words(child, results)

class TSTNode:
    def __init__(self, char):
        self.char = char
        self.left = None
        self.eq = None
        self.right = None
        self.is_end = False
        self.word = None
        self.frequency = 0

class TernarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, word, frequency=0):
        if not word:
            return
        self.root = self._insert(self.root, word, 0, frequency)

    def _insert(self, node, word, index, frequency):
        char = word[index]
        if not node:
            node = TSTNode(char)
        if char < node.char:
            node.left = self._insert(node.left, word, index, frequency)
        elif char > node.char:
            node.right = self._insert(node.right, word, index, frequency)
        else:
            if index + 1 < len(word):
                node.eq = self._insert(node.eq, word, index + 1, frequency)
            else:
                node.is_end = True
                node.word = word
                node.frequency = frequency
        return node

    def get_suggestions(self, prefix):
        if not prefix:
            return []
        node = self._search(self.root, prefix, 0)
        if not node:
            return []
        results = []
        self._collect_words(node, prefix, results)
        results.sort(key=lambda w: w[1], reverse=True)
        return [word for word, freq in results]

    def _search(self, node, prefix, index):
        if not node:
            return None
        char = prefix[index]
        if char < node.char:
            return self._search(node.left, prefix, index)
        elif char > node.char:
            return self._search(node.right, prefix, index)
        else:
            if index + 1 == len(prefix):
                return node
            return self._search(node.eq, prefix, index + 1)

    def _collect_words(self, node, prefix, results):
        if not node:
            return
        self._collect_words(node.left, prefix, results)
        new_prefix = prefix + node.char
        if node.is_end:
            results.append((node.word, node.frequency))
        self._collect_words(node.eq, new_prefix, results)
        self._collect_words(node.right, prefix, results)

class BSTNode:
    def __init__(self, word, frequency=0):
        self.word = word
        self.frequency = frequency
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, word, frequency=0):
        self.root = self._insert(self.root, word, frequency)

    def _insert(self, node, word, frequency):
        if not node:
            return BSTNode(word, frequency)
        if word < node.word:
            node.left = self._insert(node.left, word, frequency)
        elif word > node.word:
            node.right = self._insert(node.right, word, frequency)
        else:
            node.frequency = frequency
        return node

    def get_suggestions(self, prefix):
        results = []
        self._collect_with_prefix(self.root, prefix, results)
        results.sort(key=lambda w: w[1], reverse=True)
        return [word for word, freq in results]

    def _collect_with_prefix(self, node, prefix, results):
        if not node:
            return
        if node.word.startswith(prefix):
            results.append((node.word, node.frequency))
        self._collect_with_prefix(node.left, prefix, results)
        self._collect_with_prefix(node.right, prefix, results)

# Performance Monitor
class PerformanceMonitor:
    def __init__(self):
        self.metrics = []

    def measure_operation(self, algorithm, operation, func):
        start_time = time.time()
        result = func()
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Store in database
        conn = sqlite3.connect('autocomplete.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO performance_metrics (algorithm, operation, execution_time)
            VALUES (?, ?, ?)
        ''', (algorithm, operation, execution_time))
        conn.commit()
        conn.close()
        
        return result, execution_time

# Database Operations
class DatabaseManager:
    @staticmethod
    def load_words():
        conn = sqlite3.connect('autocomplete.db')
        cursor = conn.cursor()
        cursor.execute('SELECT word, frequency FROM words')
        words = dict(cursor.fetchall())
        conn.close()
        return words

    @staticmethod
    def save_word(word, frequency=0, category='general', language='en'):
        conn = sqlite3.connect('autocomplete.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO words (word, frequency, category, language)
            VALUES (?, ?, ?, ?)
        ''', (word, frequency, category, language))
        conn.commit()
        conn.close()

    @staticmethod
    def update_frequency(word):
        conn = sqlite3.connect('autocomplete.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE words SET frequency = frequency + 1 WHERE word = ?
        ''', (word,))
        conn.commit()
        conn.close()

    @staticmethod
    def save_search(prefix, suggestions, selected_word, algorithm, search_time):
        conn = sqlite3.connect('autocomplete.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO search_history (prefix, suggestions, selected_word, algorithm, search_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (prefix, json.dumps(suggestions), selected_word, algorithm, search_time))
        conn.commit()
        conn.close()

    @staticmethod
    def get_search_history(limit=50):
        conn = sqlite3.connect('autocomplete.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT prefix, selected_word, algorithm, search_time, timestamp 
            FROM search_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        history = cursor.fetchall()
        conn.close()
        return history

    @staticmethod
    def get_performance_data():
        conn = sqlite3.connect('autocomplete.db')
        df = pd.read_sql_query('''
            SELECT algorithm, operation, execution_time, timestamp 
            FROM performance_metrics 
            ORDER BY timestamp DESC 
            LIMIT 100
        ''', conn)
        conn.close()
        return df

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
        self.bloom_filter = BloomFilter(capacity=100000, error_rate=0.01)
        self.load_data()

    def load_data(self):
        words = self.db_manager.load_words()
        for word, frequency in words.items():
            for algorithm in self.algorithms.values():
                algorithm.insert(word, frequency)
            for i in range(1, len(word) + 1):
                self.bloom_filter.add(word[:i])

    def get_suggestions(self, prefix, algorithm='Trie'):
        if prefix not in self.bloom_filter:
            return [], 0.0

        alg = self.algorithms[algorithm]
        suggestions, exec_time = self.monitor.measure_operation(
            algorithm, f'autocomplete_{len(prefix)}', 
            lambda: alg.get_suggestions(prefix)
        )
        
        return suggestions, exec_time

    def select_word(self, word, prefix, algorithm, exec_time):
        self.db_manager.update_frequency(word)
        
        # Update all algorithms
        for alg in self.algorithms.values():
            if hasattr(alg, 'root'):
                self._update_frequency_in_structure(alg, word)
        
        self.db_manager.save_search(prefix, [], word, algorithm, exec_time)

    def _update_frequency_in_structure(self, structure, word):
        # This is a simplified update - in production, you'd want to properly update frequencies
        pass

    def add_word(self, word, category='general', language='en'):
        if word not in self.bloom_filter:
            for algorithm in self.algorithms.values():
                algorithm.insert(word)
            for i in range(1, len(word) + 1):
                self.bloom_filter.add(word[:i])
            self.db_manager.save_word(word, 0, category, language)

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Advanced Autocomplete Engine",
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
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🚀 Advanced Autocomplete Engine</h1>', unsafe_allow_html=True)
    
    # Sidebar for algorithm selection and settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Algorithm selection
        algorithm = st.selectbox(
            "Choose Algorithm",
            options=['Trie', 'TST', 'BST'],
            index=0,
            help="Select the data structure for autocomplete"
        )
        
        # Real-time typing toggle
        real_time = st.checkbox("🔄 Real-time Suggestions", value=True)
        
        # Performance tracking
        st.subheader("📊 Performance")
        perf_data = DatabaseManager.get_performance_data()
        if not perf_data.empty:
            avg_time = perf_data['execution_time'].mean()
            st.metric("Avg Response Time", f"{avg_time:.4f}s")
            
            # Algorithm performance comparison
            alg_perf = perf_data.groupby('algorithm')['execution_time'].mean()
            fig = px.bar(
                x=alg_perf.index, 
                y=alg_perf.values,
                title="Algorithm Performance",
                labels={'x': 'Algorithm', 'y': 'Avg Time (s)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Autocomplete Interface")
        
        # Search input with real-time support
        if real_time:
            prefix = st.text_input(
                "Type your prefix:",
                value=st.session_state.current_prefix,
                key="search_input",
                on_change=lambda: st.session_state.update({"current_prefix": st.session_state.search_input})
            )
        else:
            prefix = st.text_input("Type your prefix:", key="search_input")
        
        if prefix:
            suggestions, exec_time = st.session_state.system.get_suggestions(prefix, algorithm)
            
            # Performance metrics
            st.info(f"⚡ Found {len(suggestions)} suggestions in {exec_time:.6f}s using {algorithm}")
            
            if suggestions:
                st.subheader(f"💡 Suggestions for '{prefix}'")
                
                # Display suggestions as interactive buttons
                cols = st.columns(min(3, len(suggestions)))
                for i, word in enumerate(suggestions[:9]):  # Show top 9
                    with cols[i % 3]:
                        if st.button(f"{word}", key=f"suggestion_{i}"):
                            st.session_state.system.select_word(word, prefix, algorithm, exec_time)
                            st.success(f"✅ Selected: '{word}'")
                            st.rerun()
            else:
                st.warning("No suggestions found for this prefix.")
    
    with col2:
        st.header("📈 Search History")
        
        # Load and display search history
        history = DatabaseManager.get_search_history(10)
        if history:
            for i, (prefix, selected, alg, time_taken, timestamp) in enumerate(history):
                with st.expander(f"{prefix} → {selected or 'None'}"):
                    st.write(f"**Algorithm:** {alg}")
                    st.write(f"**Time:** {time_taken:.6f}s")
                    st.write(f"**When:** {timestamp}")
        else:
            st.info("No search history yet.")
    
    # Word Management Section
    st.header("📝 Word Management")
    
    col_add, col_import = st.columns(2)
    
    with col_add:
        st.subheader("➕ Add New Word")
        new_word = st.text_input("Enter new word:", key="new_word")
        word_category = st.selectbox("Category:", ["general", "tech", "medical", "academic"])
        word_language = st.selectbox("Language:", ["en", "es", "fr", "de"])
        
        if st.button("Add Word"):
            if new_word:
                st.session_state.system.add_word(new_word, word_category, word_language)
                st.success(f"✅ Added '{new_word}' to dictionary!")
                st.rerun()
    
    with col_import:
        st.subheader("📂 Import/Export")
        
        # Import functionality
        uploaded_file = st.file_uploader("Upload word list (.txt)", type=['txt'])
        if uploaded_file:
            content = uploaded_file.read().decode()
            words = [word.strip() for word in content.split('\n') if word.strip()]
            for word in words:
                st.session_state.system.add_word(word)
            st.success(f"✅ Imported {len(words)} words!")
        
        # Export functionality
        if st.button("Export Dictionary"):
            words = DatabaseManager.load_words()
            export_data = "\n".join(words.keys())
            st.download_button(
                label="Download word list",
                data=export_data,
                file_name="dictionary.txt",
                mime="text/plain"
            )
    
    # Advanced Analytics Dashboard
    st.header("🎯 Advanced Analytics")
    
    # Performance comparison dashboard
    perf_df = DatabaseManager.get_performance_data()
    if not perf_df.empty:
        col_perf1, col_perf2 = st.columns(2)
        
        with col_perf1:
            # Time series performance
            fig_time = px.line(
                perf_df, 
                x='timestamp', 
                y='execution_time', 
                color='algorithm',
                title="Performance Over Time"
            )
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col_perf2:
            # Operation type analysis
            fig_ops = px.box(
                perf_df, 
                x='operation', 
                y='execution_time', 
                color='algorithm',
                title="Operation Performance Distribution"
            )
            st.plotly_chart(fig_ops, use_container_width=True)
    
    # Database statistics
    conn = sqlite3.connect('autocomplete.db')
    
    # Word statistics
    word_stats = pd.read_sql_query('''
        SELECT 
            COUNT(*) as total_words,
            SUM(frequency) as total_searches,
            AVG(frequency) as avg_frequency,
            COUNT(DISTINCT category) as categories,
            COUNT(DISTINCT language) as languages
        FROM words
    ''', conn)
    
    # Search statistics
    search_stats = pd.read_sql_query('''
        SELECT 
            COUNT(*) as total_searches,
            COUNT(DISTINCT prefix) as unique_prefixes,
            AVG(search_time) as avg_search_time,
            COUNT(DISTINCT algorithm) as algorithms_used
        FROM search_history
    ''', conn)
    
    conn.close()
    
    # Display statistics
    col_stats1, col_stats2 = st.columns(2)
    
    with col_stats1:
        st.subheader("📊 Dictionary Statistics")
        stats = word_stats.iloc[0]
        st.metric("Total Words", int(stats['total_words'] or 0))
        st.metric("Total Searches", int(stats['total_searches'] or 0))
        st.metric("Avg Frequency", f"{stats['avg_frequency'] or 0:.2f}")
        st.metric("Categories", int(stats['categories'] or 0))
        st.metric("Languages", int(stats['languages'] or 0))
    
    with col_stats2:
        st.subheader("🔍 Search Statistics")
        search = search_stats.iloc[0]
        st.metric("Total Searches", int(search['total_searches'] or 0))
        st.metric("Unique Prefixes", int(search['unique_prefixes'] or 0))
        st.metric("Avg Search Time", f"{search['avg_search_time'] or 0:.6f}s")
        st.metric("Algorithms Used", int(search['algorithms_used'] or 0))

if __name__ == "__main__":
    main()

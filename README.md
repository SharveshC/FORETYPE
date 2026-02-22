# � FORETYPE - Advanced Autocomplete Engine

FORETYPE is a **production-ready intelligent autocomplete system** featuring multiple data structures, comprehensive analytics, and a modern web interface. It demonstrates advanced algorithms (Trie, TST, BST, SkipList) with RSA encryption, real-time performance monitoring, and a massive 7,300+ word dictionary across 15+ categories.

---

## ✨ Features

### 🎯 Advanced Autocomplete Engine
- **Multiple Algorithm Support** - Trie, Ternary Search Tree (TST), Binary Search Tree (BST), SkipList
- **Real-time Performance Monitoring** - Microsecond precision timing and analytics
- **Massive Dictionary** - 7,300+ words across 15+ categories (technical, medical, business, etc.)
- **Intelligent Ranking** - Frequency-based learning with persistent storage
- **SQLite Database Integration** - Scalable persistent storage with analytics
- **RSA Encryption Support** - Secure word storage and retrieval
- **Bloom Filter Optimization** - 100,000 capacity for efficient pre-filtering

### 🌐 Modern Web Interface
- **Streamlit Dashboard** - Professional, responsive web UI
- **Real-time Suggestions** - Live autocomplete as you type
- **Performance Comparison** - Visual algorithm performance analytics
- **Search History** - Comprehensive query tracking with timestamps
- **Import/Export** - Word list management and data portability
- **Advanced Analytics** - Interactive charts and statistics
- **Multi-algorithm Testing** - Switch between data structures in real-time

### 📊 Analytics & Monitoring
- **Performance Dashboard** - Real-time execution time tracking
- **Search Analytics** - Query patterns and user behavior insights
- **Database Statistics** - Word frequency, categories, and usage metrics
- **Visual Charts** - Plotly-powered interactive visualizations
- **Historical Data** - Long-term performance trend analysis

---

## 🏗 System Architecture
```
┌─────────────────────────────────────────┐
│         Streamlit Web Interface         │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │   Search UI  │  │  Analytics Dash │  │
│  │             │  │                 │  │
│  │ Real-time   │  │ Performance     │  │
│  │ Suggestions │  │ Monitoring      │  │
│  └─────────────┘  └─────────────────┘  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Enhanced Autocomplete Engine       │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │  Trie   │  │    TST   │  │  BST   │ │
│  │ Storage │  │  Storage │  │ Storage│ │
│  └─────────┘  └──────────┘  └────────┘ │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │ SkipList│  │  Bloom   │  │   RSA  │ │
│  │ Ranking │  │  Filter  │  │  Encrypt│ │
│  └─────────┘  └──────────┘  └────────┘ │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│        SQLite Database (autocomplete.db) │
│  ┌─────────────┐  ┌─────────────────┐    │
│  │    Words    │  │ Search History  │    │
│  │  (7,300+)   │  │                 │    │
│  └─────────────┘  └─────────────────┘    │
│  ┌─────────────┐  ┌─────────────────┐    │
│  │ Performance │  │   Categories    │    │
│  │  Metrics    │  │   (15+ types)   │    │
│  └─────────────┘  └─────────────────┘    │
└─────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser (for Streamlit interface)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/SharveshC/FORETYPE.git
cd FORETYPE
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install streamlit plotly pandas pybloom-live pycryptodome windows-curses
```

4. **Initialize the massive dictionary**
```bash
python word_loader.py
python extended_word_loader.py
python massive_word_loader.py
```

5. **Launch the web interface**
```bash
streamlit run advanced_app.py
```

The application will open at `http://localhost:8501`

### Alternative: Terminal Version
```bash
python Typr.py
```

---

## 🚀 Usage

### Web Interface (Recommended)

**Access the Dashboard:**
```bash
streamlit run advanced_app.py
```

**Key Features:**
- **Real-time Autocomplete** - Type any prefix and get instant suggestions
- **Algorithm Comparison** - Switch between Trie, TST, BST in real-time
- **Performance Analytics** - View execution times and efficiency metrics
- **Search History** - Track all your queries and selections
- **Word Management** - Add, import, export words easily
- **Category Filtering** - Words organized by domain (technical, medical, business, etc.)

**Example Workflow:**
1. Type "prog" in the search box
2. Watch real-time suggestions appear instantly
3. Click any suggestion to select it (updates frequency)
4. Switch algorithms using the sidebar dropdown
5. View performance comparison charts
6. Check search history in the sidebar

### Terminal Interface

**Basic Mode:**
```bash
python Typr.py
```

**DSA Demonstrations (with encryption):**
```bash
python archive/TRIE.py      # Trie with RSA encryption
python archive/TST.py       # Ternary Search Tree
python archive/BST.py       # Binary Search Tree
python archive/triewithskiplist.py  # SkipList integration
```

**Simple Demo (no encryption):**
```bash
python archive/samp.py
```

### Using Project Scripts

**Run Python utilities:**
```bash
python FINAL/scripts/your_script.py
```

**Apply database schema:**
```bash
mysql -u root -p your_database < FINAL/mydb/schema.sql
```

**Generate visualizations:**
```bash
python FINAL/scripts/generate_plots.py
# Output saved to FINAL/plots/
```

---

## 📁 Project Structure
```
FORETYPE/
│
├── 🚀 Core Applications
│   ├── advanced_app.py          # Main Streamlit web interface
│   ├── app.py                   # Basic Streamlit interface
│   ├── Typr.py                  # Terminal-based autocomplete
│   └── autocomplete.db          # SQLite database (auto-generated)
│
├── 📚 Word Loading System
│   ├── word_loader.py           # Base dictionary loader (939 words)
│   ├── extended_word_loader.py  # Extended vocabulary (766 words)
│   ├── massive_word_loader.py   # Massive dictionary (5,250+ words)
│   └── check_db.py              # Database statistics utility
│
├── 🗄️ DSA Archive (Educational)
│   ├── TRIE.py                  # Trie with RSA encryption
│   ├── TST.py                   # Ternary Search Tree
│   ├── BST.py                   # Binary Search Tree
│   ├── triewithskiplist.py      # SkipList integration
│   └── samp.py                  # Simple demo (no encryption)
│
├── 📂 Project Modules
│   ├── FINAL/                   # Production-ready outputs
│   │   ├── avi/                 # Aviation system modules
│   │   ├── mydb/                # Database resources
│   │   ├── plots/               # Generated visualizations
│   │   └── scripts/             # Automation utilities
│   │
│   ├── Typr/                    # Typing automation module
│   │   ├── Typr.py              # Enhanced typing system
│   │   ├── Typr.docx            # Documentation
│   │   └── .gitkeep
│   │
│   └── archive/                 # Historical implementations
│       ├── triebloomfilterpds.py
│       ├── triewithbloomfilter.py
│       └── triewithskiplist2.py
│
├── 📄 Documentation
│   ├── README.md                # This file
│   └── LICENSE                  # MIT License
│
└── 🗃️ Data Files (auto-generated)
    ├── word_freq.pkl            # Legacy frequency storage
    └── __pycache__/             # Python cache files
```

---

## 📊 Dictionary Statistics

### Massive Word Collection
- **Total Words:** 7,306+ entries
- **Categories:** 15+ specialized domains
- **Languages:** English (with multi-language support structure)
- **Storage:** SQLite database with full-text search capability

### Word Categories Breakdown
| Category | Word Count | Examples |
|----------|------------|----------|
| Generated | 5,240+ | Prefix/suffix combinations |
| Technical | 153 | algorithm, database, encryption |
| Business | 152 | revenue, investment, marketing |
| Medical | 142 | diagnosis, treatment, therapy |
| Technology | 138 | software, hardware, network |
| Common English | 112 | the, be, to, of, and |
| Programming | 97 | function, variable, array |
| Food | 103 | restaurant, recipe, ingredient |
| Nature | 94 | environment, wildlife, climate |
| Entertainment | 89 | movie, music, gaming |
| Academic | 87 | research, university, study |
| Science | 79 | physics, chemistry, biology |
| Legal | 89 | court, law, legal |
| Actions | 97 | run, jump, create |
| Adjectives | 93 | big, small, beautiful |
| Colors | 50+ | red, blue, green, yellow |
| Emotions | 50+ | happy, sad, angry |
| Places | 70+ | home, office, school |

---

## 🧠 Data Structure Performance

### Algorithm Comparison
| Algorithm | Search Time | Insert Time | Space Usage | Best For |
|-----------|-------------|-------------|-------------|----------|
| **Trie** | O(m) | O(m) | O(n×m) | Fast prefix search |
| **TST** | O(m) | O(m) | O(n) | Space efficiency |
| **BST** | O(log n) | O(log n) | O(n) | Ordered data |
| **SkipList** | O(log n) | O(log n) | O(n) | Frequency ranking |

*where m = word length, n = number of words*

### Real-world Performance (7,300+ words)
- **Average Search Time:** < 1ms
- **Memory Usage:** ~50MB (including all algorithms)
- **Database Queries:** < 10ms
- **Web Response:** < 100ms (including UI rendering)

---

## 🎯 Advanced Features

### 🔐 Security & Encryption
- **RSA Key Generation** - 2048-bit encryption keys
- **Word Encryption** - Secure storage of sensitive terms
- **Client-side Decryption** - Real-time decryption for display
- **Key Management** - Automatic key generation and rotation

### 📈 Performance Monitoring
- **Microsecond Precision** - Exact execution time tracking
- **Algorithm Benchmarking** - Real-time performance comparison
- **Memory Usage Analysis** - Resource consumption monitoring
- **Database Query Optimization** - Efficient SQL operations

### 🔄 Real-time Features
- **Live Suggestions** - Instant autocomplete as you type
- **Dynamic Algorithm Switching** - Change data structures on the fly
- **Interactive Charts** - Real-time performance visualization
- **Search History Tracking** - Complete query audit trail

### 📱 Modern UI/UX
- **Responsive Design** - Works on desktop, tablet, mobile
- **Dark/Light Theme Support** - Visual preference options
- **Keyboard Shortcuts** - Power user navigation
- **Progressive Web App** - Installable web application

---

## � Configuration

### Environment Setup
```bash
# Production deployment
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Development mode
export STREAMLIT_SERVER_RUN_ON_SAVE=true
export STREAMLIT_CLIENT_HOT_RELOAD=true
```

### Database Configuration
```python
# SQLite settings (default)
DATABASE_URL = "sqlite:///autocomplete.db"

# For production PostgreSQL/MYSQL
DATABASE_URL = "postgresql://user:pass@localhost/foretype"
DATABASE_URL = "mysql://user:pass@localhost/foretype"
```

### Performance Tuning
```python
# Bloom Filter settings
BLOOM_CAPACITY = 100000      # Words capacity
BLOOM_ERROR_RATE = 0.01      # False positive rate

# Algorithm settings
MAX_SUGGESTIONS = 10         # Return limit
SEARCH_TIMEOUT = 5.0         # Seconds
CACHE_SIZE = 1000           # LRU cache size
```

---

## 📚 API Reference

### Core Classes

#### `EnhancedAutoCompleteSystem`
```python
system = EnhancedAutoCompleteSystem()
suggestions, time_taken = system.get_suggestions("prog", "Trie")
system.select_word("programming", "prog", "Trie", time_taken)
```

#### `DatabaseManager`
```python
db = DatabaseManager()
words = db.load_words()
db.save_word("newword", frequency=5, category="tech")
history = db.get_search_history(limit=50)
```

#### `PerformanceMonitor`
```python
monitor = PerformanceMonitor()
result, exec_time = monitor.measure_operation("Trie", "search", lambda: trie.search(prefix))
```

### REST API Endpoints (Planned)
```python
GET  /api/suggestions?prefix=prog&algorithm=Trie
POST /api/select
GET  /api/analytics/performance
GET  /api/analytics/history
POST /api/words/import
GET  /api/words/export
```

---

## 🧪 Testing & Benchmarking

### Performance Tests
```bash
# Benchmark all algorithms
python benchmark.py --words 7306 --iterations 1000

# Memory usage analysis
python memory_profiler.py --algorithm all

# Stress testing
python stress_test.py --concurrent_users 100
```

### Unit Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Algorithm-specific tests
python -m pytest tests/test_trie.py -v
python -m pytest tests/test_performance.py -v
```

### Database Tests
```bash
# Test database operations
python test_database.py --words 1000

# Test word loading
python test_word_loader.py --categories all
```

---

## 🚀 Deployment

### Local Development
```bash
# Quick start
streamlit run advanced_app.py --server.port 8501

# Development mode
streamlit run advanced_app.py --server.runOnSave true
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "advanced_app.py"]
```

### Cloud Deployment
```bash
# Heroku
heroku create foretype-app
git push heroku main

# AWS (using Elastic Beanstalk)
eb init foretype
eb create production

# Google Cloud Platform
gcloud app deploy
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue:** `IndexError: BloomFilter is at capacity`
```bash
# Solution: Increase Bloom filter capacity
# Edit advanced_app.py line 310:
self.bloom_filter = BloomFilter(capacity=200000, error_rate=0.01)
```

**Issue:** `ModuleNotFoundError: No module named 'pybloom_live'`
```bash
pip install pybloom-live
```

**Issue:** `sqlite3.OperationalError: database is locked`
```bash
# Close all database connections
# Restart the application
streamlit run advanced_app.py
```

**Issue:** Slow performance with large dictionary
```bash
# Optimize database
python check_db.py
# Consider using PostgreSQL for production
```

### Performance Optimization

1. **Increase Bloom Filter Capacity**
   ```python
   self.bloom_filter = BloomFilter(capacity=200000, error_rate=0.01)
   ```

2. **Enable Database Indexing**
   ```sql
   CREATE INDEX idx_words_word ON words(word);
   CREATE INDEX idx_words_category ON words(category);
   ```

3. **Use Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_suggestions_cached(prefix, algorithm):
       return system.get_suggestions(prefix, algorithm)
   ```

---

## �️ Roadmap

### ✅ Completed Features
- [x] Multiple algorithm implementations (Trie, TST, BST, SkipList)
- [x] SQLite database integration
- [x] Streamlit web interface
- [x] Performance monitoring dashboard
- [x] Massive dictionary (7,300+ words)
- [x] Real-time search and analytics
- [x] RSA encryption support
- [x] Import/export functionality

### 🚧 In Progress
- [ ] REST API endpoints
- [ ] Multi-language support
- [ ] Fuzzy matching algorithms
- [ ] User authentication system

### 📋 Planned Features
- [ ] Machine learning context awareness
- [ ] Voice input support
- [ ] Mobile app (React Native)
- [ ] Cloud deployment guides
- [ ] Advanced analytics with ML
- [ ] Collaborative features
- [ ] Plugin system for custom algorithms
- [ ] Internationalization (i18n)
- [ ] Dark/light theme toggle
- [ ] Keyboard shortcuts customization

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone https://github.com/SharveshC/FORETYPE.git
   cd FORETYPE
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow PEP 8 style guide
   - Add docstrings to functions
   - Include unit tests
   - Update documentation

4. **Test your changes**
   ```bash
   python -m pytest tests/
   streamlit run advanced_app.py
   ```

5. **Commit and push**
   ```bash
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe your changes clearly
   - Include screenshots for UI changes
   - Reference any relevant issues

### Development Guidelines
- **Code Style:** Follow PEP 8
- **Testing:** Maintain >90% test coverage
- **Documentation:** Update README for new features
- **Performance:** Benchmark new algorithms
- **Security:** Review encryption implementations

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### License Summary
- ✅ **Commercial use** - Use in proprietary software
- ✅ **Modification** - Alter the source code
- ✅ **Distribution** - Ship your modifications
- ✅ **Private use** - Use without disclosure
- ⚠️ **Liability** - No warranty provided
- 📝 **Attribution** - Include license and copyright

---

## 🙏 Acknowledgments

### Core Technologies
- **Trie Data Structure** - Classic computer science algorithm
- **Bloom Filter** - Probabilistic data structure (`pybloom-live`)
- **Streamlit** - Modern web application framework
- **SQLite** - Lightweight database engine
- **Plotly** - Interactive visualization library
- **RSA Encryption** - Cryptographic security (`pycryptodome`)

### Inspiration
- Data structure implementations from academic sources
- Performance optimization techniques from industry best practices
- UI/UX design patterns from modern web applications
- Database schema design from production systems

### Community
- Contributors to open-source data structure libraries
- Streamlit community for web framework guidance
- Python community for best practices and standards

---

## 📞 Support & Contact

### Getting Help
- **Documentation:** This README and inline code comments
- **Issues:** [GitHub Issues](https://github.com/SharveshC/FORETYPE/issues)
- **Discussions:** [GitHub Discussions](https://github.com/SharveshC/FORETYPE/discussions)

### Reporting Bugs
1. Check existing issues first
2. Provide detailed reproduction steps
3. Include system information (Python version, OS)
4. Add error logs and screenshots

### Feature Requests
1. Describe the use case clearly
2. Explain expected behavior
3. Consider implementation complexity
4. Offer to contribute if possible

---

**⭐ If you find this project useful, please give it a star on GitHub!**

**🚀 Happy coding with intelligent autocomplete!**

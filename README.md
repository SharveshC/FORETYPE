# 🔤 FORETYPE



FORETYPE is an intelligent autocomplete system built with advanced data structures (Trie & Bloom Filter) combined with a structured multi-domain project workspace. It demonstrates efficient text prediction while serving as a practical development environment for various engineering projects.

---

## ✨ Features

### Autocomplete Engine
- **Trie-Based Prefix Search** – Fast O(m) lookup time where m is prefix length
- **Bloom Filter Integration** – Probabilistic membership testing for memory efficiency
- **Frequency Learning** – Adapts suggestions based on user input patterns
- **Persistent Storage** – Saves learning data across sessions
- **Interactive CLI** – Real-time word suggestions as you type

### Development Workspace
- **Multi-Domain Organization** – Separate modules for aviation, database, visualization, and automation
- **Production-Ready Builds** – Organized FINAL/ directory for completed work
- **Script Automation** – Reusable Python utilities and processing scripts
- **Data Management** – Structured storage for datasets, logs, and exports

---

## 🏗 System Architecture
```
┌─────────────────────────────────────────┐
│         User Input Interface            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Autocomplete Engine Core           │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │  Trie   │  │  Bloom   │  │  Freq  │ │
│  │ Storage │◄─┤  Filter  │◄─┤  Dict  │ │
│  └─────────┘  └──────────┘  └────────┘ │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Persistent Data (word_freq.pkl)      │
└─────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- MySQL (optional, for database modules)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/foretype.git
cd foretype
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install pybloom-live
```

4. **Verify installation**
```bash
python autocomplete.py
```

---

## 🚀 Usage

### Running the Autocomplete System

**Interactive Mode:**
```bash
python autocomplete.py
```

Type any prefix and press Enter to see suggestions. Type `exit` to quit.

**Example Session:**
```
Enter prefix (or 'exit' to quit): hel
Suggestions: ['hello', 'help', 'helmet', 'helvetica']

Enter prefix (or 'exit' to quit): prog
Suggestions: ['program', 'programming', 'progress', 'programmer']
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
├── autocomplete.py          # Main autocomplete engine
├── word_freq.pkl            # Persistent frequency data (auto-generated)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
│
├── FINAL/                  # Production-ready outputs
│   ├── avi/               # Aviation system modules
│   │   ├── flight_data.csv
│   │   ├── analysis_report.pdf
│   │   └── route_optimizer.py
│   │
│   ├── mydb/              # Database resources
│   │   ├── schema.sql
│   │   ├── seed_data.sql
│   │   └── backups/
│   │
│   ├── plots/             # Generated visualizations
│   │   ├── frequency_chart.png
│   │   ├── usage_trends.pdf
│   │   └── performance_metrics.svg
│   │
│   ├── scripts/           # Automation utilities
│   │   ├── data_processor.py
│   │   ├── batch_convert.py
│   │   └── report_generator.py
│   │
│   └── others/            # Documentation & logs
│       ├── docs/
│       ├── logs/
│       └── archive/
│
└── Typr/                  # Typing automation module
    ├── typr_main.py
    ├── config.json
    └── README.md
```

---

## 🧠 Autocomplete System Details

### Core Components

#### 1. **Trie Data Structure**
- Stores words in a tree structure for efficient prefix matching
- Each node represents a character
- Leaf nodes mark complete words
- Time Complexity: O(m) for search, where m = prefix length

#### 2. **Bloom Filter**
- Probabilistic data structure for membership testing
- Reduces memory footprint by ~90% compared to hash sets
- Zero false negatives, configurable false positive rate
- Ideal for pre-filtering before expensive Trie operations

#### 3. **Frequency Dictionary**
- Tracks how often each word is used
- Influences suggestion ranking
- Persists to disk using pickle
- Auto-updates based on user selections

### Algorithm Flow
```python
1. User inputs prefix "pro"
2. Bloom filter checks if any words start with "pro" (fast)
3. If positive, Trie performs prefix search
4. Results ranked by frequency from dictionary
5. Top N suggestions returned to user
6. User selection updates frequency data
7. Changes persisted to word_freq.pkl
```

### Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Insert | O(m) | O(alphabet_size × m) |
| Search | O(m) | O(1) |
| Prefix Match | O(p + n) | O(n) |
| Bloom Check | O(k) | O(m) bits |

*where m = word length, p = prefix length, n = matches, k = hash functions*

---

## 📊 Data Domains

### Aviation Module (`FINAL/avi/`)
- Flight routing optimization
- Aircraft performance analysis
- Airport traffic data processing
- Safety incident reports

### Database Module (`FINAL/mydb/`)
- SQL schema definitions
- Seed data generators
- Migration scripts
- Backup automation

### Visualization Module (`FINAL/plots/`)
- Statistical charts
- Usage trends
- Performance metrics
- Custom reporting graphics

### Scripts Module (`FINAL/scripts/`)
- Batch processing utilities
- Data transformation pipelines
- Automated reporting
- Format converters

---

## ⚙️ Configuration

### Autocomplete Settings

Edit these parameters in `autocomplete.py`:
```python
# Bloom Filter Configuration
BLOOM_CAPACITY = 100000        # Expected number of words
BLOOM_ERROR_RATE = 0.001       # False positive probability

# Suggestion Limits
MAX_SUGGESTIONS = 10           # Number of suggestions to return
MIN_FREQUENCY = 1              # Minimum frequency threshold

# Persistence
FREQ_FILE = 'word_freq.pkl'   # Frequency data storage
AUTO_SAVE = True               # Save after each update
```

### Database Configuration

Create `config.py` for database connections:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'foretype_db'
}
```

---

## 🛠 Development

### Adding New Words to Dictionary
```python
from autocomplete import AutocompleteSystem

ac = AutocompleteSystem()
ac.add_word('newword')
ac.save_frequencies()  # Persist changes
```

### Extending Functionality

**Custom ranking algorithm:**
```python
def custom_rank(suggestions, frequencies):
    # Your ranking logic here
    return sorted(suggestions, key=lambda w: your_metric(w))
```

**Adding domain-specific dictionaries:**
```python
# Load medical terms
ac.load_dictionary('medical_terms.txt')

# Load programming keywords
ac.load_dictionary('programming_lang.txt')
```

---

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/
```

Performance benchmark:
```bash
python benchmark.py --iterations 10000
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue:** `ImportError: No module named 'pybloom_live'`
```bash
pip install pybloom-live
```

**Issue:** `FileNotFoundError: word_freq.pkl`
- File auto-generates on first run
- Check write permissions in directory

**Issue:** Slow suggestions on large datasets
- Increase Bloom filter capacity
- Reduce MAX_SUGGESTIONS parameter
- Implement caching layer

---

## 🚧 Roadmap

- [ ] Convert modules into microservices architecture
- [ ] Add REST API endpoints for autocomplete
- [ ] Implement ML-based context-aware suggestions
- [ ] Docker containerization for easy deployment
- [ ] Comprehensive unit test coverage (target: 90%+)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Web interface using React/Vue
- [ ] Multi-language support
- [ ] Cloud deployment guides (AWS, GCP, Azure)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update README with new functionality

---

## 📄 License

This project is licensed under the MIT License.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Liability and warranty not provided

---

## 🙏 Acknowledgments

- Trie data structure implementation inspired by classic CS algorithms
- Bloom filter implementation using `pybloom-live` library
- Project structure follows best practices from Python Packaging Guide

---

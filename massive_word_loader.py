import sqlite3
import itertools
from extended_word_loader import ExtendedWordLoader

class MassiveWordLoader(ExtendedWordLoader):
    def __init__(self):
        super().__init__()
    
    def generate_common_prefixes_suffixes(self):
        """Generate words with common prefixes and suffixes"""
        
        prefixes = ["un", "re", "in", "dis", "en", "non", "im", "over", "mis", "out", "up", "pre", "anti", "de", "fore", "inter", "mid", "sub", "super", "semi", "auto", "co", "ex", "extra", "hyper", "micro", "multi", "post", "pro", "pseudo", "trans", "ultra", "under"]
        
        suffixes = ["ed", "ing", "ly", "er", "est", "ful", "ness", "less", "able", "ible", "ous", "ious", "al", "ial", "ic", "ical", "ive", "ary", "ory", "ize", "ise", "ation", "ition", "tion", "sion", "ment", "ance", "ence", "cy", "ty", "ity", "ship", "hood", "dom", "eer", "ess", "ism", "ist"]
        
        base_words = [
            "help", "work", "play", "make", "take", "give", "come", "go", "get", "see",
            "look", "watch", "listen", "hear", "speak", "talk", "say", "tell", "ask", "answer",
            "think", "know", "understand", "learn", "teach", "study", "read", "write", "draw",
            "paint", "sing", "dance", "run", "walk", "jump", "sit", "stand", "move", "stop",
            "start", "begin", "end", "finish", "continue", "break", "open", "close", "lock",
            "unlock", "turn", "push", "pull", "carry", "hold", "catch", "throw", "hit", "kick",
            "eat", "drink", "sleep", "wake", "dream", "love", "like", "hate", "want", "need",
            "have", "own", "buy", "sell", "cost", "pay", "spend", "save", "lose", "find",
            "search", "discover", "create", "build", "destroy", "fix", "repair", "clean", "wash",
            "cook", "bake", "drive", "fly", "swim", "climb", "fall", "rise", "grow", "live",
            "die", "born", "change", "stay", "leave", "arrive", "depart", "return", "travel"
        ]
        
        generated_words = set()
        
        # Generate prefix + base words
        for prefix in prefixes[:20]:  # Limit to avoid too many combinations
            for base in base_words[:30]:
                word = prefix + base
                if len(word) >= 3 and len(word) <= 15:
                    generated_words.add(word)
        
        # Generate base + suffix words
        for base in base_words:
            for suffix in suffixes[:25]:  # Limit to avoid too many combinations
                word = base + suffix
                if len(word) >= 3 and len(word) <= 15:
                    generated_words.add(word)
        
        # Generate prefix + base + suffix (limited)
        for prefix in prefixes[:10]:
            for base in base_words[:20]:
                for suffix in suffixes[:10]:
                    word = prefix + base + suffix
                    if len(word) >= 4 and len(word) <= 18:
                        generated_words.add(word)
        
        return list(generated_words)
    
    def add_technical_terms(self):
        """Add technical and scientific terms"""
        
        technical_words = [
            # Computing
            "algorithm", "binary", "decimal", "hexadecimal", "octal", "bit", "byte", "kilobyte",
            "megabyte", "gigabyte", "terabyte", "petabyte", "exabyte", "zettabyte", "yottabyte",
            "bandwidth", "latency", "throughput", "protocol", "packet", "frame", "datagram",
            "socket", "port", "firewall", "gateway", "router", "switch", "hub", "bridge",
            "repeater", "amplifier", "modulator", "demodulator", "encoder", "decoder",
            "compressor", "decompressor", "encryptor", "decryptor", "hash", "checksum",
            "signature", "certificate", "authentication", "authorization", "verification",
            
            # Mathematics
            "addition", "subtraction", "multiplication", "division", "exponentiation", "logarithm",
            "calculus", "integral", "derivative", "differential", "equation", "inequality",
            "function", "variable", "constant", "coefficient", "parameter", "matrix", "vector",
            "scalar", "tensor", "geometry", "trigonometry", "algebra", "statistics", "probability",
            "permutation", "combination", "factorial", "prime", "composite", "rational", "irrational",
            "real", "imaginary", "complex", "integer", "fraction", "decimal", "percentage",
            
            # Physics
            "velocity", "acceleration", "momentum", "force", "gravity", "friction", "tension",
            "pressure", "density", "mass", "weight", "volume", "area", "perimeter", "circumference",
            "diameter", "radius", "temperature", "heat", "energy", "power", "work", "efficiency",
            "wavelength", "frequency", "amplitude", "oscillation", "vibration", "resonance",
            "reflection", "refraction", "diffraction", "interference", "polarization", "magnetism",
            "electricity", "current", "voltage", "resistance", "capacitance", "inductance",
            
            # Chemistry
            "molecule", "atom", "element", "compound", "mixture", "solution", "suspension",
            "emulsion", "acid", "base", "salt", "oxide", "hydroxide", "carbonate", "sulfate",
            "nitrate", "phosphate", "chloride", "fluoride", "iodide", "bromide", "hydrogen",
            "oxygen", "nitrogen", "carbon", "sulfur", "phosphorus", "chlorine", "fluorine",
            "sodium", "potassium", "calcium", "magnesium", "iron", "copper", "zinc", "lead",
            
            # Biology
            "cell", "nucleus", "membrane", "cytoplasm", "mitochondria", "ribosome", "chloroplast",
            "photosynthesis", "respiration", "metabolism", "genetics", "chromosome", "gene",
            "protein", "enzyme", "hormone", "vitamin", "antibody", "vaccine", "bacteria", "virus",
            "fungus", "parasite", "organism", "species", "genus", "family", "order", "class",
            "phylum", "kingdom", "evolution", "mutation", "adaptation", "extinction", "fossil"
        ]
        
        for word in technical_words:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "technical", 'en'))
        
        self.conn.commit()
        print(f"Added {len(technical_words)} technical terms")
    
    def add_business_extended(self):
        """Add extended business and financial terms"""
        
        business_extended = [
            "revenue", "profit", "loss", "income", "expense", "budget", "forecast", "projection",
            "investment", "portfolio", "asset", "liability", "equity", "capital", "finance",
            "accounting", "audit", "tax", "compliance", "regulation", "legislation", "policy",
            "strategy", "planning", "analysis", "research", "development", "innovation",
            "marketing", "advertising", "promotion", "branding", "positioning", "segmentation",
            "targeting", "customer", "client", "consumer", "user", "market", "industry",
            "competition", "competitive", "advantage", "differentiation", "value", "proposition",
            "supply", "chain", "logistics", "inventory", "warehouse", "distribution", "retail",
            "wholesale", "ecommerce", "online", "digital", "transformation", "automation",
            "outsourcing", "offshoring", "insourcing", "procurement", "sourcing", "vendor",
            "supplier", "contract", "agreement", "negotiation", "partnership", "alliance",
            "merger", "acquisition", "takeover", "buyout", "ipo", "public", "offering",
            "stock", "share", "dividend", "bond", "commodity", "currency", "exchange",
            "trading", "broker", "dealer", "market", "maker", "arbitrage", "speculation",
            "hedging", "risk", "management", "insurance", "credit", "debit", "loan",
            "mortgage", "lease", "rental", "property", "real", "estate", "construction",
            "infrastructure", "transportation", "shipping", "aviation", "railway", "highway"
        ]
        
        for word in business_extended:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "business", 'en'))
        
        self.conn.commit()
        print(f"Added {len(business_extended)} business terms")
    
    def add_medical_extended(self):
        """Add extended medical and health terms"""
        
        medical_extended = [
            "diagnosis", "prognosis", "treatment", "therapy", "medication", "pharmaceutical",
            "prescription", "dosage", "symptom", "syndrome", "disorder", "disease", "illness",
            "condition", "infection", "inflammation", "bacteria", "virus", "fungus", "parasite",
            "cancer", "tumor", "benign", "malignant", "metastasis", "chemotherapy", "radiation",
            "surgery", "operation", "procedure", "transplant", "dialysis", "rehabilitation",
            "physical", "therapy", "occupational", "therapy", "speech", "therapy", "mental",
            "health", "psychology", "psychiatry", "neurology", "cardiology", "pulmonology",
            "gastroenterology", "hepatology", "nephrology", "endocrinology", "rheumatology",
            "immunology", "allergy", "dermatology", "ophthalmology", "otolaryngology",
            "orthopedics", "pediatrics", "geriatrics", "obstetrics", "gynecology", "urology",
            "anesthesiology", "radiology", "pathology", "emergency", "medicine", "critical",
            "care", "intensive", "care", "palliative", "care", "hospice", "preventive",
            "medicine", "public", "health", "epidemiology", "vaccination", "immunization",
            "screening", "testing", "diagnosis", "monitoring", "follow", "up", "checkup",
            "examination", "consultation", "referral", "specialist", "physician", "surgeon",
            "nurse", "practitioner", "technician", "therapist", "pharmacist", "dentist",
            "optometrist", "chiropractor", "acupuncturist", "nutritionist", "dietitian"
        ]
        
        for word in medical_extended:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "medical", 'en'))
        
        self.conn.commit()
        print(f"Added {len(medical_extended)} medical terms")
    
    def add_legal_terms(self):
        """Add legal and governmental terms"""
        
        legal_terms = [
            "law", "legal", "court", "judge", "justice", "attorney", "lawyer", "counsel",
            "plaintiff", "defendant", "prosecutor", "defense", "witness", "testimony",
            "evidence", "proof", "burden", "of", "proof", "reasonable", "doubt", "verdict",
            "judgment", "sentence", "punishment", "penalty", "fine", "imprisonment", "probation",
            "parole", "appeal", "appellate", "supreme", "constitutional", "statute", "regulation",
            "ordinance", "code", "act", "bill", "legislation", "congress", "senate", "house",
            "representatives", "president", "vice", "president", "cabinet", "department",
            "agency", "commission", "bureau", "administration", "authority", "board",
            "council", "committee", "subcommittee", "hearing", "investigation", "oversight",
            "ethics", "conflict", "of", "interest", "corruption", "bribery", "fraud",
            "embezzlement", "money", "laundering", "tax", "evasion", "insider", "trading",
            "securities", "exchange", "commission", "antitrust", "monopoly", "merger",
            "acquisition", "patent", "trademark", "copyright", "intellectual", "property",
            "trade", "secret", "non", "disclosure", "confidentiality", "privacy", "data",
            "protection", "cybersecurity", "hacking", "identity", "theft", "surveillance",
            "warrant", "subpoena", "deposition", "interrogation", "extradition", "asylum",
            "immigration", "citizenship", "naturalization", "deportation", "visa", "passport"
        ]
        
        for word in legal_terms:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "legal", 'en'))
        
        self.conn.commit()
        print(f"Added {len(legal_terms)} legal terms")
    
    def load_massive_dictionary(self):
        """Load all word collections"""
        print("Loading massive dictionary...")
        
        # Load generated words
        generated_words = self.generate_common_prefixes_suffixes()
        for word in generated_words:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "generated", 'en'))
        
        self.conn.commit()
        print(f"Added {len(generated_words)} generated words")
        
        # Load specialized vocabularies
        self.add_technical_terms()
        self.add_business_extended()
        self.add_medical_extended()
        self.add_legal_terms()
        
        # Get total word count
        self.cursor.execute("SELECT COUNT(*) FROM words")
        total_words = self.cursor.fetchone()[0]
        print(f"Total words in database: {total_words}")

if __name__ == "__main__":
    loader = MassiveWordLoader()
    loader.load_massive_dictionary()
    loader.close()

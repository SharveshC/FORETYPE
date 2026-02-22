import sqlite3
import requests
from typing import List, Dict

class WordLoader:
    def __init__(self):
        self.conn = sqlite3.connect('autocomplete.db')
        self.cursor = self.conn.cursor()
    
    def load_comprehensive_dictionary(self):
        """Load a comprehensive dictionary with thousands of words"""
        
        # English common words
        common_english = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
            "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
            "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
            "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
            "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
            "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
            "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
            "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
            "is", "was", "are", "been", "has", "had", "were", "said", "did", "having",
            "may", "am"
        ]
        
        # Technology words
        tech_words = [
            "computer", "software", "hardware", "programming", "algorithm", "database",
            "network", "internet", "website", "application", "mobile", "device", "laptop",
            "desktop", "server", "cloud", "artificial", "intelligence", "machine", "learning",
            "python", "javascript", "java", "html", "css", "react", "angular", "node",
            "express", "mongodb", "mysql", "postgresql", "redis", "docker", "kubernetes",
            "aws", "azure", "google", "microsoft", "apple", "facebook", "twitter", "instagram",
            "linkedin", "github", "stackoverflow", "api", "rest", "graphql", "json", "xml",
            "security", "encryption", "authentication", "authorization", "blockchain",
            "cryptocurrency", "bitcoin", "ethereum", "nft", "metaverse", "virtual", "reality",
            "augmented", "iot", "sensors", "robotics", "automation", "analytics", "data",
            "bigdata", "hadoop", "spark", "tensorflow", "pytorch", "keras", "scikit",
            "pandas", "numpy", "matplotlib", "plotly", "tableau", "powerbi", "excel",
            "spreadsheet", "powerpoint", "word", "document", "pdf", "presentation", "email",
            "calendar", "slack", "teams", "zoom", "skype", "telegram", "whatsapp", "signal",
            "vpn", "proxy", "firewall", "antivirus", "malware", "phishing", "spam", "backup",
            "storage", "memory", "ram", "cpu", "gpu", "motherboard", "keyboard", "mouse",
            "monitor", "printer", "scanner", "webcam", "microphone", "speakers", "headphones",
            "usb", "hdmi", "bluetooth", "wifi", "ethernet", "router", "modem", "switch",
            "cable", "fiber", "optic", "satellite", "gps", "navigation", "mapping", "geolocation"
        ]
        
        # Academic words
        academic_words = [
            "research", "study", "analysis", "methodology", "hypothesis", "theory", "experiment",
            "data", "statistics", "probability", "mathematics", "physics", "chemistry", "biology",
            "psychology", "sociology", "anthropology", "history", "philosophy", "literature",
            "linguistics", "economics", "political", "science", "geography", "geology",
            "astronomy", "engineering", "medicine", "nursing", "pharmacy", "dentistry",
            "veterinary", "agriculture", "environmental", "climate", "sustainability",
            "renewable", "energy", "solar", "wind", "hydroelectric", "nuclear", "fossil",
            "education", "university", "college", "school", "student", "teacher", "professor",
            "curriculum", "syllabus", "assignment", "examination", "thesis", "dissertation",
            "journal", "publication", "citation", "reference", "bibliography", "plagiarism",
            "academic", "scholarship", "grant", "funding", "research", "development", "innovation",
            "patent", "intellectual", "property", "copyright", "trademark", "license",
            "peer", "review", "conference", "symposium", "workshop", "seminar", "lecture",
            "tutorial", "course", "online", "distance", "learning", "platform", "mooc"
        ]
        
        # Business words
        business_words = [
            "business", "company", "corporation", "enterprise", "organization", "startup",
            "entrepreneur", "founder", "ceo", "manager", "director", "executive", "employee",
            "staff", "personnel", "human", "resources", "recruitment", "hiring", "training",
            "development", "performance", "review", "promotion", "salary", "wage", "bonus",
            "benefit", "compensation", "retirement", "pension", "insurance", "healthcare",
            "marketing", "advertising", "sales", "revenue", "profit", "loss", "income",
            "expense", "budget", "finance", "accounting", "audit", "tax", "investment",
            "portfolio", "stock", "share", "bond", "commodity", "currency", "exchange",
            "banking", "loan", "credit", "debit", "mortgage", "lease", "rent", "property",
            "real", "estate", "construction", "infrastructure", "transportation", "logistics",
            "supply", "chain", "inventory", "warehouse", "distribution", "retail", "wholesale",
            "customer", "client", "service", "support", "satisfaction", "loyalty", "retention",
            "acquisition", "merger", "partnership", "joint", "venture", "franchise", "license",
            "contract", "agreement", "negotiation", "deal", "transaction", "purchase", "sale",
            "order", "invoice", "receipt", "payment", "billing", "pricing", "discount", "offer"
        ]
        
        # Medical words
        medical_words = [
            "medicine", "medical", "doctor", "physician", "surgeon", "nurse", "patient",
            "hospital", "clinic", "emergency", "ambulance", "paramedic", "treatment", "therapy",
            "diagnosis", "symptom", "disease", "illness", "condition", "disorder", "syndrome",
            "infection", "virus", "bacteria", "cancer", "tumor", "diabetes", "hypertension",
            "heart", "attack", "stroke", "brain", "lungs", "liver", "kidney", "stomach",
            "intestine", "blood", "pressure", "cholesterol", "glucose", "insulin", "hormone",
            "vitamin", "mineral", "nutrition", "diet", "exercise", "fitness", "health",
            "wellness", "prevention", "vaccination", "immunization", "antibiotic", "medication",
            "drug", "pharmaceutical", "prescription", "dosage", "side", "effect", "allergy",
            "surgery", "operation", "procedure", "anesthesia", "recovery", "rehabilitation",
            "physical", "therapy", "occupational", "mental", "psychology", "psychiatry",
            "depression", "anxiety", "stress", "disorder", "schizophrenia", "bipolar",
            "autism", "adhd", "dementia", "alzheimer", "parkinson", "multiple", "sclerosis",
            "arthritis", "osteoporosis", "asthma", "allergy", "eczema", "psoriasis", "migraine"
        ]
        
        # Science words
        science_words = [
            "science", "scientific", "research", "experiment", "theory", "hypothesis",
            "observation", "measurement", "analysis", "conclusion", "result", "data",
            "method", "procedure", "technique", "technology", "innovation", "discovery",
            "invention", "physics", "chemistry", "biology", "astronomy", "geology", "ecology",
            "evolution", "genetics", "molecule", "atom", "particle", "quantum", "relativity",
            "gravity", "force", "energy", "power", "electricity", "magnetism", "light",
            "sound", "wave", "radiation", "nuclear", "fusion", "fission", "particle",
            "accelerator", "telescope", "microscope", "spectrometer", "laboratory", "equipment",
            "instrument", "tool", "device", "apparatus", "mechanism", "system", "process",
            "reaction", "compound", "element", "substance", "material", "property", "characteristic",
            "behavior", "function", "structure", "composition", "formula", "equation", "calculation",
            "computation", "simulation", "model", "prediction", "forecast", "projection",
            "estimation", "approximation", "accuracy", "precision", "error", "uncertainty",
            "significant", "statistical", "correlation", "causation", "variable", "parameter",
            "constant", "coefficient", "factor", "ratio", "proportion", "percentage", "rate"
        ]
        
        # Entertainment words
        entertainment_words = [
            "movie", "film", "cinema", "theater", "show", "performance", "concert", "music",
            "song", "album", "artist", "musician", "singer", "band", "orchestra", "symphony",
            "instrument", "guitar", "piano", "drums", "violin", "trumpet", "saxophone",
            "television", "tv", "series", "episode", "season", "drama", "comedy", "thriller",
            "horror", "action", "adventure", "romance", "documentary", "animation", "cartoon",
            "video", "game", "gaming", "player", "character", "level", "score", "achievement",
            "multiplayer", "online", "console", "playstation", "xbox", "nintendo", "mobile",
            "sports", "football", "basketball", "baseball", "soccer", "tennis", "golf",
            "swimming", "running", "cycling", "boxing", "wrestling", "martial", "arts",
            "yoga", "meditation", "dance", "ballet", "theater", "broadway", "musical",
            "opera", "comedy", "standup", "magic", "illusion", "circus", "carnival", "festival",
            "celebration", "party", "event", "gathering", "reunion", "vacation", "holiday",
            "travel", "tourism", "adventure", "exploration", "journey", "trip", "destination"
        ]
        
        # Food words
        food_words = [
            "food", "eat", "eating", "restaurant", "cafe", "diner", "bistro", "bakery",
            "pizza", "burger", "sandwich", "salad", "soup", "pasta", "rice", "bread",
            "cheese", "meat", "chicken", "beef", "pork", "fish", "seafood", "vegetable",
            "fruit", "apple", "banana", "orange", "grape", "strawberry", "blueberry",
            "potato", "tomato", "onion", "garlic", "carrot", "broccoli", "spinach", "lettuce",
            "breakfast", "lunch", "dinner", "meal", "snack", "dessert", "cake", "cookie",
            "ice", "cream", "chocolate", "candy", "sweet", "sugar", "salt", "pepper",
            "spice", "herb", "flavor", "taste", "delicious", "yummy", "cooking", "recipe",
            "ingredient", "kitchen", "chef", "cook", "baking", "grilling", "frying", "boiling",
            "roasting", "steaming", "microwave", "oven", "stove", "refrigerator", "freezer",
            "dish", "plate", "bowl", "cup", "glass", "fork", "spoon", "knife", "chopstick",
            "napkin", "tablecloth", "placemat", "coaster", "beverage", "drink", "water", "juice",
            "coffee", "tea", "milk", "soda", "beer", "wine", "cocktail", "alcohol", "liquor"
        ]
        
        # Nature words
        nature_words = [
            "nature", "natural", "environment", "outdoor", "wildlife", "animal", "bird",
            "fish", "insect", "plant", "tree", "flower", "grass", "leaf", "branch", "root",
            "forest", "jungle", "rainforest", "desert", "mountain", "hill", "valley", "canyon",
            "river", "stream", "creek", "lake", "pond", "ocean", "sea", "beach", "shore",
            "coast", "island", "continent", "country", "state", "city", "town", "village",
            "weather", "climate", "temperature", "season", "spring", "summer", "autumn",
            "winter", "rain", "snow", "wind", "storm", "hurricane", "tornado", "earthquake",
            "volcano", "fire", "flood", "drought", "sun", "moon", "star", "sky", "cloud",
            "rainbow", "lightning", "thunder", "fog", "mist", "dew", "frost", "ice",
            "sunrise", "sunset", "dawn", "dusk", "night", "day", "morning", "afternoon",
            "evening", "midnight", "noon", "twilight", "darkness", "brightness", "shadow",
            "reflection", "echo", "silence", "sound", "noise", "quiet", "peaceful", "calm",
            "serene", "beautiful", "scenic", "breathtaking", "magnificent", "spectacular"
        ]
        
        # Combine all word lists
        all_words = {
            "common": common_english,
            "technology": tech_words,
            "academic": academic_words,
            "business": business_words,
            "medical": medical_words,
            "science": science_words,
            "entertainment": entertainment_words,
            "food": food_words,
            "nature": nature_words
        }
        
        # Insert words into database with categories
        for category, words in all_words.items():
            for word in words:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO words (word, frequency, category, language)
                    VALUES (?, ?, ?, ?)
                ''', (word.lower(), 0, category, 'en'))
        
        self.conn.commit()
        print(f"Loaded {sum(len(words) for words in all_words.values())} words into database")
    
    def add_programming_keywords(self):
        """Add programming-specific keywords"""
        programming_words = [
            "function", "variable", "constant", "array", "list", "dictionary", "tuple", "set",
            "class", "object", "method", "property", "attribute", "constructor", "destructor",
            "inheritance", "polymorphism", "encapsulation", "abstraction", "interface", "abstract",
            "static", "dynamic", "type", "string", "integer", "float", "boolean", "character",
            "pointer", "reference", "memory", "allocation", "deallocation", "garbage", "collection",
            "recursion", "iteration", "loop", "while", "for", "foreach", "do", "until",
            "conditional", "if", "else", "switch", "case", "break", "continue", "return",
            "exception", "error", "handling", "try", "catch", "finally", "throw", "raise",
            "debugging", "testing", "unit", "integration", "system", "acceptance", "regression",
            "framework", "library", "package", "module", "dependency", "version", "control",
            "git", "github", "gitlab", "bitbucket", "repository", "commit", "push", "pull",
            "branch", "merge", "conflict", "resolution", "code", "review", "quality", "assurance",
            "continuous", "integration", "deployment", "delivery", "devops", "agile", "scrum",
            "kanban", "waterfall", "sprint", "backlog", "user", "story", "epic", "task",
            "bug", "feature", "enhancement", "hotfix", "release", "candidate", "production",
            "staging", "development", "environment", "configuration", "deployment", "pipeline"
        ]
        
        for word in programming_words:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "programming", 'en'))
        
        self.conn.commit()
        print(f"Added {len(programming_words)} programming keywords")
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    loader = WordLoader()
    loader.load_comprehensive_dictionary()
    loader.add_programming_keywords()
    loader.close()

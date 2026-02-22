import sqlite3
import random
from word_loader import WordLoader

class ExtendedWordLoader(WordLoader):
    def __init__(self):
        super().__init__()
    
    def add_extended_vocabulary(self):
        """Add thousands more words across many categories"""
        
        # Emotions and feelings
        emotions = [
            "happy", "sad", "angry", "excited", "nervous", "calm", "peaceful", "anxious",
            "confident", "insecure", "proud", "ashamed", "grateful", "resentful", "hopeful",
            "desperate", "optimistic", "pessimistic", "enthusiastic", "apathetic", "passionate",
            "indifferent", "concerned", "worried", "relieved", "frustrated", "satisfied",
            "disappointed", "thrilled", "terrified", "brave", "cowardly", "courageous",
            "fearful", "joyful", "miserable", "content", "discontent", "cheerful", "gloomy",
            "elated", "depressed", "ecstatic", "devastated", "surprised", "shocked", "amazed",
            "bored", "interested", "curious", "confused", "understanding", "doubtful", "certain",
            "uncertain", "confident", "insecure", "arrogant", "humble", "modest", "vain",
            "jealous", "envious", "generous", "selfish", "kind", "cruel", "compassionate",
            "empathetic", "sympathetic", "cold", "warm", "friendly", "hostile", "gentle",
            "harsh", "patient", "impatient", "tolerant", "intolerant", "forgiving", "resentful"
        ]
        
        # Colors and descriptions
        colors = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black",
            "white", "gray", "silver", "gold", "cyan", "magenta", "violet", "indigo", "turquoise",
            "crimson", "scarlet", "maroon", "burgundy", "navy", "sky", "royal", "baby",
            "lime", "olive", "emerald", "forest", "mint", "amber", "honey", "golden", "bronze",
            "copper", "rust", "coral", "salmon", "peach", "apricot", "lavender", "lilac",
            "plum", "orchid", "mauve", "beige", "cream", "ivory", "pearl", "charcoal", "slate",
            "steel", "ash", "smoke", "mist", "fog", "dawn", "dusk", "twilight", "midnight",
            "bright", "dark", "light", "pale", "vivid", "dull", "glossy", "matte", "shiny",
            "translucent", "transparent", "opaque", "clear", "murky", "cloudy", "hazy"
        ]
        
        # Action verbs
        action_verbs = [
            "run", "walk", "jump", "skip", "hop", "dance", "swim", "fly", "drive", "ride",
            "climb", "crawl", "slide", "glide", "float", "sink", "rise", "fall", "drop", "lift",
            "push", "pull", "drag", "carry", "hold", "grab", "catch", "throw", "kick", "hit",
            "strike", "punch", "slap", "pat", "touch", "feel", "sense", "perceive", "notice",
            "observe", "watch", "see", "look", "stare", "glance", "glimpse", "peek", "spy",
            "listen", "hear", "speak", "talk", "say", "tell", "shout", "whisper", "yell", "scream",
            "sing", "hum", "whistle", "laugh", "cry", "sob", "weep", "giggle", "chuckle", "snicker",
            "eat", "drink", "chew", "swallow", "bite", "taste", "smell", "sniff", "inhale", "exhale",
            "breathe", "sleep", "wake", "dream", "think", "remember", "forget", "learn", "teach",
            "study", "read", "write", "draw", "paint", "create", "build", "construct", "destroy",
            "break", "fix", "repair", "clean", "wash", "dry", "polish", "shine", "decorate",
            "arrange", "organize", "sort", "collect", "gather", "scatter", "distribute", "share"
        ]
        
        # Adjectives
        adjectives = [
            "big", "small", "large", "tiny", "huge", "massive", "enormous", "gigantic", "miniature",
            "short", "tall", "long", "wide", "narrow", "thick", "thin", "fat", "skinny", "slim",
            "heavy", "light", "strong", "weak", "powerful", "gentle", "rough", "smooth", "soft",
            "hard", "solid", "liquid", "gas", "hot", "cold", "warm", "cool", "freezing", "boiling",
            "wet", "dry", "moist", "damp", "soaked", "dehydrated", "fresh", "stale", "new", "old",
            "young", "ancient", "modern", "ancient", "recent", "past", "future", "present",
            "fast", "slow", "quick", "rapid", "gradual", "sudden", "immediate", "delayed",
            "early", "late", "punctual", "timely", "overdue", "permanent", "temporary", "brief",
            "extended", "short", "long", "eternal", "momentary", "instant", "prolonged",
            "beautiful", "ugly", "pretty", "handsome", "attractive", "repulsive", "gorgeous",
            "plain", "elegant", "clumsy", "graceful", "awkward", "smooth", "rough", "refined",
            "coarse", "sophisticated", "simple", "complex", "complicated", "easy", "difficult",
            "hard", "challenging", "impossible", "possible", "achievable", "unrealistic"
        ]
        
        # Places and locations
        places = [
            "home", "house", "apartment", "condo", "mansion", "cottage", "cabin", "hut", "shack",
            "office", "workplace", "factory", "warehouse", "store", "shop", "mall", "market",
            "school", "university", "college", "library", "museum", "gallery", "theater", "cinema",
            "park", "garden", "playground", "stadium", "arena", "gym", "pool", "beach", "resort",
            "hotel", "motel", "inn", "hostel", "restaurant", "cafe", "bar", "pub", "club",
            "airport", "station", "terminal", "platform", "dock", "port", "harbor", "marina",
            "hospital", "clinic", "pharmacy", "bank", "post", "office", "church", "temple",
            "mosque", "synagogue", "cathedral", "chapel", "shrine", "monument", "statue",
            "bridge", "tunnel", "road", "street", "avenue", "boulevard", "lane", "highway",
            "intersection", "corner", "square", "plaza", "courtyard", "patio", "balcony",
            "rooftop", "basement", "attic", "garage", "driveway", "parking", "lot", "garage"
        ]
        
        # Time and seasons
        time_words = [
            "morning", "afternoon", "evening", "night", "dawn", "dusk", "noon", "midnight",
            "today", "tomorrow", "yesterday", "now", "then", "soon", "later", "early", "late",
            "before", "after", "during", "while", "when", "where", "here", "there", "everywhere",
            "somewhere", "anywhere", "nowhere", "above", "below", "inside", "outside", "between",
            "among", "through", "across", "around", "behind", "front", "back", "side", "left",
            "right", "up", "down", "forward", "backward", "north", "south", "east", "west",
            "spring", "summer", "autumn", "fall", "winter", "season", "month", "january",
            "february", "march", "april", "may", "june", "july", "august", "september",
            "october", "november", "december", "monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday", "weekend", "weekday", "holiday", "vacation", "break",
            "moment", "second", "minute", "hour", "day", "week", "month", "year", "decade",
            "century", "millennium", "age", "era", "period", "phase", "stage", "step", "level"
        ]
        
        # Professional terms
        professional = [
            "manager", "director", "executive", "president", "vice", "ceo", "cto", "cfo", "coo",
            "supervisor", "team", "leader", "head", "chief", "senior", "junior", "intern",
            "trainee", "apprentice", "consultant", "advisor", "specialist", "expert", "professional",
            "amateur", "volunteer", "freelancer", "contractor", "employee", "employer", "staff",
            "personnel", "workforce", "colleague", "partner", "associate", "assistant", "secretary",
            "receptionist", "clerk", "accountant", "bookkeeper", "analyst", "researcher", "developer",
            "designer", "engineer", "architect", "planner", "coordinator", "administrator", "operator",
            "technician", "mechanic", "electrician", "plumber", "carpenter", "painter", "cleaner",
            "driver", "pilot", "captain", "sailor", "soldier", "officer", "detective", "investigator",
            "reporter", "journalist", "editor", "writer", "author", "publisher", "producer", "director",
            "actor", "actress", "musician", "artist", "performer", "entertainer", "comedian", "magician"
        ]
        
        # Technology terms
        tech_extended = [
            "smartphone", "tablet", "laptop", "desktop", "computer", "monitor", "keyboard", "mouse",
            "printer", "scanner", "camera", "webcam", "microphone", "speakers", "headphones", "earbuds",
            "charger", "battery", "cable", "wire", "adapter", "router", "modem", "switch", "hub",
            "server", "cloud", "storage", "backup", "memory", "ram", "rom", "cpu", "gpu", "ssd",
            "hdd", "usb", "hdmi", "vga", "ethernet", "wifi", "bluetooth", "nfc", "gps", "gprs",
            "lte", "5g", "4g", "3g", "2g", "network", "internet", "web", "site", "page", "link",
            "url", "domain", "host", "ip", "address", "protocol", "http", "https", "ftp", "smtp",
            "pop", "imap", "dns", "dhcp", "vpn", "proxy", "firewall", "antivirus", "malware",
            "spyware", "ransomware", "phishing", "spam", "junk", "filter", "block", "allow",
            "permit", "deny", "access", "login", "logout", "password", "username", "email",
            "account", "profile", "settings", "preferences", "options", "tools", "utilities",
            "applications", "apps", "software", "programs", "system", "operating", "windows",
            "mac", "linux", "android", "ios", "chrome", "firefox", "safari", "edge", "browser"
        ]
        
        # Extended word lists
        extended_words = {
            "emotions": emotions,
            "colors": colors,
            "actions": action_verbs,
            "adjectives": adjectives,
            "places": places,
            "time": time_words,
            "professional": professional,
            "tech_extended": tech_extended
        }
        
        # Insert extended words
        for category, words in extended_words.items():
            for word in words:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO words (word, frequency, category, language)
                    VALUES (?, ?, ?, ?)
                ''', (word.lower(), 0, category, 'en'))
        
        self.conn.commit()
        total_words = sum(len(words) for words in extended_words.values())
        print(f"Added {total_words} extended words")
    
    def add_compound_words(self):
        """Add common compound words and phrases"""
        compound_words = [
            "smartphone", "laptop", "website", "database", "software", "hardware", "network",
            "keyboard", "mousepad", "touchscreen", "screenshot", "download", "upload", "online",
            "offline", "login", "logout", "signup", "signin", "password", "username", "email",
            "mailbox", "homepage", "webpage", "hyperlink", "bookmark", "search", "engine",
            "social", "media", "facebook", "twitter", "instagram", "youtube", "netflix",
            "amazon", "google", "microsoft", "apple", "samsung", "sony", "nike", "adidas",
            "mcdonald", "starbucks", "subway", "walmart", "target", "costco", "bestbuy",
            "homeschool", "workplace", "workstation", "desktop", "notebook", "clipboard",
            "flashlight", "headlight", "taillight", "spotlight", "sunlight", "moonlight",
            "daylight", "twilight", "midnight", "overnight", "tonight", "tonite", "tonite",
            "goodnight", "goodmorning", "goodevening", "goodafternoon", "goodbye", "hello",
            "welcome", "goodluck", "congratulations", "celebration", "anniversary", "birthday",
            "wedding", "graduation", "retirement", "promotion", "vacation", "holiday", "festival"
        ]
        
        for word in compound_words:
            self.cursor.execute('''
                INSERT OR IGNORE INTO words (word, frequency, category, language)
                VALUES (?, ?, ?, ?)
            ''', (word.lower(), 0, "compound", 'en'))
        
        self.conn.commit()
        print(f"Added {len(compound_words)} compound words")
    
    def add_variations(self):
        """Add common variations and plurals"""
        base_words = ["cat", "dog", "bird", "fish", "tree", "flower", "car", "house", "book", "pen"]
        
        variations = []
        for word in base_words:
            variations.extend([
                word,  # singular
                word + "s",  # plural
                word + "ing",  # gerund
                word + "ed",  # past tense
                "un" + word,  # negative prefix
                "re" + word,  # repetition prefix
            ])
        
        for word in variations:
            if word:  # Skip empty strings
                self.cursor.execute('''
                    INSERT OR IGNORE INTO words (word, frequency, category, language)
                    VALUES (?, ?, ?, ?)
                ''', (word.lower(), 0, "variations", 'en'))
        
        self.conn.commit()
        print(f"Added {len(variations)} word variations")

if __name__ == "__main__":
    loader = ExtendedWordLoader()
    loader.add_extended_vocabulary()
    loader.add_compound_words()
    loader.add_variations()
    loader.close()

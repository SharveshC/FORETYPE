import pickle
import os
from pybloom_live import BloomFilter
from datetime import datetime

# --- Folder and File Paths ---
STATE_DIR = "system_state"
FLIGHT_REPORTS_DIR = "flight reports"
INCIDENT_REPORTS_DIR = "incident reports"
STATE_FILE = os.path.join(STATE_DIR, 'aviation_system_state.pkl')

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
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.word = word

    def get_suggestions(self, prefix):
        node = self.root
        for char in prefix.lower():
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

class AutoCompleteSystem:
    def __init__(self):
        self.trie = None
        self.bloom = None
        self.word_freq = None
        self.load_state()

    def load_state(self):
        os.makedirs(STATE_DIR, exist_ok=True)
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'rb') as f:
                    state = pickle.load(f)
                    self.trie = state['trie']
                    self.bloom = state['bloom']
                    self.word_freq = state['freq']
                    return
            except Exception as e:
                print(f"Warning: Could not load state file. Starting fresh. Error: {e}")
        
        self.trie = Trie()
        self.bloom = BloomFilter(capacity=5000, error_rate=0.01)
        self.word_freq = {}

    def save_state(self):
        os.makedirs(STATE_DIR, exist_ok=True)
        state = {
            'trie': self.trie,
            'bloom': self.bloom,
            'freq': self.word_freq
        }
        with open(STATE_FILE, 'wb') as f:
            pickle.dump(state, f)
            print(f"\nSystem state saved to '{STATE_FILE}'.")

    def add_word(self, word):
        if word not in self.word_freq:
            self.word_freq[word] = 0
        self.trie.insert(word)
        for i in range(1, len(word) + 1):
            self.bloom.add(word[:i].lower())

    def get_suggestions(self, prefix):
        if self.bloom is None or prefix.lower() not in self.bloom:
            return []
        words = self.trie.get_suggestions(prefix)
        words.sort(key=lambda w: (-self.word_freq.get(w, 0), w))
        return words

    def select_word(self, word):
        if word in self.word_freq:
            self.word_freq[word] += 1

    def _rebuild_structures(self):
        self.trie = Trie()
        self.bloom = BloomFilter(capacity=len(self.word_freq) * 2, error_rate=0.01)
        for word in self.word_freq.keys():
            self.trie.insert(word)
            for i in range(1, len(word) + 1):
                self.bloom.add(word[:i].lower())

    def replace_word(self, old_word, new_word):
        if old_word not in self.word_freq:
            return False
        freq = self.word_freq.pop(old_word)
        self.word_freq[new_word] = freq
        self._rebuild_structures()
        return True

def run_checklist(system, procedures):
    checklist_log = []
    total_steps = len(procedures)
    print("\n--- ✈️ Starting Aviation Checklist Process ---")
    input("Press Enter to begin...")
    for i, procedure in enumerate(procedures):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"--- Step {i+1}/{total_steps} ---")
        print(f"\nPROCEDURE: {procedure}\n")
        response = input("Type 'ok' to confirm, or press Enter to skip: ").strip().lower()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "OK" if response == 'ok' else "SKIPPED"
        if status == "OK":
            system.select_word(procedure)
        checklist_log.append({"procedure": procedure, "status": status, "timestamp": timestamp})
    return checklist_log

def log_incidents(system):
    incident_log = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- ⚠️ Log Failures / Incidents ---")
        print("Search for an incident (e.g., 'engine'). Type '!done' when finished.\n")
        prefix = input("Search Incident: ").strip()
        if prefix == '!done':
            break
        if not prefix:
            continue
        
        search_term = prefix.lower()
        all_words = system.word_freq.keys()
        incident_suggestions = [
            word for word in all_words 
            if word.startswith("INCIDENT:") and search_term in word.lower()
        ]
        incident_suggestions.sort(key=lambda w: (-system.word_freq.get(w, 0), w))

        if incident_suggestions:
            print("\nMatching Incidents:")
            for i, procedure in enumerate(incident_suggestions, 1):
                freq = system.word_freq.get(procedure, 0)
                print(f"  {i}. {procedure} (Logged: {freq} times)")
            
            choice = input("\nSelect incident to log (Enter to skip): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(incident_suggestions):
                    chosen_incident = incident_suggestions[idx]
                    system.select_word(chosen_incident)
                    print("\nPlease provide additional details for the incident:")
                    flight_name = input("  - Flight Name/Number: ").strip()
                    incident_time = input("  - Time of Incident: ").strip()
                    flight_journey = input("  - Flight Journey (e.g., LAX to JFK): ").strip()
                    incident_log.append({
                        "name": chosen_incident,
                        "flight": flight_name,
                        "time": incident_time,
                        "journey": flight_journey
                    })
                    print(f"\nLogged: '{chosen_incident}'")
        else:
            print("\nNo matching incidents found.")
        input("\nPress Enter to continue...")
    return incident_log

def generate_final_report(checklist_log, incident_log, report_filename):
    report_content = []
    report_content.append("="*50)
    report_content.append("--- ✈️ Post-Flight Final Report ---")
    report_content.append("="*50)
    
    if checklist_log:
        report_content.append(f"\n--- Checklist Summary ---")
        ok_count = sum(1 for item in checklist_log if item['status'] == 'OK')
        skipped_count = len(checklist_log) - ok_count
        report_content.append(f"Confirmed: {ok_count} | Skipped: {skipped_count}\n")
        for item in checklist_log:
            report_content.append(f"[{item['status']}] - {item['procedure']}")
    
    if incident_log:
        report_content.append(f"\n--- Logged Incidents & Failures ---")
        report_content.append(f"Total incidents logged: {len(incident_log)}\n")
        for incident in incident_log:
            report_content.append(f"  Incident: {incident['name']}")
            report_content.append(f"  Flight:   {incident['flight']}")
            report_content.append(f"  Time:     {incident['time']}")
            report_content.append(f"  Journey:  {incident['journey']}\n")

    report_content.append("="*50)
    final_report = "\n".join(report_content)
    with open(report_filename, 'w') as f:
        f.write(final_report)
    print(final_report)
    print(f"\nReport saved to '{report_filename}'")

def display_frequencies(system):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- 📊 Procedure & Incident Frequencies ---")
    
    if not system.word_freq:
        print("\nNo frequencies have been logged yet.")
    else:
        sorted_items = sorted(system.word_freq.items(), key=lambda item: item[1], reverse=True)
        print("\n(Most frequent items are listed first)\n")
        for item, freq in sorted_items:
            print(f"  - {item} (Logged: {freq} times)")
    input("\nPress Enter to return to menu.")

def main():
    system = AutoCompleteSystem()
    if not system.word_freq:
        print("Preloading default dictionary...")
        data = [
            "PREFLIGHT - Cockpit Preparation", "PREFLIGHT - Exterior Inspection",
            "ENGINE START - Ignition and Start", "TAXI - Brake and Steering Check",
            "TAKEOFF - Flaps and Power Set", "CLIMB - Autopilot Engage",
            "CRUISE - Fuel and Systems Monitor", "DESCENT - Pressurization Check",
            "APPROACH - Landing Gear and Flaps", "LANDING - Final Approach and Touchdown",
            "GO AROUND - Aborted Landing Procedure", "SHUTDOWN - Parking Brake and Avionics Off",
            "INCIDENT: ENGINE FIRE - Emergency Shutdown", "INCIDENT: ENGINE FAILURE - Glide and Restart",
            "INCIDENT: HYD SYS - Hydraulic System Failure", "INCIDENT: NAV SYS - Navigation System Failure",
            "INCIDENT: COMMS - Radio Communication Loss", "INCIDENT: BIRD STRIKE - Damage Assessment",
            "INCIDENT: HIJACKING - Unlawful Interference", "INCIDENT: CABIN DEPRESSURIZATION",
            "INCIDENT: MEDICAL EMERGENCY - Onboard Passenger"
        ]
        for item in data:
            system.add_word(item)

    checklist_procedures = [item for item in system.word_freq.keys() if not item.startswith("INCIDENT:")]
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- ✈️ Aviation Operations Menu ---")
        print("\n1. Start Full Checklist & Log Incidents")
        print("2. Log a Standalone Incident")
        print("3. View Frequencies")
        print("4. Exit")
        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            checklist_log = run_checklist(system, checklist_procedures)
            incident_log = log_incidents(system)
            timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs(FLIGHT_REPORTS_DIR, exist_ok=True)
            report_filename = os.path.join(FLIGHT_REPORTS_DIR, f"flight_report_{timestamp_str}.txt")
            generate_final_report(checklist_log, incident_log, report_filename)
            input("\nFull report generated. Press Enter to return to menu.")
        elif choice == '2':
            incident_log = log_incidents(system)
            if incident_log:
                timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                os.makedirs(INCIDENT_REPORTS_DIR, exist_ok=True)
                report_filename = os.path.join(INCIDENT_REPORTS_DIR, f"incident_report_{timestamp_str}.txt")
                generate_final_report([], incident_log, report_filename)
                input("\nIncident report generated. Press Enter to return to menu.")
        elif choice == '3':
            display_frequencies(system)
        elif choice == '4':
            break
        else:
            input("Invalid option. Press Enter to try again.")
            
    system.save_state()
    print("Exiting system.")

if __name__ == "__main__":
    main()

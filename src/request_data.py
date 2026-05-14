import requests
import time
import config
from data_handler import save_json

API_URL = "https://api-global-points.easypack24.net/v1/points"
TARGET_CITY = "Warszawa"
DESIRED_COUNT = 500

SEARCH_TERMS = [
    "Warszawa Domaniewska", "Warszawa Konstruktorska", "Warszawa Postępu", "Warszawa Marynarska",
    "Warszawa Puławska", "Warszawa Marszałkowska", "Warszawa Aleje Jerozolimskie",
    "Warszawa Grochowska", "Warszawa Wolska", "Warszawa Targowa",
    "Warszawa Górczewska", "Warszawa Czerniakowska", "Warszawa Ostrobramska",
    "Warszawa Modlińska", "Warszawa Radzymińska", "Warszawa Grójecka",
    "Warszawa Krakowska", "Warszawa Jana Pawła", "Warszawa Solidarności",
    "Warszawa Towarowa", "Warszawa Żelazna", "Warszawa Prosta",
    "Warszawa Jagiellońska", "Warszawa Francuska", "Warszawa Wał Miedzeszyński",
    "Warszawa Powstańców Śląskich", "Warszawa KEN", "Warszawa Rosoła",
    "Warszawa Wiertnicza", "Warszawa Sobieskiego", "Warszawa Sikorskiego"
]

def fetch_lockers_from_api(search_term: str) -> list:
    """Fetches a batch of lockers from the InPost API based on a search term."""
    params = {"search": search_term, "per_page": 50}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {search_term}: {e}")
        return []

def is_valid_locker(item: dict) -> bool:
    """Checks if the locker meets our strict criteria."""
    city = item.get('address', {}).get('city', '')
    has_image = bool(item.get('image_url'))
    return city == TARGET_CITY and has_image

def collect_lockers() -> list:
    """Orchestrates the downloading process and ensures uniqueness."""
    unique_lockers = {}
    
    print(f"🚀 Starting smart download for {DESIRED_COUNT} UNIQUE {TARGET_CITY} lockers...")
    
    for term in SEARCH_TERMS:
        if len(unique_lockers) >= DESIRED_COUNT:
            break
            
        print(f"🔍 Searching area: {term}...")
        items = fetch_lockers_from_api(term)
        
        added_this_round = 0
        for item in items:
            name = item.get('name')
            if name not in unique_lockers and is_valid_locker(item):
                unique_lockers[name] = item
                added_this_round += 1
                if len(unique_lockers) >= DESIRED_COUNT:
                    break
                    
        print(f"   ✅ Found {added_this_round} new lockers. Total so far: {len(unique_lockers)}")
        time.sleep(0.2)
        
    return list(unique_lockers.values())

def main():
    final_lockers = collect_lockers()
    
    save_json(final_lockers, config.INPUT_FILE)
    
    print(f"\n🎉 SUCCESS! Saved {len(final_lockers)} UNIQUE lockers to {config.INPUT_FILE}")

if __name__ == "__main__":
    main()
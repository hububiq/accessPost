import requests
import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config
from data_handler import save_json

API_URL = "https://api-global-points.easypack24.net/v1/points"
TARGET_CITY = "Warszawa"
DESIRED_COUNT = 500

def fetch_all_lockers_page(page: int) -> list:
    """Fetches a raw page of 100 lockers from the global database."""
    params = {"per_page": 100, "page": page}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Page {page}: {e}")
        return []

def is_valid_locker(item: dict) -> bool:
    """Checks if the locker is in Warsaw and has an image."""
    city = item.get('address_details', {}).get('city', '')
    has_image = bool(item.get('image_url'))
    return city == TARGET_CITY and has_image

def collect_lockers() -> list:
    unique_lockers = {}
    page_number = 1300 
    
    print(f"🚀 Bruteforcing the API to find {DESIRED_COUNT} UNIQUE {TARGET_CITY} lockers...")
    print("⏩ Fast-forwarding directly to the 'W' section of the database...\n")
    
    while len(unique_lockers) < DESIRED_COUNT:
        items = fetch_all_lockers_page(page_number)
        
        if not items:
            print("Reached the end of the InPost database!")
            break
            
        first_locker_name = items[0].get('name', 'Unknown')
            
        for item in items:
            name = item.get('name')
            if name not in unique_lockers and is_valid_locker(item):
                unique_lockers[name] = item
                
                if len(unique_lockers) >= DESIRED_COUNT:
                    break
                    
        print(f"   📄 Scanned Page {page_number} (Currently at: {first_locker_name}) | Warsaw Lockers found: {len(unique_lockers)} / {DESIRED_COUNT}")
        page_number += 1
        time.sleep(0.1) 
        
    return list(unique_lockers.values())

def main():
    final_lockers = collect_lockers()
    
    save_json(final_lockers, config.INPUT_FILE)
    
    print(f"\n🎉 SUCCESS! Saved {len(final_lockers)} UNIQUE lockers to {config.INPUT_FILE}")

if __name__ == "__main__":
    main()
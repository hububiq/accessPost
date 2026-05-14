import requests
import json
import time
import os 

DESIRED_COUNT = 500
TARGET_CITY = "Warszawa"


all_points_sample = []
page_count = 1

print(f"🚀 Started downloading {DESIRED_COUNT} locker for the city of: {TARGET_CITY}...")

while len(all_points_sample) < DESIRED_COUNT:
    url = f"https://api-global-points.easypack24.net/v1/points?city={TARGET_CITY}"
    try:
        response = requests.get(url)
        response.raise_for_status() # throws and error if status is not 200
        
        data = response.json()
        items = data.get('items', [])
        if len(items) == 0:
            print("Reached the end of the available lockers for this city.")
            break
        all_points_sample.extend(data['items'])

        print(f"   Downloaded page {page_count}... We currently have {len(all_points_sample)} points.")

        page_count += 1
        time.sleep(0.1)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error occured during download {e}")
        break
final_points = all_points_sample[:DESIRED_COUNT]
print(f"\n✅ Download completed.!")
print(f"📊 Went through number of pages: {page_count}")
print(f"📦 Retrieving exactly: {len(final_points)} lockers.")

output_folder = "data"
os.makedirs(output_folder, exist_ok=True)
file_name = f"lockers_{TARGET_CITY.lower()}_{DESIRED_COUNT}.json"
output_filepath = os.path.join(output_folder, file_name)
with open(output_filepath, "w", encoding="utf-8") as f:
    json.dump(final_points, f, indent=4, ensure_ascii=False)

print(f"💾 Done. Data are in a file: {output_filepath}")
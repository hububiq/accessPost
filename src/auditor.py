import time
from vision_service import analyze_accessibility
from vertexai.generative_models import GenerativeModel

def run_accessibility_audit(lockers: list, ai_model: GenerativeModel) -> list:
    """Iterates through lockers, audits their images, and enriches the data - core business logic"""
    processed_count = 0
    total = len(lockers)

    for locker in lockers:
        processed_count += 1
        image_url = locker.get('image_url')
        
        if image_url:
            print(f"[{processed_count}/{total}] Auditing locker: {locker.get('name')}...")
            result = analyze_accessibility(ai_model, image_url)
            locker['accessibility_score'] = result.get('accessibility_score') # enriching
            locker['accessibility_reasoning'] = result.get('reasoning')
            time.sleep(1)
        else:
            print(f"[{processed_count}/{total}] Locker {locker.get('name')} has no image. Skipping.")
            locker['accessibility_score'] = None
            locker['accessibility_reasoning'] = "No image available."

    return lockers
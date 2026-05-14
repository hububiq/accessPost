import config
from data_handler import load_json, save_json
from vision_service import initialize_ai_model
from auditor import run_accessibility_audit

def main():
    print(" Initializing accessPost Auditor...")

    model = initialize_ai_model(config.PROJECT_ID, config.LOCATION, config.MODEL_NAME)

    print(f" Loading lockers from {config.INPUT_FILE}...")
    lockers_data = load_json(config.INPUT_FILE)
    print("\n Starting image analysis...")
    enriched_lockers = run_accessibility_audit(lockers_data, model)
    save_json(enriched_lockers, config.OUTPUT_FILE)
    print(f"\n Audit complete! Enriched data saved to {config.OUTPUT_FILE}")

if __name__ == '__main__':
    main()
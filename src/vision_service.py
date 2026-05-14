import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part  # Part - class built by Google for AI to be multimodal - not only text, also images etc.
from prompt import ACCESSIBILITY_AUDITOR_PROMPT

def initialize_ai_model(project_id: str, location: str, model_name: str) -> GenerativeModel:
    """Initializes and returns the Vertex AI Generative Model."""
    vertexai.init(project=project_id, location=location)
    return GenerativeModel(model_name)

def analyze_accessibility(vision_model: GenerativeModel, image_url: str) -> dict:
    """
    Analyzes an image URL using the provided AI model and returns an accessibility score.
    """
    try:
        image_part = Part.from_uri(uri=image_url, mime_type="image/jpeg")
        response = vision_model.generate_content([image_part, ACCESSIBILITY_AUDITOR_PROMPT])
        json_text = response.text.strip().replace("```json", "").replace("```", "") # cleaning json
        return json.loads(json_text)
    except Exception as api_error:
        print(f"   [!] AI Service Error for {image_url}: {api_error}")
        return {
            "accessibility_score": 0, 
            "reasoning": "Failed to analyze image due to an API error."
        }
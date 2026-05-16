import json
from google import genai
from agent.config import GEMINI_API_KEY, LLM_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_llm(prompt: str) -> dict:
    """Envía el prompt a Gemini y devuelve la respuesta parseada como dict."""
    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        config={
            "temperature": 0.9,
            "top_p": 0.95,
            "response_mime_type": "application/json"
        }
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        clean = response.text.strip().strip("```json").strip("```").strip()
        return json.loads(clean)
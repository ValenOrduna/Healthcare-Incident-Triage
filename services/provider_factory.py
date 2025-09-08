from utils.config import load_enviroment
from services.gemini_service import GeminiAIService
from services.mock_service import MockService

# Cargamos las variables de entorno
config = load_enviroment()

LLM_PROVIDER = config.get("LLM_PROVIDER","mock")

GEMINI_API_KEY = config.get("GEMINI_API_KEY")

def get_llm_provider ():
  if LLM_PROVIDER == "gemini":
    return GeminiAIService(api_key=GEMINI_API_KEY)
  elif LLM_PROVIDER == "mock":
    return MockService()
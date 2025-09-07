from google import genai
from google.genai import types
import json
from uuid import uuid4
from models.incidents import IncidentResponse
from exceptions.service_exceptions import PromptError,GeminiError
from services.llm_provider import LLMProvider


# Clase encargada de controlar y efectuar la conexion de Gemini
class GeminiAIService(LLMProvider) :
  def __init__(self,api_key:str):
    # Extraemos el entrenamiento del modelo de un archivo TXT
    try:
      with open("./prompts/prompt.txt","r") as prompt:
        SYSTEM_INSTRUCTION = prompt.read()
    except FileNotFoundError:
      raise PromptError("No se pudo encontrar el archivo 'prompt.txt'. Verifica que el archivo exista.")
    except Exception:
        raise PromptError(f"Ocurrió un error inesperado al leer el prompt")
    
    self.__client = genai.Client(api_key=api_key)
    
    self.__model = 'gemini-2.5-pro'
    
    # Configuramos todo el modelo de Gemini a nuestra manera
    self.__config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=IncidentResponse,
    )
  
  def generate_response (self,incident_request:str) -> dict :
    try:
      
      # Petición para generar la respuesta
      response = self.__client.models.generate_content(
        model=self.__model,
        contents=incident_request,
        config=self.__config
      )

      incident = json.loads(response.text)
      
      if not incident["error"]:
        # Generamos el id de la incidencia
        incident["id"] = f"inc_{uuid4()}"
        del incident["error"]
        del incident["error_mensaje"]
        
      return incident
    
    except Exception:
      raise GeminiError( "No se pudo inicializar el cliente de Gemini. Verifica que la API Key sea válida y que la cuenta tenga saldo suficiente.")
      
  

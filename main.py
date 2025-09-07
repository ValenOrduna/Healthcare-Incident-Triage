from fastapi import FastAPI,Response ,HTTPException,status
from models.incidents import IncidentRequest
from services.gemini_service import GeminiAIService
from models.incidents import IncidentResponse
import structlog
from config.logging_config import setup_logging
from exceptions.service_exceptions import PromptError,GeminiError
from models.persistence import Csv

# Iniciamos el logger
setup_logging()

logger = structlog.get_logger()

app = FastAPI(title="Healthcare Incident Triage",description="Ejercicio de Xoolix",version="1.0.0")

# Inicializamos la IA
try:
    ai_service = GeminiAIService() 
except PromptError as e:
    logger.critical("Iniciar modelo", razon=str(e))
  
# Instanciamos la persistencia
csv = Csv("data","incidents")

# Ruta para comprobar el estado del servidor
@app.get("/health",tags=["Estado del Servicio"])
def get_health_status () -> dict:
  return {"status":"ok"}

# Ruta para subir incidentes 
@app.post("/incidents", tags=["Incidentes"])
def create_incident (body:IncidentRequest) -> dict:

  incident_request = body.texto
    
  try:
    # Generamos la respuesta en base a la incidencia
    incident_response = ai_service.generate_response(incident_request)
    
    # Si la incidencia contiene algun error
    if "error" in incident_response:
      raise HTTPException(
              status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
              detail=incident_response["error_mensaje"]
      )
    
    # La subimos a la persistencia
    csv.add_incident(incident_response)
    
    logger.info("Creacion de incidente",id_incidente=incident_response["id"])
      
    return incident_response
  
  except GeminiError as e:
    logger.critical("Generar respuesta", razon=str(e))
    raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail="Error al abrir el modelo"
    )
  
from fastapi import FastAPI,Response ,HTTPException,status
from models.incidents import IncidentRequest
from services.provider_factory import get_llm_provider
from models.incidents import IncidentResponse
import structlog
from config.logging_config import setup_logging
from exceptions.service_exceptions import PromptError,GeminiError
from models.persistence import Csv
from analytics.metrics_service import MetricsService
from models.metrics import MetricsResponse

# Iniciamos el logger
setup_logging()

logger = structlog.get_logger()

app = FastAPI(title="Healthcare Incident Triage",description="Ejercicio de Xoolix",version="1.0.0")

# Inicializamos la IA
try:
    ai_service = get_llm_provider()
except PromptError as e:
    logger.critical("Iniciar modelo", razon=str(e))
  
# Instanciamos la persistencia
csv = Csv("data","incidents")

# Ruta para comprobar el estado del servidor
@app.get("/health",tags=["Estado del Servicio"])
def get_health_status () -> dict:
  return {"status":"ok"}

# Ruta para obtener incidentes
@app.get("/incidents",tags=["Incidentes"])
def get_incidents (categoria:str = None,prioridad:int = None):
  try:
    incidents = csv.get_incidents(categoria,prioridad)
    return incidents
  except Exception as e:
    logger.error(
      "Obtener incidentes", 
      razon=str(e)
    )
        
  raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ocurrió un error interno al obtener los incidentes."
  )

# Ruta para subir incidentes 
@app.post("/incidents", tags=["Incidentes"],status_code=status.HTTP_201_CREATED)
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

# Ruta para obtener metricas 
@app.get("/metrics",tags=["Metricas"],response_model=MetricsResponse)
def get_metrics () :
  try:
    incidents = csv.get_incidents()
    metrics = MetricsService(incidents)
    total_incidents = metrics.get_total_incidents()
    categorys_incidents = metrics.get_category_summary()
    prioritys_incidents = metrics.get_priority_summary()
    
    return {"total_incidencias":total_incidents,"categorias_incidencias":categorys_incidents,"prioridades_incidencias":prioritys_incidents}
  except Exception as e:
    logger.error(
            "Generacion de metricas",
            razon=str(e)
    )
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Ocurrió un error al generar las métricas."
    )

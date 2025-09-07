from fastapi import APIRouter,HTTPException,status,Depends
from models.incidents import IncidentRequest
import structlog
from services.provider_factory import get_llm_provider
from models.incidents import IncidentResponse
from exceptions.service_exceptions import PromptError,GeminiError
from models.persistence import Csv
from utils.security import validate_api_key

router = APIRouter(
  prefix="/incidents",
  tags=["Incidentes"],
  dependencies=[Depends(validate_api_key)]
)

logger = structlog.get_logger()

# Inicializamos la IA
try:
    ai_service = get_llm_provider()
except PromptError as e:
    logger.critical("Iniciar modelo", razon=str(e))
  
# Instanciamos la persistencia
csv = Csv("data","incidents")

# Ruta para obtener incidentes
@router.get("/",tags=["Incidentes"])
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
@router.post("/", tags=["Incidentes"],status_code=status.HTTP_201_CREATED)
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
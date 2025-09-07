from fastapi import APIRouter, HTTPException,Depends,status
from models.metrics import MetricsResponse
from models.persistence import Csv
from analytics.metrics_service import MetricsService
import structlog
from utils.security import validate_api_key

router = APIRouter(
  prefix="/metrics",
  tags=["Metricas"],
  dependencies=[Depends(validate_api_key)]
)

logger = structlog.get_logger()

# Instanciamos la persistencia
csv = Csv("data","incidents")

# Ruta para obtener metricas 
@router.get("/",tags=["Metricas"],response_model=MetricsResponse)
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
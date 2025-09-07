from fastapi import FastAPI,Response ,HTTPException,status
from routes import incidents,metrics
from config.logging_config import setup_logging
from analytics.metrics_service import MetricsService
from models.metrics import MetricsResponse

# Iniciamos el logger
setup_logging()

app = FastAPI(title="Healthcare Incident Triage",description="Ejercicio de Xoolix",version="1.0.0")

app.include_router(incidents.router)

app.include_router(metrics.router)

# Ruta para comprobar el estado del servidor
@app.get("/health",tags=["Estado del Servicio"])
def get_health_status () -> dict:
  return {"status":"ok"}


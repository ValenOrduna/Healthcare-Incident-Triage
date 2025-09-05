from fastapi import FastAPI
from utils.response import send_response

app = FastAPI(title="Healthcare Incident Triage",description="Ejercicio de Xoolix",version="1.0.0")

@app.get("/health",tags=["Estado del Servicio"])
def get_health_status ():
  return send_response(200,"Ok")
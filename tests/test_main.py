from fastapi.testclient import TestClient
from main import app
from utils.config import load_enviroment

config = load_enviroment()

SECRET_API_KEY = config.get("SECRET_API_KEY")

client = TestClient(app)

# Test: Comprobar estado del servicio
def test_health_check():

    response = client.get("/health")
    
    assert response.status_code == 200
    
    assert response.json() == {"status": "ok"}
    
# Test: Crear incidente sin autenticación
def test_create_incident_no_auth ():
    headers = {"X-API-Key": "API_KEY_INVALIDA"}
    response = client.post("/incidents",headers=headers,json={"texto": "asdsad"})

    assert response.status_code == 401
    
# Test: Obtener incidentes sin autenticación
def test_get_incidents_no_auth ():
     headers = {"X-API-Key": "API_KEY_INVALIDA"}
     
     response = client.get("/incidents",headers=headers)
     
     assert response.status_code == 401

# Test: Obtener metricas sin autenticación
def test_get_metrics_no_auth ():
     headers = {"X-API-Key": "API_KEY_INVALIDA"}
     
     response = client.get("/metrics",headers=headers)
     
     assert response.status_code == 401

# Test: Crear incidencia con menos de 10 caracteres
def test_create_incident_no_length ():
    headers = {"X-API-Key": SECRET_API_KEY}
    
    response = client.post("/incidents",headers=headers,json={"texto": "Corto"})

    assert response.status_code == 422
  
# Test: Crear incidencia con autenticación
def test_create_incident_auth ():
    headers = {"X-API-Key": SECRET_API_KEY}
    
    response = client.post("/incidents",headers=headers,json={"texto": "El sistema PACS no carga las tomografías."})

    assert response.status_code == 201

# Test: Obtener incidencias con autenticación
def test_get_incidents_auth():

    headers = {"X-API-Key": SECRET_API_KEY}
    
    response = client.get("/incidents", headers=headers)
    
    assert response.status_code == 200
    
    assert isinstance(response.json(), list)
    
# Test: Obtener incidencias filtrandolas con autenticación
def test_get_incident_filter ():

    headers = {"X-API-Key": SECRET_API_KEY}
    
    querys = {
        "categoria": "sistema_imagenes",
        "prioridad":3
    }
    
    response = client.get("/incidents", headers=headers,params=querys)
    
    assert response.status_code == 200
    
    assert isinstance(response.json(), list)
    
    assert len(response.json()) > 0

# Test: Obtener metricas con autenticación
def test_get_metrics_auth():

    headers = {"X-API-Key": SECRET_API_KEY}
    
    response = client.get("/metrics", headers=headers)
    
    assert response.status_code == 200
    
    response_data = response.json()
    assert "total_incidencias" in response_data
    assert "categorias_incidencias" in response_data
    assert "prioridades_incidencias" in response_data
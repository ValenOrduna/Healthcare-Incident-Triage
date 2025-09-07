from uuid import uuid4
from services.llm_provider import LLMProvider

class MockService (LLMProvider) :
  
  def generate_response (self,text:str) -> dict:
    
    incident = {
      "id":f"inc_{uuid4()}",
      "texto_original":text,
      "categoria":"sistema_imagenes | sistema_laboratorio | agenda_turnos | facturacion | acceso_pacientes | infraestructura_it | otra",
      "prioridad":1,
      "resumen": f"Resumen breve de la incidencia: {text}",
      "entidades": [
        { "tipo": "sintoma | sistema | modalidad | sede | ubicacion | analisis | resultado | obra_social | accion | dispositivo | area | ...", 
        "valor": "texto extraído" }
      ]
    }
    
    return incident
    

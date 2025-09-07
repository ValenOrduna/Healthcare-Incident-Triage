from pydantic import BaseModel, Field, AfterValidator
from typing import List, Optional, Annotated

# Verifica que el texto cumpla con la longitud minima
def check_min_length(value: str) -> str:
    min_len = 10
    if len(value) < min_len:
        raise ValueError(f'La descripción de la incidencia debe tener al menos {min_len} caracteres.')
    return value

# Modelo que valida y crea documentación de un incidente
IncidentText = Annotated[str, Field(
        description="Descripción en texto libre de la incidencia reportada.",
        example="El sistema PACS no carga las tomografías."
    ),
    AfterValidator(check_min_length)]

# Modelo petición incidencia
class IncidentRequest(BaseModel):
  texto: IncidentText

# Modelo entidad
class Entity (BaseModel):
    tipo: Optional[str]
    valor: Optional[str]

# Modelo respuesta de la incidencia
class IncidentResponse (BaseModel):
    id:Optional[str]
    texto_original: Optional[str]
    categoria: Optional[str]
    prioridad: Optional[str]
    resumen: Optional[str]
    entidades: Optional[List[Entity]]
    error: Optional[bool]
    error_mensaje:Optional[str]
  
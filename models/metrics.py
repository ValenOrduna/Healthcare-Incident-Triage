from pydantic import BaseModel
from typing import List

class CategorySummary (BaseModel) :
  categoria:str
  cantidad:int
  porcentaje:int
  
class PrioritySummary (BaseModel):
  prioridad:int
  cantidad:int
  porcentaje:int
  
class MetricsResponse (BaseModel):
  total_incidencias:int
  categorias_incidencias:List[CategorySummary]
  prioridades_incidencias:List[PrioritySummary]
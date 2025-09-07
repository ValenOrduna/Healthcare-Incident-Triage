import pandas as pd
from pandas.errors import EmptyDataError
from pathlib import Path
import os
import json

class Csv () :
  def __init__ (self,folder:str = "data",file:str = "incidents.csv"):
    # Ruta de la carpeta y el archivo Csv
    self.__data_folder = Path(folder)
    self.__incidents_file_path = self.__data_folder / f"{file}.csv"
    self._create_if_not_exists()
    
  def _create_if_not_exists(self):
      self.__data_folder.mkdir(exist_ok=True)
        
      if not self.__incidents_file_path.exists():
          columnas = ["id", "texto_original", "categoria", "prioridad", "resumen", "entidades"]
          df = pd.DataFrame(columns=columnas)
          df.to_csv(self.__incidents_file_path, index=False)

  # Función para subir incidente al archivo
  def add_incident (self,incident):
    
    data_incidents = pd.DataFrame([incident])

    data_incidents.to_csv(
        self.__incidents_file_path,  
        mode='a',     
        header=False,  
        index=False,    
        encoding='utf-8-sig' 
    )
  
  # Funcion para filtrar incidentes
  def _filter_incidents (self,incident:dict,category:str = None, priority:int = None):
    is_category = not category or incident.get("categoria") == category
    is_priority = not priority or incident.get("prioridad") == priority
            
    return is_category and is_priority

  
  # Obtener incidentes
  def get_incidents (self,category:str = None,priority:int = None):
    try:
      data_incidents = pd.read_csv(self.__incidents_file_path)
      all_incidents = data_incidents.to_dict(orient='records')
      incidents = [inc for inc in all_incidents if self._filter_incidents(inc, category, priority)]
    except EmptyDataError:
      incidents = []
    
    return incidents
    
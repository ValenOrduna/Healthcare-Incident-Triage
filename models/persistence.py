import pandas as pd
from pathlib import Path
import os

class Csv () :
  def __init__ (self,folder,file):
    # Ruta de la carpeta y el archivo Csv
     self.__data_folder = Path(folder)
     self.__incidents_file_path = f"{self.__data_folder}/{file}.csv"
  
  # Función para subir incidente al archivo
  def add_incident (self,incident):
    self.__data_folder.mkdir(exist_ok=True)
    
    header_incidents = not os.path.exists(self.__incidents_file_path)
    
    df = pd.DataFrame([incident])

    df.to_csv(
        self.__incidents_file_path,  
        mode='a',       
        index=False,    
        header=header_incidents,
        encoding='utf-8-sig' 
    )
class MetricsService () :
  
  def __init__(self,incidents:list):
    self.__incidents = incidents
    self.__total_incidents = len(incidents)
    
  def get_total_incidents (self) :
    return self.__total_incidents
  
  def __calculate_summary (self,property:str):
    counts = {}
    summary = []
    
    for incident in self.__incidents:
      name = incident[property]
      counts[name] = counts.get(property, 0) + 1
    
    for key, value in counts.items():
      percentage = round(value / self.__total_incidents * 100,1)
      summary.append({property:key,"cantidad":value,"porcentaje":percentage})
    
    return summary
  
  def get_category_summary (self):
    return self.__calculate_summary("categoria")

  def get_priority_summary (self):
    return self.__calculate_summary("prioridad")
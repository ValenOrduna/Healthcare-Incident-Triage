from dotenv import load_dotenv,dotenv_values

def load_enviroment ():
  load_dotenv()
  config = dotenv_values(".env")
  return config
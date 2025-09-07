from fastapi import Security,HTTPException,status
from fastapi.security import APIKeyHeader
from utils.config import load_enviroment

config = load_enviroment()

SECRET_API_KEY = config.get("SECRET_API_KEY")

api_key_header = APIKeyHeader(name="X-API-Key")

def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o ausente."
        )
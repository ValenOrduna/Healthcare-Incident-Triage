# Healthcare Incident Triage API

Una API inteligente que utiliza IA para clasificar, priorizar y gestionar automáticamente incidencias en centros de salud, optimizando los tiempos de respuesta.

## 📄 Resumen del Proyecto

Este proyecto resuelve la necesidad de automatizar la gestión de incidencias en un centro de diagnóstico. La API RESTful, construida con **FastAPI**, recibe descripciones de problemas en texto libre, las procesa con **Google Gemini** para clasificarlas y extraer datos clave, y persiste los resultados para su posterior análisis.

La arquitectura está diseñada para ser robusta y escalable, separando la lógica en capas de servicios, modelos e incluye un proveedor de IA "mock" para facilitar las pruebas.

## 🚀 Características Principales

- **Clasificación Inteligente**: Analiza y clasifica automáticamente cada incidencia.
- **Extracción de Datos**: Identifica información crucial como equipo afectado, ubicación, etc.
- **Asignación de Prioridad**: Asigna un nivel de prioridad para guiar la respuesta.
- **Persistencia de Datos**: Guarda todas las incidencias y sus análisis en un archivo CSV.
- **API Segura**: Endpoints protegidos mediante autenticación por API Key.
- **Métricas y Salud**: Incluye endpoints para monitoreo del servicio y obtención de métricas.

## 🛠️ Stack Tecnológico

- **Lenguaje**: **Python**
- **Framework**: **FastAPI**
- **IA Generativa**: **Google Gemini**
- **Almacenamiento**: **Pandas** (para CSV)
- **Logging**: **Structlog**
- **Testing**: **Pytest**
- **Configuración**: **Dotenv**

## ⚙️ Cómo Empezar

Sigue estos pasos para levantar el proyecto en tu máquina local.

### **1. Prerrequisitos**

- Python 3.9+
- Git

### **2. Instalación**

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/ValenOrduna/Healthcare-Incident-Triage.git


   cd Healthcare-Incident-Triage
   ```

2. **Crea y activa un entorno virtual:**

   ```bash
   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate


   # En Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto y añade las siguientes claves.

   ```ini
   # Clave secreta para proteger los endpoints
   SECRET_API_KEY="tu_clave_secreta"


   # Tu clave de API para Google Gemini
   GEMINI_API_KEY="tu_api_key_de_gemini"


   # Define el proveedor de IA a usar: "gemini" (real) o "mock" (para tests)
   LLM_PROVIDER="gemini"
   ```

### **3. Ejecución**

Una vez configurado, inicia el servidor con Uvicorn:

```bash
uvicorn main:app --reload
```

### **4. Ejecutar los Tests**

Para correr la suite de tests automatizados:

```bash
pytest
```

## 📡 Endpoints de la API

| Endpoint     | Método | Descripción                                          | Auth Requerida |
| :----------- | :----- | :--------------------------------------------------- | :------------- |
| `/health`    | `GET`  | Verifica que el servicio esté funcionando.           | No             |
| `/incidents` | `POST` | Procesa y clasifica una nueva incidencia.            | Sí             |
| `/incidents` | `GET`  | Obtiene la lista de incidencias (permite filtros).   | Sí             |
| `/metrics`   | `GET`  | Devuelve un resumen con métricas de las incidencias. | Sí             |

## 📚 Documentación y Uso de la API

Con el servidor corriendo, la documentación interactiva OpenAPI (generada por FastAPI) está disponible en:

http://127.0.0.1:8000/docs

Desde esa URL puedes explorar y probar todos los endpoints. Recuerda que las rutas protegidas requieren un encabezado X-API-Key con el valor de tu SECRET_API_KEY.

from fastapi import FastAPI
from app import auth, chat
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine
from alembic.config import Config
from alembic import command
import os

app = FastAPI()

# Миграции Alembic
@app.on_event("startup")
def apply_migrations():
    try:
        # Путь до alembic.ini
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        logging.info("✅ Alembic migrations applied")
    except Exception as e:
        logging.error(f"❌ Failed to apply Alembic migrations: {e}")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://10.121.252.227",
        "http://10.121.252.227:3000",
        "http://frontend:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, tags=["Chat"])

# OpenAPI с BearerAuth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ML API",
        version="1.0.1",
        description="Custom API with Bearer Auth only",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Запуск в Docker
if __name__ == "__main__":
    import uvicorn
    import os
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=False)

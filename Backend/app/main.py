from fastapi import FastAPI
from app import auth, chat  # ✅ auth.py и chat.py в папке app
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://87.255.209.201",        # без порта (если нужно)
        "http://87.255.209.201:3000",    # с портом, если фронт работает на 3000
         "http://frontend:3000"  # если фронт работает в контейнере с именем frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, tags=["Chat"])

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
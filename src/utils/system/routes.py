# src/routes.py
from src.interfaces.api.v1.gateway_controller import router as gateway_controller
from src.interfaces.api.v1.microservice_controller import router as microservice_controller

def register_routers(app):
    app.include_router(gateway_controller, prefix="/api/v1", tags=["gateway"])
    app.include_router(microservice_controller, prefix="/api/v1", tags=["microservice"])

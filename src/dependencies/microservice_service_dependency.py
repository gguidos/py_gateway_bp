# src/dependencies/microservice_service_dependency.py

from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from src.services.ms_service import MicroserviceService
from src.infrastructure.di_container import Container
from src.dependencies.request_id_dependency import get_request_id
import logging

logger = logging.getLogger(__name__)

@inject
async def get_ms_service(
    request_id: str = Depends(get_request_id),  # First, get the request ID
    ms_service: MicroserviceService = Depends(Provide[Container.microservice_service])  # Get an instance of MsRegistrationService from the DI container
) -> MicroserviceService:
    """Create a MsRegistrationService instance with the provided request_id."""
    logger.debug(f"Creating MsRegistrationService with request_id: {request_id}")
    
    # Set the request_id dynamically for the service
    ms_service.request_id = request_id
    
    logger.debug(f"MsRegistrationService created: {ms_service}")
    return ms_service

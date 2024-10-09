from typing import Optional
from fastapi import HTTPException
from src.core.entities.microservice import Microservice
from src.core.repositories.db_repository import DBRepository
from src.core.use_cases.get_ms import GetMicroservices
from src.core.use_cases.get_all_ms import GetAllMicroservices
import logging


logger = logging.getLogger(__name__)
class GetMicroservices:
    """Service layer for managing microservice registration."""

    def __init__(self, db_repository: DBRepository, request_id: Optional[str] = None):
        self.db_repository = db_repository
        self.get_microservices_use_case = GetMicroservices(self.db_repository)
        self.get_all_microservices_use_case = GetAllMicroservices(self.db_repository)
        self.request_id = request_id
    
    async def get_microservice_by_name(self, service_name: str) -> Optional[Microservice]:
        """Retrieve a microservice by its service name.

        Args:
            service_name (str): The name of the microservice to retrieve.

        Returns:
            Optional[Microservice]: The Microservice entity if found, otherwise None.
        """
        try:
            microservice = await self.get_microservices_use_case.execute(service_name=service_name)
            if not microservice:
                logger.info(f"Microservice with name '{service_name}' not found.", extra={"request_id": self.request_id})
            return microservice

        except Exception as e:
            # Log and raise unexpected exceptions
            logger.error(f"Failed to retrieve microservice '{service_name}': {e}", extra={"request_id": self.request_id})
            raise HTTPException(status_code=500, detail=f"Failed to retrieve microservice '{service_name}': {e}")
        
    async def get_all_microservices(self):
        """Retrieve all microservices.
        
        Returns:
            Optional[Microservice]: The Microservice entities if found, otherwise None.
        """
        try:
            microservice = await self.get_microservices_use_case.execute()
            return microservice

        except Exception as e:
            # Log and raise unexpected exceptions
            logger.error(f"Failed to retrieve microservices: {e}", extra={"request_id": self.request_id})
            raise HTTPException(status_code=500, detail=f"Failed to retrieve microservices: {e}")

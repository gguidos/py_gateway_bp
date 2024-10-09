from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from src.core.entities.microservice import Microservice
from src.core.repositories.db_repository import DBRepository
from src.core.use_cases.create_ms import CreateMicroservice
from src.core.use_cases.get_ms import GetMicroservices
from src.core.use_cases.get_all_ms import GetAllMicroservices
from src.infrastructure.exception_handlers import DuplicateMsException
import logging

logger = logging.getLogger(__name__)

class MicroserviceService:
    """Service layer for managing microservice registration."""

    def __init__(self, db_repository: DBRepository, request_id: Optional[str] = None):
        self.db_repository = db_repository
        self.create_microservice_use_case = CreateMicroservice(self.db_repository)
        self.get_microservices_use_case = GetMicroservices(self.db_repository)
        self.get_all_microservices_use_case = GetAllMicroservices(self.db_repository)
        self.request_id = request_id

    async def register_microservice(self, microservice_data: Dict[str, Any]) -> Microservice:
        """Register a new microservice using the create_ms use-case."""
        # Convert the dictionary to a Microservice entity for validation
        microservice_entity = Microservice(**microservice_data)

        # Check if a microservice with the same name already exists
        existing_microservice = await self.get_microservices_use_case.execute(service_name=microservice_entity.service_name)
        if existing_microservice:
            logger.error(f"Microservice with name: {microservice_entity.service_name} already exists.", extra={"request_id": self.request_id})
            raise DuplicateMsException(service_name=microservice_entity.service_name)  # Raise custom exception

        # Register the microservice using the create use-case
        try:
            registered_microservice = await self.create_microservice_use_case.execute(microservice_entity)
            logger.info(f"Microservice created successfully: {registered_microservice}", extra={"request_id": self.request_id})
            return registered_microservice

        except ValueError as ve:
            # Catch any value errors and re-raise them with HTTP exception
            logger.error(f"Validation error occurred: {ve}", extra={"request_id": self.request_id})
            raise ve

        except Exception as e:
            # Log and raise unexpected exceptions to be handled by global exception handlers
            logger.error(f"Failed to register microservice: {e}", extra={"request_id": self.request_id})
            raise HTTPException(status_code=500, detail=f"Failed to register microservice: {e}")

    async def get_all_microservices(self):
        """Retrieve all microservices."""
        try:
            # Retrieve documents and convert them to Pydantic Microservice models
            documents = await self.get_all_microservices_use_case.execute()
            print(documents)
            # microservices = [Microservice.from_mongo_dict(doc) for doc in documents]
            return documents

        except Exception as e:
            # Log and raise unexpected exceptions
            logger.error(f"Failed to retrieve microservices: {e}", extra={"request_id": self.request_id})
            raise HTTPException(status_code=500, detail=f"Failed to retrieve microservices: {e}")

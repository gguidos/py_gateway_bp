# src/core/use_cases/get_microservices.py

from typing import List, Optional
from src.core.entities.microservice import Microservice
from src.core.repositories.db_repository import DBRepository

class GetAllMicroservices:
    """Use-case for getting microservices by service name."""

    def __init__(self, db_repository: DBRepository):
        self.db_repository = db_repository

    async def execute(self, service_name: Optional[str] = None) -> List[Microservice]:
        """Execute the use-case to get microservices.

        Args:
            service_name (Optional[str]): Service name to filter the microservices by.

        Returns:
            List[Microservice]: A list of microservice entities.
        """
        # Call the repository method using the instance of DBRepository
        documents = await self.db_repository.find_all()
        return [Microservice.from_mongo_dict(doc) for doc in documents]  # Convert each document to a Microservice entity

# src/core/use_cases/get_microservices.py

from typing import List, Optional
from src.core.entities.microservice import Microservice
from src.core.repositories.db_repository import DBRepository

class GetMicroservices:
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
        # Build the query dictionary to filter by service_name if provided
        query = {}
        if service_name:
            query["service_name"] = service_name
        # Call the repository method using the instance of DBRepository
        documents = await self.db_repository.find(query=query)
        return [Microservice(**doc) for doc in documents]  # Convert each document to a Microservice entity

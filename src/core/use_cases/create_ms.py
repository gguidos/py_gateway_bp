from src.core.entities.microservice import Microservice
from src.core.repositories.db_repository import DBRepository
import logging

logger = logging.getLogger(__name__)

class CreateMicroservice:
    """Use-case for creating a new microservice."""

    def __init__(self, db_repository: DBRepository):
        self.db_repository = db_repository

    async def execute(self, microservice: Microservice) -> Microservice:
        """Create a new microservice and return the created entity.

        Args:
            microservice (Microservice): Microservice entity to create.

        Returns:
            Microservice: The created microservice entity.

        Raises:
            DuplicateMsException: If a microservice with the same service_name already exists.
        """

        # Convert the Pydantic model to a dictionary with simple data types
        microservice_dict = microservice.model_dump(exclude_unset=True, by_alias=True)
        
        # Convert the 'base_url' field to a string if it's a URL type
        microservice_dict["base_url"] = str(microservice.base_url)

        # Log the dictionary to see the result before saving it
        logger.info(f"Saving Microservice: {microservice_dict}")

        # Save the microservice in the database using the modified dictionary
        microservice_id = await self.db_repository.create(microservice_dict)
        microservice.id = microservice_id
        return microservice

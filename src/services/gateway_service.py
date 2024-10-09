from typing import Any, Dict, Optional
from src.core.repositories.db_repository import DBRepository

class GatewayService:
    """Service layer for the API Gateway microservice."""

    def __init__(self, user_repository: DBRepository, request_id: Optional[str] = None):
        self.user_repository = user_repository

    async def forward_request_to_service(self, service_name: str, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Forward a request to a registered microservice.
        
        Args:
            service_name (str): The name of the target microservice.
            path (str): The endpoint path of the target microservice.
            params (Optional[Dict[str, Any]]): Query parameters or data to send.

        Returns:
            Dict[str, Any]: The response data from the microservice.
        """
        # Retrieve microservice details from MongoDB
        microservice = await self.collection.find_one({"service_name": service_name})
        if not microservice:
            raise ValueError(f"Microservice '{service_name}' is not registered.")
        
        url = f"{microservice['base_url']}/{path}"
        headers = {"Authorization": f"Bearer {microservice['api_key']}"}

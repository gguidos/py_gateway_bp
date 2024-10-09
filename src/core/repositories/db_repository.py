from typing import Dict, Any, List
from datetime import datetime
from src.infrastructure.db.mongo_client import MongoDBClient
from bson import ObjectId

class DBRepository:
    """Repository to interact with the MongoDB database."""

    def __init__(self, client: MongoDBClient):
        self.client = client

    async def create(self, service_data: Dict[str, Any]) -> str:
        """Create a new user."""
        # Remove _id if it is None or not set
        if "_id" in service_data and service_data["_id"] is None:
            del service_data["_id"]
        service_data["created"] = service_data.get("created", datetime.utcnow())
        service_data["modified"] = service_data.get("modified", datetime.utcnow())
        user_id = await self.client.insert_one(service_data)
        return str(user_id)

    async def find_all(self) -> List[Dict[str, Any]]:
        """Retrieve all users."""
        return await self.client.find({})

    async def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Retrieve documents that match the specified query.

        Args:
            query (Dict[str, Any]): A dictionary representing the query to be executed.

        Returns:
            List[Dict[str, Any]]: A list of documents that match the query.
        """
        return await self.client.find(query)

    async def update(self, id: str, data: Dict[str, Any]) -> bool:
        """Update a document by ID."""
        query = {"_id": ObjectId(id)}
        updated_data = {"$set": data}
        updated_data["modified"] = datetime.utcnow()  
        result = await self.client.update_one(query, updated_data)
        return result.modified_count > 0

    async def delete(self, id: str) -> bool:
        """Delete a document by ID."""
        query = {"_id": ObjectId(id)}
        result = await self.client.delete_one(query)
        return result.deleted_count > 0

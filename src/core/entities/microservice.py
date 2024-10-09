from pydantic import BaseModel, Field, HttpUrl
from bson import ObjectId
from typing import List, Optional

class RateLimitConfig(BaseModel):
    """Schema for defining rate limit configurations."""
    requests_per_minute: Optional[int] = Field(None, description="Number of allowed requests per minute.")
    requests_per_hour: Optional[int] = Field(None, description="Number of allowed requests per hour.")
    requests_per_day: Optional[int] = Field(None, description="Number of allowed requests per day.")

class PathDetails(BaseModel):
    """Schema representing a single path with its associated method, protection status, and rate limit configuration."""
    path: str = Field(..., description="The endpoint path, must start with a forward slash ('/').")
    method: str = Field(..., description="HTTP method for the endpoint (e.g., GET, POST).")
    protected: bool = Field(default=False, description="Indicates whether the endpoint is protected (requires authentication).")
    rate_limit: Optional[RateLimitConfig] = Field(None, description="Optional rate limit configuration for this specific path.")

class ObjectIdStr(str):
    """Custom data type for handling ObjectId as a string."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, field=None):
        """Validate that the value is an ObjectId and return it as a string."""
        if not isinstance(value, ObjectId):
            raise TypeError(f"Expected ObjectId, but got {type(value)} instead.")
        return str(value)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        """Modify the JSON schema to represent ObjectIdStr as a string."""
        schema.update(type="string")
        return schema

class Microservice(BaseModel):
    """Entity representing a microservice with its registration details."""
    id: Optional[ObjectIdStr] = Field(None, alias="_id")
    service_name: str = Field(..., description="Unique identifier for the microservice.")
    base_url: HttpUrl = Field(..., description="Base URL of the microservice.")
    paths: List[PathDetails] = Field(..., description="List of paths exposed by the microservice.")
    api_key: Optional[str] = Field(None, description="API key for the microservice.")

    class Config:
        schema_extra = {
            "example": {
                "service_name": "user-service",
                "base_url": "http://localhost:8000",
                "paths": [
                    {
                        "path": "/users",
                        "method": "GET",
                        "protected": True,
                        "rate_limit": {
                            "requests_per_minute": 10,
                            "requests_per_hour": 100
                        }
                    }
                ],
                "api_key": "some-api-key"
            }
        }

    @classmethod
    def from_mongo_dict(cls, mongo_dict: dict) -> "Microservice":
        """Convert a MongoDB document to a Microservice entity."""
        if "_id" in mongo_dict:
            mongo_dict["id"] = str(mongo_dict["_id"])
        return cls(**mongo_dict)

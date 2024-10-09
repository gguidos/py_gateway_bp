from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Annotated
from pydantic.types import StringConstraints

class RateLimitConfig(BaseModel):
    """Schema for defining rate limit configurations."""
    requests_per_minute: Optional[int] = Field(None, description="Number of allowed requests per minute.")
    requests_per_hour: Optional[int] = Field(None, description="Number of allowed requests per hour.")
    requests_per_day: Optional[int] = Field(None, description="Number of allowed requests per day.")

class PathDetails(BaseModel):
    """Schema representing a single path with its associated method, protection status, and rate limit configuration."""
    path: Annotated[str, StringConstraints(pattern=r'^/.*')] = Field(..., description="The endpoint path, must start with a forward slash ('/').")
    method: Annotated[str, StringConstraints(pattern=r'^(GET|POST|PUT|DELETE|PATCH)$', to_upper=True)] = Field(..., description="HTTP method for the endpoint (e.g., GET, POST).")
    protected: bool = Field(default=False, description="Indicates whether the endpoint is protected (requires authentication).")
    rate_limit: Optional[RateLimitConfig] = Field(None, description="Optional rate limit configuration for this specific path.")

class MicroserviceSchema(BaseModel):
    """Schema for registering a new microservice."""
    service_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(..., description="Unique identifier for the microservice.")
    base_url: HttpUrl = Field(..., description="Base URL of the microservice.")
    paths: List[PathDetails] = Field(..., description="List of paths exposed by the microservice.")
    api_key: Optional[str] = Field(None, description="API key for the microservice.")

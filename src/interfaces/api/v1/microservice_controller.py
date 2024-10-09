from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import Any, Dict, List, Optional
from src.core.entities.microservice import Microservice
from src.core.schemas.microservice_schema import MicroserviceSchema
from src.services.ms_service import MicroserviceService
from src.dependencies.microservice_service_dependency import get_ms_service
from src.infrastructure.exception_handlers import DuplicateMsException

# Create a FastAPI router for microservice-related endpoints
router = APIRouter()

@router.post(
    "/microservice/",
    response_model=Microservice,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def register_microservice(
    request: MicroserviceSchema,  # Use the validated schema
    service: MicroserviceService = Depends(get_ms_service)
):
    """Register a new microservice."""
    try:
        # Pass the Pydantic model directly instead of converting it to a dictionary
        registered_microservice = await service.register_microservice(
            microservice_data=request.dict()  # Use .dict() to convert Pydantic model to dictionary
        )
        return registered_microservice
    except DuplicateMsException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/microservice/",
        response_model=List[Microservice],
        dependencies=[
            Depends(RateLimiter(times=2, seconds=4))])
async def get_all_users(
    service: MicroserviceService = Depends(get_ms_service)  # Use Provide to inject UserService from Container
):
    """Get all users."""
    print("-----Get all microservices")
    return await service.get_all_microservices()

from fastapi import APIRouter, Depends, HTTPException

# Create a FastAPI router for microservice-related endpoints
router = APIRouter()

@router.get('/')
async def get_description():
    """Get a list of available endpoints"""
    return 'List of available endpoints for microservice registration'

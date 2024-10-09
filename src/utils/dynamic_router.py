from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.routing import APIRoute
from httpx import AsyncClient
from typing import Callable, List
from src.core.entities.microservice import Microservice

import logging

logger = logging.getLogger(__name__)

async def proxy_request_handler(request: Request, service_name: str, base_url: str):
    """Generic proxy request handler to forward requests to microservices."""
    # Convert base_url to string before applying string methods
    base_url_str = str(base_url)  # Convert Pydantic HttpUrl to string
    target_url = f"{base_url_str.rstrip('/')}/{request.url.path.lstrip('/')}"

    async with AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),  # Forward headers
            params=dict(request.query_params),  # Forward query parameters
            content=await request.body(),  # Forward the request body
        )

    # Return the forwarded response as a FastAPI response
    return Response(content=response.content, status_code=response.status_code)

def create_dynamic_route(service_name: str, path: str, method: str, base_url: str) -> APIRoute:
    """Create a dynamic APIRoute object for the specified path and method."""
    # Convert base_url to string before using it
    base_url_str = str(base_url)
    if not path.endswith("/"):
        path += "/"
    async def dynamic_endpoint(request: Request):
        return await proxy_request_handler(request, service_name, base_url_str)
    print(method)

    return APIRoute(
        path=path,
        endpoint=dynamic_endpoint,
        methods=[method],
        name=f"{service_name}-{method}-{path}",
    )

async def register_microservice_routes(app: FastAPI, microservices: List[Microservice]):
    """Dynamically register routes for each microservice based on configuration."""
    for microservice in microservices:
        # Use dot notation to access the attributes of the Microservice object
        service_name = microservice.service_name
        base_url = str(microservice.base_url)  # Convert to string
        base_url += 'api/v1'
        logger.info(f"Registering service '{service_name}' with base URL: {base_url}")

        for path_details in microservice.paths:
            path = path_details.path
            method = path_details.method

            # Create and register a new APIRoute dynamically
            route = create_dynamic_route(service_name, path, method, base_url)
            app.router.routes.append(route)
            logger.info(f"Registered route: {method} {path} -> {base_url}")

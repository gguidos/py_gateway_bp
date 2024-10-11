# src/middleware_setup.py
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.response_interceptor import ResponseFormatMiddleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.middleware.request_id_middleware import RequestIDMiddleware

def add_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ResponseFormatMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

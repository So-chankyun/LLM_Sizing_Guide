import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.api.routers import calculator, specs

# Set up logging early
setup_logging()
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add exception handlers
    setup_exception_handlers(app)

    # Include routers
    app.include_router(calculator.router, prefix=settings.API_V1_STR)
    app.include_router(specs.router, prefix=settings.API_V1_STR)
    
    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "ok"}

    return app

app = create_app()

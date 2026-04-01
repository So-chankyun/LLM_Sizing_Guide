from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class CalculatorDomainError(Exception):
    """Base exception for calculator domain errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class OOMError(CalculatorDomainError):
    """Exception raised when an OOM condition is detected."""
    def __init__(self, message: str = "Out of Memory (OOM)"):
        super().__init__(message)

def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CalculatorDomainError)
    async def calculator_exception_handler(request: Request, exc: CalculatorDomainError):
        return JSONResponse(
            status_code=400,
            content={"detail": {"message": exc.message, "type": "calculator_error"}},
        )

    @app.exception_handler(OOMError)
    async def oom_exception_handler(request: Request, exc: OOMError):
        return JSONResponse(
            status_code=422,
            content={"detail": {"message": exc.message, "type": "oom_error"}},
        )

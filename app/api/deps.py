from typing import Generator
from app.domains.calculator.service import CalculatorService

def get_calculator_service(num_gpu: int = 1) -> Generator[CalculatorService, None, None]:
    # Could be modified if we need dependency injection properly per request basis
    service = CalculatorService(num_gpu=num_gpu)
    yield service

import logging
import sys

def setup_logging() -> None:
    """Setup basic structured logging."""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

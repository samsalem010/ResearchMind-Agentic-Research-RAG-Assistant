import logging
import sys

from agentic_research_rag.config import settings


def setup_logger(name: str = "agentic_research_rag") -> logging.Logger:
    """
    Configures and returns a standard logger for the application.
    Uses the log level defined in environment settings.
    """
    logger = logging.getLogger(name)

    # Only configure if no handlers are attached to prevent duplicate logs
    if not logger.handlers:
        logger.setLevel(settings.log_level.upper())

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(settings.log_level.upper())

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False

    return logger


# Create a default logger instance
logger = setup_logger()

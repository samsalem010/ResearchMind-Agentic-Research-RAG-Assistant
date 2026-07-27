import os

from agentic_research_rag.config import Settings
from agentic_research_rag.logger import logger


def test_settings_load_defaults():
    """Test that settings load default values correctly."""
    # Temporarily override any .env file variables
    os.environ.pop("ENVIRONMENT", None)
    settings = Settings()
    assert settings.environment == "development"
    assert settings.log_level == "INFO"


def test_logger_initialization():
    """Test that the logger is initialized correctly."""
    assert logger.name == "agentic_research_rag"
    assert len(logger.handlers) >= 1

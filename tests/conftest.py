"""
Pytest configuration and fixtures
Ensures test isolation by clearing singleton caches
"""

import pytest
from agent_router.config import AgentConfig


@pytest.fixture(autouse=True)
def clear_singleton_cache():
    """
    Automatically clear singleton cache before each test
    This ensures tests see fresh configuration with updated keywords
    """
    AgentConfig.clear_cache()
    yield
    # Optionally clear after test as well
    AgentConfig.clear_cache()

"""
Agent Router Package
Intelligent task routing system for specialized agents
"""

from .router import AgentRouter
from .config import AgentConfig
from .personality import AgentPersonality
from .coordination import CoordinationPlanner
from .protocols import ProtocolEnforcer
from .errors import (
    AgentConfigError,
    PersonalityLoadError,
    RoutingError,
    ValidationError
)

__all__ = [
    'AgentRouter',
    'AgentConfig',
    'AgentPersonality',
    'CoordinationPlanner',
    'ProtocolEnforcer',
    'AgentConfigError',
    'PersonalityLoadError',
    'RoutingError',
    'ValidationError'
]

__version__ = '0.1.0'

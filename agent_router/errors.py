"""
Custom errors for agent router system
"""


class AgentConfigError(Exception):
    """Raised when agent configuration is invalid"""
    pass


class PersonalityLoadError(Exception):
    """Raised when personality loading fails"""
    pass


class RoutingError(Exception):
    """Raised when routing fails"""
    pass


class ValidationError(Exception):
    """Raised when validation fails"""
    pass

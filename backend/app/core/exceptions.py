class InsightFlowError(Exception):
    """Base exception for domain-specific failures."""


class ValidationError(InsightFlowError):
    """Raised when request input is invalid."""


class AuthenticationError(InsightFlowError):
    """Raised when authentication fails."""


class AuthorizationError(InsightFlowError):
    """Raised when a user lacks permissions."""


class NotFoundError(InsightFlowError):
    """Raised when a targeted resource cannot be found."""

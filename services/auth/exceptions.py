"""Custom exceptions for the Polymarket authentication module."""

class PolyAuthError(Exception):
    """Base exception for Polymarket authentication errors."""
    pass

class PolyAuthConfigError(PolyAuthError):
    """Raised when there's an error in the authentication configuration."""
    pass

class PolyAuthKeyGenerationError(PolyAuthError):
    """Raised when API key generation fails."""
    pass

class PolyAuthConnectionError(PolyAuthError):
    """Raised when connection to Polymarket API fails."""
    pass 
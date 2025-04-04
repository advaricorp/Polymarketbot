"""
Polymarket Authentication Module

This module handles all authentication-related functionality for interacting with
Polymarket's API, including API key generation and management.
"""

from .poly_auth import PolyAuth, PolyAuthConfig
from .exceptions import PolyAuthError

__all__ = ['PolyAuth', 'PolyAuthConfig', 'PolyAuthError'] 
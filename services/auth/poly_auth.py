"""
Polymarket Authentication Manager

This module provides a class for managing Polymarket API authentication,
including generating and managing API keys.
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Tuple
from py_clob_client.client import ClobClient
from .exceptions import (
    PolyAuthError,
    PolyAuthConfigError,
    PolyAuthKeyGenerationError,
    PolyAuthConnectionError
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PolyAuthConfig:
    """Configuration for Polymarket authentication."""
    private_key: str
    chain_id: int = 137  # Polygon mainnet
    host: str = "https://clob.polymarket.com"
    signature_type: int = 0  # 0 for EOA, 1 for Magic Link, 2 for Gnosis Safe
    proxy_address: Optional[str] = None  # Required for signature_type 1 or 2

    def validate(self) -> None:
        """Validate the configuration."""
        # Clean and validate private key
        self.private_key = self.private_key.strip().lower()
        if not self.private_key:
            raise PolyAuthConfigError("Private key cannot be empty")
        
        # Add 0x prefix if missing
        if not self.private_key.startswith("0x"):
            self.private_key = "0x" + self.private_key
            
        # Check length (32 bytes = 64 chars + 2 for '0x')
        if len(self.private_key) != 66:
            raise PolyAuthConfigError("Invalid private key length")
            
        # Validate hex format
        try:
            int(self.private_key[2:], 16)
        except ValueError:
            raise PolyAuthConfigError("Invalid private key format - must be hexadecimal")
        
        if self.signature_type not in [0, 1, 2]:
            raise PolyAuthConfigError("Invalid signature_type. Must be 0, 1, or 2")
        
        if self.signature_type in [1, 2] and not self.proxy_address:
            raise PolyAuthConfigError("proxy_address is required for Magic Link or Gnosis Safe")
        
        if self.proxy_address:
            if not self.proxy_address.startswith("0x"):
                self.proxy_address = "0x" + self.proxy_address.strip().lower()
            try:
                int(self.proxy_address[2:], 16)
            except ValueError:
                raise PolyAuthConfigError("Invalid proxy address format - must be hexadecimal")

class PolyAuth:
    """Manager for Polymarket authentication and API keys."""
    
    def __init__(self, config: PolyAuthConfig):
        """Initialize the auth manager with configuration."""
        self.config = config
        self.config.validate()
        self._client: Optional[ClobClient] = None
        
    @property
    def client(self) -> ClobClient:
        """Get or create the CLOB client."""
        if not self._client:
            try:
                kwargs = {
                    "host": self.config.host,
                    "key": self.config.private_key,
                    "chain_id": self.config.chain_id,
                }
                
                if self.config.signature_type > 0:
                    kwargs.update({
                        "signature_type": self.config.signature_type,
                        "funder": self.config.proxy_address
                    })
                
                logger.info(f"Initializing CLOB client with address: {kwargs.get('key')}")
                self._client = ClobClient(**kwargs)
                logger.info(f"CLOB client initialized successfully")
            except Exception as e:
                raise PolyAuthConnectionError(f"Failed to create CLOB client: {str(e)}")
        
        return self._client

    def generate_api_key(self, nonce: int = 0) -> Dict[str, str]:
        """Generate new API credentials or derive existing ones."""
        try:
            logger.info(f"Getting address from client...")
            address = self.client.get_address()
            logger.info(f"Using address: {address}")
            
            logger.info(f"Attempting to generate API credentials...")
            creds = self.client.create_or_derive_api_creds()
            logger.info("API credentials received")
            
            # Extract credentials from the response
            api_key = getattr(creds, 'api_key', None) or creds.get('api_key')
            secret = getattr(creds, 'api_secret', None) or creds.get('api_secret')
            passphrase = getattr(creds, 'api_passphrase', None) or creds.get('api_passphrase')
            
            if not all([api_key, secret, passphrase]):
                raise PolyAuthKeyGenerationError("Incomplete credentials received from API")
            
            logger.info("Successfully generated API credentials")
            return {
                "POLY_API_KEY": api_key,
                "POLY_API_SECRET": secret,
                "POLY_PASSPHRASE": passphrase
            }
        except Exception as e:
            logger.error(f"Failed to generate API key: {str(e)}")
            raise PolyAuthKeyGenerationError(f"Failed to generate API key: {str(e)}")

    def save_credentials_to_env(self, env_file: str = ".env") -> None:
        """Generate API credentials and save them to an env file."""
        try:
            logger.info("Generating API credentials...")
            creds = self.generate_api_key()
            
            logger.info(f"Saving credentials to {env_file}")
            
            # Read existing env file
            env_contents = {}
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            try:
                                key, value = line.split('=', 1)
                                env_contents[key.strip()] = value.strip()
                            except ValueError:
                                continue  # Skip malformed lines
            
            # Update with new credentials
            env_contents.update(creds)
            
            # Write back to file, preserving comments and formatting
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    lines = f.readlines()
            else:
                lines = []
            
            # Update or add new values while preserving comments and order
            new_lines = []
            creds_added = set()
            
            for line in lines:
                line = line.rstrip('\n')
                if line.startswith('#') or not line.strip():
                    new_lines.append(line)
                    continue
                    
                try:
                    key = line.split('=', 1)[0].strip()
                    if key in creds:
                        new_lines.append(f"{key}={creds[key]}")
                        creds_added.add(key)
                    else:
                        new_lines.append(line)
                except ValueError:
                    new_lines.append(line)
            
            # Add any new credentials that weren't in the file
            for key, value in creds.items():
                if key not in creds_added:
                    new_lines.append(f"{key}={value}")
            
            # Write back to file
            with open(env_file, 'w') as f:
                f.write('\n'.join(new_lines) + '\n')
            
            logger.info("Successfully saved credentials to .env file")
                    
        except Exception as e:
            logger.error(f"Failed to save credentials: {str(e)}")
            raise PolyAuthError(f"Failed to save credentials: {str(e)}")

    def get_address(self) -> str:
        """Get the address associated with this authentication."""
        try:
            return self.client.get_address()
        except Exception as e:
            raise PolyAuthError(f"Failed to get address: {str(e)}")

    def verify_credentials(self) -> bool:
        """Verify that the current credentials are valid."""
        try:
            # Try to get API keys - this will fail if auth is invalid
            self.client.get_api_keys()
            return True
        except Exception:
            return False 
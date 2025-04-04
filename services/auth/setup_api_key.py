#!/usr/bin/env python3
"""
CLI script for generating Polymarket API keys.

Usage:
    python setup_api_key.py --private-key 0x... [--proxy 0x...] [--type {0,1,2}] [--env-file .env]
"""

import argparse
import os
import sys
from typing import Optional

from .poly_auth import PolyAuth, PolyAuthConfig
from .exceptions import PolyAuthError

def setup_argparse() -> argparse.ArgumentParser:
    """Set up command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate Polymarket API keys and save to .env file"
    )
    
    parser.add_argument(
        "--private-key",
        required=True,
        help="Private key (with 0x prefix) for signing API key generation"
    )
    
    parser.add_argument(
        "--type",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Signature type: 0=EOA, 1=Magic Link, 2=Gnosis Safe"
    )
    
    parser.add_argument(
        "--proxy",
        help="Proxy wallet address (required for Magic Link or Gnosis Safe)"
    )
    
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file to update (default: .env)"
    )
    
    parser.add_argument(
        "--nonce",
        type=int,
        default=0,
        help="Nonce for deriving existing keys (default: 0 for new keys)"
    )
    
    return parser

def main(args: Optional[list] = None) -> int:
    """Main entry point for the script."""
    parser = setup_argparse()
    args = parser.parse_args(args)
    
    try:
        # Create config
        config = PolyAuthConfig(
            private_key=args.private_key,
            signature_type=args.type,
            proxy_address=args.proxy
        )
        
        # Initialize auth manager
        auth = PolyAuth(config)
        
        # Generate and save credentials
        auth.save_credentials_to_env(env_file=args.env_file)
        
        # Get the address for confirmation
        address = auth.get_address()
        
        print(f"\n✅ Successfully generated API keys for address: {address}")
        print(f"📝 Credentials have been saved to: {args.env_file}")
        
        # Verify the credentials work
        if auth.verify_credentials():
            print("✅ Credentials verified successfully!")
        else:
            print("⚠️ Warning: Could not verify credentials. They might still be valid.")
        
        return 0
        
    except PolyAuthError as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
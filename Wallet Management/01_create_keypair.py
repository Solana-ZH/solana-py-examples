#!/usr/bin/env python3
"""
Solana Cookbook - How to Create a Keypair
"""

from solders.keypair import Keypair

def main():
    # Generate a new keypair
    keypair = Keypair()
    
    print(f"address: {keypair.pubkey()}")
    print(f"secret: {keypair.secret()}")

if __name__ == "__main__":
    main()
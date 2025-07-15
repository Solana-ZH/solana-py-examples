#!/usr/bin/env python3
"""
Solana Cookbook - Getting Test SOL
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair

async def main():
    keypair = Keypair()
    
    async with AsyncClient("https://api.devnet.solana.com") as client:
        # Request airdrop (1 SOL = 1_000_000_000 lamports)
        res = await client.request_airdrop(keypair.pubkey(), 1_000_000_000)
        print(f"Airdrop signature: {res.value}")
        
        # Check balance
        balance = await client.get_balance(keypair.pubkey())
        print(f"Balance: {balance.value} lamports")

if __name__ == "__main__":
    asyncio.run(main())
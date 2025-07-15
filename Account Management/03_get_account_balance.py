#!/usr/bin/env python3
"""
Solana Cookbook - How to Get Account Balance
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example public key (you can replace with any valid public key)
    account_pubkey = Pubkey.from_string("11111111111111111111111111111111")
    
    async with rpc:
        # Get account balance
        balance = await rpc.get_balance(account_pubkey)
        
        print(f"Account: {account_pubkey}")
        print(f"Balance: {balance.value} lamports")
        print(f"Balance: {balance.value / 1_000_000_000} SOL")

if __name__ == "__main__":
    asyncio.run(main())
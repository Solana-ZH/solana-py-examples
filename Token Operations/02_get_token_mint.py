#!/usr/bin/env python3
"""
Solana Cookbook - How to Get a Token Mint
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    async with rpc:
        mint = await rpc.get_account_info(address)
        print(mint)

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Solana Cookbook - Connecting to a Solana Environment
"""

import asyncio
from solana.rpc.async_api import AsyncClient

async def main():
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
    print(res)  # True

asyncio.run(main())
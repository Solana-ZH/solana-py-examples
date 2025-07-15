#!/usr/bin/env python3
"""
Solana Cookbook - Subscribing to Events
"""

import asyncio
from solana.rpc.websocket_api import connect
from solders.keypair import Keypair

async def main():
    keypair = Keypair()
    
    async with connect("wss://api.devnet.solana.com") as websocket:
        # Subscribe to account changes
        await websocket.account_subscribe(keypair.pubkey())
        
        # Subscribe to logs
        await websocket.logs_subscribe()
        
        # Listen for messages
        async for message in websocket:
            print(f"Received: {message}")

if __name__ == "__main__":
    asyncio.run(main())
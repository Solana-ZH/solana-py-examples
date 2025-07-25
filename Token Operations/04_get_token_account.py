#!/usr/bin/env python3
"""
Solana Cookbook - How to Get a Token Account
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example mint and authority addresses
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    authority = Pubkey.from_string("AC5RDfQFmDS1deWZos921JfqscXdByf8BKHs5ACWjtW2")
    
    # Find associated token address
    associated_token_address = get_associated_token_address(
        owner=authority,
        mint=mint_address,
        token_program_id=TOKEN_PROGRAM_ID
    )
    
    async with rpc:
        try:
            # Get token account info
            account_info = await rpc.get_account_info(associated_token_address)
            
            print(f"Associated Token Address: {associated_token_address}")
            if account_info.value:
                print(f"Owner: {account_info.value.owner}")
                print(f"Lamports: {account_info.value.lamports}")
                print(f"Data Length: {len(account_info.value.data)} bytes")
                print(f"Executable: {account_info.value.executable}")
            else:
                print("Token account not found")
            
        except Exception as e:
            print(f"Error getting token account info: {e}")

if __name__ == "__main__":
    asyncio.run(main())
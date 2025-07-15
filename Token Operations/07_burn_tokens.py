#!/usr/bin/env python3
"""
Solana Cookbook - How to Burn Tokens
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import burn, BurnParams
from spl.token.constants import TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example keypairs and addresses
    payer = Keypair()
    owner = Keypair()
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    token_account = Pubkey.from_string("GfVPzUxMDvhFJ1Xs6C9i47XQRSapTd8LHw5grGuTquyQ")
    
    # Amount to burn (in smallest unit)
    amount_to_burn = 500000000  # 0.5 tokens with 9 decimals
    
    async with rpc:
        # Create burn instruction
        burn_instruction = burn(
            BurnParams(
                program_id=TOKEN_PROGRAM_ID,
                account=token_account,
                mint=mint_address,
                owner=owner.pubkey(),
                amount=amount_to_burn
            )
        )
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[burn_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, owner])
        
        print(f"Mint: {mint_address}")
        print(f"Token Account: {token_account}")
        print(f"Amount to burn: {amount_to_burn}")
        print(f"Owner: {owner.pubkey()}")
        print(f"Payer: {payer.pubkey()}")
        print(f"Burn transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
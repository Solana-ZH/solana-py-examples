#!/usr/bin/env python3
"""
Solana Cookbook - How to Close Token Accounts
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import close_account, CloseAccountParams
from spl.token.constants import TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example keypairs and addresses
    payer = Keypair()
    owner = Keypair()
    token_account = Pubkey.from_string("GfVPzUxMDvhFJ1Xs6C9i47XQRSapTd8LHw5grGuTquyQ")
    
    # Account to receive the remaining lamports (usually the owner)
    destination = owner.pubkey()
    
    async with rpc:
        # Create close account instruction
        close_instruction = close_account(
            CloseAccountParams(
                program_id=TOKEN_PROGRAM_ID,
                account=token_account,
                dest=destination,
                owner=owner.pubkey()
            )
        )
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[close_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, owner])
        
        print(f"Token Account: {token_account}")
        print(f"Owner: {owner.pubkey()}")
        print(f"Destination: {destination}")
        print(f"Close token account transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
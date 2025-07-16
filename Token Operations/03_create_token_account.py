#!/usr/bin/env python3
"""
Solana Cookbook - How to Create a Token Account
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    payer = Keypair()
    owner = Keypair()
    
    # Example mint address (USDC on devnet)
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    # Get associated token account address
    associated_token_account = get_associated_token_address(owner.pubkey(), mint_address)
    
    async with rpc:
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create associated token account instruction
        create_token_account_instruction = create_associated_token_account(
            payer=payer.pubkey(),
            owner=owner.pubkey(),
            mint=mint_address,
            token_program_id=TOKEN_PROGRAM_ID
        )
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[create_token_account_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer])
        
        print(f"Payer: {payer.pubkey()}")
        print(f"Owner: {owner.pubkey()}")
        print(f"Associated Token Account: {associated_token_account}")
        print(f"Mint: {mint_address}")
        print(f"Associated token account created successfully")

if __name__ == "__main__":
    asyncio.run(main())
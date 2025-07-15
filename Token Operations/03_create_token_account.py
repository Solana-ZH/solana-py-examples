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
from spl.token.instructions import initialize_account, InitializeAccountParams
from spl.token.constants import TOKEN_PROGRAM_ID, ACCOUNT_LEN
from solders.system_program import create_account as create_system_account, CreateAccountParams as CreateSystemAccountParams

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    payer = Keypair()
    owner = Keypair()
    token_account = Keypair()
    
    # Example mint address (USDC on devnet)
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    async with rpc:
        # Get minimum balance for rent exemption
        rent_lamports = await rpc.get_minimum_balance_for_rent_exemption(ACCOUNT_LEN)
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create system account instruction
        create_system_account_instruction = create_system_account(
            CreateSystemAccountParams(
                from_pubkey=payer.pubkey(),
                to_pubkey=token_account.pubkey(),
                lamports=rent_lamports.value,
                space=ACCOUNT_LEN,
                owner=TOKEN_PROGRAM_ID
            )
        )
        
        # Initialize token account instruction
        initialize_account_instruction = initialize_account(
            InitializeAccountParams(
                program_id=TOKEN_PROGRAM_ID,
                account=token_account.pubkey(),
                mint=mint_address,
                owner=owner.pubkey()
            )
        )
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[create_system_account_instruction, initialize_account_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, token_account])
        
        print(f"Payer: {payer.pubkey()}")
        print(f"Owner: {owner.pubkey()}")
        print(f"Token Account: {token_account.pubkey()}")
        print(f"Mint: {mint_address}")
        print(f"Token account created successfully")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Solana Cookbook - How to Create an Account
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.system_program import create_account, CreateAccountParams
from solders.transaction import VersionedTransaction
from solders.message import MessageV0

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    sender = Keypair()
    new_account = Keypair()
    space = 0  # Account data space
    
    async with rpc:
        # Get minimum balance for rent exemption
        rent_lamports = await rpc.get_minimum_balance_for_rent_exemption(space)
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create account instruction
        create_account_instruction = create_account(
            CreateAccountParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=new_account.pubkey(),
                lamports=rent_lamports.value,
                space=space,
                owner=sender.pubkey()  # System program owns the account
            )
        )
        
        # Create message
        message = MessageV0.try_compile(
            payer=sender.pubkey(),
            instructions=[create_account_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [sender, new_account])
        
        print(f"Payer: {sender.pubkey()}")
        print(f"New Account: {new_account.pubkey()}")
        print(f"Rent Lamports: {rent_lamports.value}")
        print(f"Space: {space} bytes")
        print(f"Account creation transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Solana Cookbook - How to Create a PDA's Account
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import create_account, CreateAccountParams
from solders.transaction import VersionedTransaction
from solders.message import MessageV0

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    payer = Keypair()
    program_id = Pubkey.from_string("11111111111111111111111111111111")
    
    # Create PDA (Program Derived Address)
    seed = "hello"
    pda, bump = Pubkey.find_program_address([seed.encode()], program_id)
    
    space = 100  # Account data space
    
    async with rpc:
        # Get minimum balance for rent exemption
        rent_lamports = await rpc.get_minimum_balance_for_rent_exemption(space)
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # For PDA accounts, we need to use create_account_with_seed since PDA cannot sign
        from solders.system_program import create_account_with_seed, CreateAccountWithSeedParams
        
        # Use the payer as base for seed derivation
        create_account_instruction = create_account_with_seed(
            CreateAccountWithSeedParams(
                from_pubkey=payer.pubkey(),
                to_pubkey=pda,
                base=payer.pubkey(),
                seed=seed,
                lamports=rent_lamports.value,
                space=space,
                owner=program_id
            )
        )
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[create_account_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer])
        
        print(f"Payer: {payer.pubkey()}")
        print(f"PDA: {pda}")
        print(f"Bump: {bump}")
        print(f"Program ID: {program_id}")
        print(f"Seed: {seed}")
        print(f"Rent Lamports: {rent_lamports.value}")
        print(f"PDA account creation transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
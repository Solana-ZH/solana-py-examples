#!/usr/bin/env python3
"""
Solana Cookbook - How to Delegate Token Accounts
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.system_program import create_account, CreateAccountParams
from spl.token.instructions import (
    initialize_mint, InitializeMintParams,
    create_associated_token_account, 
    mint_to_checked, MintToCheckedParams,
    approve_checked, ApproveCheckedParams,
    get_associated_token_address
)
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID

# Constants
DECIMALS = 9

async def setup(rpc, mint_authority):
    """
    The setup function initializes the mint and associated token accounts,
    and mints tokens to said associated token account
    """
    mint = Keypair()
    
    space = 82  # getMintSize() equivalent for SPL Token
    
    # Get minimum balance for rent exemption
    rent = await rpc.get_minimum_balance_for_rent_exemption(space)
    
    # Create & initialize mint account
    create_account_instruction = create_account(
        CreateAccountParams(
            from_pubkey=mint_authority.pubkey(),
            to_pubkey=mint.pubkey(),
            lamports=rent.value,
            space=space,
            owner=TOKEN_PROGRAM_ID
        )
    )
    
    initialize_mint_instruction = initialize_mint(
        InitializeMintParams(
            program_id=TOKEN_PROGRAM_ID,
            mint=mint.pubkey(),
            decimals=DECIMALS,
            mint_authority=mint_authority.pubkey(),
            freeze_authority=None
        )
    )
    
    # Create associated token account
    authority_ata = get_associated_token_address(
        owner=mint_authority.pubkey(),
        mint=mint.pubkey(),
        token_program_id=TOKEN_PROGRAM_ID
    )
    
    create_authority_ata_instruction = create_associated_token_account(
        payer=mint_authority.pubkey(),
        owner=mint_authority.pubkey(),
        mint=mint.pubkey()
    )
    
    # Mint to token account
    mint_to_instruction = mint_to_checked(
        MintToCheckedParams(
            program_id=TOKEN_PROGRAM_ID,
            mint=mint.pubkey(),
            dest=authority_ata,
            mint_authority=mint_authority.pubkey(),
            amount=1_000_000_000_000,  # 1000 tokens
            decimals=DECIMALS
        )
    )
    
    instructions = [
        create_account_instruction,
        initialize_mint_instruction,
        create_authority_ata_instruction,
        mint_to_instruction
    ]
    
    # Get latest blockhash
    latest_blockhash = await rpc.get_latest_blockhash()
    
    # Create message
    transaction_message = MessageV0.try_compile(
        payer=mint_authority.pubkey(),
        instructions=instructions,
        address_lookup_table_accounts=[],
        recent_blockhash=latest_blockhash.value.blockhash
    )
    
    # Create and sign transaction
    signed_transaction = VersionedTransaction(transaction_message, [mint_authority, mint])
    
    print("Setup transaction created successfully")
    print(f"Mint: {mint.pubkey()}")
    print(f"Authority ATA: {authority_ata}")
    
    return {
        "mint": mint.pubkey(),
        "authority_ata": authority_ata
    }

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Constants
    mint_authority = Keypair()
    delegate = Keypair()
    
    async with rpc:
        # Get latest blockhash
        latest_blockhash = await rpc.get_latest_blockhash()
        
        # Setup mint and associated token accounts
        setup_result = await setup(rpc, mint_authority)
        mint = setup_result["mint"]
        authority_ata = setup_result["authority_ata"]
        
        # Create delegate instruction
        delegate_instruction = approve_checked(
            ApproveCheckedParams(
                program_id=TOKEN_PROGRAM_ID,
                source=authority_ata,
                mint=mint,
                delegate=delegate.pubkey(),
                owner=mint_authority.pubkey(),
                amount=1_000_000_000,  # 1 token
                decimals=DECIMALS
            )
        )
        
        # Create transaction message
        transaction_message = MessageV0.try_compile(
            payer=mint_authority.pubkey(),
            instructions=[delegate_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash.value.blockhash
        )
        
        # Create and sign transaction
        signed_transaction = VersionedTransaction(transaction_message, [mint_authority])
        
        print(f"\nDelegate Transaction:")
        print(f"Source: {authority_ata}")
        print(f"Mint: {mint}")
        print(f"Delegate: {delegate.pubkey()}")
        print(f"Owner: {mint_authority.pubkey()}")
        print(f"Amount: 1_000_000_000 (1 token)")
        print(f"Decimals: {DECIMALS}")
        print(f"Delegation transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
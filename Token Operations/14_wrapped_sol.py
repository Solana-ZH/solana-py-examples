#!/usr/bin/env python3
"""
Solana Cookbook - How to Use Wrapped SOL
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.system_program import transfer, TransferParams
from spl.token.instructions import (
    create_associated_token_account,
    sync_native, SyncNativeParams,
    close_account, CloseAccountParams,
    get_associated_token_address
)
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.pubkey import Pubkey

# Native mint address for wrapped SOL
NATIVE_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example keypairs
    payer = Keypair()
    owner = Keypair()
    
    # Amount to wrap (in lamports)
    amount_to_wrap = 1000000000  # 1 SOL
    
    async with rpc:
        # Get associated token address for wrapped SOL
        wrapped_sol_account = get_associated_token_address(
            owner=owner.pubkey(),
            mint=NATIVE_MINT,
            token_program_id=TOKEN_PROGRAM_ID
        )
        
        # Create associated token account for wrapped SOL
        create_ata_instruction = create_associated_token_account(
            payer=payer.pubkey(),
            owner=owner.pubkey(),
            mint=NATIVE_MINT
        )
        
        # Transfer SOL to the wrapped SOL account
        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=payer.pubkey(),
                to_pubkey=wrapped_sol_account,
                lamports=amount_to_wrap
            )
        )
        
        # Sync native instruction to update the wrapped SOL balance
        sync_native_instruction = sync_native(
            SyncNativeParams(
                program_id=TOKEN_PROGRAM_ID,
                account=wrapped_sol_account
            )
        )
        
        instructions = [
            create_ata_instruction,
            transfer_instruction,
            sync_native_instruction
        ]
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=instructions,
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer])
        
        print(f"Wrapped SOL Operations:")
        print(f"Owner: {owner.pubkey()}")
        print(f"Wrapped SOL Account: {wrapped_sol_account}")
        print(f"Amount to wrap: {amount_to_wrap} lamports ({amount_to_wrap / 1e9} SOL)")
        print(f"Native Mint: {NATIVE_MINT}")
        print(f"Payer: {payer.pubkey()}")
        print(f"Wrapped SOL transaction created successfully")

async def unwrap_sol_example():
    """Example of unwrapping SOL (closing wrapped SOL account)"""
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    payer = Keypair()
    owner = Keypair()
    
    async with rpc:
        # Get wrapped SOL account
        wrapped_sol_account = get_associated_token_address(
            owner=owner.pubkey(),
            mint=NATIVE_MINT,
            token_program_id=TOKEN_PROGRAM_ID
        )
        
        # Close account instruction (unwraps SOL)
        close_account_instruction = close_account(
            CloseAccountParams(
                program_id=TOKEN_PROGRAM_ID,
                account=wrapped_sol_account,
                dest=owner.pubkey(),  # SOL will be sent back to owner
                owner=owner.pubkey()
            )
        )
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[close_account_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, owner])
        
        print(f"\nUnwrap SOL Example:")
        print(f"Wrapped SOL Account: {wrapped_sol_account}")
        print(f"Owner: {owner.pubkey()}")
        print(f"Destination: {owner.pubkey()}")
        print(f"Unwrap SOL transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(unwrap_sol_example())
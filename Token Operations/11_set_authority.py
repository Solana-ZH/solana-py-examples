#!/usr/bin/env python3
"""
Solana Cookbook - How to Set Authority on Token Accounts or Mints
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import set_authority, SetAuthorityParams
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import AuthorityType

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example keypairs and addresses
    payer = Keypair()
    current_authority = Keypair()
    new_authority = Keypair()
    mint_or_account = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    async with rpc:
        # Set new mint authority
        set_mint_authority_instruction = set_authority(
            SetAuthorityParams(
                program_id=TOKEN_PROGRAM_ID,
                account=mint_or_account,
                authority=AuthorityType.MINT_TOKENS,
                current_authority=current_authority.pubkey(),
                new_authority=new_authority.pubkey()
            )
        )
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[set_mint_authority_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, current_authority])
        
        print(f"Account/Mint: {mint_or_account}")
        print(f"Current Authority: {current_authority.pubkey()}")
        print(f"New Authority: {new_authority.pubkey()}")
        print(f"Authority Type: MintTokens")
        print(f"Payer: {payer.pubkey()}")
        print(f"Set authority transaction created successfully")

async def set_freeze_authority_example():
    """Example of setting freeze authority"""
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    payer = Keypair()
    current_authority = Keypair()
    new_authority = Keypair()
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    async with rpc:
        # Set freeze authority
        set_freeze_authority_instruction = set_authority(
            SetAuthorityParams(
                program_id=TOKEN_PROGRAM_ID,
                account=mint_address,
                authority=AuthorityType.FREEZE_ACCOUNT,
                current_authority=current_authority.pubkey(),
                new_authority=new_authority.pubkey()
            )
        )
        
        recent_blockhash = await rpc.get_latest_blockhash()
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[set_freeze_authority_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        transaction = VersionedTransaction(message, [payer, current_authority])
        
        print(f"\nFreeze Authority Example:")
        print(f"Mint: {mint_address}")
        print(f"Current Freeze Authority: {current_authority.pubkey()}")
        print(f"New Freeze Authority: {new_authority.pubkey()}")
        print(f"Set freeze authority transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(set_freeze_authority_example())
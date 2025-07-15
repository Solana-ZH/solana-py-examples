#!/usr/bin/env python3
"""
Solana Cookbook - How to Mint Tokens
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import mint_to, MintToParams
from spl.token.constants import TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example keypairs and addresses
    payer = Keypair()
    mint_authority = Keypair()
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    destination_token_account = Pubkey.from_string("GfVPzUxMDvhFJ1Xs6C9i47XQRSapTd8LHw5grGuTquyQ")
    
    # Amount to mint (in smallest unit)
    amount_to_mint = 1000000000  # 1 token with 9 decimals
    
    async with rpc:
        # Create mint instruction
        mint_instruction = mint_to(
            MintToParams(
                program_id=TOKEN_PROGRAM_ID,
                mint=mint_address,
                dest=destination_token_account,
                mint_authority=mint_authority.pubkey(),
                amount=amount_to_mint
            )
        )
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[mint_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, mint_authority])
        
        print(f"Mint: {mint_address}")
        print(f"Destination: {destination_token_account}")
        print(f"Amount: {amount_to_mint}")
        print(f"Mint authority: {mint_authority.pubkey()}")
        print(f"Payer: {payer.pubkey()}")
        print(f"Mint transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Solana Cookbook - How to Transfer Tokens (SPL Token Transfer Checked)
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import transfer_checked, TransferCheckedParams
from spl.token.instructions import get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    # Example keypairs and addresses
    payer = Keypair()
    owner = Keypair()
    receiver = Keypair()
    mint_address = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    # Token decimals (usually 9 for most tokens)
    decimals = 9
    
    # Amount to transfer (in smallest unit)
    amount_to_transfer = 10_000_000_000  # 10 tokens with 9 decimals
    
    async with rpc:
        # Get associated token addresses
        source_token_account = get_associated_token_address(
            owner=owner.pubkey(),
            mint=mint_address,
            token_program_id=TOKEN_PROGRAM_ID
        )
        
        destination_token_account = get_associated_token_address(
            owner=receiver.pubkey(),
            mint=mint_address,
            token_program_id=TOKEN_PROGRAM_ID
        )
        
        # Create transfer checked instruction
        transfer_instruction = transfer_checked(
            TransferCheckedParams(
                program_id=TOKEN_PROGRAM_ID,
                source=source_token_account,
                mint=mint_address,
                dest=destination_token_account,
                owner=owner.pubkey(),
                amount=amount_to_transfer,
                decimals=decimals
            )
        )
        
        # Get latest blockhash
        recent_blockhash = await rpc.get_latest_blockhash()
        
        # Create message
        message = MessageV0.try_compile(
            payer=payer.pubkey(),
            instructions=[transfer_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [payer, owner])
        
        print(f"Mint: {mint_address}")
        print(f"Source: {source_token_account}")
        print(f"Destination: {destination_token_account}")
        print(f"Amount: {amount_to_transfer}")
        print(f"Decimals: {decimals}")
        print(f"Owner: {owner.pubkey()}")
        print(f"Receiver: {receiver.pubkey()}")
        print(f"Transfer transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
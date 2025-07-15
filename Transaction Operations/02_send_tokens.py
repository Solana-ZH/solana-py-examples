#!/usr/bin/env python3
"""
Solana Cookbook - How to Send Tokens
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from spl.token.instructions import transfer_checked, TransferCheckedParams
from spl.token.constants import TOKEN_PROGRAM_ID

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    sender = Keypair()
    recipient = Keypair()
    
    # Example token mint (USDC devnet)
    token_mint = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    
    # Example token accounts (would need to be created first)
    sender_token_account = Pubkey.from_string("11111111111111111111111111111111")
    recipient_token_account = Pubkey.from_string("11111111111111111111111111111111")
    
    amount = 1_000_000  # 1 token (6 decimals)
    decimals = 6
    
    async with rpc:
        # Get latest blockhash
        latest_blockhash = await rpc.get_latest_blockhash()
        
        # Create transfer instruction
        transfer_instruction = transfer_checked(
            TransferCheckedParams(
                program_id=TOKEN_PROGRAM_ID,
                source=sender_token_account,
                mint=token_mint,
                dest=recipient_token_account,
                owner=sender.pubkey(),
                amount=amount,
                decimals=decimals
            )
        )
        
        # Create message
        message = MessageV0.try_compile(
            payer=sender.pubkey(),
            instructions=[transfer_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [sender])
        
        print(f"Sender: {sender.pubkey()}")
        print(f"Recipient: {recipient.pubkey()}")
        print(f"Token Mint: {token_mint}")
        print(f"Amount: {amount / (10 ** decimals)} tokens")
        print(f"Token transfer transaction created successfully")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Solana Cookbook - How to Add a Memo to a Transaction
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.instruction import Instruction
from solders.pubkey import Pubkey

# Memo Program ID
MEMO_PROGRAM_ID = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")

def create_memo_instruction(memo_text: str, signer_pubkey: Pubkey) -> Instruction:
    """Create a memo instruction"""
    return Instruction(
        program_id=MEMO_PROGRAM_ID,
        accounts=[],
        data=memo_text.encode('utf-8')
    )

async def main():
    rpc = AsyncClient("https://api.devnet.solana.com")
    
    sender = Keypair()
    recipient = Keypair()
    
    amount = 1_000_000_000  # 1 SOL
    memo_text = "Hello, Solana! This is a memo."
    
    async with rpc:
        # Get latest blockhash
        latest_blockhash = await rpc.get_latest_blockhash()
        
        # Create transfer instruction
        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=recipient.pubkey(),
                lamports=amount
            )
        )
        
        # Create memo instruction
        memo_instruction = create_memo_instruction(memo_text, sender.pubkey())
        
        # Create message with both instructions
        message = MessageV0.try_compile(
            payer=sender.pubkey(),
            instructions=[transfer_instruction, memo_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash.value.blockhash
        )
        
        # Create transaction
        transaction = VersionedTransaction(message, [sender])
        
        print(f"Sender: {sender.pubkey()}")
        print(f"Recipient: {recipient.pubkey()}")
        print(f"Amount: {amount / 1_000_000_000} SOL")
        print(f"Memo: {memo_text}")
        print(f"Transaction with memo created successfully")

if __name__ == "__main__":
    asyncio.run(main())
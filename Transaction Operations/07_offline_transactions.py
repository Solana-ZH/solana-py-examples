#!/usr/bin/env python3
"""
Solana Cookbook - Offline Transactions
"""

import asyncio
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.hash import Hash
import base58

async def create_offline_transaction():
    """Create a transaction offline without network connection"""
    
    sender = Keypair()
    recipient = Keypair()
    
    amount = 1_000_000_000  # 1 SOL
    
    # In offline mode, you need to provide a recent blockhash
    # This would typically be obtained from a previous network call
    # For demo purposes, we'll use a dummy blockhash
    recent_blockhash = Hash.from_string("11111111111111111111111111111111")
    
    # Create transfer instruction
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=sender.pubkey(),
            to_pubkey=recipient.pubkey(),
            lamports=amount
        )
    )
    
    # Create message
    message = MessageV0.try_compile(
        payer=sender.pubkey(),
        instructions=[transfer_instruction],
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash
    )
    
    # Create and sign transaction
    transaction = VersionedTransaction(message, [sender])
    
    return {
        "transaction": transaction,
        "sender": sender.pubkey(),
        "recipient": recipient.pubkey(),
        "amount": amount,
        "blockhash": recent_blockhash
    }

async def main():
    print("=== Creating Offline Transaction ===")
    
    # Create transaction offline
    offline_tx = await create_offline_transaction()
    
    print(f"Sender: {offline_tx['sender']}")
    print(f"Recipient: {offline_tx['recipient']}")
    print(f"Amount: {offline_tx['amount'] / 1_000_000_000} SOL")
    print(f"Blockhash: {offline_tx['blockhash']}")
    print(f"Transaction created offline successfully")
    
    # Serialize transaction for storage or transmission
    serialized = bytes(offline_tx['transaction'])
    print(f"Serialized transaction length: {len(serialized)} bytes")
    print(f"Serialized (base58): {base58.b58encode(serialized).decode()[:50]}...")
    
    print("\n=== Note ===")
    print("In a real scenario:")
    print("1. Get a recent blockhash from the network")
    print("2. Create and sign the transaction offline")
    print("3. Serialize the transaction")
    print("4. Later, broadcast the serialized transaction to the network")

if __name__ == "__main__":
    asyncio.run(main())
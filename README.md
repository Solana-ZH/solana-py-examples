# Solana Cookbook for Python

The [`Solana Cookbook`](https://solana.com/zh/developers/cookbook) is a developer resource that provides examples and references for building applications on Solana. Each example and reference will focus on specific aspects of Solana development while providing additional details and usage examples.

Built with  [`solana-py`](https://github.com/michaelhly/solana-py) library.

## Table of Contents

- [Installation](#installation)
- [Examples](#examples)
  - [Development Guides](#development-guides)
  - [Account Management](#account-management)
  - [Token Operations](#token-operations)
  - [Transaction Operations](#transaction-operations)
  - [Wallet Management](#wallet-management)
- [Contributing](#contributing)

## Installation

```bash
pip install -r requirements.txt
```

## Examples

### Development Guides

| Topic | Description | Code |
|-------|-------------|------|
| Connecting to Solana | How to connect to Solana clusters | [01_connecting_to_solana.py](Development%20Guides/01_connecting_to_solana.py) |
| Getting Test SOL | How to get test SOL for development | [02_getting_test_sol.py](Development%20Guides/02_getting_test_sol.py) |
| Subscribing to Events | How to subscribe to account changes | [03_subscribing_to_events.py](Development%20Guides/03_subscribing_to_events.py) |
| Create Account | How to create a new account on Solana | [04_create_account.py](Development%20Guides/04_create_account.py) |

### Account Management

| Topic | Description | Code |
|-------|-------------|------|
| Calculate Account Creation Cost | How to calculate the cost of creating an account | [01_calculate_account_creation_cost.py](Account%20Management/01_calculate_account_creation_cost.py) |
| Create PDA Account | How to create a Program Derived Address (PDA) account | [02_create_pda_account.py](Account%20Management/02_create_pda_account.py) |
| Get Account Balance | How to get the balance of an account | [03_get_account_balance.py](Account%20Management/03_get_account_balance.py) |

### Token Operations

| Topic | Description | Code |
|-------|-------------|------|
| Create Token | How to create a new SPL token | [01_create_token.py](Token%20Operations/01_create_token.py) |
| Get Token Mint | How to get token mint information | [02_get_token_mint.py](Token%20Operations/02_get_token_mint.py) |
| Create Token Account | How to create a token account | [03_create_token_account.py](Token%20Operations/03_create_token_account.py) |
| Get Token Account | How to get token account information | [04_get_token_account.py](Token%20Operations/04_get_token_account.py) |
| Get Token Balance | How to get the balance of a token account | [05_get_token_balance.py](Token%20Operations/05_get_token_balance.py) |
| Mint Tokens | How to mint tokens to an account | [06_mint_tokens.py](Token%20Operations/06_mint_tokens.py) |
| Burn Tokens | How to burn tokens from an account | [07_burn_tokens.py](Token%20Operations/07_burn_tokens.py) |
| Transfer Tokens | How to transfer tokens between accounts | [08_transfer_tokens.py](Token%20Operations/08_transfer_tokens.py) |
| Close Token Account | How to close a token account | [09_close_token_account.py](Token%20Operations/09_close_token_account.py) |
| Get All Token Accounts by Owner | How to get all token accounts owned by an address | [10_get_all_token_accounts_by_owner.py](Token%20Operations/10_get_all_token_accounts_by_owner.py) |
| Set Authority | How to set authority on token accounts or mints | [11_set_authority.py](Token%20Operations/11_set_authority.py) |
| Delegate Token Account | How to delegate token accounts | [12_delegate_token_account.py](Token%20Operations/12_delegate_token_account.py) |
| Revoke Delegate | How to revoke a token delegate | [13_revoke_delegate.py](Token%20Operations/13_revoke_delegate.py) |
| Wrapped SOL | How to use wrapped SOL | [14_wrapped_sol.py](Token%20Operations/14_wrapped_sol.py) |

### Transaction Operations

| Topic | Description | Code |
|-------|-------------|------|
| Send SOL | How to send SOL between accounts | [01_send_sol.py](Transaction%20Operations/01_send_sol.py) |
| Send Tokens | How to send tokens between accounts | [02_send_tokens.py](Transaction%20Operations/02_send_tokens.py) |
| Calculate Transaction Cost | How to calculate transaction costs | [03_calculate_transaction_cost.py](Transaction%20Operations/03_calculate_transaction_cost.py) |
| Add Memo to Transaction | How to add a memo to a transaction | [04_add_memo_to_transaction.py](Transaction%20Operations/04_add_memo_to_transaction.py) |
| Add Priority Fees | How to add priority fees to transactions | [05_add_priority_fees.py](Transaction%20Operations/05_add_priority_fees.py) |
| Optimize Compute Requested | How to optimize compute units for transactions | [06_optimize_compute_requested.py](Transaction%20Operations/06_optimize_compute_requested.py) |
| Offline Transactions | How to create and sign transactions offline | [07_offline_transactions.py](Transaction%20Operations/07_offline_transactions.py) |

### Wallet Management

| Topic | Description | Code |
|-------|-------------|------|
| Create Keypair | How to create a new keypair | [01_create_keypair.py](Wallet%20Management/01_create_keypair.py) |
| Restore Keypair | How to restore a keypair from a seed phrase | [02_restore_keypair.py](Wallet%20Management/02_restore_keypair.py) |
| Verify Keypair | How to verify a keypair | [03_verify_keypair.py](Wallet%20Management/03_verify_keypair.py) |
| Validate Public Key | How to validate a public key | [04_validate_public_key.py](Wallet%20Management/04_validate_public_key.py) |
| Sign and Verify Message | How to sign and verify messages | [05_sign_verify_message.py](Wallet%20Management/05_sign_verify_message.py) |

## Running Examples

Each example can be run independently:

```bash
cd "Token Operations"
python 01_create_token.py
```

## Requirements

- Python 3.8+
- solana-py
- solders
- spl-token

## Network Configuration

Most examples are configured to use Solana Devnet. To use a different network, modify the RPC endpoint in the examples:

```python
# Devnet (default)
rpc = AsyncClient("https://api.devnet.solana.com")

# Mainnet
rpc = AsyncClient("https://api.mainnet-beta.solana.com")

# Local
rpc = AsyncClient("http://localhost:8899")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

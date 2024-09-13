from abstract_solana import pump_fun_sell,load_from_private_key,sendTransaction
payer_keypair = load_from_private_key()
mint_str = "3bb6QmvustnZ627Kg2QvwTSi8gmxp7Y6orwXUokEwUyV"
txn = pump_fun_sell(mint=mint_str, token_balance=None, slippage=25)
txn_sig = sendTransaction(txn, payer_keypair, TxOpts(skip_preflight=True))
print("Transaction Signature", txn_sig)
confirm = confirm_txn(txn_sig)
print(confirm)

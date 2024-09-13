from spl.token.instructions import CloseAccountParams
from abstract_solana import get_pubkey,confirm_txn,pump_fun_buy,load_from_private_key,sendTransaction,load_from_private_key
from solana.rpc.types import TxOpts
payer_keypair = load_from_private_key()
payer_pubkey = get_pubkey(payer_keypair.pubkey())
mint_str = "3bb6QmvustnZ627Kg2QvwTSi8gmxp7Y6orwXUokEwUyV"
#txn = pump_fun_sell(mint=mint_str,payer_pubkey=payer_pubkey, token_balance=None, slippage=25)
txn = pump_fun_buy(mint=mint_str,payer_pubkey=payer_pubkey)
txn.sign(payer_keypair)
txn_sig = sendTransaction(txn, payer_keypair, TxOpts(skip_preflight=True))
print("Transaction Signature", txn_sig)
confirm = confirm_txn(txn_sig)
print(confirm)

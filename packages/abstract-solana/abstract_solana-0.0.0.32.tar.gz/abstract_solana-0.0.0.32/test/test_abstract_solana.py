from abstract_solana.pumpFun import pump_fun_sell
from abstract_solcatcher import *
 #type: ignore
mint_str = "3bb6QmvustnZ627Kg2QvwTSi8gmxp7Y6orwXUokEwUyV"
result = pump_fun_sell(mint_str=mint_str, token_balance=None, slippage=25)
# Example usage
input(result)



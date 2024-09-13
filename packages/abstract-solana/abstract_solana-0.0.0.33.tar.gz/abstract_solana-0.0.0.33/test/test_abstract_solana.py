from abstract_solana import pump_fun_sell,load_from_private_key
payer_keypair = load_from_private_key()
mint_str = "3bb6QmvustnZ627Kg2QvwTSi8gmxp7Y6orwXUokEwUyV"
result = pump_fun_sell(mint=mint_str, token_balance=None, slippage=25)
input(result)



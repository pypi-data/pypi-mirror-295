from abstract_solana import *
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from price_functions import *
from abstract_solcatcher import *
def get_solcatcher_api(endpoint,*args,**kwargs):
    return get_async_response(get_solcatcher_endpoint,endpoint=endpoint,*args,**kwargs)

mint = "911eA3wRZ85ZiSTpmCH1hksPGLGgzyVpfMXtJ4zSzVJ5"
bonding_curve = str(derive_bonding_curve(mint)[0])
bonding_curve_signature = get_solcatcher_api("getGenesisSignature",account=str(bonding_curve))
transfers = []
txnData = get_solcatcher_api("getTransaction",tx_sig=str(bonding_curve_signature))
txnData = get_transfer_instructions(txnData)
input(txnData)
txnData = get_for_program_ids_info(txnData)
input(txnData)



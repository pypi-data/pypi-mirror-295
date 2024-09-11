from abstract_solana import *
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from price_functions import *


PUMP_FUN_PROGRAM = get_pubkey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
PUMP_FUN_GLOBAL = get_pubkey("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf")
PUMP_FUN_FEE_RECIPIENT = get_pubkey("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM")
PUMP_FUN_SYSTEM_PROGRAM = get_pubkey("11111111111111111111111111111111")
PUMP_FUN_TOKEN_PROGRAM = get_pubkey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
PUMP_FUN_ASSOC_TOKEN_ACC_PROG = get_pubkey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
PUMP_FUN_RENT = get_pubkey("SysvarRent111111111111111111111111111111111")
PUMP_FUN_EVENT_AUTHORITY = get_pubkey("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1")
PUMP_FUN_PROGRAM = get_pubkey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

PUMP_FUN_ASSOC_TOKEN_ACC_PROG = get_pubkey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
from abstract_solcatcher import *
def get_solcatcher_api(endpoint,*args,**kwargs):
    return get_async_response(get_solcatcher_endpoint,endpoint=endpoint,*args,**kwargs)
def get_balance_info(balanceInfo, programId, authority):
    return next((bal for bal in balanceInfo if programId == bal.get("programId") and authority == bal.get("owner")), {})

def get_transfer_info(transfer_instructions, txnData):
    for transfer_instruction in transfer_instructions:
        updated_instruction = get_balance_from_instruction(transfer_instruction, txnData)
        transfer_instruction.update(updated_instruction)
    return transfer_instructions

def get_transfer_instructions(txnData,programId=None):
    programId = programId or PUMP_FUN_ASSOC_TOKEN_ACC_PROG
    return get_transfer_info(find_in_catalog('transfer',txnData,programId=programId),txnData)

mint = "911eA3wRZ85ZiSTpmCH1hksPGLGgzyVpfMXtJ4zSzVJ5"
bondingCurve = str(derive_bonding_curve(mint))
#input(getsignaturesforaddress(str(derive_bonding_curve(mint)[0])))
signature = get_solcatcher_api("getGenesisSignature",account=str(derive_associated_bonding_curve(mint,PUMP_FUN_PROGRAM)[0]))
txnData = get_solcatcher_api("getTransaction",tx_sig=str(signature))
input(get_all_account_keys(txnData))
parsed_txnData=parse_instruction_and_token_balances(txnData)
input(parsed_txnData)
input(find_in_catalog('Transfer',parsed_txnData,programId=PUMP_FUN_PROGRAM))
input(get_transfer_instructions(txnData))

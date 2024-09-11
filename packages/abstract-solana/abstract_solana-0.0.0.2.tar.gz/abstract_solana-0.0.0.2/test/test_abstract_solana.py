from abstract_solana import *
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from solders_rpc import *
PUMP_FUN_PROGRAM = get_pubkey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

PUMP_FUN_ASSOC_TOKEN_ACC_PROG = get_pubkey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
from abstract_solcatcher import *
def get_solcatcher_api(endpoint,*args,**kwargs):
    return get_async_response(get_solcatcher_endpoint,endpoint=endpoint,*args,**kwargs)
def get_balance_info(balanceInfo, programId, authority):
    return next((bal for bal in balanceInfo if programId == bal.get("programId") and authority == bal.get("owner")), {})
def get_balance_from_instruction(transfer_instruction, txnData):
    preBalance = txnData["meta"].get("preTokenBalances", [])
    postBalance = txnData["meta"].get("postTokenBalances", [])
    
    # Update transfer_instruction with source, destination, and authority
    accounts = transfer_instruction.get("accounts", [])
    transfer_instruction.update({
        key: accounts[i] for i, key in enumerate(["source", "destination", "authority"])
    })
    
    preBalanceInfo = get_balance_info(preBalance, transfer_instruction['programId'], transfer_instruction['authority'])
    postBalanceInfo = get_balance_info(postBalance, transfer_instruction['programId'], transfer_instruction['authority'])
    
    amount = preBalanceInfo.get('uiTokenAmount', {}).get('amount', 0) - postBalanceInfo.get('uiTokenAmount', {}).get('amount', 0)
    transfer_instruction['amount'] = amount
    
    return transfer_instruction
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
input(get_solcatcher_api("getGenesisSignature",account=str(derive_bonding_curve(mint)[0])))
parsed_txn = get_solcatcher_api("getParsedTransaction",signature="2pQRuCawe8it1X4bvKZnmSZZfcLUXd3q1ki8z1kMBCKm52eU2obQxGSkpRR1tX88nquy5iNiycebit3BFsQaDPcx")
input(get_transfer_instructions(parsed_txn,programId=PUMP_FUN_ASSOC_TOKEN_ACC_PROG))

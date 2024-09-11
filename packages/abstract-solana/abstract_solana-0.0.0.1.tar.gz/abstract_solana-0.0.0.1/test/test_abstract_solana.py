from abstract_solana import *
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from solders_rpc import *
PUMP_FUN_PROGRAM = get_pubkey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

PUMP_FUN_ASSOC_TOKEN_ACC_PROG = get_pubkey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
from abstract_solcatcher import *
def get_solcatcher_api(endpoint,*args,**kwargs):
    return get_async_response(get_solcatcher_endpoint,endpoint=endpoint,*args,**kwargs)
def derive_associated_bonding_curve(mint):
    return get_associated_token_address(derive_bonding_curve(mint)[0], get_pubkey(mint))
def derive_bonding_curve(mint):
    return Pubkey.find_program_address(["bonding-curve".encode(), bytes(get_pubkey(mint))],PUMP_FUN_PROGRAM)

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
async def async_getSignaturesForAddress(account: Pubkey,
                                        before: Optional[Signature] = None,
                                        until: Optional[Signature] = None,
                                        limit: Optional[int] = None,
                                        commitment: Optional[Commitment] = None,
                                        errorProof=False):
    """Returns confirmed signatures for transactions involving an address.

    Signatures are returned backwards in time from the provided signature or
    most recent confirmed block.

    Args:
        account: Account to be queried.
        before: (optional) Start searching backwards from this transaction signature.
            If not provided the search starts from the top of the highest max confirmed block.
        until: (optional) Search until this transaction signature, if found before limit reached.
        limit: (optional) Maximum transaction signatures to return (between 1 and 1,000, default: 1,000).
        commitment: (optional) Bank state to query. It can be either "finalized", "confirmed" or "processed".

    Example:
        >>> solana_client = Client("http://localhost:8899")
        >>> from solders.pubkey import Pubkey
        >>> pubkey = Pubkey.from_string("Vote111111111111111111111111111111111111111")
        >>> solana_client.get_signatures_for_address(pubkey, limit=1).value[0].signature # doctest: +SKIP
        Signature(
            1111111111111111111111111111111111111111111111111111111111111111,
        )
    """
    account=get_pubkey(account)
    before=get_sigkey(before)
    until=until
    limit=limit or 1000
    commitment=commitment
    response = json.loads(str(Client().get_signatures_for_address(account=account,before=before,until=until,limit=limit,commitment=commitment)))
    signatureArray= await makeLimitedCall(response.get('method'),response.get('params'))
    if errorProof:
        signatureArray = [signatureData for signatureData in signatureArray if signatureData.get('err') == None]
    return signatureArray
def getsignaturesforaddress(account,before=None,until=None,limit=None,commitment=None,errorProof=None):
    return get_async_response(async_getSignaturesForAddress,account=account,before=before,until=until,limit=limit,commitment=commitment,errorProof=errorProof)

def get_transfer_instructions(txnData,programId=None):
    programId = programId or PUMP_FUN_ASSOC_TOKEN_ACC_PROG
    return get_transfer_info(find_in_catalog('transfer',txnData,programId=programId),txnData)
async def async_getGenesisSignature(account,before=None,limit=1000,commitment=None):
    method = "getGenesisSignature"
    limit=1000

    genesisSignature=None
    if genesisSignature == None:
        before = before or None
        genesisSignature = None  # This will store the last seen valid signature
        while True:
            signatureArray = await getsignaturesforaddress(account=account,before=before,limit=limit,commitment=commitment)
            signatureArrayInfo = return_oldest_last_and_original_length_from_signature_array(signatureArray)
            genesisSignature = signatureArrayInfo.get("oldestValid") or genesisSignature

            if before == signatureArrayInfo.get("oldest") or signatureArrayInfo.get("length") < limit:
                #insert_Db(method.lower(), str(account), (str(account), str(genesisSignature)))
                return genesisSignature 
            before = signatureArrayInfo.get("oldest")
    return genesisSignature  

def getgenesissignature(account,before=None,limit=None,commitment=None):
    return get_async_response(async_getGenesisSignature,account=account,before=before,limit=limit,commitment=commitment)

mint = "911eA3wRZ85ZiSTpmCH1hksPGLGgzyVpfMXtJ4zSzVJ5"
bondingCurve = str(derive_bonding_curve(mint))
#input(getsignaturesforaddress(str(derive_bonding_curve(mint)[0])))
input(getgenesissignature(str(derive_bonding_curve(mint)[0])))
parsed_txn = get_solcatcher_api("getParsedTransaction",signature="2pQRuCawe8it1X4bvKZnmSZZfcLUXd3q1ki8z1kMBCKm52eU2obQxGSkpRR1tX88nquy5iNiycebit3BFsQaDPcx")
input(get_transfer_instructions(parsed_txn,programId=PUMP_FUN_ASSOC_TOKEN_ACC_PROG))

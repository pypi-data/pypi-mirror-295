from abstract_solana import Pubkey,get_pubkey,Optional,Union,LAMPORTS_PER_SOL,get_any_value
from abstract_solana.pumpFunKeys import get_pump_fun_data
from abstract_solcatcher import *
from abstract_security import *
import struct
import base58,time
from solders.hash import Hash
from solders.instruction import Instruction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price #type: ignore
from solana.rpc.types import TokenAccountOpts,TxOpts
from solders.keypair import Keypair
from solana.transaction import AccountMeta, Transaction
from construct import Padding, Struct, Int64ul, Flag
LAMPORTS_PER_SOL = 1_000_000_000
UNIT_PRICE =  1_000_000
UNIT_BUDGET =  100_000
def sendTransaction(txn: Transaction, payer_keypair, opts=TxOpts(skip_preflight=True)) -> dict:
    # Sign the transaction
    txn.sign(payer_keypair)
    
    # Serialize the transaction to a base64 string
    txn_base64 = base58.b58encode(txn.serialize()).decode('utf-8')
    
    # Prepare the RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [txn_base64, {"skipPreflight": opts.skip_preflight, "preflightCommitment": "finalized"}]
    }
    
    # Send the transaction
    response = requests.post(
        url="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",
        json=payload
    )
    
    # Parse the JSON response
    response_json = response.json()
    
    # Return the result or the entire response in case of error
    return response_json.get('result', response_json)
def load_from_private_key(env_key='AMM_P'):
    env_value = get_env_value(key=env_key)
    if env_value:
        return Keypair.from_base58_string(env_value)

def load_keypair_from_file(filename):
    curr = os.path.join(sys.path[0], 'data',  filename)
    with open(curr, 'r') as file:
        secret = json.load(file)
        secret_key = bytes(secret)
        print(base58.b58encode(secret_key))
        return Keypair.from_bytete_key()
payer_keypair = load_from_private_key()
payer_pubkey = str(payer_keypair.pubkey())
owner=Pubkey.from_string(payer_pubkey)
def get_token_balance(payer,mint_str: str):
    
    response = getTokenAccountBalance(str(payer),str(mint_str))
    response=response.get('value',response)
    ui_amount = get_any_value(response, "uiAmount") or 0
    return float(ui_amount)
def check_existing_token_account(owner: Pubkey, mint: Pubkey):
    try:
        account_data = get_account_by_owner(str(owner), str(mint))
        if account_data:
            token_account = account_data['pubkey']
            print(f"Existing token account found: {token_account}")
            return token_account, None
        else:
            print("No existing token account found. Creating a new one...")
            token_account = get_associated_token_address(owner, mint)
            token_account_instructions = create_associated_token_account(owner, owner, mint)
            return token_account, token_account_instructions
    except Exception as e:
        print(f"Error checking or creating token account: {e}")
        return None, None
def confirm_txn(txn_sig, max_retries=20, retry_interval=3):
    retries = 0
    
    while retries < max_retries:
        try:
            
            txn_res = get_transaction(signature=str(txn_sig))
            if txn_res:
                print(txn_res)
                print(f"\n\nhttps://solscan.io/tx/{str(txn_sig)}")
                break
            txn_json = safe_json_loads(txn_res.get('transaction',{}).get('meta',{}))
            error = txn_json.get('err')
            if error is None:
                print("Transaction confirmed... try count:", retries+1)
                return True
            print("Error: Transaction not confirmed. Retrying...")
            if error:
                print("Transaction failed.")
                return False
        except Exception as e:
            print("Awaiting confirmation... try count:", retries+1)
            retries += 1
            time.sleep(retry_interval)
    print("Max retries reached. Transaction confirmation failed.")
    return None

def get_coin_data(mint_str):
    return get_pump_fun_data(str(mint_str))



def buildTxn(mint, amount, slippage, token_account_pubkey,sol_in=0,token_price=None,token_balance=None,token_account_instructions=None,close_token_account=False,buy=True):
    # Get keys for the transaction, pass the token account's pubkey instead of the AccountMeta object
    keys = getKeys(get_coin_data(mint), token_account_pubkey, owner,buy=buy)
    
    if buy:
        # Calculate max_sol_cost
        slippage_adjustment = 1 + (slippage / 100)
        sol_in_with_slippage = sol_in * slippage_adjustment
        max_sol_cost = int(sol_in_with_slippage * LAMPORTS_PER_SOL)
        print("Max Sol Cost:", sol_in_with_slippage)
        hex_data = bytes.fromhex("66063d1201daebea")
        solCost = max_sol_cost
    else:
        # Calculate minimum SOL output
        sol_out = float(token_balance) * float(token_price)
        slippage_adjustment = 1 - (slippage / 100)
        sol_out_with_slippage = sol_out * slippage_adjustment
        min_sol_output = int(sol_out_with_slippage * LAMPORTS_PER_SOL)
        print("Min Sol Output:", sol_out_with_slippage)
        hex_data = bytes.fromhex("33e685a4017f83ad")
        solCost = min_sol_output
    
    data = bytearray()
    data.extend(hex_data)
    data.extend(struct.pack('<Q', amount))
    data.extend(struct.pack('<Q', solCost))
    data = bytes(data)
    PUMP_FUN_PROGRAM = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

    swap_instruction = Instruction(PUMP_FUN_PROGRAM, data, keys)
    blockHash = requests.post(url="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",data=json.dumps({"id":1,"jsonrpc":"2.0","method":"getLatestBlockhash","params":[{"commitment":"processed"}]}))
    recent_blockhash = get_any_value(blockHash.json(),'blockhash')
    recent_blockhash = Hash.from_string(recent_blockhash)
    txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=owner)
    txn.add(set_compute_unit_price(UNIT_PRICE))
    txn.add(set_compute_unit_limit(UNIT_BUDGET))
    
    if buy:
        if token_account_instructions:
            txn.add(token_account_instructions)
        txn.add(swap_instruction)
    else:
        txn.add(swap_instruction)
        if close_token_account:
            close_account_instructions = close_account(CloseAccountParams(PUMP_FUN_PROGRAM_PUBKEY, token_account_pubkey, owner, owner))
            txn.add(close_account_instructions)
    
    txn.sign(payer_keypair)
    # Send and confirm transaction
    txn_sig = sendTransaction(txn, payer_keypair, TxOpts(skip_preflight=True))
    print("Transaction Signature", txn_sig)
    confirm = confirm_txn(txn_sig)
    print(confirm)






def isListZero(obj):
    if obj and isinstance(obj, list):
        return obj[0]
    return obj







mint_str = "3bb6QmvustnZ627Kg2QvwTSi8gmxp7Y6orwXUokEwUyV"
result = pump_fun_sell(mint_str=mint_str, token_balance=None, slippage=25)
# Example usage
input(result)



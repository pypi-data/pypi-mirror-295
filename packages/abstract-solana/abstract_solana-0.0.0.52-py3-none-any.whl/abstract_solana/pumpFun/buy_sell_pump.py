import struct,base58,time
from typing import Optional,Union
from solders.hash import Hash
from solders.keypair import Keypair
from solders.instruction import Instruction
from solana.rpc.types import TokenAccountOpts,TxOpts
from solana.transaction import Transaction
from abstract_solcatcher import getLatestBlockHash
from ..pubkey_utils import Pubkey,get_pubkey
from ..constants import PUMP_FUN_PROGRAM_PUBKEY,LAMPORTS_PER_SOL
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from .token_utils import get_token_balance,check_existing_token_account,get_token_price
from .pump_fun_keys import getKeys
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
def buildTxn(mint,payer_pubkey, amount, slippage, token_account_pubkey,sol_in=0,token_price=0,token_balance=0,token_account_instructions=None,close_token_account=False,buy=True):
    # Get keys for the transaction, pass the token account's pubkey instead of the AccountMeta object
    keys = getKeys(mint, token_account_pubkey=token_account_pubkey, payer_pubkey=payer_pubkey,buy=buy)
    slippage_adjustment = 1 - (slippage / 100)
    sol_change = sol_in if buy else float(token_balance) * float(token_price)
    sol_change_with_slippage = sol_change * slippage_adjustment
    limit_sol_change = int(sol_change_with_slippage * LAMPORTS_PER_SOL)
    print(f"Max Sol {'Cost' if buy else 'Output'}:", sol_change_with_slippage)
    hex_data = bytes.fromhex("66063d1201daebea" if buy else "33e685a4017f83ad")
    data = bytearray()
    data.extend(hex_data)
    data.extend(struct.pack('<Q', amount))
    data.extend(struct.pack('<Q', limit_sol_change))
    swap_instruction = Instruction(PUMP_FUN_PROGRAM_PUBKEY, bytes(data), keys)
    blockHash = getLatestBlockHash(commitment="processed")
    recent_blockhash = get_any_value(blockHash.json(),'blockhash')
    recent_blockhash = Hash.from_string(recent_blockhash)
    txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=payer_pubkey)
    txn.add(set_compute_unit_price(UNIT_PRICE))
    txn.add(set_compute_unit_limit(UNIT_BUDGET))
    if buy and token_account_instructions:
        txn.add(token_account_instructions)
    txn.add(swap_instruction)
    if buy == False and close_token_account:
        close_account_instructions = close_account(CloseAccountParams(PUMP_FUN_PROGRAM_PUBKEY, token_account_pubkey, payer_pubkey, payer_pubkey))
        txn.add(close_account_instructions)
    txn.sign(payer_keypair)
    return txn

def get_all_buy_sell_info(mint,payer_pubkey,token_balance=None,sol_in=0):
    try:
        print("Owner Public Key:", payer_pubkey)
        mint_str = str(mint)
        if not get_pubkey(mint_str).is_on_curve():
            print('Mint public key is not on curve')
            return False
        mint_pubkey = get_pubkey(mint_str)
        token_account, token_account_instructions = check_existing_token_account(payer_pubkey, mint_pubkey)
        token_account_pubkey = get_pubkey(token_account)
        # Ensure the token_account is a valid Pubkey
        if not isinstance(token_account_pubkey, Pubkey):
            print("Failed to create or retrieve a valid token account Pubkey...")
            return False
        print("Token Account:", token_account)
        if not token_account:
            print("Failed to retrieve or create token account.")
            return False
        # Calculate token price
        token_price = get_token_price(mint_str)
        print(f"Token Price: {token_price:.20f} SOL")
        amount = int(LAMPORTS_PER_SOL * token_price)
        print("Calculated Amount:", amount)
        if token_balance == None:
            token_balance = get_token_balance(token_account,mint_str)
        print("Token Balance:", token_balance)
        if token_balance == 0:
            return False        
        return mint,amount,token_balance,token_price,token_account_pubkey,token_account_instructions
    except Exception as e:
        print(e)
        
def pump_fun_sell(mint: str,payer_pubkey:Pubkey, token_balance: Optional[Union[int, float]] = None,  slippage: int = 25, close_token_account: bool = True) -> bool:
    mint,amount,token_balance,token_price,token_account_pubkey,token_account_instructions = get_all_buy_sell_info(mint,payer_pubkey,token_balance=token_balance)
    return buildTxn(mint=mint,
             payer_pubkey=payer_pubkey,
             amount=amount,
             slippage=slippage,
             sol_in=0,
             token_balance=token_balance,
             token_price=token_price,
             token_account_pubkey=token_account_pubkey,
             token_account_instructions=token_account_instructions,
             buy=False)

def pump_fun_buy(mint: str,payer_pubkey:Pubkey, sol_in: float = 0.001, slippage: int = 25) -> bool:
    mint,amount,token_balance,token_price,token_account_pubkey,token_account_instructions = get_all_buy_sell_info(mint,payer_pubkey,sol_in=sol_in)
    # Build the transaction
    return buildTxn(mint=mint,
             payer_pubkey=payer_pubkey,
             amount=amount,
             slippage=slippage,
             sol_in=sol_in,
             token_balance=0,
             token_price=0,
             token_account_pubkey=token_account_pubkey,
             token_account_instructions=token_account_instructions,
             buy=True)
    return True

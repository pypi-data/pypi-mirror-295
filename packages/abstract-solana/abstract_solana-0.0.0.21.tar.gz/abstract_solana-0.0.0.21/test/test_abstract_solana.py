from abstract_solana import *
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from price_functions import *
from abstract_solcatcher import *
def get_solcatcher_api(endpoint,*args,**kwargs):
    return get_async_response(get_solcatcher_endpoint,endpoint=endpoint,*args,**kwargs)
def get_create_map():
  return [{'instruction_number': '1', 'instruction_name': 'Mint', 'token_address': 'AkAUSJg1v9xYT3HUxdALH7NsrC6owmwoZuP9MLw8fxTL', 'token_name': '3CAT'},
          {'instruction_number': '2', 'instruction_name': 'Mint Authority', 'token_address': 'TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM', 'token_name': 'Pump.fun Token Mint Authority'},
          {'instruction_number': '3', 'instruction_name': 'Bonding Curve', 'token_address': '9nhxvNxfSUaJddVco6oa6NodtsCscqCScp6UU1hZkfGm', 'token_name': 'Pump.fun (3CAT) Bonding Curve'},
          {'instruction_number': '4', 'instruction_name': 'Associated Bonding Curve', 'token_address': '889XLp3qvVAHpTYQmhn6cBpYSppV8Gi8E2Rgp9RH2vRy', 'token_name': 'Pump.fun (3CAT) Vault'},
          {'instruction_number': '5', 'instruction_name': 'Global', 'token_address': '4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf', 'token_name': '4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf'},
          {'instruction_number': '6', 'instruction_name': 'Mpl Token Metadata', 'token_address': 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s', 'token_name': 'Metaplex Token Metadata'},
          {'instruction_number': '7', 'instruction_name': 'Metadata', 'token_address': 'CH41RxpjSXHqr1vfLTVYJMsfNs2fBCCWoAE13tPihXh7', 'token_name': 'CH41RxpjSXHqr1vfLTVYJMsfNs2fBCCWoAE13tPihXh7'},
          {'instruction_number': '8', 'instruction_name': 'User', 'token_address': 'Fuy5MvbgzjSok1U8hH6mUY6WnLynzUextDxfEWMiTkn4', 'token_name': 'Fuy5MvbgzjSok1U8hH6mUY6WnLynzUextDxfEWMiTkn4'},
          {'instruction_number': '9', 'instruction_name': 'System Program', 'token_address': '11111111111111111111111111111111', 'token_name': 'System Program'},
          {'instruction_number': '10', 'instruction_name': 'Token Program', 'token_address': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', 'token_name': 'Token Program'},
          {'instruction_number': '11', 'instruction_name': 'Associated Token Program', 'token_address': 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL', 'token_name': 'Associated Token Account Program'},
          {'instruction_number': '12', 'instruction_name': 'Rent', 'token_address': 'SysvarRent111111111111111111111111111111111', 'token_name': 'Rent Program'},
          {'instruction_number': '13', 'instruction_name': 'Event Authority', 'token_address': 'Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1', 'token_name': 'Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1'},
          {'instruction_number': '14', 'instruction_name': 'Program', 'token_address': '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P', 'token_name': 'Pump.fun'}]

def getTxnTypes(signature,maps=None):
  maps = maps or get_create_pump_map()
  token_types = {}
  txnData = get_solcatcher_api('getTransaction',signature=signature)
  txnData = get_for_program_ids_info(txnData)
  for new_map in maps:
    instructions = txnData['transaction']['message']['instructions']
    innerInstructions = txnData['meta']['innerInstructions'][0]['instructions']
    allInstructions = instructions+innerInstructions
    for instruction in allInstructions:
      input(instruction.get('event'))
      if new_map.get('instruction_name') in instruction.get('events'):
        account = instruction.get('accounts')[new_map.get('account')]
        token_types[new_map.get('address_type')]=account
        break
  return token_types
def getTxnTypesFromMint(mint):
  mintPubKey = get_pubkey(mint)
  if not mintPubKey.is_on_curve():
    print('not on curve')
    return
  bonding_curve = str(derive_bonding_curve(mint)[0])
  bonding_curve_signature = get_solcatcher_api("getGenesisSignature",account=str(bonding_curve))
  txnTypes = getTxnTypes(bonding_curve_signature,maps=get_create_map())
  txnTypes['signature']=bonding_curve_signature
  return txnTypes
mint = "911eA3wRZ85ZiSTpmCH1hksPGLGgzyVpfMXtJ4zSzVJ5"
input(getTxnTypesFromMint(mint))





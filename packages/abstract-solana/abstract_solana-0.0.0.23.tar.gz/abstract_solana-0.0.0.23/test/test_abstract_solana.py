from abstract_solana import *
# Fetches and organizes transaction types based on provided mint
def getTxnTypes(mint):
    bonding_curve = str(derive_bonding_curve(mint)[0])
    bonding_curve_signature = getGenesisSignature(address=bonding_curve)
    txn_data = getTransaction(signature=bonding_curve_signature)
    txn_data = get_for_program_ids_info(txn_data)

    for new_map in get_create_map():
        instructions = txn_data['transaction']['message']['instructions']
        inner_instructions = txn_data['meta']['innerInstructions'][0]['instructions']
        all_instructions = instructions + inner_instructions

        instruction = [inst for inst in all_instructions if len(inst.get('associatedAccounts', [])) > 13]
        
        txn_types = {create_index['instruction_name']: instruction[0]['associatedAccounts'][int(create_index['instruction_number']) - 1] for create_index in get_create_map()}

        if txn_types:
            txn_types['signature'] = bonding_curve_signature
            break
    return txn_types


# Example usage
mint = "911eA3wRZ85ZiSTpmCH1hksPGLGgzyVpfMXtJ4zSzVJ5"
mint_pub_key = getTxnTypes(mint)

if not mint_pub_key.is_on_curve():
    print('Mint public key is not on curve')

txn_types = get_pump_fun_data(mint)

input(txn_types)

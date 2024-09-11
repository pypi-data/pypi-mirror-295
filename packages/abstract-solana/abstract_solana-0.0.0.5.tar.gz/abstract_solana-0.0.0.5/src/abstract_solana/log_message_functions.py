from abstract_utilities import make_list
import json,pprint
from .signature_data_parse import get_log_messages_from_txn,get_instructions_from_txn,get_inner_instructions_from_txn
from  .account_key_utils import get_all_account_keys
def ifListGetSection(list_obj,i=0):
    if list_obj and isinstance(list_obj,list) and len(list_obj)>i:
        list_obj = list_obj[i]
    return list_obj
def get_logs_from_index(txnData,index=None):
    if index is not None:
        allLogs = get_log_messages_from_txn(txnData)
        endLog = get_end_log_index(txnData,index)
        return allLogs[index:endLog]
def get_program_ids(txnData):
    allLogs = get_log_messages_from_txn(txnData)
    return [log.split(' ')[1] for log in allLogs if 'invoke' in log]
def get_program_id_from_log(logs):
    for log in make_list(logs):
        if 'invoke' in log.lower():
            return log.split(' ')[1]
def get_stack_height_from_logs(logs):
    for log in make_list(logs):
        if 'invoke' in log.lower():
            return int(log.split(' ')[-1][1:-1])
def get_end_log_index(txnData,index):
    allLogs = get_log_messages_from_txn(txnData)
    i=0
    for i,log in enumerate(allLogs[index+1:]):
        if 'invoke' in log.lower():
            return index+1+i
    return len(allLogs)
def get_for_program_ids_info(txnData):
    allLogs = get_log_messages_from_txn(txnData)
    return [{"programId":get_program_id_from_log(allLogs[i]),
             "start":i,
             "end":get_end_log_index(txnData,i),
             'stackHeight':get_stack_height_from_logs(allLogs[i]),
             'events':[event.split(':')[0] for event in get_log_events(get_logs_from_index(txnData,index=i))],
             'logs':get_logs_from_index(txnData,index=i)
             } for i in range(len(allLogs)) if 'invoke' in allLogs[i].lower()]
def split_log_for_instruction(log):
    return log.split('log:')[-1].split('Instruction:')[-1]
def clean_split_string(string,delim=' '):
    return delim.join([spl for spl in string.split(' ') if spl])
def get_log_events(logs=None,index=None):
    return [clean_split_string(split_log_for_instruction(log)) for log in logs if 'log:' in log.lower() or 'instruction:' in log.lower()]
def get_instruction_accounts(instruction,txnData):
    accounts = get_all_account_keys(txnData)
    return [accounts[index] for index in instruction.get('accounts',[]) if index < len(accounts)]  
def get_instruction_info(instruction,txnData,instruction_index=0):
  
    stack_height = instruction.get('stackHeight') or 1
    accounts = instruction.get('accounts',[])
    associatedAccounts = get_instruction_accounts(instruction,txnData)
    instruction_info = {'instruction_index':instruction_index,'accounts':accounts,'associatedAccounts':associatedAccounts,'instructionStackHeight':stack_height}

    instruction_info.update(get_for_program_ids_info(txnData)[instruction_index])
    return instruction_info
def process_instructions(instructions,txnData,start_index=1):
    catalog = []
    for i, inst in enumerate(instructions):
        instruction_index = start_index-1 + i
        instruction_info = get_instruction_info(inst,txnData,instruction_index)
        catalog.append(instruction_info)
    return catalog
def get_instructions_catalog(txnData,printIt=False,saveIt=False):
    instructions = get_instructions_from_txn(txnData)
    outer_instructions_catalog = process_instructions(instructions,txnData)
    inner_instructions = get_inner_instructions_from_txn(txnData)
    if inner_instructions:
        inner_instructions_catalog = process_instructions(inner_instructions,txnData,start_index=len(instructions))
    complete_catalog =  outer_instructions_catalog+inner_instructions_catalog
    if printIt:
        pprint.pprint(complete_catalog)
    if saveIt:
        with open(saveIt, 'w') as f:
            json.dump(complete_catalog, f, indent=4)
    return complete_catalog

def find_in_catalog(string,txnData,programId=None):
    complete_catalog = get_instructions_catalog(txnData)
    return [txn for txn in complete_catalog if [event for event in txn['events'] if string.lower() in event.lower()]]
def findKeyValueIdInCatalog(key,value,txnData,programId=None):
    complete_catalog = get_instructions_catalog(txnData)
    if programId:
        complete_catalog = findKeyValueIdInCatalog('programId',programId,txnData)
    return [txn for txn in make_list(complete_catalog) if txn.get(key) == value]
def find_account_in_catalog(account,catalog):
    return ifListGetSection([txn for txn in make_list(catalog) if account in txn.get('associatedAccounts')])

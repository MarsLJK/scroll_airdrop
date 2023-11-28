# coding=utf-8
import os
import csv
import random
import time

from eth_abi.abi import encode
from config.web3_provider import W3
from config.dev import GAS_PRICE

INTERACT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.csv")
MAIN_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main_contract.csv")

# 分组长度
SUB_LIST_LENGTH = 10

# 调用方法
STAKE, REDEEM, CLAIM_ETH, DIRECT_STAKE, DIRECT_REDEEM = range(5)
FUNC_NAME_LIST = ["STAKE", "REDEEM", "CLAIM", "DIRECT_STAKE", "DIRECT_REDEEM"]


# 生成随机value
def gen_value():
    random_int = random.randint(1, 10)
    random_number = random_int * 10000
    return random_number


# 调用stake
def call_stake(account_index, caller_contract_address, main_contract_address, is_main_rpc):
    pd = W3(False, account_index, is_main_rpc)
    gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
    caller_contact = pd.load_contract("ContractCaller", caller_contract_address)
    nonce = pd.get_nonce(pd.account.address)
    value = pd.w3.to_wei(gen_value(), "gwei")
    tx = caller_contact.functions.callFunc(
        main_contract_address,
        "0x3a4b66f1"
    ).build_transaction({
        'from': pd.account.address,
        'chainId': W3.get_chain_id(),
        'gas': 200000,
        'gasPrice': gas_price,
        'value': value,
        "nonce": nonce
    })
    signed_tx = pd.w3.eth.account.sign_transaction(tx, pd.account_pk)
    tx_hash = pd.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
    status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
    gas_fee = pd.w3.to_wei(gas_used * gas_price, "ether")
    return gas_used, gas_fee, tx_hash, value


# 直接调用stake
def direct_call_stake(account_index, main_contract_address, is_main_rpc):
    pd = W3(False, account_index, is_main_rpc)
    gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
    main_contract = pd.load_contract("SXEN", main_contract_address)
    nonce = pd.get_nonce(pd.account.address)
    value = pd.w3.to_wei(gen_value(), "gwei")
    tx = main_contract.functions.stake().build_transaction({
        'from': pd.account.address,
        'chainId': W3.get_chain_id(),
        'gas': 200000,
        'gasPrice': gas_price,
        'value': value,
        "nonce": nonce
    })
    signed_tx = pd.w3.eth.account.sign_transaction(tx, pd.account_pk)
    tx_hash = pd.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
    status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
    gas_fee = pd.w3.to_wei(gas_used * gas_price, "ether")
    return gas_used, gas_fee, tx_hash, value


# 调用redeem
def call_redeem(account_index, caller_contract_address, main_contract_address, is_main_rpc):
    pd = W3(False, account_index, is_main_rpc)
    gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
    caller_contact = pd.load_contract("ContractCaller", caller_contract_address)
    main_contract = pd.load_contract("SXEN", main_contract_address)
    balance_of = main_contract.functions.balanceOf(caller_contract_address).call()
    params_data = encode(
        ["uint256"],
        [balance_of]
    ).hex()
    call_data = "0xdb006a75" + params_data
    nonce = pd.get_nonce(pd.account.address)
    tx = caller_contact.functions.callFunc(
        main_contract_address,
        call_data
    ).build_transaction({
        'from': pd.account.address,
        'chainId': W3.get_chain_id(),
        'gas': 200000,
        'gasPrice': gas_price,
        "nonce": nonce
    })
    signed_tx = pd.w3.eth.account.sign_transaction(tx, pd.account_pk)
    tx_hash = pd.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
    status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
    gas_fee = pd.w3.to_wei(gas_used * gas_price, "ether")
    return gas_used, gas_fee, tx_hash, 0


# 直接调用redeem
def direct_call_redeem(account_index, main_contract_address, is_main_rpc):
    pd = W3(False, account_index, is_main_rpc)
    gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
    main_contract = pd.load_contract("SXEN", main_contract_address)
    balance_of = main_contract.functions.balanceOf(pd.account.address).call()
    nonce = pd.get_nonce(pd.account.address)
    tx = main_contract.functions.redeem(
        balance_of
    ).build_transaction({
        'from': pd.account.address,
        'chainId': W3.get_chain_id(),
        'gas': 200000,
        'gasPrice': gas_price,
        "nonce": nonce
    })
    signed_tx = pd.w3.eth.account.sign_transaction(tx, pd.account_pk)
    tx_hash = pd.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
    status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
    gas_fee = pd.w3.to_wei(gas_used * gas_price, "ether")
    return gas_used, gas_fee, tx_hash, 0


# 调用claimETH
def call_claim(account_index, caller_contract_address, is_main_rpc):
    pd = W3(False, account_index, is_main_rpc)
    gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
    caller_contact = pd.load_contract("ContractCaller", caller_contract_address)
    nonce = pd.get_nonce(pd.account.address)
    tx = caller_contact.functions.claimETH().build_transaction({
        'from': pd.account.address,
        'chainId': W3.get_chain_id(),
        'gas': 200000,
        'gasPrice': gas_price,
        "nonce": nonce
    })
    signed_tx = pd.w3.eth.account.sign_transaction(tx, pd.account_pk)
    tx_hash = pd.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
    status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
    gas_fee = pd.w3.to_wei(gas_used * gas_price, "ether")
    return gas_used, gas_fee, tx_hash, 0


def interact_sxen(sub_list_length=SUB_LIST_LENGTH, is_main_rpc=True):
    with open(MAIN_PATH, "r", newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        contract_data_list = list(reader)[1:]
        for contact_data in contract_data_list:
            print("[%s] 主合约地址：%s" % (contact_data[0], contact_data[1]))
    select_contract_num = int(input("-> 步骤1：请输入选用第几个主合约进行交互，从0开始，最大为%s，输入参数：" % (len(contract_data_list)-1)))
    select_contract = contract_data_list[select_contract_num][1]
    if select_contract_num >= len(contract_data_list):
        print("❌ 选择的主合约超过上界索引%s" % (len(contract_data_list)-1))
    if select_contract_num < 0:
        print("❌ 选择的主合约超过下界索引0")
    print("✅ 已选择第%s个主合约，合约地址：%s" % (select_contract_num, select_contract))
    with open(INTERACT_PATH, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        user_data_list = list(reader)[1:]
        divided_data = [[i, i + sub_list_length] for i in range(0, len(user_data_list), sub_list_length)]
        print("交互地址分组，每组%s个地址" % sub_list_length)
        max_group = 0
        for i, group in enumerate(divided_data):
            start, end = group
            if end >= len(user_data_list):
                end = len(user_data_list) - 1
            else:
                end -= 1
            print("第%s组，范围：%s ~ %s" % (i, start, end))
            max_group = i
        group_num = int(input("-> 步骤2：请输入选用第几组地址进行交互，从0开始，最大为%s，输入参数：" % max_group))
        if group_num > max_group:
            print("❌ 选择的分组数大于最大分组数%s" % max_group)
        if group_num < 0:
            print("❌ 选择的分组数小于最小分组数0")
        for i, group in enumerate(divided_data):
            if i == group_num:
                select_start, select_end = group
                if select_end >= len(user_data_list):
                    select_end = len(user_data_list)
                print("✅ 已选择第%s组，范围：%s ~ %s" % (group_num, select_start, select_end-1))
                select_func = int(input("-> 步骤3：请输入选择执行的方法，0:STAKE 1:REDEEM 2:CLAIM 3:DIRECT_STAKE 4:DIRECT_REDEEM 输入参数："))
                print("✅ 已选择%s方法" % FUNC_NAME_LIST[select_func])
                for data in user_data_list[select_start:select_end]:
                    account_index = int(data[0])
                    caller_contract = data[2]
                    if select_func == STAKE:
                        gas_used, gas_fee, tx_hash, value = call_stake(account_index, caller_contract, select_contract, is_main_rpc)
                    elif select_func == REDEEM:
                        gas_used, gas_fee, tx_hash, value = call_redeem(account_index, caller_contract, select_contract, is_main_rpc)
                    elif select_func == CLAIM_ETH:
                        gas_used, gas_fee, tx_hash, value = call_claim(account_index, caller_contract, is_main_rpc)
                    elif select_func == DIRECT_STAKE:
                        gas_used, gas_fee, tx_hash, value = direct_call_stake(account_index, select_contract, is_main_rpc)
                    else:
                        gas_used, gas_fee, tx_hash, value = direct_call_redeem(account_index, select_contract, is_main_rpc)
                    print("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (account_index, data[1], caller_contract, select_contract, FUNC_NAME_LIST[select_func], gas_used, gas_fee, tx_hash, value))


if __name__ == "__main__":
    interact_sxen()
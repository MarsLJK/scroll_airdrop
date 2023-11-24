# coding=utf-8
import os
import csv
from config.web3_provider import W3

# 配置gasPrice，gwei为单位
GAS_PRICE = 1.1
# 交互账户结束索引，到100结束
ACCOUNT_INDEX_END = 100

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.csv")


def deploy_contract_caller(is_main_account=False, account_end_index=ACCOUNT_INDEX_END, is_main_rpc=True):
    with open(FILE_PATH, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        user_data_list = list(reader)
    with open(FILE_PATH, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for index in range(len(user_data_list)-1, account_end_index):
            pd = W3(is_main_account, index, is_main_rpc)
            print("---> 加载交互账户，Index: %s，Address: %s" % (index, pd.account.address))
            gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
            deploy_tx = pd.build_deploy_contract_tx("ContractCaller", [], gas_price)
            tx_hash = pd.send_tx(deploy_tx)
            print("     正在部署ContractCaller合约，TxHash: ", tx_hash)
            status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
            print("     交易状态: %s, 使用gas: %s, 部署区块号: %s, 合约地址: %s" % (status, gas_used, block_num, contract_address))
            row = [index, pd.account.address, contract_address]
            writer.writerow(row)


if __name__ == "__main__":
    deploy_contract_caller()
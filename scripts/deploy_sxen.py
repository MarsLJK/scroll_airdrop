# coding=utf-8

from config.web3_provider import W3
from config.dev import GAS_PRICE

# 主账户索引，从0开始
ACCOUNT_INDEX = 0


def deploy_sxen(is_main_account=True, account_index=ACCOUNT_INDEX, is_main_rpc=True):
    pd = W3(is_main_account, account_index, is_main_rpc)
    print("---> 加载主账户，Address: ", pd.account.address)
    gas_price = pd.w3.to_wei(GAS_PRICE, "gwei")
    deploy_tx = pd.build_deploy_contract_tx("SXEN", [10000], gas_price)
    tx_hash = pd.send_tx(deploy_tx)
    print("---> 正在部署XSEN合约，TxHash: ", tx_hash)
    status, contract_address, gas_used, block_num = pd.get_tx_hash_receipt(tx_hash)
    print("---> 交易状态: %s, 使用gas: %s, 部署区块号: %s, 合约地址: %s" % (status, gas_used, block_num, contract_address))


if __name__ == "__main__":
    deploy_sxen()
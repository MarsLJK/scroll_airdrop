# coding=utf-8

from web3 import Web3
from web3.gas_strategies.time_based import construct_time_based_gas_price_strategy
from config import dev as config
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import os
import json


class W3:

    def __init__(self, is_main_account=True, account_index=0, is_main_rpc=True):
        self.w3 = self.get_web3(is_main_rpc)
        self.account_pk, self.account = self.load_account(is_main_account, account_index)

    @staticmethod
    def get_web3(is_main_rpc):
        if is_main_rpc:
            provider = Web3.HTTPProvider(config.SCROLL_RPC_1)
        else:
            provider = Web3.HTTPProvider(config.SCROLL_RPC_2)
        w3 = Web3(provider)
        gas_strategy = construct_time_based_gas_price_strategy(
            max_wait_seconds=1, sample_size=1, probability=100, weighted=True
        )
        w3.eth.set_gas_price_strategy(gas_strategy)
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return w3

    # 获取chainId
    @staticmethod
    def get_chain_id():
        return 534352

    # 加载账户
    @staticmethod
    def load_account(is_main_account, account_index):
        if is_main_account:
            account_pk = config.MAIN_ACCOUNT_PK_LIST[account_index]
            if not account_pk:
                raise Exception('选择的主地址索引超过上限，主地址数量：%s，选择的索引： %s' % (len(config.MAIN_ACCOUNT_PK_LIST), account_index))
        else:
            seed_bytes = Bip39SeedGenerator(config.INTERACT_ACCOUNT_MNEMONIC).Generate()
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
            bip44_addr_ctx = bip44_acc_ctx.AddressIndex(addr_idx=account_index)
            account_pk = bip44_addr_ctx.PrivateKey().Raw().ToHex()
        return account_pk, Account.from_key(account_pk)

    # 加载合约abi
    @staticmethod
    def get_contract_abi(contract_name):
        contract_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contract")
        contract_file = os.path.join(contract_path, "%s.json" % contract_name)
        with open(contract_file, "r") as abi_code:
            abi_json = json.load(abi_code)
            abi = abi_json["abi"]
            return abi

    # 加载合约bytecode
    @staticmethod
    def get_contract_bytecode(contract_name):
        contract_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contract")
        contract_file = os.path.join(contract_path, "%s.bin" % contract_name)
        with open(contract_file, "r") as bin_code:
            return bin_code.read()

    # 加载合约
    def load_contract(self, contract_name, contract_address):
        abi = W3.get_contract_abi(contract_name)
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        return contract

    # 构建部署合约的交易
    def build_deploy_contract_tx(self, contract_name, constructor_parameters, gas_price):
        contract_abi = W3.get_contract_abi(contract_name)
        contract_bytecode = W3.get_contract_bytecode(contract_name)
        Contract = self.w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        transaction = Contract.constructor(*constructor_parameters).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 2000000,  # 设置足够的gas
            'gasPrice': gas_price,
            'chainId': W3.get_chain_id(),
        })
        return transaction

    # 获取最近区块
    def get_latest_block_num(self):
        block = self.w3.eth.get_block('latest')
        latest_block_num = block["number"]
        return latest_block_num

    # 发送交易
    def send_tx(self, tx):
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account_pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
        return tx_hash

    # 获取tx执行结果
    def get_tx_hash_receipt(self, tx_hash):
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        status = receipt["status"]
        contract_address = receipt["contractAddress"]
        gas_used = receipt["gasUsed"]
        block_num = receipt["blockNumber"]
        return status, contract_address, gas_used, block_num

    # 调用合约view方法，并返回格式化的数据
    def call_view_func(self, contract_address, call_data):
        res = self.w3.eth.call({
            "to": self.w3.to_checksum_address(contract_address),
            "data": call_data
        }).hex()[2:]
        start = 0
        end = start + 64
        i = 0
        while True:
            item = res[start:end]
            print("[%s] %s %s" % (i, item, int(item, 16)))
            if end >= len(res):
                break
            start = end
            end = start + 64
            i += 1


if __name__ == "__main__":
    pass
# coding=utf-8

from config.web3_provider import W3

# 交互账户结束索引，到100结束
ACCOUNT_INDEX_END = 100


def display_address(is_main_account=False, account_end_index=ACCOUNT_INDEX_END, is_main_rpc=True):
    for index in range(account_end_index):
        pd = W3(is_main_account, index, is_main_rpc)
        print("%s" % pd.account.address)


if __name__ == "__main__":
    display_address()
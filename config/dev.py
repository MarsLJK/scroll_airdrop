# coding=utf-8
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

"""
开发环境使用的配置
"""

# 主账户私钥
MAIN_ACCOUNT_PK_LIST = os.getenv("MAIN_ACCOUNT_PK_LIST").split(",")
# 交互账户助记词
INTERACT_ACCOUNT_MNEMONIC = os.getenv("INTERACT_ACCOUNT_MNEMONIC")

# RPC
SCROLL_RPC_1 = "https://rpc.ankr.com/scroll"
SCROLL_RPC_2 = "https://rpc.scroll.io"
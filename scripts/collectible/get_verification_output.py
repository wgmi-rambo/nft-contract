#!/usr/bin/python3
import os
from brownie import WGMINFT, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False

    verification_info = WGMINFT.get_verification_info()

    # print("verification_info: ", verification_info)
    print("\nflattened_source: ", verification_info)

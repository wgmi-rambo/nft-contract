#!/usr/bin/python3
from brownie import WGMINFT, accounts, config, network


def main():
    CREATOR_PRIVATE_KEY = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    contract = WGMINFT.at("0x78C4864f49a6Ac8104491789BFcF3cC04a19E23c")

    transaction = contract.setPause(False, {"from": CREATOR_PRIVATE_KEY})

    transaction.wait(1)
    print("PAUSE set to False")

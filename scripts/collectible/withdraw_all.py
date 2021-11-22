#!/usr/bin/python3
from brownie import WGMINFT, accounts, network, config
from scripts.helpful_scripts import OPENSEA_FORMAT


def main():
    CREATOR_PRIVATE_KEY = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    cool_collectible = WGMINFT[len(WGMINFT) - 1]

    transaction = cool_collectible.withdrawAll({"from": CREATOR_PRIVATE_KEY})

    transaction.wait(1)
    print("All funds withdrawn to CREATOR_ADDRESS")

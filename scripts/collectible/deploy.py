#!/usr/bin/python3
import os

from brownie import WGMINFT, accounts, config, network

# Constructor Config
NFT_NAME = "WGMINFT Name"
NFT_SYMBOL = "THE"
INITIAL_BASE_URI = "https://domain.invalid/token"
INITIAL_NOT_REVEALED_URI = "https://domain.invalid/pre-reveal/"


def main():
    CREATOR_PRIVATE_KEY = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False

    WGMINFT.deploy(
        NFT_NAME,
        NFT_SYMBOL,
        INITIAL_BASE_URI,
        INITIAL_NOT_REVEALED_URI,
        {"from": CREATOR_PRIVATE_KEY},
        publish_source=publish_source,
    )

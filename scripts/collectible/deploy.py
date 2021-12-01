#!/usr/bin/python3
import os

from brownie import WGMINFT, accounts, config, network

# Constructor Config
NFT_NAME = "WGMINFT Name"
NFT_SYMBOL = "THE"
METADATA_REVEAL_SECRET = os.getenv("METADATA_REVEAL_SECRET")
INITIAL_BASE_URI = f"https://unrgblmd-4vb3u.ondigitalocean.app/{METADATA_REVEAL_SECRET}?id="
INITIAL_NOT_REVEALED_URI = "https://unrgblmd-4vb3u.ondigitalocean.app/preview"
COMMUNITY_OWNER_ADDRESS = os.getenv("COMMUNITY_OWNER_ADDRESS")


def main():
    CREATOR_PRIVATE_KEY = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False

    WGMINFT.deploy(
        NFT_NAME,
        NFT_SYMBOL,
        INITIAL_BASE_URI,
        INITIAL_NOT_REVEALED_URI,
        COMMUNITY_OWNER_ADDRESS,
        {"from": CREATOR_PRIVATE_KEY},
        publish_source=publish_source,
    )

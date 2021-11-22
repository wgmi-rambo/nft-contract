#!/usr/bin/python3
import os
from brownie import WGMINFT, accounts, network, config
from scripts.helpful_scripts import OPENSEA_FORMAT


def main():
    _MINTER_PRIVATE_KEY = os.getenv("MINTER_PRIVATE_KEY")
    MINTER_PRIVATE_KEY = accounts.add(_MINTER_PRIVATE_KEY)

    print(network.show_active())
    simple_collectible = WGMINFT[len(WGMINFT) - 1]
    token_id = simple_collectible.tokenCounter()

    tx_data = {"from": MINTER_PRIVATE_KEY, "value": 60000000000000000}

    transaction = simple_collectible.mint(1, tx_data)
    transaction.wait(1)

    print(
        "Awesome! You can view your WGMINFT at {}".format(
            OPENSEA_FORMAT.format(simple_collectible.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')

#!/usr/bin/python3
import os, sys
from brownie import WGMINFT, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print("Current network:", network.show_active())

    token = WGMINFT.at(os.getenv("ADDRESS_TO_VERIFY"))
    WGMINFT.publish_source(token)

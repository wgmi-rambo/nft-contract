#!/usr/bin/python3

import json

from brownie import WGMINFT, network


def main():
    print(network.show_active())

    verification_info = WGMINFT.get_verification_info()

    print("verification_info:\n")
    print(json.dumps(verification_info))

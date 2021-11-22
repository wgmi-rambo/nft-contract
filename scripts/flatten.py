#!/usr/bin/python3
from brownie import WGMINFT, accounts, network, config, interface
import json


def main():
    flatten()


def flatten():
    file = open("./WGMINFT_flattened.json", "w+")
    json.dump(WGMINFT.get_verification_info(), file)
    file.close()

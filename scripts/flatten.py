#!/usr/bin/python3
import json

from brownie import WGMINFT


def main():
    flatten()


def flatten():
    file = open("./WGMINFT_flattened.json", "w+")
    json.dump(WGMINFT.get_verification_info(), file)
    file.close()

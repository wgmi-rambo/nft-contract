#!/usr/bin/python3

from brownie import WGMINFT, network


def main():
    print(network.show_active())

    verification_info = WGMINFT.get_verification_info()

    print("verification_info: ", verification_info)

#!/usr/bin/python3
from brownie import WGMINFT, network


def main():
    print(network.show_active())
    contract = WGMINFT.at("0x4B2289FddD49398CC603075339c3CF1fF17Cd95A")

    user = input("Address to check: ")
    white = contract.isWhitelisted(user)
    print("white: ", white)

    dev = contract.isDev(user)
    print("dev: ", dev)

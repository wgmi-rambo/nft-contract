#!/usr/bin/python3

import os

from brownie import WGMINFT


def main():
    token = WGMINFT.at(os.getenv("ADDRESS_TO_VERIFY"))
    WGMINFT.publish_source(token)

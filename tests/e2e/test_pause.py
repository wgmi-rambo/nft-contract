import pytest
from brownie import WGMINFT, network, reverts

from scripts.helpful_scripts import get_account

from .. import settings

MINT_PRICE = settings.MINT_PRICE


class TestPause:
    def setup(self):
        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=2)

        # Deploy and disable onlyWhitelisted
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "INITIAL_BASE_URI",
            "INITIAL_NOT_REVEALED_URI",
            {"from": self.owner},
        )
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})

    def test_initial_pause_state(self):
        """Should be paused"""
        assert self.collectible.paused.call({"from": self.owner}) is False

    def test_unpause(self):
        """Should be able to mint"""
        self.collectible.pause(True, {"from": self.owner})

        with reverts("the contract is paused"):
            self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})

        self.collectible.pause(False, {"from": self.owner})
        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})

    def test_pause(self):
        """Should be unable to mint"""
        self.collectible.pause(True, {"from": self.owner})

        with reverts("the contract is paused"):
            self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})

import pytest
from brownie import WGMINFT, network, reverts

from scripts.helpful_scripts import get_account

from .. import settings

MINT_PRICE = settings.MINT_PRICE


class TestWithdrawal:
    def setup(self):
        """
        Setup by: minting a collectible and sending MINT_PRICE.
        """

        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=2)
        self.ORIGINAL_OWNER_BALANCE = self.owner.balance()

        # Deploy and disable onlyWhitelisted
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "INITIAL_BASE_URI",
            "INITIAL_NOT_REVEALED_URI",
            {"from": self.owner},
        )
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})

        # Send mint message with MINT_PRICE
        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})
        self.collectible.mint(1, {"from": self.owner, "amount": MINT_PRICE})

    def test_owner_can_withdraw_all(self):
        """
        Owner should be able to withdraw.
        """

        # assert contract has MINT_PRICE*2
        assert self.collectible.balance() == MINT_PRICE * 2

        # withdraw
        self.collectible.withdraw({"from": self.owner})

        # assert owner has MINT_PRICE + original balance
        assert self.owner.balance() == MINT_PRICE + self.ORIGINAL_OWNER_BALANCE

    def test_non_owner_cannot_withdraw_all(self):
        """
        Non-owner should NOT be able to withdraw.
        """

        # assert contract has MINT_PRICE*2
        assert self.collectible.balance() == MINT_PRICE * 2

        # withdraw
        with reverts("Ownable: caller is not the owner"):
            self.collectible.withdraw({"from": self.non_owner})

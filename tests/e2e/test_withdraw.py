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
        self.community_owner = get_account(index=4)
        self.ORIGINAL_COMMUNITY_OWNER_BALANCE = self.community_owner.balance()

        # Deploy and disable onlyWhitelisted
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "INITIAL_BASE_URI",
            "INITIAL_NOT_REVEALED_URI",
            self.community_owner,
            {"from": self.owner},
        )
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})

        # Send mint message with MINT_PRICE
        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})
        self.collectible.mint(1, {"from": self.owner, "amount": MINT_PRICE})

    def test_withdraw_to_withdraw_address(self):
        """
        Anybody should be able to withdraw.
        All withdrawals should go to the withdrawAddress address
        """

        #set withdraw address to community owner address
        self.collectible.setWithdrawAddress(self.community_owner, {"from": self.community_owner})

        # assert contract has MINT_PRICE*2
        contract_balance_before_withdrawal = self.collectible.balance()
        assert contract_balance_before_withdrawal == MINT_PRICE * 2
        

        # withdraw
        self.collectible.withdraw({"from": self.non_owner})

        # assert owner has MINT_PRICE + original balance
        assert self.community_owner.balance() == contract_balance_before_withdrawal + self.ORIGINAL_COMMUNITY_OWNER_BALANCE

    def test_anybody_can_withdraw(self):
        """
        Non-owner should NOT be able to withdraw.
        """

        # assert contract has MINT_PRICE*2
        assert self.collectible.balance() == MINT_PRICE * 2

        # withdraw
        self.collectible.withdraw({"from": self.non_owner})
        self.collectible.withdraw({"from": self.owner})
        self.collectible.withdraw({"from": self.community_owner})

"""
Methods tested:

- setNftPerAddressLimit
- setWhitelistNftPerAddressLimit
- setCost
- setBaseURI
- whitelistUsers
"""


import pytest
from brownie import WGMINFT, Wei, network
from brownie.exceptions import VirtualMachineError

from scripts.helpful_scripts import get_account

from .. import settings

MINT_PRICE = settings.MINT_PRICE
NFT_PER_ADDRESS_LIMIT = settings.NFT_PER_ADDRESS_LIMIT
WHITELIST_NFT_PER_ADDRESS_LIMIT = settings.WHITELIST_NFT_PER_ADDRESS_LIMIT


class TestPublicMethods:
    def setup(self):
        """
        Deploy contract
        """

        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=2)
        self.community_owner = get_account(index=4)

        # Deploy
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "my_initial_base_uri",
            "my_initial_not_revealed_uri",
            self.community_owner,
            {"from": self.owner},
        )

        # Give self.non_owner some extra eth
        for i in range(3, 6):
            get_account(index=i).transfer(self.non_owner, "10 ether")

    def test_method_setNftPerAddressLimit(self):
        """
        First, disable whitelistOnly.
        nftPerAddressLimit should be NFT_PER_ADDRESS_LIMIT, then should be changed to 5.
        """

        # assert nftPerAddressLimit is NFT_PER_ADDRESS_LIMIT
        assert (
            self.collectible.nftPerAddressLimit.call({"from": self.owner})
            == NFT_PER_ADDRESS_LIMIT
        )

        # call setNftPerAddressLimit(5)
        self.collectible.setNftPerAddressLimit(5, {"from": self.owner})

        # assert nftPerAddressLimit is 5
        assert self.collectible.nftPerAddressLimit.call({"from": self.owner}) == 5

        # Try to mint 6 tokens
        with pytest.raises(VirtualMachineError):
            self.collectible.mint(6, {"from": self.non_owner, "amount": 6 * MINT_PRICE})

    def test_method_setWhitelistNftPerAddressLimit(self):
        """
        First, Add non_owner to whitelist.
        whitelistNftPerAddressLimit should be WHITELIST_NFT_PER_ADDRESS_LIMIT,
        then should be changed to 1.
        """

        # Add non_owner to whitelist
        self.collectible.whitelistUsers([self.non_owner], {"from": self.owner})

        # assert whitelistNftPerAddressLimit is WHITELIST_NFT_PER_ADDRESS_LIMIT
        assert (
            self.collectible.whitelistNftPerAddressLimit.call({"from": self.owner})
            == WHITELIST_NFT_PER_ADDRESS_LIMIT
        )

        # call setNftPerAddressLimit(1)
        self.collectible.setWhitelistNftPerAddressLimit(1, {"from": self.owner})

        # assert whitelistNftPerAddressLimit is 1
        assert (
            self.collectible.whitelistNftPerAddressLimit.call({"from": self.owner}) == 1
        )

        # Try to mint 2 tokens
        with pytest.raises(VirtualMachineError):
            self.collectible.mint(2, {"from": self.non_owner, "amount": 2 * MINT_PRICE})

        # Try to mint 1 token
        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})

    def test_method_setCost(self):
        """
        Check cost, change it, then check it again.
        """

        # assert whitelistNftPerAddressLimit is WHITELIST_NFT_PER_ADDRESS_LIMIT
        assert self.collectible.cost.call({"from": self.owner}) == MINT_PRICE

        # call setNftPerAddressLimit(5)
        new_mint_cost = Wei("10 ether")
        self.collectible.setCost(new_mint_cost, {"from": self.owner})

        # assert whitelistNftPerAddressLimit is 1
        assert self.collectible.cost.call({"from": self.owner}) == new_mint_cost

    def test_method_setBaseURI(self):
        """
        Check baseURI, change it, then check it again.
        """

        # use reaveled baseURI
        self.collectible.reveal({"from": self.owner})

        # assert baseURI is correct
        assert self.collectible.baseURI() == "my_initial_base_uri"

        # call setBaseURI
        self.collectible.setBaseURI("my_new_base_uri", {"from": self.owner})

        # assert whitelistNftPerAddressLimit is 1
        assert self.collectible.baseURI() == "my_new_base_uri"

    def test_method_whitelistUsers(self):
        """
        Add non_owner to whitelist, check isWhitelisted, replace with non_owner_2,
        then check it again.
        """

        non_owner_2 = get_account(index=6)

        # Add non_owner to whitelist
        self.collectible.whitelistUsers([self.non_owner], {"from": self.owner})

        # assert non_owner is whitelisted
        assert self.collectible.isWhitelisted(self.non_owner) is True

        # Add non_owner_2 to whitelist
        self.collectible.whitelistUsers([non_owner_2], {"from": self.owner})

        # assert non_owner is whitelisted
        assert self.collectible.isWhitelisted(non_owner_2) is True

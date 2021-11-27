import pytest
from brownie import WGMINFT, Wei, network

from scripts.helpful_scripts import get_account

FIVE_ETH = Wei("5 ether")


class TestTokenUri:
    def setup(self):
        """
        Setup by: minting a collectible and sending 5 eth.
        """

        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=2)
        self.ORIGINAL_OWNER_BALANCE = self.owner.balance()
        self.community_owner = get_account(index=4)

        # Deploy
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "initial_base_uri_example/",
            "initial_not_revealed_uri_example/",
            self.community_owner,
            {"from": self.owner},
        )
        self.collectible.pause(False, {"from": self.owner})
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})

    # def test_not_revealed_uri(self):
    #     """
    #     Should return 'initial_not_revealed_uri_example/'
    #     """

    #     # Mint a token
    #     self.collectible.mint(1, {"from": self.non_owner, "amount": FIVE_ETH})

    #     # assert contract has correct tokenURI
    #     assert self.collectible.tokenURI(1) == "initial_not_revealed_uri_example/"

    def test_is_revealed(self):
        # assert contract's revealed variable is true
        assert self.collectible.revealed.call({"from": self.owner}) is True

    def test_revealed_uri(self):
        # Mint a token
        self.collectible.mint(1, {"from": self.non_owner, "amount": FIVE_ETH})

        # Reveal
        self.collectible.reveal({"from": self.owner})

        # assert contract has correct tokenURI
        assert self.collectible.tokenURI(1) == "initial_base_uri_example/" + "1"

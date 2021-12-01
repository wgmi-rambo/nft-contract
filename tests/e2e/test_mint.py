import pytest
from brownie import WGMINFT, network, reverts

from scripts.helpful_scripts import get_account

from .. import settings

MINT_PRICE = settings.MINT_PRICE
NFT_PER_ADDRESS_LIMIT = settings.NFT_PER_ADDRESS_LIMIT
WHITELIST_NFT_PER_ADDRESS_LIMIT = settings.WHITELIST_NFT_PER_ADDRESS_LIMIT


class TestNonWhitelistMinting:
    def setup(self):
        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=2)
        self.non_owner_2 = get_account(index=3)
        self.community_owner = get_account(index=4)

        # Deploy, disable onlyWhitelisted, and unpause
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "INITIAL_BASE_URI",
            "INITIAL_NOT_REVEALED_URI",
            self.community_owner,
            {"from": self.owner},
        )
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})
        self.collectible.pause(False, {"from": self.owner})

    def test_can_mint_single(self):
        """A single token should be minted by the owner"""

        self.collectible.mint(1, {"from": self.owner, "amount": MINT_PRICE})
        assert self.collectible.ownerOf(1) == self.owner

        # Only 1 token should be minted.
        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(2)

    def test_can_mint_by_non_owner(self):
        """A single token should be minted by a non-owner"""

        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})
        assert self.collectible.ownerOf(1) == self.non_owner

        # Only 1 token should be minted.
        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(2)

    def test_can_mint_many(self):
        """
        Mint multiple tokens, but less than NFT_PER_ADDRESS_LIMIT.
        Should be able to.
        """

        quantity = int(NFT_PER_ADDRESS_LIMIT / 2)

        token_ids = range(1, quantity + 1)
        self.collectible.mint(quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity})

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

    def test_can_mint_max(self):
        """Mint NFT_PER_ADDRESS_LIMIT tokens. Should be able to."""

        token_ids = range(1, NFT_PER_ADDRESS_LIMIT + 1)
        self.collectible.mint(
            NFT_PER_ADDRESS_LIMIT,
            {"from": self.non_owner, "amount": MINT_PRICE * NFT_PER_ADDRESS_LIMIT},
        )

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

    def test_cannot_mint_more_than_max(self):
        """
        Mint NFT_PER_ADDRESS_LIMIT+1 tokens.
        Should not be able to.
        """

        quantity = NFT_PER_ADDRESS_LIMIT + 1
        token_ids = range(1, quantity + 1)
        with reverts("max NFT per address exceeded"):
            self.collectible.mint(
                quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity}
            )

        for index, token in enumerate(token_ids):
            with reverts("ERC721: owner query for nonexistent token"):
                self.collectible.ownerOf(token)

    def test_cannot_mint_more_than_max_in_multiple_transactions(self):
        """
        Mint NFT_PER_ADDRESS_LIMIT-1, then 2 tokens.
        Should not be able to.
        """

        # Mint first x tokens: should succeed to mint
        quantity = NFT_PER_ADDRESS_LIMIT - 1
        token_ids = range(1, quantity + 1)
        self.collectible.mint(quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity})

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

        # Mint next x tokens: should fail to mint
        start_token_id = quantity + 1
        new_quantity = 2
        token_ids = range(start_token_id, start_token_id + new_quantity)

        with reverts("max NFT per address exceeded"):
            self.collectible.mint(
                new_quantity, {"from": self.non_owner, "amount": MINT_PRICE * new_quantity}
            )

        # Mint next x tokens: should succeed to mint
        start_token_id = quantity + 1
        new_quantity = 1
        token_ids = range(start_token_id, start_token_id + new_quantity)
        self.collectible.mint(
            new_quantity, {"from": self.non_owner, "amount": MINT_PRICE * new_quantity}
        )

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

    def test_can_mint_multiple_addresses(self):
        """
        Mint NFT_PER_ADDRESS_LIMIT to one address, then NFT_PER_ADDRESS_LIMIT to another.
        Should be able to.
        """

        quantity = NFT_PER_ADDRESS_LIMIT
        token_ids = range(1, quantity + 1)
        self.collectible.mint(quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity})

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

        start_token_id = quantity + 1
        quantity = NFT_PER_ADDRESS_LIMIT
        token_ids = range(start_token_id, start_token_id + quantity)
        self.collectible.mint(
            quantity, {"from": self.non_owner_2, "amount": MINT_PRICE * quantity}
        )

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner_2

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)


class TestWhitelistMinting:
    def setup(self):
        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=2)
        self.non_owner_2 = get_account(index=3)
        self.community_owner = get_account(index=4)
        self.guille23_owner = get_account(index=-1)

        # Deploy, and unpause
        self.collectible = WGMINFT.deploy(
            "My Cool NFT",
            "MCN",
            "INITIAL_BASE_URI",
            "INITIAL_NOT_REVEALED_URI",
            self.community_owner,
            {"from": self.owner},
        )
        self.collectible.pause(False, {"from": self.owner})

        # Add non_owner to whitelist
        self.collectible.whitelistUsers([self.non_owner], {"from": self.community_owner})

    def test_mint_guille23(self):
        """
        Make sure only guille23 can mint #888
        test edge cases
        """

        with reverts("Only token #888 can be minted"):
            self.collectible.guille23Mint({"from": self.guille23_owner, "amount": 0})

        # mint 887 nfts
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})

        # speed up minting
        self.collectible.setNftPerAddressLimit(887, {"from": self.community_owner})
        with reverts("max NFT limit exceeded"):
            for _ in range(8):
                self.collectible.mint(100, {"from": self.owner, "amount": MINT_PRICE * 100})
            self.collectible.mint(87, {"from": self.owner, "amount": MINT_PRICE * 87})
            self.collectible.mint(1, {"from": self.owner, "amount": MINT_PRICE * 1})
        assert self.collectible.totalSupply() == 887

        # return to original state
        self.collectible.setNftPerAddressLimit(3, {"from": self.community_owner})

        # test non-guille23 address can't mint
        with reverts("guille23Address is not the caller"):
            self.collectible.guille23Mint({"from": self.non_owner, "amount": 0})

        # test guille23 can mint once
        self.collectible.guille23Mint({"from": self.guille23_owner, "amount": 0})
        with reverts("Only token #888 can be minted"):
            self.collectible.guille23Mint({"from": self.guille23_owner, "amount": 0})

        # assert no more minting allowed
        with reverts("max NFT limit exceeded"):
            self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE * 1})

        # make sure state is as-expected
        assert self.collectible.totalSupply() == 888
        guille23_tokens = self.collectible.walletOfOwner(
            self.guille23_owner, {"from": self.non_owner}
        )
        assert 888 in guille23_tokens

    def test_can_mint(self):
        """A single token should be minted, since the sender is on the whitelist."""

        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})
        assert self.collectible.ownerOf(1) == self.non_owner

        # Only 1 token should be minted.
        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(2)

    def test_non_whitelisted_account_cannot_mint(self):
        """No tokens should be minted, since the sender is not on the whitelist."""

        with reverts("user is not whitelisted"):
            self.collectible.mint(1, {"from": self.non_owner_2, "amount": MINT_PRICE})

    def test_can_mint_many(self):
        """
        Mint multiple tokens, but less than NFT_PER_ADDRESS_LIMIT.
        Should be able to.
        """

        quantity = int(WHITELIST_NFT_PER_ADDRESS_LIMIT / 2)

        token_ids = range(1, quantity + 1)
        self.collectible.mint(quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity})

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

    def test_can_mint_max(self):
        """Mint NFT_PER_ADDRESS_LIMIT tokens. Should be able to."""

        token_ids = range(1, WHITELIST_NFT_PER_ADDRESS_LIMIT + 1)
        self.collectible.mint(
            WHITELIST_NFT_PER_ADDRESS_LIMIT,
            {"from": self.non_owner, "amount": MINT_PRICE * WHITELIST_NFT_PER_ADDRESS_LIMIT},
        )

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

    def test_cannot_mint_more_than_max(self):
        """
        Mint WHITELIST_NFT_PER_ADDRESS_LIMIT+1 tokens.
        Should not be able to.
        """

        quantity = WHITELIST_NFT_PER_ADDRESS_LIMIT + 1
        token_ids = range(1, quantity + 1)
        with reverts("max NFT per address exceeded while onlyWhitelisted is true"):
            self.collectible.mint(
                quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity}
            )

        for index, token in enumerate(token_ids):
            with reverts("ERC721: owner query for nonexistent token"):
                self.collectible.ownerOf(token)

    def test_cannot_mint_more_than_max_in_multiple_transactions(self):
        """
        Mint WHITELIST_NFT_PER_ADDRESS_LIMIT-1, then 2 tokens.
        Should not be able to.
        """

        # Mint first x tokens: should succeed to mint
        quantity = WHITELIST_NFT_PER_ADDRESS_LIMIT - 1
        token_ids = range(1, quantity + 1)
        self.collectible.mint(quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity})

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

        # Mint next x tokens: should fail to mint
        start_token_id = quantity + 1
        new_quantity = 2
        token_ids = range(start_token_id, start_token_id + new_quantity)

        with reverts("max NFT per address exceeded while onlyWhitelisted is true"):
            self.collectible.mint(
                new_quantity, {"from": self.non_owner, "amount": MINT_PRICE * new_quantity}
            )

        # Mint next x tokens: should succeed to mint
        start_token_id = quantity + 1
        new_quantity = 1
        token_ids = range(start_token_id, start_token_id + new_quantity)
        self.collectible.mint(
            new_quantity, {"from": self.non_owner, "amount": MINT_PRICE * new_quantity}
        )

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

    def test_can_mint_multiple_addresses(self):
        """Multiple whitelisted users should be able to mint."""

        # Add non_owner to whitelist
        self.collectible.whitelistUsers(
            [self.non_owner, self.non_owner_2], {"from": self.community_owner}
        )

        quantity = WHITELIST_NFT_PER_ADDRESS_LIMIT
        token_ids = range(1, quantity + 1)
        self.collectible.mint(quantity, {"from": self.non_owner, "amount": MINT_PRICE * quantity})

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

        start_token_id = quantity + 1
        quantity = WHITELIST_NFT_PER_ADDRESS_LIMIT
        token_ids = range(start_token_id, start_token_id + quantity)
        self.collectible.mint(
            quantity, {"from": self.non_owner_2, "amount": MINT_PRICE * quantity}
        )

        for token in token_ids:
            assert self.collectible.ownerOf(token) == self.non_owner_2

        with reverts("ERC721: owner query for nonexistent token"):
            self.collectible.ownerOf(token_ids[-1] + 1)

    def test_disable_whitelist_only_then_mint(self):
        """Mint with onlyWhitelisted enabled. Then disable it and mint another token."""

        # WhitelistOnly mint
        self.collectible.mint(1, {"from": self.non_owner, "amount": MINT_PRICE})

        # Disable WhitelistOnly, then mint
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})
        self.collectible.mint(1, {"from": self.non_owner_2, "amount": MINT_PRICE})

        assert self.collectible.ownerOf(1) == self.non_owner
        assert self.collectible.ownerOf(2) == self.non_owner_2

    def test_mint_whitelist_max_then_nft_max(self):
        """
        Mint WHITELIST_NFT_PER_ADDRESS_LIMIT.
        Then disable whitelistOnly.
        Then mint NFT_PER_ADDRESS_LIMIT.
        """

        # WhitelistOnly mint
        self.collectible.mint(
            WHITELIST_NFT_PER_ADDRESS_LIMIT,
            {"from": self.non_owner, "amount": WHITELIST_NFT_PER_ADDRESS_LIMIT * MINT_PRICE},
        )

        # Disable WhitelistOnly, then mint
        self.collectible.setOnlyWhitelisted(False, {"from": self.owner})
        quantity = NFT_PER_ADDRESS_LIMIT - WHITELIST_NFT_PER_ADDRESS_LIMIT
        if quantity > 0:  # mint fails if quantity=0
            self.collectible.mint(
                quantity, {"from": self.non_owner, "amount": quantity * MINT_PRICE}
            )

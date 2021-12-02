import pytest
from brownie import CommunityOwnableMock, network, reverts

from scripts.helpful_scripts import get_account


class TestCommunityOwnable:
    def setup(self):
        """
        Deploy contract
        """

        if network.show_active() not in ["development"] or "fork" in network.show_active():
            pytest.skip("Only for local testing")

        self.owner = get_account()
        self.non_owner = get_account(index=1)
        self.community_owner = get_account(index=2)

        # Deploy
        self.collectible = CommunityOwnableMock.deploy(
            self.community_owner,
            {"from": self.owner},
        )
        
    def test_onlyCommunityOwnerModifier(self):
        # with pytest.raises(reverts("XXX")):
        self.collectible.testOnlyCommunityOwnerModifier({"from": self.community_owner})

        with reverts("CommunityOwnable: caller is not the community owner"):
            self.collectible.testOnlyCommunityOwnerModifier({"from": self.owner})

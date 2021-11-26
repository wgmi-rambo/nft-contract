// SPDX-License-Identifier: UNLICENSED

pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "../CommunityOwnable.sol";

contract CommunityOwnableMock is CommunityOwnable {
    using Strings for uint256;

    constructor(address _communityOwner)
    CommunityOwnable(_communityOwner) {
    }


    function testOnlyCommunityOwnerModifier() public onlyCommunityOwner {
    }
}

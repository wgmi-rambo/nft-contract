pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WGMINFT is ERC721Enumerable, Ownable {
    using Strings for uint256;

    string public baseURI;
    string public baseExtension = "";
    string public notRevealedUri;
    uint256 public cost = 0.5 ether;
    uint256 public maxSupply = 10000;
    uint256 public nftPerAddressLimit = 10;
    uint256 public whitelistNftPerAddressLimit = 3;
    bool public paused = false;
    bool public revealed = false;
    bool public onlyWhitelisted = true;
    address[] public whitelistedAddresses;
    mapping(address => uint256) public addressMintedBalance;

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _initBaseURI,
        string memory _initNotRevealedUri
        ) ERC721(_name, _symbol) {
        setBaseURI(_initBaseURI);
        setNotRevealedURI(_initNotRevealedUri);
    }

    // internal
    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    // public
    function mint(uint256 _mintAmount) public payable {
        require(!paused, "the contract is paused");
        require(_mintAmount > 0, "need to mint at least 1 NFT");
        uint256 supply = totalSupply();
        require(supply + _mintAmount <= maxSupply, "max NFT limit exceeded");

        if (msg.sender != owner()) {
            uint256 senderMintedCount = addressMintedBalance[msg.sender];

            if(onlyWhitelisted == true) {
                require(isWhitelisted(msg.sender), "user is not whitelisted");
                require(
                    senderMintedCount + _mintAmount <= whitelistNftPerAddressLimit,
                    "max NFT per address exceeded while onlyWhitelisted is true"
                );
            }

            require(msg.value >= cost * _mintAmount, "insufficient funds");
            require(senderMintedCount + _mintAmount <= nftPerAddressLimit, "max NFT per address exceeded");
        }

        for (uint256 i = 1; i <= _mintAmount; i++) {
            addressMintedBalance[msg.sender]++;
            _safeMint(msg.sender, supply + i);
        }
    }

    function isWhitelisted(address _user) public view returns (bool) {
        for (uint i = 0; i < whitelistedAddresses.length; i++) {
            if (whitelistedAddresses[i] == _user) {
                return true;
            }
        }
        return false;
    }

    function walletOfOwner(address _owner) public view returns (uint256[] memory) {
        uint256 ownerTokenCount = balanceOf(_owner);
        uint256[] memory tokenIds = new uint256[](ownerTokenCount);
        for (uint256 i; i < ownerTokenCount; i++) {
            tokenIds[i] = tokenOfOwnerByIndex(_owner, i);
        }
        return tokenIds;
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

        if(revealed == false) {
            return notRevealedUri;
        }

        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0
        ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension))
        : "";
    }

    // only owner
    function reveal() public onlyOwner {
        revealed = true;
    }

    function setNftPerAddressLimit(uint256 _limit) public onlyOwner {
        nftPerAddressLimit = _limit;
    }

    function setWhitelistNftPerAddressLimit(uint256 _limit) public onlyOwner {
        whitelistNftPerAddressLimit = _limit;
    }

    function setCost(uint256 _newCost) public onlyOwner {
        cost = _newCost;
    }

    function setBaseURI(string memory _newBaseURI) public onlyOwner {
        baseURI = _newBaseURI;
    }

    function setBaseExtension(string memory _newBaseExtension) public onlyOwner {
        baseExtension = _newBaseExtension;
    }

    function setNotRevealedURI(string memory _notRevealedURI) public onlyOwner {
        notRevealedUri = _notRevealedURI;
    }

    function pause(bool _state) public onlyOwner {
        paused = _state;
    }

    function setOnlyWhitelisted(bool _state) public onlyOwner {
        onlyWhitelisted = _state;
    }

    function whitelistUsers(address[] calldata _users) public onlyOwner {
        delete whitelistedAddresses;
        whitelistedAddresses = _users;
    }

    function withdraw() public payable onlyOwner {
        (bool success, ) = payable(owner()).call{value: address(this).balance}("");
        require(success, "withdrawal failed");
    }
}

# $WGMI NFT Contract

## Discussion

**Discord**

- Invite: https://discord.com/invite/UrC32AKzyG
- \#dev-talk: https://discord.com/channels/908727219600388207/909143956632260628
- \#dev-talk/multi-sig: https://discord.com/channels/908727219600388207/912380991786590269
- \#nft: https://discord.com/channels/908727219600388207/909789293344616448

## Notes for guille23Mint and devMint
In order to use these functions, go to the contract on etherscan.
Using the test contract as an example:
1. Visit: https://rinkeby.etherscan.io/address/0x975eb08A1B1FF1782bb889dFa1D043657d1fCA23#code
2. Click "Write Contract".
3. Click connect to Web3 to connect your wallet.
4. Find the guille23Mint or devMint tab and click to expand it.
5. For "payableAmount" enter 0.
6. **devMint() Only**: Enter your desired quantity.
7. Click the blue "Write" button.
8. Review and complete the transaction in your wallet.

## Prerequisites

Please install or have installed the following:

- Python v3.9.7
- NodeJS ~16.0

## Installation

Install project dependencies:

```bash
pip install pipenv;
pipenv install;
```
Install **[ganache-cli](https://www.npmjs.com/package/ganache-cli)**:

```bash
npm install -g ganache-cli;
```

Install [ethlint](https://www.npmjs.com/package/solium):

```bash
npm install -g ethlint;
```

Install [pre-commit](https://pre-commit.com/):

```bash
pip install pre-commit;
pre-commit install;
```



# Usage

## Config

In `.env`:

- WEB3_INFURA_PROJECT_ID
- ETHERSCAN_TOKEN
- MINTER_PRIVATE_KEY
- CREATOR_PRIVATE_KEY
- COMMUNITY_OWNER_ADDRESS
- METADATA_REVEAL_SECRET
- ADDRESS_TO_VERIFY - added after the contract is deployed

## Lint

```bash
solium -d contracts/ --fix;
```



## Test

```bash
brownie test;
```



## Local Development

In a new window, launch *ganache*.

```bash
ganache-clie
```

Then, deploy the contract locally.

```bash
brownie run scripts/collectible/deploy.py --network development
```

Then we can mint.

```bash
brownie run scripts/collectible/mint.py --network development
```



## Deploy

First, enter the virtual env (`pipenv shell`).

Then run:

```bash
brownie run scripts/collectible/deploy.py --network rinkeby
```

**Make sure to choose the correct network.**

## Mint

```bash
brownie run scripts/collectible/mint.py --network rinkeby
```

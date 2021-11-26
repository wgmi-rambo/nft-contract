# $WGMI NFT Contract

## Discussion

**Discord**

- Invite: https://discord.com/invite/UrC32AKzyG
- \#dev-talk: https://discord.com/channels/908727219600388207/909143956632260628
- \#dev-talk/multi-sig: https://discord.com/channels/908727219600388207/912380991786590269
- \#nft: https://discord.com/channels/908727219600388207/909789293344616448

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

# Token Quotes
Token Quotes is a Python package for fetching and processing cryptocurrency token balances and quotes for a list of wallet addresses that you provide. It interacts with the Covalent API to retrieve token data, process it, and save it in a structured format.

## Features
- Fetch token balances for specified wallet addresses across different blockchains
- Process and structure token balance data
- Save processed data in csv format
- Command-line interface for easy data retrieval and processing

## Installation
### Using pip
```bash
pip install token-quotes
```

### Using poetry
```bash
poetry add token-quotes
```

### Docker
Pull from DockerHub
```bash
docker pull zaxier/token-quotes:latest
```

Or build locally
```bash
docker build -t token-quotes .
```

## Usage
### Input file
Example input YAML 
```yaml
wallets:
  - name: "MetaMask"
    metadata:
      details: "A MetaMask wallet with multiple addresses secured by a single seed phrase. MetaMask wallet can secure addresses multiple blockchains."
      provider: "MetaMask - https://metamask.io/"
      access: "Get metamask browser extension. Input the seed phrase to access the wallet."
    addresses:
      - address: "0x123"
        chain_ids: ["eth-mainnet", "arbitrum-mainnet"]
        owner: "me"
        purpose: "personal"
      - address: "0x456"
        chain_ids: ["eth-mainnet", "matic-mainnet"]
        owner: "LB"
        purpose: "personal"
  - name: "wallet 2"
    metadata: ...
    addresses: ...
```

### As a Python package
```python
import os
from report_builder import fetch_token_balances, save_to_jsonlines, extract_data, save_to_csv

COVALENT_API_KEY = os.getenv("COVALENT_API_KEY")

wallets = [
        {
            "name": "Main Wallet",
            "metadata": {"key": "value"},
            "addresses": [
                {
                    "address": "0x1234",
                    "owner": "me",
                    "purpose": "personal",
                    "chain_ids": ["eth-mainnet", "arbitrum-mainnet"],
                }
            ],
        },
    ]
raw_token_balances = fetch_token_balances(wallets, COVALENT_API_KEY, "usd")
save_to_jsonlines(raw_token_balances, "/tmp/raw_token_balances.jsonl")
data = extract_data("/tmp/raw_token_balances.jsonl")
save_to_csv(data, "output_file.csv")
```

### Command-line interface
```bash
token-quotes input.yml -o output.csv --currency usd --api-key $COVALENT_API_KEY
```
### Using Docker
```bash
docker run -v /path/to/your/local/directory:/app/data token-quotes:latest input.yml -o output.csv --currency usd --api-key $COVALENT_API_KEY
```
This command mounts your local directory to the /app/data directory in the container. Adjust the paths as necessary.

Example
```bash

docker run \
    -v $logs_dir:$logs_dir -v $input_file_dir:$input_file_dir -v $output_file_dir:$output_file_dir \
    zaxier/token-quotes:latest $input_file_path \
    -o $output_file_path \
    --api-key $COVALENT_API_KEY \
    --log-dir $logs_dir \
    --debug
```
To run the help message
```bash
docker run token-quotes:latest --help
```

## Development
To set up the development environment:

Clone the repository:
```bash
git clone https://github.com/zaxier/token-quotes.git
cd token-quotes
```

Install dependencies:
```bash
poetry install
```

Run tests:
```bash
poetry run pytest
```

## Configuration
Set your Covalent API key as an environment variable:
```sh
export COVALENT_API_KEY=your_api_key_here
```

## Logging
Logs are saved in the /app/logs directory. When running the Docker container, mount this directory to persist logs:
```sh
docker run -v /path/to/your/logs:/app/logs ...
```

## References

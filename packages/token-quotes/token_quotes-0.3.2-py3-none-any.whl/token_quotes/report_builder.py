import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd
import requests
import yaml
from covalent import CovalentClient

logger = logging.getLogger(__name__)


class TokenQuotesFetcher:
    def __init__(self, api_key):
        self.client = CovalentClient(api_key)
        logger.info("Covalent client initialized")

    def get_token_balances(self, chain_id, address, quote_currency):
        try:
            response = self.client.balance_service.get_token_balances_for_wallet_address(
                chain_id, address, quote_currency=quote_currency
            )

            # Check if the response indicates an error
            if hasattr(response, "error") and response.error:
                if response.error_code == 401:
                    logger.error("Invalid API key")
                    raise ValueError("Invalid API key. Please check your Covalent API key.")
                else:
                    logger.error(f"API error: {response.error_message}")
                    raise ValueError(f"API error: {response.error_message}")

            return response
        except requests.RequestException as e:
            logger.error(f"Network error when connecting to Covalent API: {str(e)}")
            raise ConnectionError(f"Network error when connecting to Covalent API: {str(e)}") from e
        except ValueError as e:  # noqa: F841
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}") from e

    @staticmethod
    def process_response(response) -> Dict[str, Any]:
        return {
            **response.__dict__,
            "items": [
                {
                    **item.__dict__,
                    "logo_urls": item.logo_urls.__dict__ if item.logo_urls else None,
                    "protocol_metadata": (item.protocol_metadata.__dict__ if item.protocol_metadata else None),
                }
                for item in response.data.items
                if item.balance != 0
            ],
        }


def load_wallets(input_source: str) -> List[Dict[str, str]]:
    if not os.path.isfile(input_source):
        raise ValueError(f"Input source is not a file: {input_source}")

    _, ext = os.path.splitext(input_source)
    if ext not in [".yaml", ".yml"]:
        raise ValueError(f"Unsupported file type: {ext}. Only YAML files are supported.")

    logger.info(f"Loading wallets from YAML file: {input_source}")
    with open(input_source, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise ValueError(f"Invalid YAML file: {input_source}") from e

    if not isinstance(data, dict) or "wallets" not in data:
        raise ValueError("Invalid YAML structure. Expected a 'wallets' key at the root level.")

    wallets = data["wallets"]
    if not isinstance(wallets, list):
        raise ValueError("Invalid 'wallets' data. Expected a list of wallet dictionaries.")

    logger.debug(f"Loaded wallets: {wallets}")
    return wallets


def fetch_token_balances(wallets: List[Dict[str, Any]], api_key: str, quote_currency: str) -> List[Dict]:
    fetcher = TokenQuotesFetcher(api_key)
    results = []
    for wallet in wallets:
        wallet_name = wallet.get("name")
        logger.info(f"Getting ready for wallet name: {wallet_name}")
        wallet_metadata = json.dumps(wallet.get("metadata", {}))
        for address_info in wallet.get("addresses", []):
            address = address_info.get("address")
            owner = address_info.get("owner")
            purpose = address_info.get("purpose")
            for chain_id in address_info.get("chain_ids", []):
                try:
                    response = fetcher.get_token_balances(chain_id, address, quote_currency)
                    response.name = wallet_name
                    response.address = address
                    response.chain_id = chain_id
                    response.owner = owner
                    response.purpose = purpose
                    response.quote_currency = quote_currency
                    response.metadata = wallet_metadata
                    processed = fetcher.process_response(response)
                    results.append(processed)
                except Exception as e:
                    logger.error(f"Error fetching balances for {address}: {str(e)}")
    return results


def extract_data(file_path: str) -> List[Dict]:
    extracted_data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                json_data = json.loads(line)
                name = json_data.get("name")
                address = json_data.get("address")
                chain_id = json_data.get("chain_id")
                owner = json_data.get("owner")
                purpose = json_data.get("purpose")
                quote_currency = json_data.get("quote_currency")
                metadata = json_data.get("metadata")
                for item in json_data.get("items", []):
                    extracted_item = {
                        "name": name,
                        "address": address,
                        "chain_id": chain_id,
                        "owner": owner,
                        "purpose": purpose,
                        "metadata": metadata,
                        "contract_name": item.get("contract_name"),
                        "contract_display_name": item.get("contract_display_name"),
                        "contract_ticker_symbol": item.get("contract_ticker_symbol"),
                        "contract_address": item.get("contract_address"),
                        "balance": float(item.get("balance")) / pow(10, item.get("contract_decimals")),
                        "quote_rate": item.get("quote_rate"),
                        "quote": item.get("quote"),
                        "quote_currency": quote_currency,
                        "last_transferred_at": item.get("last_transferred_at"),
                    }
                    extracted_data.append(extracted_item)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")
    return extracted_data


def save_to_jsonlines(data_list: List[Dict], path: str) -> str:
    logger.info(f"Saving temp token balances to {path}")
    with open(path, "w") as f:
        for item in data_list:
            f.write(json.dumps(item, default=str) + "\n")
    return path


def save_to_csv(data: List[Dict], output_file: str):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"Token balances saved to {output_file}")


def build_report(
    input_source: str,
    output_file: str,
    quote_currency: str,
    api_key: str,
    jsonl_output: str = "/tmp/token_balances.jsonl",
):
    wallets = load_wallets(input_source)
    results = fetch_token_balances(wallets, api_key, quote_currency)
    save_to_jsonlines(results, jsonl_output)
    data = extract_data(jsonl_output)
    save_to_csv(data, output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch token balances for wallets")
    parser.add_argument("input", help="Path to input file (YAML, JSON, CSV) or a single wallet address")
    parser.add_argument("-o", "--output", default="token_quotes.csv", help="Path to output file (CSV)")
    parser.add_argument("--currency", default="usd", help="Quote currency (default: usd)")
    parser.add_argument(
        "--api-key",
        help="Covalent API key (or set COVALENT_API_KEY environment variable)",
    )
    parser.add_argument(
        "--jsonl_output",
        default="/tmp/token_balances.jsonl",
        help="Path to output JSON Lines file",
    )

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("COVALENT_API_KEY")
    if not api_key:
        raise ValueError("Covalent API key must be provided via --api-key " "or COVALENT_API_KEY environment variable")

    build_report(args.input, args.output, args.currency, api_key, args.jsonl_output)

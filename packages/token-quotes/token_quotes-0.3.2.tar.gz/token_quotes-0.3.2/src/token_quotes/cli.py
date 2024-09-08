#!/usr/bin/env python3
import argparse
import logging
import os

from .logging_config import setup_logging
from .report_builder import build_report

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Fetch token balances for wallets")
    parser.add_argument("input", help="Path to input YAML file")
    parser.add_argument("-o", "--output", help="Path to output file (CSV)")
    parser.add_argument("--currency", default="usd", help="Quote currency (default: usd)")
    parser.add_argument(
        "--api-key",
        help="Covalent API key (or set COVALENT_API_KEY environment variable)",
    )
    parser.add_argument(
        "--jsonl_output",
        default="/tmp/token_balances.jsonl",
        help="Path to output intermediate JSON lines file. Non-essential. (default: /tmp/token_balances.jsonl)",
    )
    parser.add_argument(
        "--log-dir",
        default="./logs",
        help="Path to log directory (default: ./logs)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_dir=args.log_dir, log_level=log_level)

    api_key = args.api_key or os.environ.get("COVALENT_API_KEY")
    if not api_key:
        raise ValueError("Covalent API key must be provided via --api-key " "or COVALENT_API_KEY environment variable")

    build_report(args.input, args.output, args.currency, api_key, args.jsonl_output)


if __name__ == "__main__":
    main()

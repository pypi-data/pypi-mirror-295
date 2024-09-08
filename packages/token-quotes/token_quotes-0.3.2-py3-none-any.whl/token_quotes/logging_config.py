# logging_config.py
import logging
import os
from datetime import datetime


def setup_logging(log_dir: str = "./logs", log_level: int = logging.DEBUG):
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"token_quotes_log_{timestamp}.log")

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # This will output to stdout/stderr
        ],
    )

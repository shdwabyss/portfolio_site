import logging
import sys

logger = logging.getLogger(name="portfolio_backend")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)

log_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

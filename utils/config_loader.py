import yaml
import os
import sys
from logger.logger import logger
from exception.exception_handling import TripMateException


def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Loads configuration from a YAML file.
    Args:
        config_path (str): The path to the configuration file.
    Returns:
        dict: The loaded configuration.
    Raises:
        TripMateException: If the configuration file cannot be found or parsed.
    """
    try:
        logger.info(f"Loading configuration from {config_path}")
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        error = TripMateException(e, sys)
        logger.error(error.error_message)
        raise error

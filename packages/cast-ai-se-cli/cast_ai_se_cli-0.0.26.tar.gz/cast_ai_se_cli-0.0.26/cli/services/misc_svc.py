import logging
import os
import platform
import sys

from dotenv import load_dotenv
from docopt import ParsedOptions


from cli.constants import LOG_DIR, LOG_FILE, CONFIG_PATH
from cli.models.config import ConfigObject


def init(parsed_options: ParsedOptions) -> ConfigObject:
    CONFIG_PATH_PREFIX = os.getenv('CONFIG_PATH_PREFIX') or ""
    cfg = ConfigObject(parsed_options, config_file_path=CONFIG_PATH_PREFIX + CONFIG_PATH)

    if cfg.app_inputs["debug"]:
        log_level = logging.DEBUG
        os.makedirs(LOG_DIR, exist_ok=True)
        logging.basicConfig(filename=os.path.join(LOG_DIR, LOG_FILE),
                            format='%(asctime)s - %(levelname)s:%(name)s - %(message)s',
                            level=log_level)
    else:
        logging.basicConfig(level=logging.CRITICAL + 1)
    logger = logging.getLogger(__name__)
    logger.info(f"{'=' * 200}")
    logger.info(f"Starting executing SE CLI Command Sequencer with the following inputs: {sys.argv[1:]}")
    logger.debug(f"{get_system_info()}")
    return cfg


def get_system_info():
    return {'OS': platform.system(), 'OS Version': platform.version(), 'Machine': platform.machine()}


def load_env():
    if os.path.exists("constants.env"):
        load_dotenv(dotenv_path="constants.env")

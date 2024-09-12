import configparser
import logging
import os
import sys
from ..utils.logger import Logging

Logging()


def load_config(configPath):
    config_path = os.path.join(configPath)

    # 确认文件存在
    if os.path.exists(config_path):
        pass
    else:
        logging.error(f"Config file does not exist at: {config_path}")
        sys.exit("1")

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)

    return config

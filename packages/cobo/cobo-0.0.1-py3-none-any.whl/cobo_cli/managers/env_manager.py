import logging
from typing import Tuple, Union

from dotenv import dotenv_values, find_dotenv, get_key, load_dotenv, set_key, unset_key

logger = logging.getLogger(__name__)


class EnvManager(object):
    def __init__(self, env_file: str = None):
        """
        初始化 环境变量文件管理器
        :param env_file: 环境变量文件存储位置
        """
        self.env_file = env_file
        self.dotenv_path = find_dotenv(env_file)

        if not self.dotenv_path:
            logger.debug(
                f"No dotenv file found for {self.env_file}, creating a new one"
            )
            with open(self.env_file, "w") as f:
                f.write("")
            self.dotenv_path = find_dotenv(self.env_file)

        if not self.dotenv_path:
            raise IOError("Env file cannot be found or created.")

        load_dotenv(
            self.dotenv_path, verbose=logger.level <= logging.DEBUG, override=True
        )
        logger.debug(f"Load dotenv from {self.dotenv_path}")

    def set_config(self, key: str, value: str) -> str:
        """
        Set a key-value pair in the configuration.
        :param key:
        :param value:
        :return: 是否存储，存储位置
        """
        set_key(self.dotenv_path, key, value)
        return self.dotenv_path

    def get_config(self, key: str = None, wrap: bool = False) -> Union[dict, str]:
        """
        Get configs
        :param key: None for all
        :param wrap: True for wrap, return value wrapped
        :return:
        """
        if key:
            value = get_key(self.dotenv_path, key)
            if wrap:
                return {key: value}
            return value
        else:
            return dotenv_values(self.dotenv_path)

    def unset_config(self, key: str) -> Tuple[bool, str]:
        return unset_key(self.dotenv_path, key)

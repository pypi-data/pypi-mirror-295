from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from cobo_cli.data.enums import EnvironmentType
from cobo_cli.managers.env_manager import EnvManager


@dataclass
class CommandContext(object):
    env_manager: EnvManager = None
    env: EnvironmentType = EnvironmentType.DEVELOPMENT


class ApiSigner(metaclass=ABCMeta):
    @abstractmethod
    def get_headers(self):
        raise NotImplementedError


class UserTokenSigner(ApiSigner):
    def __init__(self, user_token):
        self.user_token = user_token

    def get_headers(self):
        return {
            "AUTHORIZATION": f"Bearer {self.user_token}",
        }

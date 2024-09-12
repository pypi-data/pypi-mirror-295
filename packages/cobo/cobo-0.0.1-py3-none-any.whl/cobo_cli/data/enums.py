import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

import yaml
from dataclasses_json import dataclass_json

from cobo_cli.constants import FrameworkEnum
from cobo_cli.data.constants import default_manifest_file


class EnvironmentType(Enum):
    SANDBOX = "sandbox"
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    LOCAL = "local"

    @classmethod
    def values(cls):
        return [e.value for e in cls]


EnvironmentType.SANDBOX.default_app_id = "b70c5912-a039-4a92-bba7-a1b26512275a"
EnvironmentType.DEVELOPMENT.default_app_id = "98bbd74a-49b1-40ef-a7f4-207b2c708bd7"
EnvironmentType.PRODUCTION.default_app_id = ""
EnvironmentType.LOCAL.default_app_id = ""


@dataclass_json
@dataclass
class Manifest:
    app_name: Optional[str] = None
    app_id: Optional[str] = None
    dev_app_id: Optional[str] = None
    client_id: Optional[str] = None
    dev_client_id: Optional[str] = None
    callback_urls: Optional[List[str]] = field(default_factory=lambda: [])
    app_desc: Optional[str] = None
    app_icon_url: Optional[str] = None
    homepage_url: Optional[str] = None
    policy_url: Optional[str] = None
    client_key: Optional[str] = None
    app_desc_long: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=lambda: [])
    screen_shots: Optional[List[str]] = field(default_factory=lambda: [])
    creator_name: Optional[str] = None
    contact_email: Optional[str] = None
    support_site_url: Optional[str] = None
    permission_notice: Optional[str] = None
    required_permissions: Optional[List[str]] = field(default_factory=lambda: [])
    optional_permissions: Optional[List[str]] = field(default_factory=lambda: [])
    framework: Optional[str] = None

    @staticmethod
    def load(file_path=default_manifest_file):
        if not os.path.exists(file_path):
            return Manifest()  # 返回默认的 Manifest 实例

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = f.read().strip()  # 读取文件内容并去除两端空白字符
                if not data:
                    return Manifest()  # 返回默认的 Manifest 实例

                if file_path.endswith(".json"):
                    Manifest.check_json_types(data)
                    return Manifest.from_json(data)
                elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
                    return Manifest.from_dict(yaml.safe_load(data))
                else:
                    raise ValueError("Unsupported file format")
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON file")
            except yaml.YAMLError:
                raise ValueError("Invalid YAML file")
            except ValueError as e:
                raise e

    def save(self, file_path=default_manifest_file):
        with open(file_path, "w", encoding="utf-8") as f:
            if file_path.endswith(".json"):
                # 设置 ensure_ascii=False 来防止 unicode 转义
                f.write(self.to_json(indent=4, ensure_ascii=False))
            elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
                yaml.safe_dump(self.to_dict(), f, default_flow_style=False)
            else:
                raise ValueError("Unsupported file format")

    def validate_required_fields(self, manifest_file: str, env: EnvironmentType = None):
        required_fields = [
            "app_name",
            "callback_urls",
            "client_key",
            "creator_name",
            "app_desc",
            "app_icon_url",
            "homepage_url",
            "contact_email",
            "support_site_url",
            "screen_shots",
            "app_desc_long",
            "required_permissions"
        ]
        error_fields = []
        for _field in required_fields:
            _value = getattr(self, _field, None)
            if not _value or len(_value) == 0:
                error_fields.append(_field)
        if len(error_fields) > 0:
            raise ValueError(
                f"Required field{'' if len(error_fields) == 1 else 's'} {', '.join(error_fields)} not exist{'' if len(error_fields) == 1 else 's'} in {manifest_file}.",
            )
        if env and env.value == EnvironmentType.PRODUCTION.value:
            if not self.homepage_url.startswith("https://"):
                raise ValueError("home_page_url should starts with https://")
        elif (not self.homepage_url.startswith("https://") and
              not self.homepage_url.startswith("http://localhost") and
              not self.homepage_url.startswith("http://127.0.0.1")):
            raise ValueError("home_page_url should starts with https:// or http://localhost or http://127.0.0.1")

        length_errors = []
        length_limits = {
            "app_desc": 80,
            "app_desc_long": 1000,
        }
        for field, max_length in length_limits.items():
            _value = getattr(self, field, None)
            if len(_value) > max_length:
                length_errors.append(f"{field} exceeds max length of {max_length} characters")
        if length_errors:
            raise ValueError(
                f"Field length error{'' if len(length_errors) == 1 else 's'}: {', '.join(length_errors)}."
            )
        framework_values = [l.value for l in FrameworkEnum]
        if self.framework and self.framework not in framework_values:
            raise ValueError(
                f"framework support {', '.join(framework_values)} for now"
            )

    @staticmethod
    def check_json_types(json_str):
        check_fields = {
            "app_name": str,
            "callback_urls": list,
            "app_desc": str,
            "app_icon_url": str,
            "homepage_url": str,
            "policy_url": str,
            "client_key": str,
            "app_desc_long": str,
            "tags": list,
            "screen_shots": list,
            "creator_name": str,
            "contact_email": str,
            "support_site_url": str,
            "permission_notice": str,
            "required_permissions": list,
            "optional_permissions": list,
            "framework": str,
        }
        json_data = json.loads(json_str)
        for key, value in json_data.items():

            if key not in check_fields:
                continue
            expected_type = check_fields[key]

            if not isinstance(value, expected_type):
                raise ValueError(f"Field '{key}' should be {expected_type.__name__}, but got {type(value).__name__}")

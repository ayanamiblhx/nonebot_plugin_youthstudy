from pydantic import BaseSettings, Extra
from typing import List


class Config(BaseSettings):
    # plugin custom config
    plugin_setting: str = "default"

    qq_friends: List[int] = []
    qq_groups: List[int] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False

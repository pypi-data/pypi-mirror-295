from __future__ import annotations

from typing import TYPE_CHECKING

from msgspec import json
from nonebot_plugin_localstore import get_plugin_config_dir

from .exception import UnSupportedError

if TYPE_CHECKING:
    from nonebot_plugin_session import Session

PATH = get_plugin_config_dir()
DECODER = json.Decoder(type=list[str])
ENCODER = json.Encoder()


def find(session: Session) -> list[str] | None:
    if session.id1 is None:
        return None
    if (config_path := PATH / session.platform / session.id1).exists() and config_path.is_file():
        return DECODER.decode(config_path.read_bytes())
    return None


def save(session: Session, language_code: list[str]) -> None:
    if session.id1 is None:
        raise UnSupportedError
    (path := PATH / session.platform / session.id1).parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ENCODER.encode(language_code))

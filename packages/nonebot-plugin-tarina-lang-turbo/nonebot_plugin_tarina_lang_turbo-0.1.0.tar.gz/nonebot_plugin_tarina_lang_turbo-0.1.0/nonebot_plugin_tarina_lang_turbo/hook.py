from __future__ import annotations

from nonebot import get_driver
from nonebot.log import logger
from nonebot.matcher import current_bot, current_event
from nonebot_plugin_session import extract_session
from tarina.lang import lang  # type: ignore[import-untyped]

from .manager import find

driver = get_driver()


original = lang.require


def wrapper(scope: str, type: str, locale: str | None = None) -> str:  # noqa: A002
    if locale is not None:
        # Prioritize specified language
        logger.debug(f'{scope} using incoming locale {locale}')
        return original(scope=scope, type=type, locale=locale)
    try:
        session = extract_session(current_bot.get(), current_event.get())
        if (locales := find(session)) is not None:
            for i in locales:
                try:
                    return original(scope=scope, type=type, locale=i)
                except ValueError:  # noqa: PERF203
                    logger.debug(f'{scope} does not support {i} language')
    except LookupError:
        logger.debug('Can not get session')
    return original(scope=scope, type=type, locale=locale)


lang.require = wrapper

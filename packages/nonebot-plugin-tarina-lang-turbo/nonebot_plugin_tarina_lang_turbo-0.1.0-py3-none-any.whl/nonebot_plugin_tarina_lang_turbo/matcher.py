from nonebot_plugin_alconna import Alconna, Args, MultiVar, Option, on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_session import EventSession
from tarina.lang import _LangConfigData, lang  # type: ignore[import-untyped]

from .i18n import model
from .manager import save

alc = on_alconna(
    Alconna(
        'tlang',
        Option('list', help_text='查看支持的语言列表'),
        Option(
            'set',
            Args['locale', MultiVar(str, flag='+')],
            help_text='设置语言',
        ),
    ),
    use_cmd_start=True,
)


@alc.assign('list')
async def _() -> None:
    configs: dict[str, _LangConfigData] = lang.__dict__['_LangConfig__configs']
    msg = ''
    for k, v in configs.items():
        if k == '$root':
            continue
        msg += f'{k}:\n'
        for i in sorted(v.locales):
            msg += f'  - {i}\n'
    await UniMessage(msg.strip()).finish()


@alc.assign('set')
async def _(locale: list[str], session: EventSession) -> None:
    save(session, locale)
    await alc.finish(model.Tlang.command.set())

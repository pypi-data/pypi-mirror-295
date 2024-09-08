from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require('nonebot_plugin_localstore')
require('nonebot_plugin_alconna')
require('nonebot_plugin_session')

__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-tarina-lang-turbo',
    description='Enhance tarina.lang to support user-level configuration',
    usage="""\
tlang list
tlang set zh-CN en-US""",
    type='application',
    homepage='https://github.com/shoucandanghehe/nonebot-plugin-tarina-lang-turbo',
    config=None,
    supported_adapters=inherit_supported_adapters('nonebot_plugin_alconna', 'nonebot_plugin_session'),
)

from . import hook, matcher  # noqa: E402, F401

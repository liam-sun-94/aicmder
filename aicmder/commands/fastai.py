from aicmder.commands import register, get_command
from aicmder.commands.utils import _command_prefix


@register(name=_command_prefix)
class AICommand:
    def execute(self, argv):
        help = get_command('{}.help'.format(_command_prefix))
        return help().execute(argv)

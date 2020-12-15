from typing import List


from aicmder.commands import register, _commands
from aicmder.commands.utils import _command_prefix as cmd


@register(name='{}.help'.format(cmd), description='Show help for commands.')
class HelpCommand:
    def execute(self, argv: List) -> bool:
        msg = 'Usage:\n'
        msg += '    {} <command> <options>\n\n'.format(cmd)
        msg += 'Commands:\n'
        for command, detail in _commands[cmd].items():
            if command.startswith('_'):
                continue

            if not '_description' in detail:
                continue
            msg += '    {:<15}        {}\n'.format(command, detail['_description'])
            if hasattr(detail['_entry'], 'help'):
                msg += '    {:<15}        {}\n'.format('', detail['_entry'].help())
        print(msg)
        return True
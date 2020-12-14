

from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd 


@register(name='{}.version'.format(cmd), description='Show version.')
class VersionCommand:
    def execute(self, argv: List) -> bool:
        print(cmder.__version__)
        return True
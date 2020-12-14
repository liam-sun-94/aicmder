

from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd 


@register(name='{}.onnx'.format(cmd), description='convert to onnx.')
class ONNXCommand:
    def execute(self, argv: List) -> bool:
        print('convert to onnx')
        return True
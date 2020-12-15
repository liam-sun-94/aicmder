from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
import argparse
import os
from shutil import copyfile
from pprint import pprint
@register(name='{}.init'.format(cmd), description='init convertint environment')
class InitCommand:
    
    _export_helper = 'export_helper.py'
    def execute(self, argv: List) -> bool:
        cur_path = os.getcwd()
        model_dir = os.path.join(cur_path, 'model')
        
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            os.system('touch {}'.format(os.path.join(model_dir, '__init__.py')))
        
        dest = os.path.join(model_dir, self._export_helper)
        if not os.path.exists(dest):
            src = os.path.abspath(os.path.dirname(__file__))
            src = os.path.join(src, '../../model', self._export_helper)
            copyfile(src, dest)
        
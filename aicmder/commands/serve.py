from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
import argparse
import os
from shutil import copyfile
from pprint import pprint
@register(name='{}.serve'.format(cmd), description='start all module')
class ServeCommand:
    
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description=self.__class__.__doc__, prog='{} serve'.format(cmd), usage='%(prog)s', add_help=True)
        self.parser.add_argument('--workers', '-w', default=1)

    def execute(self, argv: List) -> bool:
        args = self.parser.parse_args(argv)
        
        
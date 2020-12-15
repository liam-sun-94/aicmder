

from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
import argparse
from importlib import import_module
import os
from pprint import pprint

@register(name='{}.onnx'.format(cmd), description='convert to onnx.')
class ONNXCommand:
    
    def __init__(self) -> None:
        self.description = 'Start to convert to onnx model'
        self.parser = argparse.ArgumentParser(description=self.__class__.__doc__, prog='{} onnx'.format(cmd), usage='%(prog)s', add_help=True)
        self.parser.add_argument('--save_dir', '-s', required=False)
        # self.parser.add_argument('--model', '-m', required=True)
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        
        
    def execute(self, argv: List) -> bool:
        pprint('convert to onnx')
        args = self.parser.parse_args(argv)
        save_dir = self.cur_path if args.save_dir is None else args.save_dir
        
        print(args, save_dir)
        return True

from typing import List
from aicmder.commands.utils import help_str
import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
import argparse
import os
import onnx
from onnx_tf.backend import prepare


@register(name='{}.pb'.format(cmd), description='convert onnx to pb.')
class PbCommand:

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description=self.__class__.__doc__, prog='{} pb'.format(cmd), usage='%(prog)s', add_help=True)
        self.parser.add_argument('--onnx', '-o', required=True)
        self.parser.add_argument('--save_dir', '-s', required=False)
        self.cur_path = os.getcwd()

    def execute(self, argv: List) -> bool:
        args = self.parser.parse_args(argv)
        
        assert os.path.exists(args.onnx)
        save_dir = self.cur_path if args.save_dir is None else args.save_dir
    
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        onnx_model = onnx.load(args.onnx)
        tf_rep = prepare(onnx_model)
        tf_rep.export_graph(os.path.join(save_dir, 'saved_model')) 
        
    @staticmethod
    def help():
        str = "pb example\n"
        str += help_str("aicmder pb -o output/export.onnx")
        str += help_str("-o onnx model filepath")
        return str

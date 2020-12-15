from aicmder.utils.utils import load_py_dir
from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
from aicmder.commands.utils import help_str
import argparse
from importlib import import_module
import os, sys
from pprint import pprint
import torch
import importlib.util
@register(name='{}.onnx'.format(cmd), description='convert to onnx.')
class ONNXCommand:
    
    _helper = 'export_helper'
    
    def __init__(self) -> None:
        self.description = 'Start to convert to onnx model'
        self.parser = argparse.ArgumentParser(description=self.__class__.__doc__, prog='{} onnx'.format(cmd), usage='%(prog)s', add_help=True)
        self.parser.add_argument('--save_dir', '-s', required=False)
        self.parser.add_argument('--model', '-m', required=True)
        self.parser.add_argument('--ckpt', '-c', required=True)
        self.parser.add_argument('--gpu', action="store_true", default=False)
        self.parser.add_argument('--verbose', action="store_true", default=False)
        self.parser.add_argument('--export', '-e', default='export.onnx')
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        
        
    def execute(self, argv: List) -> bool:
        pprint('begin to convert to onnx')
        args = self.parser.parse_args(argv)
        save_dir = self.cur_path if args.save_dir is None else args.save_dir
        assert os.path.exists(args.model) and os.path.exists(args.ckpt)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        model_name = os.path.basename(args.model)
        model_dir = os.path.dirname(args.model)
        model_basename = os.path.basename(model_dir)
        # sys.path.append(model_dir)
        
        ## import module
        module = load_py_dir(model_dir)

        MODLE = import_module('{}.{}'.format(model_basename, model_name.replace('.py', '')))
        
        device = 'cuda:0' if args.gpu and torch.cuda.is_available() else 'cpu'
        # print(model_dir, module, spec.name, MODLE, args.gpu, device)
        
        ## build model
        export_helper = import_module('{}.{}'.format(model_basename, self._helper))
        model = MODLE.make_model(export_helper.args).to(device)
        state_dicts = torch.load(args.ckpt, map_location=device)
        model.load_state_dict(state_dicts)
        print('load model success.')
        
        ## export model
        dummy_input = export_helper.dummy_input.to(device)
        torch.onnx.export(model, dummy_input,os.path.join(save_dir, args.export),verbose=args.verbose)
        # print(model)
        return True

    @staticmethod
    def help():
        str = "onnx example\n"
        str += help_str("aicmder onnx -s output_dir -m './model/edsr.py' -c ckpt")
        str += help_str("-s onnx model output dir")
        str += help_str("-m py file of model")
        return str
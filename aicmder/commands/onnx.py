from typing import List

import aicmder as cmder
from aicmder.commands import register
from aicmder.commands.utils import _command_prefix as cmd
import argparse
from importlib import import_module
import os, sys
from pprint import pprint
@register(name='{}.onnx'.format(cmd), description='convert to onnx.')
class ONNXCommand:
    
    def __init__(self) -> None:
        self.description = 'Start to convert to onnx model'
        self.parser = argparse.ArgumentParser(description=self.__class__.__doc__, prog='{} onnx'.format(cmd), usage='%(prog)s', add_help=True)
        self.parser.add_argument('--save_dir', '-s', required=False)
        self.parser.add_argument('--model', '-m', required=True)
        self.parser.add_argument('--ckpt', '-c', required=True)
        self.parser.add_argument('--gpu', action="store_true", default=False)
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        
        
    def execute(self, argv: List) -> bool:
        pprint('begin to convert to onnx')
        args = self.parser.parse_args(argv)
        save_dir = self.cur_path if args.save_dir is None else args.save_dir
        assert os.path.exists(args.model) and os.path.exists(args.ckpt)
        
        model_name = os.path.basename(args.model)
        model_dir = os.path.dirname(args.model)
        model_basename = os.path.basename(model_dir)
        # sys.path.append(model_dir)
        import importlib.util
        spec = importlib.util.spec_from_file_location(model_basename, os.path.join(model_dir, '__init__.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module 
        spec.loader.exec_module(module)

        MODLE = import_module('{}.{}'.format(model_basename, model_name.replace('.py', '')))
        import torch
        device = 'cuda:0' if args.gpu and torch.cuda.is_available() else 'cpu'
        # print(model_dir, module, spec.name, MODLE, args.gpu, device)
        
        ARGS = import_module('{}.args'.format(model_basename))

        model = MODLE.make_model(ARGS.args).to(device)
        state_dicts = torch.load(args.ckpt, map_location=device)
        model.load_state_dict(state_dicts)
        print('load model success.')
        
        
        # patch_size = 224
        # dummy_input = Variable(torch.randn(1, 3, patch_size, patch_size)).cuda()
        # # dummy_input.to('cuda:1')
        # onnx_filename = "new_edsr.onnx"
        # torch.onnx.export(model, dummy_input,onnx_filename,verbose=True)
        
        
        # print(model)
        return True

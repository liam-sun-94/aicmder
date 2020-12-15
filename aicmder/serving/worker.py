from multiprocessing import Process
import aicmder as cmder
import json
class Worker(Process):
    
    
    def __init__(self, module_info, device_id='cpu', **kwargs):
        super(Worker, self).__init__()
        self.module_info = json.loads(module_info) if type(module_info) == str else module_info
        self.device_id = device_id
        self.kwargs = kwargs
        
        module_name = cmder.ModuleDefine.ModuleName.str()
        self.module = self.module_info[module_name] or self.kwargs.get(module_name)
        assert self.module is not None

        init_args = module_info.get('init_args', {})
        init_args.update({'name': self.module})
        module = cmder.Module(**init_args)
        
        print(module)
        
    def run(self) -> None:
        return super().run()
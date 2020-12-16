from multiprocessing import Process
import aicmder as cmder
import json
class Worker(Process):
    
    
    def __init__(self, module_infos, device_id='cpu', **kwargs):
        super(Worker, self).__init__()
        self.module_infos = json.loads(module_infos) if type(module_infos) == str else module_infos
        self.device_id = device_id
        self.kwargs = kwargs
        

        for module_name, module_info in self.module_infos.items():
            print(module_name, module_info)
        
        # self.module = self.module_info[module_name] or self.kwargs.get(module_name)
        # assert self.module is not None
            init_args = module_info.get('init_args', {})
            init_args.update({'name': module_info['name']})
            module = cmder.Module(**init_args)
            method_name = module.serving_func_name
            serving_method = getattr(module, method_name)

            serving_method()
        
    def run(self) -> None:
        return super().run()
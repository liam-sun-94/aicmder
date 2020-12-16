
from enum import Enum


class ModuleDefine(Enum):
    
    ModuleName = 'name'
    ModuleMethod = 'serving_method'
    ModuleParams = 'serving_args'
    ModuleInitArgs = 'init_args'
    DeviceId = 'device_id'
    
    def str(self):
        return self.value
    
if __name__ == "__main__":
    print(ModuleDefine.ModuleName.str())
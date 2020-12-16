
from enum import Enum


class ModuleDefine(Enum):
    
    ModuleName = 'name'
    ModuleMethod = 'serving_method'
    def str(self):
        return self.value
    
if __name__ == "__main__":
    print(ModuleDefine.ModuleName.str())
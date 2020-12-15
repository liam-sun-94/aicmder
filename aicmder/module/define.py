
from enum import Enum


class ModuleDefine(Enum):
    
    ModuleName = 'name'
    
    def str(self):
        return self.value
    
if __name__ == "__main__":
    print(Module.ModuleName.str())
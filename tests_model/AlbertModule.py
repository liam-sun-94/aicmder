import aicmder as cmder
from aicmder.module.module import serving, moduleinfo

@moduleinfo(name='albert')
class Albert(cmder.Module):
    
    def __init__(self, dummpy_params, **kwargs):
        self.dummpy_params = dummpy_params
    
    @serving
    def predict(self):
        str = '123'
        import time
        time.sleep(1)
        return 'hello world' + self.dummpy_params + ' {}'.format(str)
        
        
        
class Foo:
    
    def test():
        pass
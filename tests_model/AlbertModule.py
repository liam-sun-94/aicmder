import aicmder as cmder
from aicmder.module.module import serving, moduleinfo

@moduleinfo(name='albert')
class Albert(cmder.Module):
    @serving
    def predict(self):
        import time
        time.sleep(1)
        return 'hello world'
        
        
        
class Foo:
    
    def test():
        pass
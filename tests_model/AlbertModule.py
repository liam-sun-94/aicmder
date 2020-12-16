import aicmder as cmder
from aicmder.module.module import serving, moduleinfo

@moduleinfo(name='albert')
class Albert(cmder.Module):
    @serving
    def predict(self):
        print('hello')
        
        
        
class Foo:
    
    def test():
        pass
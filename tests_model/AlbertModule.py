import aicmder as cmder
from aicmder.module.module import serving, moduleinfo

@moduleinfo(name='albert')
class AlbertModule(cmder.Module):
    @serving
    def predict(self):
        print('hello')
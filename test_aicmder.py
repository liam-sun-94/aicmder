import unittest
import aicmder as cmder
import time

class TestCommands(unittest.TestCase):

    def test_worker(self):
        worker = cmder.Worker(
            {'albert': {'name': 'tests_model/AlbertModule'}})
        worker.start()

    # def test_help(self):
    #     print(cmder)
    #     help = cmder.help.HelpCommand()
    #     help.execute(['onnx'])

    # def test_init(self):
    #     init = cmder.init.InitCommand()
    #     init.execute([])

    # def test_onnx(self):
    #     print(cmder)
    #     onnx = cmder.onnx.ONNXCommand()
    #     # onnx.execute(['-s', './save'])
    #     onnx.execute(['-s', 'output', '-m', '/Users/faith/AI_Commander/model/edsr.py',
    #                   '-c', '/Users/faith/AI_Commander/edsr_baseline_x4-6b446fab.pt'])

    # def test_init(self):
    #     init = cmder.pb.PbCommand()
    #     init.execute(['-o', 'output/export.onnx'])


def test_worker():
    predict_params = {'str': '123'}
    worker = cmder.Worker(
        {'albert': {'name': 'tests_model/AlbertModule', 'serving_args': predict_params, 'init_args': {'dummpy_params': 'dummpy'}}})
    worker.start()
    queue = cmder.ServerQueue()
    queue.start()
    queue.join()
    worker.join()


def test_PPworker():
    worker = cmder.PPworker()
    worker.start()
    
def test_func(*args, **kwargs):
    print(args, *args)
    print(kwargs)


if __name__ == "__main__":
    d = {'c': 123, 'd': 123}
    test_func({'a': 123, 'b': 123}, **d)
    # test_worker()
    # unittest.main()

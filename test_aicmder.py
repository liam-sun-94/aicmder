from multiprocessing.context import Process
import unittest
import aicmder as cmder
import time, json 

class MyProcess(Process):
    
    def run(self) -> None:
        import time
        while True:
            print('hello')
            time.sleep(1)
class TestCommands(unittest.TestCase):

    def test_worker(self):
        worker = cmder.Worker(
            {'albert': {'name': 'tests_model/AlbertModule'}})
        worker.start()

    # def test_process(self):
    #     worker = MyProcess()
    #     worker.start()
        
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
    workers = []
    config = {'albert': {'name': 'tests_model/AlbertModule', 'init_args': {'dummpy_params': 'dummpy'}}}
    device_map = ["cpu" for i in range(5)]
    for idx, device_id in enumerate(device_map):
        worker = cmder.Worker(config, device_id=device_id)
        workers.append(worker)
        worker.start()
    for worker in workers:
        worker.is_ready.wait()
    queue = cmder.ServerQueue()
    queue.start()
    queue.join()
    


def test_PPworker():
    worker = cmder.PPworker()
    worker.start()
    
def test_func(*args, **kwargs):
    print(args, *args)
    print(kwargs)

def test_albert():
    from tests_model.AlbertModule import Albert   
    albert = Albert(**{'dummpy_params': 'dummpy'})
    print(albert.predict('今天吃饭了吗'))
    
def test_serving():
    print(cmder)
    config = {'albert': {'name': 'tests_model/AlbertModule', 'init_args': {'dummpy_params': 'dummpy'}}}
    serve = cmder.serve.ServeCommand()
    serve.execute(['-w', '5', '-c', json.dumps(config), '-p', '8080', '--max_connect', '10'])

def test_process():
    worker = MyProcess()
    worker.start()

if __name__ == "__main__":
    # d = {'c': 123, 'd': 123}
    # test_func({'a': 123, 'b': 123}, **d)
    # test_worker()
    # test_albert()
    # unittest.main()
    # test_process()
    test_serving()

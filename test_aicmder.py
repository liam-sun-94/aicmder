from multiprocessing.context import Process
import unittest
import aicmder as cmder
import time, json 
from termcolor import colored
import sqlite3
class MyProcess(Process):
    
    def run(self) -> None:
        import time
        while True:
            print('hello')
            time.sleep(1)
class TestCommands(unittest.TestCase):

    # def test_worker(self):
    #     worker = cmder.Worker(
    #         {'albert': {'name': 'tests_model/AlbertModule'}})
    #     worker.start()
    
    def test_stop(self):
        print(cmder)
        stop = cmder.stop.StopCommand()
        stop.execute([])

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
    device_map = ["cpu" for i in range(2)]
    logger = cmder.Common.set_logger(colored('WORKER-%d' % 1, 'yellow'), True)
    for idx, device_id in enumerate(device_map):
        worker = cmder.Worker(config, logger, device_id=device_id)
        workers.append(worker)
        worker.start()
    for worker in workers:
        worker.is_ready.wait()
    queue = cmder.ServerQueue()
    queue.start()
    queue.join()
    

def test_single_worker():
    config = {'chatbot': {'name': 'tests_model/ChatbotModule', 'init_args': {'file_path': '/Users/faith/AI_Commander/tests_model/config.yaml'}}}
    logger = cmder.Common.set_logger(colored('WORKER-%d' % 1, 'yellow'), True)
    worker = cmder.Worker(config, logger, device_id=-1)
    worker.run()

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
    serve.execute(['-w', '2', '-c', json.dumps(config), '-p', '8080', '--max_connect', '10'])
    
def test_chatbot():
    print(cmder)
    config = {'chatbot': {'name': 'tests_model/ChatbotModule', 'init_args': {'file_path': './tests_model/config.yaml'}}}
    serve = cmder.serve.ServeCommand()
    serve.execute(['-w', '1', '-c', json.dumps(config), '-p', '8099', '--max_connect', '5'])

def test_process():
    worker = MyProcess()
    worker.start()

def test_execute():
    from aicmder.commands.utils import execute
    execute()

def test_write_community():
    conn = sqlite3.connect('/Users/faith/wechat_admin/db.sqlite3')
    c = conn.cursor()
    # 'select name from wechat_community'
    sql = 'select name from wechat_school'
    c.execute(sql)
    
    ret = c.fetchall()
    conn.close()
    print(len(ret), type(ret))
    communiy = set(ret)
    print(len(communiy))
    
    with open('c.txt', 'w+') as f:
        for commu in communiy:
            c = commu[0]
    #         s = '''    select ws.name, c.name  from wechat_communitytoschool s, wechat_community c, wechat_school ws where c.name like '{}' and s.communityId_id = c.communityId and ws.schoolId = s.schoolId:
    #   - {}的学区房\n'''.format(c, c)
    #         s = '''    select description from wechat_school where name = '{}':
    #   - {}怎么样
    #   - {}如何\n'''.format(c,c,c)
            s = '''    SELECT name from wechat_community where communityId in (SELECT communityId_id from wechat_communitytoschool where schoolId in ( SELECT schoolId from wechat_school where name = '{}' )):
      - {}的学区房\n'''.format(c, c)
            f.writelines(s)
            
    
        
if __name__ == "__main__":
    # d = {'c': 123, 'd': 123}
    # test_func({'a': 123, 'b': 123}, **d)
    # test_single_worker()
    # test_albert()
    # unittest.main()
    # test_process()
    # test_serving()
    test_chatbot()
    # test_write_community()
    # test_execute()

# from multiprocessing import Process
# import multiprocessing
import aicmder as cmder
import json
from aicmder.service.PPpolicy import *
from random import randint
import time
import zmq
import datetime, json, sys, os
def worker_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    worker = context.socket(zmq.DEALER) # DEALER
    identity = b"%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
    worker.setsockopt(zmq.IDENTITY, identity)
    poller.register(worker, zmq.POLLIN)
    worker.connect("tcp://localhost:5556")
    worker.send(PPP_READY)
    return worker

ModuleName = cmder.ModuleDefine.ModuleName.str()
ModuleMethod = cmder.ModuleDefine.ModuleMethod.str()
ModuleInitArgs = cmder.ModuleDefine.ModuleInitArgs.str()
ModuleParams = cmder.ModuleDefine.ModuleParams.str()
DeviceId = cmder.ModuleDefine.DeviceId.str()
class Worker:
    
    
    def __init__(self, module_infos, device_id=-1, **kwargs):
        super(Worker, self).__init__()
        if type(module_infos) == dict:
            self.module_infos = module_infos
        else:
            self.module_infos = json.loads(module_infos) if type(module_infos) == str else module_infos
        self.device_id = device_id
        self.kwargs = kwargs
        assert len(self.module_infos) > 0
        self.serving_methods = {}

        for module_name, module_info in self.module_infos.items():
            print(module_name, module_info)
            
            init_args = module_info.get(ModuleInitArgs, {})
            init_args.update({ModuleName: module_info[ModuleName], DeviceId: self.device_id})
            init_args.update(module_info[ModuleInitArgs])
            
            module = cmder.Module(**init_args)
            method_name = module.serving_func_name
            serving_method = getattr(module, method_name)
            # serving_args = module_info.get(ModuleParams, {})
            self.serving_methods[module_name] = {ModuleName: module_info[ModuleName], ModuleMethod: serving_method}
        # self.is_ready = multiprocessing.Event()
        
        
    def run(self):    
        context = zmq.Context(1)
        poller = zmq.Poller()

        liveness = HEARTBEAT_LIVENESS
        interval = INTERVAL_INIT
        # self.is_ready.set()
        heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        print("{} is ready!".format(os.getpid()))
        worker = worker_socket(context, poller)
        while True:
            socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

            # Handle worker activity on backend
            if socks.get(worker) == zmq.POLLIN:
                #  Get message
                #  - 3-part envelope + content -> request
                #  - 1-part HEARTBEAT -> heartbeat
                frames = worker.recv_multipart()
                if not frames:
                    break # Interrupted

                if len(frames) == 3:
                    module = self.serving_methods['albert']
                    serving_args = frames[len(frames) - 1].decode()
                    serving_args_dict = json.loads(serving_args)

                    frames[len(frames) - 1] = module[ModuleMethod](**serving_args_dict).encode()
                    print("I: Normal reply")
                    worker.send_multipart(frames)
                    liveness = HEARTBEAT_LIVENESS
                    
                elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
                    # print("I: Queue heartbeat", datetime.datetime.now())
                    liveness = HEARTBEAT_LIVENESS
                else:
                    print("E: Invalid message: %s" % frames)
                interval = INTERVAL_INIT
            else:
                liveness -= 1
                if liveness == 0:
                    print("W: Heartbeat failure, can't reach queue")
                    print("W: Reconnecting in %0.2fs..." % interval)
                    time.sleep(interval)

                    if interval < INTERVAL_MAX:
                        interval *= 2
                    poller.unregister(worker)
                    worker.setsockopt(zmq.LINGER, 0)
                    worker.close()
                    worker = worker_socket(context, poller)
                    liveness = HEARTBEAT_LIVENESS
            if time.time() > heartbeat_at:
                heartbeat_at = time.time() + HEARTBEAT_INTERVAL
                # print("I: Worker heartbeat", datetime.datetime.now())
                worker.send(PPP_HEARTBEAT)
                
if __name__ == "__main__":
    # config = {'albert': {'name': 'tests_model/AlbertModule', 'init_args': {'dummpy_params': 'dummpy'}}}
    argv = sys.argv
    assert len(argv) >= 3
    config = json.loads(argv[1])
    device_id = int(argv[2])
    worker = Worker(config, device_id)
    worker.run()
from multiprocessing import Process
import aicmder as cmder
import json
from aicmder.service.PPpolicy import *
from random import randint
import time
import zmq

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
class Worker(Process):
    
    
    def __init__(self, module_infos, device_id='cpu', **kwargs):
        super(Worker, self).__init__()
        self.module_infos = json.loads(module_infos) if type(module_infos) == str else module_infos
        self.device_id = device_id
        self.kwargs = kwargs
        
        self.context = zmq.Context(1)
        self.poller = zmq.Poller()
        # start connections
        self.worker = worker_socket(self.context, self.poller)
        
        # for module_name, module_info in self.module_infos.items():
        #     print(module_name, module_info)
        
        # # self.module = self.module_info[module_name] or self.kwargs.get(module_name)
        # # assert self.module is not None
        #     init_args = module_info.get('init_args', {})
        #     init_args.update({'name': module_info['name']})
        #     module = cmder.Module(**init_args)
        #     method_name = module.serving_func_name
        #     serving_method = getattr(module, method_name)

        #     serving_method()
        
    def run(self):    
        context = zmq.Context(1)
        poller = zmq.Poller()

        liveness = HEARTBEAT_LIVENESS
        interval = INTERVAL_INIT

        heartbeat_at = time.time() + HEARTBEAT_INTERVAL

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
                    print("I: Normal reply")
                    worker.send_multipart(frames)
                    liveness = HEARTBEAT_LIVENESS
                    time.sleep(1)  # Do some heavy work
                elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
                    print("I: Queue heartbeat")
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
                print("I: Worker heartbeat")
                worker.send(PPP_HEARTBEAT)
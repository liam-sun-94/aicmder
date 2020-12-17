from multiprocessing import Process, Event
from collections import OrderedDict
import time
from aicmder.service.PPpolicy import *
import zmq
import datetime

class Worker(object):
    def __init__(self, address):
        self.address = address
        self.expiry = time.time() + HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS

class WorkerQueue(object):
    def __init__(self):
        self.queue = OrderedDict()

    def ready(self, worker):
        # print('I: worker: {} ready, the address is {}'.format(worker, worker.address), datetime.datetime.now())
        self.queue.pop(worker.address, None)
        self.queue[worker.address] = worker

    def purge(self):
        """Look for & kill expired workers."""
        t = time.time()
        expired = []
        for address, worker in self.queue.items():
            if t > worker.expiry:  # Worker expired
                expired.append(address)
        for address in expired:
            self.queue.pop(address, None)
            print("W: Idle worker expired: {}, remaining worker: {}".format(address, len(self.queue)), datetime.datetime.now())

    def next(self):
        address, worker = self.queue.popitem(False)
        return address


class ServerQueue(Process):
    
    def __init__(self):
        super(ServerQueue, self).__init__()
        self.is_ready = Event()
    
    def run(self):
        context = zmq.Context(1)

        frontend = context.socket(zmq.ROUTER) # ROUTER
        backend = context.socket(zmq.ROUTER)  # ROUTER
        frontend.bind("tcp://*:5555") # For clients
        backend.bind("tcp://*:5556")  # For workers

        poll_workers = zmq.Poller()
        poll_workers.register(backend, zmq.POLLIN)

        poll_both = zmq.Poller()
        poll_both.register(frontend, zmq.POLLIN)
        poll_both.register(backend, zmq.POLLIN)

        workers = WorkerQueue()
        self.is_ready.set()
        heartbeat_at = time.time() + HEARTBEAT_INTERVAL

        while True:
            if len(workers.queue) > 0:
                poller = poll_both
            else:
                poller = poll_workers
            socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

            # Handle worker activity on backend
            if socks.get(backend) == zmq.POLLIN:
                # Use worker address for LRU routing
                frames = backend.recv_multipart()
                if not frames:
                    # can not break, waiting
                    continue
                    # break 

                address = frames[0]
                workers.ready(Worker(address))

                # Validate control message, or return reply to client
                msg = frames[1:]
                if len(msg) == 1:
                    if msg[0] not in (PPP_READY, PPP_HEARTBEAT):
                        print("E: Invalid message from worker: %s" % msg)
                else:
                    # print("I: Sending message to client: %s" % msg)
                    frontend.send_multipart(msg)

                # Send heartbeats to idle workers if it's time
                if time.time() >= heartbeat_at:
                    for worker in workers.queue:
                        msg = [worker, PPP_HEARTBEAT]
                        backend.send_multipart(msg)
                    heartbeat_at = time.time() + HEARTBEAT_INTERVAL
            if socks.get(frontend) == zmq.POLLIN:
                frames = frontend.recv_multipart()
                if not frames:
                    # break
                    continue

                frames.insert(0, workers.next())
                backend.send_multipart(frames)


            workers.purge()
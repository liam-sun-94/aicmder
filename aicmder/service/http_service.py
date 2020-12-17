from multiprocessing import Process, Event
import logging
import zmq
import sys
from termcolor import colored
import json
# from .helper import set_logger
from aicmder.common import set_logger, LOG_VERBOSE

# 8s for timeout
REQUEST_TIMEOUT = 8000  
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

verbose = LOG_VERBOSE
logging = set_logger(colored('SERVER_QUEUE', 'magenta'), verbose)


class Client:

    def __init__(self) -> None:
        self.context = zmq.Context()

        logging.info("Connecting to server…")
        self.client = self.context.socket(zmq.REQ)
        self.client.connect(SERVER_ENDPOINT)

    def send_request(self, request):
        self.client.send(request)

        retries_left = REQUEST_RETRIES
        while True:
            
            if (self.client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                reply = self.client.recv()
                # logging.info("Server replied msg (%s)", reply.decode())
                return reply
            
            retries_left -= 1
            logging.warning("No response from server")
            # Socket is confused. Close and remove it.
            self.client.setsockopt(zmq.LINGER, 0)
            self.client.close()
            if retries_left == 0:
                logging.error("Server seems to be offline, abandoning")
                raise Exception("Server seems to be offline, abandoning")
                # sys.exit()

            logging.info("Reconnecting to server…")
            # Create new connection
            self.client = self.context.socket(zmq.REQ)
            self.client.connect(SERVER_ENDPOINT)
            logging.info("Resending (%s)", request)
            self.client.send(request)

    def close(self):
        """
            Gently close all connections of the client. 
        """
        self.client.close()
        self.context.term()

class BCManager():
    def __init__(self, available_bc):
        self.available_bc = available_bc
        self.bc = None

    def __enter__(self):
        self.bc = self.available_bc.pop()
        return self.bc

    def __exit__(self, *args):
        self.available_bc.append(self.bc)

class ConcurrentClient:

    def __init__(self, max_concurrency = 500) -> None:
        self.max_concurrency = max_concurrency
        self.available_bc = [Client() for _ in range(max_concurrency)]
        
    def send_request(self, request):
        with BCManager(self.available_bc) as bc:
            return bc.send_request(request)
  

    def close(self):
        for bc in self.available_bc:
            bc.close()


class HTTPProxy(Process):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.is_ready = Event()

    def create_fastapi_app(self):

        from fastapi import FastAPI, Request
        from flask_json import JsonError

        app = FastAPI()

        # logger = set_logger(colored('PROXY', 'red'), self.args.verbose)

        # @app.get('/status/server')
        # def get_server_status():
        #     return bc.server_status

        # @app.get('/status/client')
        # def get_client_status():
        #     return bc.status

        @app.post('/predict')
        def predict(data: dict, request: Request):
            # data = request.form if request.form else request.json
            try:
                logging.debug(request, data)
                json_str = json.dumps(data)
                # logger.info('new request from %s' % request.client.host)
                result = self.concurrent.send_request(json_str.encode())
                return result
            except Exception as e:
                print(e)
                # logger.error('error when handling HTTP request', exc_info=True)
                raise JsonError(description=str(e), type=str(type(e).__name__))

        return app

    def run(self):
        import uvicorn
        app = self.create_fastapi_app()
        self.concurrent = ConcurrentClient(max_concurrency = self.args.max_connect)
        self.is_ready.set()
        uvicorn.run(app, host="0.0.0.0", port=self.args.http_port)

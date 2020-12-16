import zmq

LRU_READY = "\x01"

context = zmq.Context(1)

frontend = context.socket(zmq.ROUTER) # ROUTER
backend = context.socket(zmq.DEALER) # DEALER
frontend.bind("tcp://*:5555") # For clients
backend.bind("tcp://*:5556")  # For workers

zmq.device(zmq.QUEUE, frontend, backend)


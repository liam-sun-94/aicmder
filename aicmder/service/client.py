#
#  Lazy Pirate client
#  Use zmq_poll to do a safe request-reply
#  To run, start lpserver and then randomly kill/restart it
#
#   Author: Daniel Lundin <dln(at)eintr(dot)org>
#
import itertools
import logging
import sys
import zmq
import time, json
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# 3s for timeout
REQUEST_TIMEOUT = 10000 #2500 
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

context = zmq.Context()

logging.info("Connecting to server…")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

def send_request(client, request):
    client.send(request)

    retries_left = REQUEST_RETRIES
    while True:
        
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            reply = client.recv()
            logging.info("Server replied msg (%s)", reply.decode())
            return reply
        
        retries_left -= 1
        logging.warning("No response from server")
        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()
        if retries_left == 0:
            logging.error("Server seems to be offline, abandoning")
            sys.exit()

        logging.info("Reconnecting to server…")
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect(SERVER_ENDPOINT)
        logging.info("Resending (%s)", request)
        client.send(request)

for sequence in itertools.count():
    sequence = {'str': '今天吃饭了吗'}
    sequence = json.dumps(sequence)
    request = sequence.encode()
    logging.info("Sending (%s)", request)
    send_request(client, request)
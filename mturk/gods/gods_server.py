import logging
import traceback
import json
import time
import uuid
import threading
from SocketServer import ThreadingMixIn
import BaseHTTPServer

logger = logging.getLogger(__name__)

HOST_NAME = 'localhost'
PORT_NUMBER = 22222


class ResponseCollectionServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def _process_response(self, conversation_id, response_payload):
        context_id = response_payload['id']
        user_response = response_payload['data']
        self.server.gods_system.agent.accept_response(conversation_id, context_id, user_response)

    def _get_next_context(self, conversation_id):
        return self.server.gods_system.input_device.request_context(conversation_id)

    def _process_request(self, json_payload):
        if 'conversation_id' not in json_payload:
            return None
        conversation_id = json_payload['conversation_id']

        response = json_payload['response']
        if response: # If there exists a response
            self._process_response(conversation_id, response)

        result = {}
        if 'context' in json_payload: # Request for a new context
            next_context = self._get_next_context(conversation_id)
            result = {
                'context' : {
                    'id' : next_context.context_id,
                    'data' : next_context.data
                }
            }

        print "Returning {}".format(result)
        return result

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        print self.server.gods_system
        self.send_response(400)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Not supported.</title></head>")
        self.wfile.write("<body><p>Not supported.</p>")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def do_POST(self):
        """Respond to a POST request."""
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        json_payload = json.loads(data_string)

        try:
            result = self._process_request(json_payload)
            # result = {'result' : 'sample_result'}
            status_code = 200
        except:
            result = traceback.format_exc()
            logger.warning(result)
            status_code = 500

        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result))

class ScoringServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def _process_request(self, json_payload):
        print "Request: {}".format(json_payload)

        if 'conversation_id' not in json_payload:
            return None
        conversation_id = json_payload['conversation_id']
        returned_object = {}

        if 'context' in json_payload and json_payload['context']:
            data = json_payload['context']
            new_context = data['data']

            event = threading.Event(0)
            new_id = self.server.gods_system.input_device.accept_context(conversation_id, new_context)
            self.server.gods_system.output_device.register_response_event(new_id, event)
            event.wait(10)
            response = self.server.gods_system.output_device.get_response(new_id)

            returned_object['response'] = {
                'id' : new_id,
                'data' : response.data if hasattr(response, 'data') else response
            }

        if 'scoring' in json_payload and json_payload['scoring']:
            data = json_payload['scoring']
            response_id = data['id']
            response_score = data['score']
            self.server.gods_system.input_device.accept_score(conversation_id, response_id, response_score)

            returned_object['scoring'] = { 'status' : 'success' }

        print "Returning %s" % returned_object
        return returned_object if len(returned_object) > 0 else None

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        print self.server.gods_system
        self.send_response(400)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Not supported.</title></head>")
        self.wfile.write("<body><p>Not supported.</p>")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def do_POST(self):
        """Respond to a POST request."""
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        json_payload = json.loads(data_string)

        try:
            result = self._process_request(json_payload)
            # result = {'result' : 'sample_result'}
            status_code = 200
        except:
            result = traceback.format_exc()
            logger.warning(result)
            status_code = 500

        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result))

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""
    pass

def main(server_implementation_class, gods_system):
    logger.info('Initializing gods server.')

    # server_class = BaseHTTPServer.HTTPServer
    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), server_implementation_class)
    httpd.gods_system = gods_system

    logger.info("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Caught interrupt signal. Terminating...")
    httpd.server_close()
    logger.info("Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

def main_response(gods_system):
    main(ResponseCollectionServer, gods_system)

def main_scoring(gods_system):
    main(ScoringServer, gods_system)

if __name__ == '__main__':
    main(None)
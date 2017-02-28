import logging
import traceback
import json
import time
import uuid
from SocketServer import ThreadingMixIn
import BaseHTTPServer

logger = logging.getLogger(__name__)

HOST_NAME = 'localhost'
PORT_NUMBER = 22222


class GodsServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def _process_response(self, response_payload):
        context_id = response_payload['id']
        user_response = response_payload['data']
        self.server.gods_system.agent.accept_response(context_id, user_response)

    def _get_next_context(self):
        return self.server.gods_system.input_device.request_context()

    def _process_request(self, json_payload):
        response = json_payload['response']
        if response: # If there exists a response
            self._process_response(response)

        result = {}
        if 'context' in json_payload: # Request for a new context
            next_context = self._get_next_context()
            result = {
                'context' : next_context
            }


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

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""
    pass

def main(gods_system):
    logger.info('Initializing gods server.')

    # server_class = BaseHTTPServer.HTTPServer
    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), GodsServer)
    httpd.gods_system = gods_system

    logger.info("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Caught interrupt signal. Terminating...")
    httpd.server_close()
    logger.info("Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

if __name__ == '__main__':
    main(None)
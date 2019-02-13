# -*- coding: utf-8 -*-


from .context import services
import threading
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
import json, socket

import unittest
import sys

class StatesHTTPRequestTestSuite(unittest.TestCase):


    def test_states_request(self):
        server = HTTPServer((socket.gethostbyname(socket.gethostname()), 12345), services.http.server.StatesHTTPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        # Also tried this:
        # server_thread.setDaemon(True)
        server_thread.start()
        # Wait a bit for the server to come up
        time.sleep(5)
        self.states=json.loads(urlopen("http://"+socket.gethostname()+":12345/states").read())
        print(self.states)



if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-


from .context import services
import threading
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from urllib import request, parse
import json

from shapely.geometry import Point, Polygon
import unittest


class StateEndpointHTTPRequestTestSuite(unittest.TestCase):


    def test_endpoint_request(self):
        server = HTTPServer(("127.0.0.1", 9090), services.http.server.StatesHTTPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        # Also tried this:
        # server_thread.setDaemon(True)
        server_thread.start()
        # Wait a bit for the server to come up
        time.sleep(3)

        endpoint_server = HTTPServer(("127.0.0.1", 8080), services.http.endpoint.StateEndpointHTTPRequestHandler)
        endpoint_server_thread = threading.Thread(target=endpoint_server.serve_forever)
        endpoint_server_thread.start()

        time.sleep(3)

        # Test GET
        print(urlopen("http://localhost:8080/?longitude=-77.036133&latitude=40.513799").read().decode())

        #Test POST
        post_data = parse.urlencode({"longitude":-77.036133,"latitude":40.513799}).encode()
        req = request.Request("http://localhost:8080", data = post_data)  # this will make the method "POST"
        resp = request.urlopen(req)
        print(resp.read().decode())

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3.7

import sys, getopt, json, socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from shapely.geometry import Point, Polygon

from urllib.parse import urlparse,parse_qs
from urllib.request import urlopen




class StateEndpointHTTPRequestHandler(BaseHTTPRequestHandler):

    states=None

    def _set_headers(self, response_code=200, content_type='application/json'):
        '''
        set  headers
        :param response_code: http response code, default to 200
        :param content_type: http response content type. default to applicaiton/json
        :return: None
        '''
        self.send_response(response_code)
        self.send_header('Content-type', content_type)
        self.end_headers()


    def do_GET(self):
        '''
        GET: /?longitude=-77.036133&latitude=40.513799
        :return: ["Pennsylvania"]
        '''
        try:
            # parse the url path to get the query string
            query_string = urlparse(self.path).query

            # get the states in json that contain the given longtitude and latitude
            json_response = self.find_states_response(query_string=query_string)

            # initializes the headers for the response
            self._set_headers(200, 'application/json')

            self.wfile.write(json_response.encode())

        except (KeyError,ValueError)  as kvErr:
            self._set_headers(500, 'text/html')
            self.wfile.write("Key or Value Error: Please validate the query string")
            print("Error message:", kvErr)

        except TypeError as typeErr:
            self._set_headers(500, 'text/html')
            self.wfile.write("Type Error happened in the server side.")
            print("Type error:", typeErr)

        except:
            self._set_headers(500, 'text/html')
            self.wfile.write("Unexpected Error happened in the server side")
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def do_POST(self):
        '''
        POST: curl  -d "longitude=-77.036133&latitude=40.513799" http://localhost:8080/
        :return: ["Pennsylvania"]
        '''


        try:
            # get the content length of the POST request
            content_length = self.headers['content-length']

            # type cast the content length to integer
            length = int(content_length) if content_length else 0

            # read the content of the request and decode
            query_string=self.rfile.read(length).decode('utf-8')

            # get the states in json that contain the given longtitude and latitude
            json_response = self.find_states_response(query_string=query_string)

            # initializes the headers for the response
            self._set_headers(200, 'application/json')

            self.wfile.write(json_response.encode())

        except (KeyError, ValueError)  as kvErr:
            self._set_headers(500, 'text/html')
            self.wfile.write("Key or Value Error: Please validate the query string")
            print("Error message:", kvErr)

        except TypeError as typeErr:
            self._set_headers(500, 'text/html')
            self.wfile.write("Type Error Occurred at Server")
            print("Type error:", typeErr)

        except:
            self._set_headers(500, 'text/html')
            self.wfile.write("Unexpected Error Occurred at Server")
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def find_states_response(self, query_string=None):
        if query_string is None:
            return json.dumps({})

        # parse the query string into a dictionary
        query_dict = parse_qs(query_string)

        # convert to float, if the key is not present or any error in the query string then KeyError is raised
        longitude = float(query_dict['longitude'][0])
        latitude = float(query_dict['latitude'][0])

        # get those states in list that contain the given longtitude and latitude
        contained_states = self.find_states(longitude=longitude, latitude=latitude)

        return json.dumps(contained_states)


    def query_states(self):
        '''
        query the states services "/states" to get the states list with border definitions
        :return: cache the dictionary of states in the format {["state_ame":[[],[],...],...} with state name as the key and border points as the value array
        '''
        if StateEndpointHTTPRequestHandler.states is None:
            StateEndpointHTTPRequestHandler.states = json.loads(json.loads(urlopen("http://localhost:9595/states").read()).replace("'", "\""))
        return StateEndpointHTTPRequestHandler.states


    def find_states(self, longitude=None, latitude=None):
        '''
        Checking the giving longtitude and latitude to find which state or states it belongs to.
        :param longitude: the longtitude of the giving point
        :param latitude: the latitude of the giving point
        :return: list of the states the giving point belongs to
        '''

        # return empty list if the longtitude or latitude is not defined
        if longitude is None or latitude is None:
            return []
        location = Point(longitude, latitude)

        # The states list the giving point belongs to
        contained_states = []

        # load it with the states list by calling the states services.
        # It is not necessary to cache the states in class variable or instance level because each request will create a new handler instance.
        json_states=self.query_states()

        for state_name, state_json in json_states.items():
            state_polygon = Polygon(state_json)
            # if the polygon contains or touches the giving point, add the state name to the result list
            if state_polygon.contains(location) or location.touches(state_polygon):
                contained_states.append(state_name)

        return contained_states



def run(server_class=HTTPServer, handler_class=StateEndpointHTTPRequestHandler, port=8080):
    '''
    Starts the HTTPServer with StateEndpointHTTPRequestHandler at the given port (default: 8080)
    '''
    server_address = ("0.0.0.0", port)
    http_server = server_class(server_address, handler_class)
    print('Starting Endpoint HTTP server...')
    http_server.serve_forever()

if __name__ == '__main__':
    '''
    Run this python script
    '''
    if len(sys.argv) > 1 and type(sys.argv[1]) == type(int):
        run(port=int(sys.argv[1]))
    else:
        run()

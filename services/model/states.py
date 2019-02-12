#!/usr/bin/env python3.7

import sys, os, json

# This class reads the content from the data file "states.json" and return as Json Object.
class States:

    def __init__(self, states_filename='states.json'):
        '''
        class initialization
        :param states_filename: json file that contains the states information - name, border points
        '''
        self.states = {}
        self.initialize(states_filename=states_filename)

    def initialize(self, states_filename = None):
        '''
        initializing States dictionary with the giving state json data file
        :param states_filename:
        :return: States dictionary with
                key - state name
                value - list of the border points
        '''

        # return and do nothing if states_filename is None
        if states_filename is None:
            print("Please provide state json data file, states_filename is None")
            return
        print("Loading state json data to States dictionary...")
        try:
            # open the state json file with the absolute path
            with open(os.path.dirname(os.path.realpath(__file__))+"/"+states_filename) as states_file:
                # read line by line and convert it into json object
                for state in states_file.readlines():
                    state_json = json.loads(state)
                    # key as state's name, value as the list of the it's border points
                    self.states[str(state_json['state'])] = state_json['border']
        except IOError as ioErr:
            print("I/O error({0}): {1}".format(ioErr.errno, ioErr.strerror))
            print("IO error while opening/closing the state json data file:", sys.exc_info()[0])
            print("Unable to initialize the States dictionary")
            sys.exit()


    def to_json(self):
        '''
        convert the dictionary into json
        :return: json object
        '''
        return json.dumps(str(self.states))

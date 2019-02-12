# -*- coding: utf-8 -*-


from .context import services


import unittest


class StatesTestSuite(unittest.TestCase):
    #States test cases

    def test_states(self):
        states=services.model.states.States()
        print(states.to_json())
        #self.assertIsNotNone(actual, 'message')(states.to_json())


if __name__ == '__main__':
    unittest.main()

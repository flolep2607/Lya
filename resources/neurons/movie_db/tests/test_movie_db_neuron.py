import json
import unittest

import mock

from kalliope.core.NeuronModule import MissingParameterException, InvalidParameterException
from kalliope.neurons.movie_db.movie_db import Movie_db


class TestMovieDb(unittest.TestCase):

    def setUp(self):
        self.action="MOVIE"
        self.api_key="kalliokey"
        self.movie = "Matrix"
        self.people = "Keanu Reeves"

    def testMissingParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Movie_db(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # Missing action
        parameters = {
            "api_key": self.api_key,
        }
        run_test(parameters)

        # Missing api_key
        parameters = {
            "action": self.action,
        }
        run_test(parameters)
   
        # missing Movie for ACTION MOVIE
        parameters = {
            "action": self.action,
            "api_key": self.api_key,
        }
        run_test(parameters)

        # missing Movie for ACTION PEOPLE
        parameters = {
            "action": 'PEOPLE',
            "api_key": self.api_key,
        }
        run_test(parameters)

    def testInvalidParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(InvalidParameterException):
                Movie_db(**parameters_to_test)

        # invalid action
        parameters = {
            "action": 'INVALID',
            "api_key": self.api_key,
        }
        run_test(parameters)

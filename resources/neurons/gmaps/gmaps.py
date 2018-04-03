import logging
import googlemaps
from bs4 import BeautifulSoup

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from datetime import datetime

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Gmaps (NeuronModule):
    def __init__(self, **kwargs):
        super(Gmaps, self).__init__(**kwargs)

        # Get parameters form the neuron
        # TODO: allow departure_time and arrival_time to be configurable
        self.configuration = {
            "gmaps_api_key": kwargs.get('gmaps_api_key', None),
            "origin": kwargs.get('origin', None),
            "destination": kwargs.get('destination', None),
            "direction": kwargs.get('direction', False),
            "language": kwargs.get('language', "en"),
            "units": kwargs.get('units', 'metric'),
            "mode": kwargs.get('mode', 'driving'),
            "traffic_model": kwargs.get('traffic_model', "best_guess"),
            "search": kwargs.get('search', None)
        }

        # Check parameters:
        if self._is_parameters_ok():
            # TODO: handle exceptions and errors 

            self.gmaps = googlemaps.Client(key=self.configuration['gmaps_api_key'])
            response = {
                "status": "KO",
                "distance": 0,
                "time": 0,
                "time_traffic": 0,
                "directions": False
            }

            # If no destination is given, find searched place instead
            if self.configuration['search']:
                self.configuration['destination'] = self._get_place_address(self.configuration['search'])
                response['status'] = "OK"

            if self.configuration['origin'] is not None:
                # re-init status:
                response['status'] == "KO"
                # Calculate destination between origin and distance
                results = self._get_distance()
                if results['status'] == "OK":
                    response['status'] = "OK"
                    # Just the first result is enough:
                    response['time'] = results['rows'][0]['elements'][0]['duration']['text']
                    if 'duration_in_traffic' in results['rows'][0]['elements'][0]:
                        response['time_traffic'] = results['rows'][0]['elements'][0]['duration_in_traffic']['text']
                    response['distance'] = results['rows'][0]['elements'][0]['distance']['text']

                if self.configuration['direction']:
                    # Calculate the direction to go from origin to destination
                    response['directions'] = self._get_directions()

            message = {
                'status': response['status'],
                'origin': self.configuration['origin'],
                'destination': self.configuration['destination'],
                'search': self.configuration['search'],
                'distance': response['distance'],
                'time': response['time'],
                'time_traffic': response['time_traffic'],
                'directions': response['directions']
            }

            logger.debug("message: %s" % message)
            self.say(message)

    def _get_distance(self):
        """
        Return the API results of googlemaps distance matrix API
        :return: the response
        """
        logger.debug('In _get_distance, origin: %s - destination: %s' % (self.configuration['origin'], self.configuration['destination']))
        try:
            now = datetime.now()
            return self.gmaps.distance_matrix(origins = self.configuration['origin'], 
                                                 destinations = self.configuration['destination'], 
                                                 mode = self.configuration['mode'], 
                                                 language = self.configuration['language'], 
                                                 departure_time = now, 
                                                 units = self.configuration['units'], 
                                                 traffic_model = self.configuration['traffic_model'])

        except googlemaps.exceptions.HTTError, googlemaps.exceptions.ApiError:
            return {"status": "KO"}


    def _get_place_address(self, place):
        """
        Return an address based on a name place.
        :return: An address in string format, raise an exception otherwise
        .. raises:: InvalidParameterException
        """
        logger.debug('In _get_place_address: %s' % place)
        results = self.gmaps.places(place, language=self.configuration['language']) 
      
        if results['status'] == "OK":
            # TODO: improve result choice
            # Get first result
            pid = results['results'][0]['place_id']

            results = self.gmaps.place(pid, self.configuration['language'])

            if results['status'] == 'OK':
                return results['result']['formatted_address'] 
        
        raise InvalidParameterException("Google maps couldn't found your place name")

    def _get_directions(self):
        """
        Calculate direction between origin and destination
        :return: a List of direction steps
        .. raises:: InvalidParameterException
        """
        logger.debug('In _get_direction')
        results = self.gmaps.directions(self.configuration['origin'], 
                                        self.configuration['destination'], 
                                        mode = self.configuration['mode'], 
                                        alternatives=False, 
                                        language = self.configuration['language'], 
                                        units = self.configuration['units'])

        directions = []
        for leg in results[0]['legs']:
            for step in leg['steps']:
                directions.append(BeautifulSoup(step['html_instructions'], "html.parser").text)
                if 'steps' in step:
                    for s in step['steps']:
                        if 'html_instructions' in s:
                            directions.append(BeautifulSoup(s['html_instructions'], "html.parser").text)

        return directions

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['gmaps_api_key'] is None:
            raise InvalidParameterException("Google Maps require an API key")

        if self.configuration['destination'] is None and self.configuration['search'] is None:
            raise InvalidParameterException("Google Maps needs a destination or place name")


        return True


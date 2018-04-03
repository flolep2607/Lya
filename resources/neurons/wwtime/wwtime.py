import logging
import googlemaps

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from datetime import datetime
import time

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Wwtime (NeuronModule):
    def __init__(self, **kwargs):
        super(Wwtime, self).__init__(**kwargs)

        # Get parameters form the neuron
        # TODO: allow departure_time and arrival_time to be configurable
        self.configuration = {
            "gmaps_api_key": kwargs.get('gmaps_api_key', None),
            "local": kwargs.get('local', None),
            "city": kwargs.get('city', None)
        }

        # Check parameters:
        if self._is_parameters_ok():
            # TODO: handle exceptions and errors

            tn = time.time()
            message = {'status': "KO"}

            self.gmaps = googlemaps.Client(key=self.configuration['gmaps_api_key'])

            geocode_result = self.gmaps.geocode(self.configuration['local'])
            local_tz = self.gmaps.timezone((geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']), tn)

            geocode_result = self.gmaps.geocode(self.configuration['city'])
            city_tz = self.gmaps.timezone((geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']), tn)

            diff_offset = int((city_tz['rawOffset'] + city_tz['dstOffset']) - (local_tz['rawOffset'] + local_tz['dstOffset'])) / 3600
            hour = time.strftime("%H")
            minute = time.strftime("%M")

            message['city'] = {
                'arg': self.configuration['city'],
                'timezoneid': city_tz['timeZoneId'],
                'time': {
                    'hour': (int(hour) + diff_offset) % 24,
                    'minute': minute
                },
                'timezonename': city_tz['timeZoneName']
            }
            message['local'] = {
                'arg': self.configuration['local'],
                'timezoneid': local_tz['timeZoneId'],
                'time': {
                    'hour': hour,
                    'minute': minute
                },
                'timezonename': local_tz['timeZoneName']
            }

            message['status'] = "OK"

            logger.debug("message: %s" % message)
            self.say(message)


    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['gmaps_api_key'] is None:
            raise InvalidParameterException("Google Maps require an API key")

        if self.configuration['local'] is None:
            raise InvalidParameterException("WW Time needs a local")

        if self.configuration['city'] is None:
            raise InvalidParameterException("WW Time needs a city")

        return True


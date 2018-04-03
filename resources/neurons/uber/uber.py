import logging

from uber_rides.session import Session
from uber_rides.client import UberRidesClient

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Uber (NeuronModule):
    def __init__(self, **kwargs):
        super(Uber, self).__init__(**kwargs)

        # Get parameters form the neuron
        self.configuration = {
            'uber_api_key': kwargs.get('uber_api_key', None), 
            'gmaps_api_key': kwargs.get('gmaps_api_key', None), 
            'drive_mode': kwargs.get('drive_mode', 'uberX'), 
            'start_latitude': kwargs.get('start_latitude', None),
            'start_longitude': kwargs.get('start_longitude', None),
            'start_address': kwargs.get('start_address', None),
            'end_address': kwargs.get('end_address', None)
        }

        logger.debug(self.configuration)

        # Check parameters:
        if self._is_parameters_ok():
            session = Session(server_token=self.configuration['uber_api_key'])
            client = UberRidesClient(session)

            # Get start address geocoding if needed
            if self.configuration['start_address']:
                address = self._get_address(self.configuration['start_address'])
                self.configuration['start_longitude'] = address['longitude']
                self.configuration['start_latitude'] = address['latitude']

            # Get wating time estimates 
            response = client.get_pickup_time_estimates(
                start_latitude=self.configuration['start_latitude'],
                start_longitude=self.configuration['start_longitude'],
            )

            message = {}

            time = response.json.get('times')
            for t in time:
                if t['display_name'] == self.configuration['drive_mode']:
                    message['driving_mode'] = t['display_name']
                    message['time_to_get_driver'] = t['estimate'] / 60


            if self.configuration['end_address']:
                # Get from address geocoding
                address = self._get_address(self.configuration['end_address'])
                self.configuration['end_longitude'] = address['longitude']
                self.configuration['end_latitude'] = address['latitude']

                # Get price and time for the ride
                response = client.get_price_estimates(
                    start_latitude=self.configuration['start_latitude'],
                    start_longitude=self.configuration['start_longitude'],
                    end_latitude=self.configuration['end_latitude'],
                    end_longitude=self.configuration['end_longitude']
                )

                estimate = response.json.get('prices')


                # Get price estimates and time estimates
                for e in estimate:
                    if e['display_name'] == self.configuration['drive_mode']:
                        message['ride'] = {
                            'distance': e['distance'],
                            'high_estimate': int(e['high_estimate']),
                            'low_estimate': int(e['low_estimate']),
                            'duration': e['duration'] / 60,
                            'estimate': e['estimate'],
                        }

        self.say(message)


    def _get_address(self, address):
        # Geocoding gmaps api.
        import googlemaps

        gmaps = googlemaps.Client(key=self.configuration['gmaps_api_key'])

        # Geocoding an address
        geocode_result = gmaps.geocode(address)
    
        return {
            'latitude': geocode_result[0]['geometry']['location']['lat'], 
            'longitude': geocode_result[0]['geometry']['location']['lng']
        }


    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """
        if self.configuration['uber_api_key'] is None:
            raise InvalidParameterException("Uber neuronrequire an Uber API key")

        if self.configuration['start_address'] is None \
            and (self.configuration['start_longitude'] is None or self.configuration['start_latitude'] is None):
            raise InvalidParameterException("Missing start_address or start longitude and latitude")

        if (self.configuration['start_address'] or self.configuration['end_address']) \
            and self.configuration['gmaps_api_key'] is None:
            raise InvalidParameterException('To transform start or end address into longitute and latitude, a gmaps API key is required')


        return True


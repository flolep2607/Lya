import logging
import httplib2
import os

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

flags = tools.argparser.parse_args(args=[])
flags.noauth_local_webserver = True

import datetime
import dateutil.parser
import locale

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Google_calendar (NeuronModule):
    def __init__(self, **kwargs):

        # we don't need the TTS cache for this neuron
        cache = kwargs.get('cache', None)
        if cache is None:
            cache = False
            kwargs["cache"] = cache
        super(Google_calendar, self).__init__(**kwargs)

        self.scopes = 'https://www.googleapis.com/auth/calendar.readonly'

        # get parameters form the neuron
        self.configuration = {
            'credentials_file': kwargs.get('credentials_file', None),
            'client_secret_file': kwargs.get('client_secret_file', None),
            'application_name': kwargs.get('application_name', None),
            'max_results': kwargs.get('max_results', 1),
            'locale': kwargs.get('locale', None)
        }

        # check parameters
        if self._is_parameters_ok():
            self.infos = {
                "events": [],
                "count": 0
            }

            if self.configuration['locale'] is not None:
                locale.setlocale(locale.LC_ALL, self.configuration['locale'])

            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)

            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            eventsResult = service.events().list(
                calendarId='primary', timeMin=now, maxResults=self.configuration['max_results'],
                singleEvents=True, orderBy='startTime').execute()
            events = eventsResult.get('items', [])

            for event in events:
                start = event['start'].get('dateTime')

                # All day event
                if start is None:
                    start = event['start'].get('date')

                weekday = dateutil.parser.parse(start).strftime('%A')
                day = dateutil.parser.parse(start).strftime('%d')
                month = dateutil.parser.parse(start).strftime('%B')
                hour = dateutil.parser.parse(start).strftime('%H')
                minute = dateutil.parser.parse(start).strftime('%M')
                self.infos["events"].append({'summary': event['summary'],
                    'time': {'hour': hour, 'minute': minute, 'weekday': weekday, 'day': day, 'month': month}})
                self.infos['count'] += 1

            logger.debug("Google news return : %s" % self.infos)

            self.say(self.infos)


    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['credentials_file'] is None:
            raise InvalidParameterException("Google news needs a credentials_file")

        if self.configuration['client_secret_file'] is None:
            raise InvalidParameterException("Google news needs a client_secret_file")

        if self.configuration['max_results'] is None:
            raise InvalidParameterException("Google news needs a max_results")

        if self.configuration['application_name'] is None:
            raise InvalidParameterException("Google news needs a application_name")

        return True

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_path = os.path.join(self.configuration['credentials_file'])

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.configuration['client_secret_file'], self.scopes)
            flow.user_agent = self.configuration['application_name']
            credentials = tools.run_flow(flow, store, flags)

        return credentials


import logging
import requests

from bs4 import BeautifulSoup
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Web_scraper (NeuronModule):
    def __init__(self, **kwargs):
        # we don't need the TTS cache for this neuron
        cache = kwargs.get('cache', None)
        if cache is None:
            cache = False
            kwargs["cache"] = cache
        super(Web_scraper, self).__init__(**kwargs)

        # get parameters form the neuron
        self.configuration = {
            "url": kwargs.get('url', None),
            "main_selector": {
                'tag': kwargs.get('main_selector_tag', None),
                'class': kwargs.get('main_selector_class', None)
            },
            "title_selector": {
                'tag': kwargs.get('title_selector_tag', None),
                'class': kwargs.get('title_selector_class', None)
            },
            "description_selector": {
                'tag': kwargs.get('description_selector_tag', None),
                'class': kwargs.get('description_selector_class', None)
            }
        }

        # check parameters
        if self._is_parameters_ok():
            self.infos = {
                "data": [],
                "returncode": None
            }

            try:
                r = requests.get(self.configuration['url'])
                self.infos['returncode'] = r.status_code

                soup = BeautifulSoup(r.text, 'html.parser')
                for selector in soup.find_all('div',
                                              class_="tvm-grid-channel__prog"):
                    self.infos['data'].append({
                        'title': selector.find(
                            'span',
                            class_="tvm-channel__logo").get_text(),
                        'content': selector.find(
                            'h3',
                            class_="tvm-grid-channel__name").get_text()
                    })

            except requests.exceptions.HTTPError:
                print("exception")
                self.infos['returncode'] = "HTTPError"

            logger.debug("Web scraper return : %s" % len(self.infos))

            self.say(self.infos)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['url'] is None:
            raise InvalidParameterException("Web scraper needs a url")

        if self.configuration['main_selector']['tag'] is None:
            raise InvalidParameterException(
                "Web scraper needs a main_selector tag")

        if self.configuration['main_selector']['class'] is None:
            raise InvalidParameterException(
                "Web scraper needs a main_selector class")

        if self.configuration['title_selector']['tag'] is None:
            raise InvalidParameterException(
                "Web scraper needs a title_selector tag")

        if self.configuration['title_selector']['class'] is None:
            raise InvalidParameterException(
                "Web scraper needs a title_selector class")

        if self.configuration['description_selector']['tag'] is None:
            raise InvalidParameterException(
                "Web scraper needs a description_selector tag")

        if self.configuration['description_selector']['class'] is None:
            raise InvalidParameterException(
                "Web scraper needs a description_selector class")

        return True

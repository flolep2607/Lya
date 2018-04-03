import re
import logging

from kalliope.core.NeuronModule import NeuronModule
from kalliope.core.Models import Signal

logging.basicConfig()
logger = logging.getLogger("kalliope")

class List_available_orders(NeuronModule):
    def __init__(self, **kwargs):
        super(List_available_orders, self).__init__(**kwargs)

        ignore_machine_name = kwargs.get('ignore_machine_name', None)
        query_replace_text = kwargs.get("query_replace_text", None)
        order_per_synapse_limit = kwargs.get("order_per_synapse_limit", None)

        self.values = dict()
        self.values['orders'] = []
        self.values['nb_orders'] = 0

        for synapse in self.brain.synapses:
            cptr = 0
            for signal in synapse.signals:
                if isinstance(signal, Signal):
                    if signal.name == "order" and self._is_valid_order(signal.parameters, ignore_machine_name):
                        self.values['orders'].append(
                            self._get_final_sentence(signal.parameters, query_replace_text))
                        cptr += 1
                        if order_per_synapse_limit is not None and order_per_synapse_limit == cptr:
                            break

        self.values['nb_orders'] = len(self.values['orders'])

        self.say(self.values)


    def _is_valid_order(self, sentence, ignore_machine_name):
        """
        Check if the order should be added to the list of available orders.

        :return: true if the order is valid, false otherwise
        :rtype: Boolean
        """

        if ignore_machine_name == 1 and re.compile("\w+(-\w)+").match(sentence) is not None:
            return False

        return True

    def _get_final_sentence(self, sentence, query_replace_text):
        """
        Return the final sentence with the changed text if applicable

        :return: the final sentence
        :rtype: String
        """

        s = sentence
        pattern = re.compile("\{\{ *\w+ *\}\}")

        if pattern.search(sentence) is not None and query_replace_text is not None:
            s = re.sub(pattern, query_replace_text, sentence)

        return s


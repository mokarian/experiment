"""
This file contains modules used to call Bing Spellcheck
"""
import os

import logging
import requests

from src.constants import Constants
from src.utils import Utils


class SpellCheck:
    """
    This Class contains modules used to call Bing Spellcheck
    """

    def __init__(self):
        self.utils = Utils(os.path.join("resources"))
        self.config = self.utils.get_config()
        self.endpoint = self.config["cognitive_services"]["endpoint"]
        self.subscription_key = self.config["cognitive_services"]["key"]

    def get_spellcheck(self, text, mode='spell'):
        """
        this method calls the bing spell_check service,
        if there is no suggestion it simply returns the passed text
        :param text:
        :param mode: 'proof' or 'spell'
        :return: bing suggested word with highest rank
        """
        params = {
            'mkt': 'en-us',
            'mode': mode  # 'proof' or 'spell'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        data = {Constants.text: text}
        endpoint = self.endpoint
        try:
            response = requests.post(endpoint, headers=headers, params=params, data=data)
        except Exception as ex:
            logging.error("could not call the spell check service , {}".format(ex))

        json_response = response.json()
        corrected = self.process_spellcheck_response(text, json_response)
        return corrected

    @staticmethod
    def process_spellcheck_response(text, json_response):
        """
        This method parses the response of the bing spellcheck service,
        to return the suggestion with the highest rank,
        if there is no suggestion it returns the text itself
        :param text:
        :param json_response:
        :return: highest rank suggestion from the json
        """
        if json_response[Constants.flagged_tokens]:
            for flagged in json_response[Constants.flagged_tokens]:
                if Constants.token in flagged:
                    token = flagged[Constants.token]
                    if Constants.suggestions in flagged:
                        suggestions = flagged[Constants.suggestions]
                        selected = token
                        score = 0
                        for suggestion in suggestions:
                            if suggestion[Constants.score] > score:
                                selected = suggestion[Constants.suggestion]
                                score = suggestion[Constants.score]
                        text = text.replace(token, selected)
        return text


if __name__ == '__main__':
    SPELLCHECK = SpellCheck()

    print(SPELLCHECK.get_spellcheck("apli pickings"))

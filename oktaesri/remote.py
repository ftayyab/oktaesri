"""
    Class for making remote class
"""
import json

import requests


class Remote:
    def __init__(self):
        pass

    @staticmethod
    def make_get_call(url):
        """
        :param url: url to the endpoint
        :return 0 or 1

        """
        try:
            r = requests.get(url)
            if r and r.status_code == 200:
                return 1 if json.loads(r.text)['status'] == 'success' else 0
            else:
                return 0
        except Exception as e:
            return 0

    @staticmethod
    def make_post_call( url, data):
        """
        :param url: url to the endpoint
        :param data: data to be sent to the server
        """
        try:
            r = requests.post(url, data)
            if r and r.status_code == 200:
                return {"status": r.status_code, "payload": r.text}
            else:
                raise Exception("Error: Unable to make post request")
        except Exception as e:
            return {"status": r.status_code, "payload": str(e)}

    @staticmethod
    def make_post_json_call(url, data):

        """
        :param url:
        :param data: passing json data for OKTA API
        :return: respone in json
        """
        try:

            r = requests.post(url, json=data)

            if r and r.status_code == 200:
                return {"status": r.status_code, "payload": r.text}
            else:
                raise Exception("Error: Unable to make post request")
        except Exception as e:
            return {"status": r.status_code, "payload": str(e)}
"""
Purpose: Class for logging purposes
"""
import datetime
import logging
import os


class Logger:
    """
        Logger class used for logging purposes
    """
    def __init__(self):
        pass

    @staticmethod
    def write_2_log(err_message):
        """
        Function to write to log
        :param err_message:
        :return: None
        """
        logging.basicConfig(filename=os.path.join(os.path.dirname(__file__),'app.log'), level="ERROR", filemode='a',
                            format='%(name)s - %(levelname)s - %(message)s')
        timestamp = str(datetime.datetime.now())
        logging.error(timestamp + ': ' + str(err_message))

"""
Purpose: Class to handler configuration
Author: Faizan Tayyab
"""

import configparser
import os


class ConfigHandler(object):
    """
        Class to deal with setting file via configparser
    """
    context = None

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str

        cwd = os.path.dirname(os.path.realpath(__file__))

        if os.path.exists(os.path.join(cwd, 'settings.ini')):
            self.config.read(os.path.join(cwd, 'settings.ini'))
        else:
            pass
            # Logger.write_2_log('Missing Settings File')

    def get_sections(self):
        return self.config.sections()

    def write_2_config_section(self, section, settings):

        if self.config.has_section(section):
            for item in settings:
                self.config.set(section, item, settings[item])

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

        configfile = None



    def get_config_section_values(self, section):
        settings_dict = {}
        options = self.config.options(section)
        for option in options:
            try:
                settings_dict[option] = self.config.get(section, option)
                if settings_dict[option] == -1:
                    pass
            except:
                # Logger.write_2_log('Unable to read settings')
                settings_dict[option] = None
        return settings_dict

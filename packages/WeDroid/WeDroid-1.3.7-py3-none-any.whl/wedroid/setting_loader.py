#!/usr/bin/env python3

#  Copyright (c) 2020. Steven@oddineers.co.uk

import os
from configparser import ConfigParser, NoOptionError
from wedroid import logkit


class WeDroidConfiguration:
    parser = ConfigParser()
    logger = logkit.LogKit()

    def __init__(self, config_file):
        self.cfg_file = config_file
        self.cfg_path = os.path.dirname(os.path.abspath(config_file))

    def convert_str_bool(self, str_test: str) -> bool:
        """
        Convert string values that equate to true or false.

        :param str_test:
        :type str_test: str
        :return: str_test
        :rtype: bool
        """
        temp = False

        # False matches though not needed:
        #  str_test.lower() in ('false', 'no', 'n', '0'):
        if str_test.lower() in ('true', 'yes', 'y', '1'):
            temp = True
        return temp

    def get_with_default(self, section, name, default='None'):
        if self.parser.has_section(section) and self.parser.has_option(section, name):
            return self.parser.get(section, name)
        else:
            self.parser.set(section, name, default)
            self.logger.cli_log('Missing options: [' + section + '][' + name + ']')

            if default == 'required':
                self.logger.cli_log('Default required for missing option: [' + section + '][' + name + ']')
                exit()

    def create_config(self, path):
        """
        Create a wedroid config file.
        """
        config = ConfigParser()
        config.add_section("weathvars")

        with open(path, "w") as config_file:
            config.write(config_file)

    def get_config(self, path):
        """
        Returns the wedroid_settings object
        """
        if not os.path.exists(path):
            self.create_config(path)

        config = ConfigParser()
        config.read(path)
        return config

    def get_setting(self, path, section, setting):
        """
        Retrieve a setting from a section by option name.
        """
        config = self.get_config(path)
        try:
            value = config.get(section, setting)
            self.logger.cli_log("[{section}] [{setting}] is [{value}]".format(
                section=section, setting=setting, value=value))
            return value
        except KeyError as e:
            self.logger.cli_log(f"Missing: [{section}] {e}")
            return None
        except NoOptionError as e:
            self.logger.cli_log(f"Missing: [{section}] {e}")
            return None

    def update_setting(self, path, section, setting, value):
        """
        Update a setting
        """
        config = self.get_config(path)
        config.set(section, setting, str(value))
        with open(path, "w") as config_file:
            config.write(config_file)

    def delete_setting(self, path, section, setting):
        """
        Delete a setting
        """
        config = self.get_config(path)
        config.remove_option(section, setting)
        with open(path, "w") as config_file:
            config.write(config_file)

    @staticmethod
    def create_storage_path(path):
        """
        Create the directory on the local filesystem
        """
        os.makedirs(path, exist_ok=True)

    def test_config(self):
        self.logger.cli_log('Configuration data found in class: ')

        for key, value in self.__dict__.items():
            self.logger.cli_log(f"{str(key)} = {str(value)}")

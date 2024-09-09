#  Copyright (c) 2020. Steven@oddineers.co.uk
import json
import os
from wedroid.logkit import LogKit


class ConfigurationHelper:
    """
    Provides functions for creating and validation required configuration files.
    """
    logger = LogKit()
    file_contents = '''
{
    "run_type": "tasker",
    "intercept_task_name": "WeDroid Received",
    "owm_api_key": "<owm_api_key>",
    "announce_temp": "True",
    "announce_time": "True",
    "announce_humidty": "False",
    "announce_wind": "False",
    "announce_sun": "True",
    "sl4a_gtts": "False",
    "bot_name": "WeDroid",
    "mattermost_url": "<webhook>",
    "device_location": "True",
    "longitude": "-3",
    "latitude": "52",
    "log_level": "INFO"
}
    '''

    def check_configuration(self, config_path):
        """
        Validates a setting.py contains the required options.

        :param config_path: Path to configuration file.
        :type config_path: str
        :return: True or False if configuration file is valid.
        :rtype: bool
        """
        fail_count = 0

        if config_path is None:
            self.logger.cli_log('Configuration cannot be None.', 'error')
            return False
        if not isinstance(config_path, dict):
            # File doesn't exizt
            if not os.path.isfile(config_path):
                self.logger.cli_log('Configuration must be a dict; example: \n\r' + self.file_contents, 'error')
                return False

            # Load the json from the file
            with open(config_path) as f:
                config_path = json.load(f)

        defaults = ['run_type',
                    'intercept_task_name',
                    'announce_time',
                    'announce_temp',
                    'announce_humidty',
                    'announce_wind',
                    'announce_sun',
                    'sl4a_gtts',
                    'bot_name',
                    'mattermost_url',
                    'device_location',
                    'owm_api_key',
                    'longitude',
                    'latitude']

        # Check any settings missing from configuration
        for default in defaults:
            if default not in config_path:
                self.logger.cli_log('Setting `{}` missing.'.format(default), 'error')
                fail_count += 1
        # Any settings missing exit
        if fail_count > 0:
            self.logger.cli_log('Configuration missing settings.', 'error')
            return False

        return True

    def create_configuration(self, path):
        """
        Creates settings.py at path.

        :param path: Path to create settings file.
        :type path: str
        :return: Success state
        :rtype: bool
        """
        self.logger.cli_log('Attempting to create settings.json containing:\n\n' + self.file_contents, 'info')
        if os.path.exists(path):
            new_file = open(path + '\\settings.json', 'w')
            new_file.write(self.file_contents)
            new_file.close()
            return True
        else:
            return False

    def load_configuration(self, path):
        if os.path.isfile(path):
            # Load the json from the file
            with open(path) as f:
                config_path = json.load(f)
                return config_path
        return None

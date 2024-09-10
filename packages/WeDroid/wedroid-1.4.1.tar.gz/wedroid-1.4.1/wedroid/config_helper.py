#  Copyright (c) 2020. Steven@oddineers.co.uk
import json
import os
from wedroid.logkit import LogKit


class ConfigurationHelper:
    """
    Provides functions for creating and validation required configuration files.
    """
    logger = LogKit()
    file_contents = '''{
    "run_type": "tasker",
    "intercept_task_name": "WeDroid Received",
    "owm_api_key": "<OWM-KEY-HERE>",
    "announce_temp": true,
    "announce_time": true,
    "announce_humidity": false,
    "announce_wind": false,
    "announce_sun": true,
    "sl4a_gtts": false,
    "bot_name": "WeDroid",
    "mattermost_url": "<web-hook-url>",
    "device_location": true,
    "longitude": -3.0,
    "latitude": 53.0,
    "log_level": "DEBUG",
    "log_gps_coords": true,
    "location_provider": "gps",
    "location_request": "once"
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
                    'announce_humidity',
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
        self.logger.cli_log('Attempting to create wedroid_settings.json containing:\n\n' + self.file_contents, 'info')
        if os.path.exists(path):
            new_file = open(path + '/wedroid_settings.json', 'w')
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

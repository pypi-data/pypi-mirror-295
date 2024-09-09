#!/usr/bin/python3

__author__ = "Steven Brown"
__copyright__ = "Copyright 2021, Oddineers Ltd."
__credits__ = []
__license__ = "Apache License v2"
__version__ = "1.3.7"
__maintainer__ = "Steven Brown"
__email__ = "steven@oddineers.co.uk"
__status__ = "Production"

import argparse
import json
import subprocess
import os
import time
import pyowm
from json.decoder import JSONDecodeError
from decimal import Decimal
from wedroid.logkit import LogKit
from wedroid.time_utilities import TimeUtilities
from wedroid.setting_loader import WeDroidConfiguration
from wedroid.config_helper import ConfigurationHelper
from wedroid.matterping import Notifications


class WeDroid:
    """
    The WeDroid class provides access to formalised weather announcements with customisable levels of observation
    details. The Time, weather, temperature, humidity and wind direction/speeds are accessible through class attributes.
    """
    time_utils = TimeUtilities()
    logger = LogKit()
    # observation check used to cache results
    observation = None
    wcode = 0
    temp = 0
    last_code = 0
    last_temp = 0
    last_weather_object = None

    def init_android_import(self):
        try:
            import android
            if not hasattr(android, 'Android'):
                self.enable_fakedroid()
            else:
                self.android = android.Android()
        except (ModuleNotFoundError, ImportError):
            self.enable_fakedroid()

    def __init__(self, config_path=None, translation_path=None, store_ini='none'):
        self.version = __version__
        # Test if the android module is available SL4A
        self.android = None
        self.wedroid_settings = None
        self.run_path = os.path.dirname(os.path.abspath(__file__))

        # Determine whether to use internal waether.ini, user provided or None.
        if store_ini == 'builtin':
            weather_file = os.path.abspath(self.run_path + '/../weather.ini')
            self.weather_settings = WeDroidConfiguration(weather_file)
            self.weather_store = 'builtin'
        elif store_ini is not None and store_ini == "custom":
            weather_file = store_ini
            self.weather_settings = WeDroidConfiguration(weather_file)
            self.weather_store = 'custom'
        else:
            self.weather_settings = None
            self.weather_store = 'none'

        mod_err_msg = 'When used as a module/package you must pass a `settings.json` configuration.'

        # Setup a default configuration from settings.json should be in: <project-root>
        if not config_path:
            config_path = os.path.abspath(self.run_path + '/../settings.json')

        # Simple check to determine if running as module and ensure a setting.json is supplied
        if "site-packages" in self.run_path and not config_path:
            self.logger.cli_log(mod_err_msg, 'error')
            exit(1)

        # Validate the WeDroid settings file contains the settings expected.
        ch = ConfigurationHelper()
        # Preferred JSON format
        if os.path.isfile(config_path):
            self.wedroid_settings = ch.load_configuration(config_path)
        # If setting is a dict (older format: settings.py)
        elif type(config_path) is dict:
            self.wedroid_settings = config_path
        else:
            self.logger.cli_log(mod_err_msg, 'error')
            exit(1)

        # Validate the loaded configuration
        if not ch.check_configuration(self.wedroid_settings):
            exit(1)

        self.logger.cli_log(f'WeDroid version {self.version}', 'info')

        # Load settings from configuration file
        self.cfg_path = None
        self.wedroid_run_type = self.wedroid_settings['run_type']
        self.tasker_task_name = self.wedroid_settings['intercept_task_name']
        self.announce_time = self.wedroid_settings['announce_time']
        self.announce_temp = self.wedroid_settings['announce_temp']
        self.announce_humidty = self.wedroid_settings['announce_humidty']
        self.announce_wind = self.wedroid_settings['announce_wind']
        self.announce_sun = self.wedroid_settings['announce_sun']
        self.sl4a_gtts = self.wedroid_settings['sl4a_gtts']
        self.bot_name = self.wedroid_settings['bot_name']
        self.mattermost_url = self.wedroid_settings['mattermost_url']
        self.device_location = self.wedroid_settings['device_location']
        self.owm_api_key = self.wedroid_settings['owm_api_key']
        self.owm = None

        # Get logging level if available
        self.log_level = "DEBUG"
        if 'log_level' in self.wedroid_settings:
            log_level = self.wedroid_settings['log_level']

            if log_level in ['DEBUG', 'ERROR', 'INFO']:
                self.logger.set_log_level(log_level)
                self.log_level = log_level

        # Check android support
        self.init_android_import()
        # self.logger.cli_log(f'WeDroid log level {self.log_level}')

        # If the translation path has been overriden
        self.translation_path = None
        if translation_path is not None and type(translation_path) is str:
            if os.path.isdir(translation_path):
                self.translation_path = translation_path

        # Check key is not empty or our default
        if self.owm_api_key == '<OWM-KEY-HERE>' or self.owm_api_key == '':
            self.logger.cli_log('OpenWeatherMap API key is not valid.')
            exit()

        # WeDroid attributes
        self.sunset = None
        self.sunrise = None
        self.status = None
        self.wcode = 0
        self.temp = 0
        self.last_code = 0
        self.last_temp = 0
        self.now = None
        self.wind_speed = None
        self.wind_direction = None
        self.humidity = None
        self.day_state = None
        self.time_msg = None
        self.weather_msg = None
        self.temp_msg = None
        self.wind_msg = None
        self.sun_msg = None
        self.humidity_msg = None
        self.outburst_msg = None
        self.last_report = None
        self.forecast_msg = None
        self.longitude = self.wedroid_settings['longitude']
        self.latitude = self.wedroid_settings['latitude']
        self.icon = None
        self.location_source = None
        self.location_provider = "gps"
        self.location_request = "once"

        if 'location_provider' in self.wedroid_settings:
            location_provider = self.wedroid_settings['location_provider']

            if location_provider in ['gps', 'network', 'passive']:
                # if does not match stored provider update and set it
                if location_provider != self.location_provider:
                    self.set_location_provider(location_provider)
                    self.location_provider = location_provider
                    self.logger.cli_log(f'Location provider: {location_provider}', 'debug')

        if 'location_request' in self.wedroid_settings:
            location_request = self.wedroid_settings['location_request']

            if location_request in ['once', 'last', 'updates']:
                # if does not match stored request type update + set it
                if location_request != self.location_request:
                    self.set_location_request_type(location_request)
                    self.location_request = location_request
                    self.logger.cli_log(f'Location request type: {location_request}', 'debug')

        # Speech translations
        keys = ["time-notification", "no-weather", "no-location", "unknown", "sunrise-past", "sunrise-future",
                "sunset-past", "sunset-future", "temp-decrease", "temp-increase", "temp-approach-zero", "temp-zero",
                "temp-remains", "temp-measurement", "weather-nochange", "rain-clear", "mist-clear", "wind", "humidity"]

        self.other_vrm = self.get_json(self.get_translation_path("announcements.json"))
        self.validate_json(self.other_vrm, keys)

        keys = [
            "0", "200", "201", "202", "210", "211", "212", "221", "230", "231", "232", "300", "301", "302", "310",
            "311", "312", "313", "314", "321", "500", "501", "502", "503", "504", "511", "520", "521", "522", "531",
            "600", "601", "602", "611", "612", "615", "616", "620", "621", "622", "701", "711", "721", "731", "741",
            "751", "761", "762", "771", "781", "800", "801", "802", "803", "804", "900", "901", "902", "903", "904",
            "905", "906", "951", "952", "953", "954", "955", "956", "957", "958", "959", "960", "961", "962",
        ]

        self.weather_vrm = self.get_json(self.get_translation_path("weather.json"))
        self.validate_json(self.weather_vrm, keys, True)

    def set_location_provider(self, provider: str = "gps"):
        if provider in ['gps', 'network', 'passive']:
            provider = "gps"

        self.location_provider = provider
        return provider

    def set_location_request_type(self, request: str = "once"):
        if request not in ['once', 'last', 'updates']:
            request = "once"

        self.location_request = request
        return request

    def get_translation_path(self, filename):
        """
        Build the path to translation directory.
        :param filename:
        :type filename:str
        :return: filename
        :rtype: str
        """
        path = f"{self.run_path}/translations"

        if self.translation_path is not None:
            path = f"{self.translation_path}"

        path = f"{path}/{filename}"
        return path

    def enable_fakedroid(self):
        """
        Triggers if the SL4A android module is not available returns a class used to pass other platforms usage.

        :return:
        :rtype:
        """
        self.logger.cli_log('Import `android` is not available loading `fakedroid`', 'debug')
        from wedroid import fakedroid
        self.android = fakedroid.Android()

    def connect_owm(self):
        """
        Connect to the OpenWeatherMap API.

        :return: OWM
        :rtype: object
        """

        # Weather_at_coords uses latitude and longitude
        return pyowm.OWM(self.owm_api_key)

    def set_prev_weather_attr(self, last_code=0, last_temp=0):
        """
        Updates the last weather code and last temperature attributes in class and if enabled writes the values to the
        `weather.ini`.

        :param last_code:
        :type last_code:int
        :param last_temp:
        :type last_temp:float or int
        :return:
        :rtype:
        """
        tmp_last_temp = None
        tmp_last_code = None

        if self.wedroid_run_type != 'file':
            tmp_last_temp = last_temp
            tmp_last_code = last_code
        elif self.wedroid_run_type == 'file' and self.weather_store == 'builtin':
            if self.weather_settings:
                self.cfg_path = self.weather_settings.cfg_file
                tmp_last_temp = self.weather_settings.get_setting(self.cfg_path, 'weathvars', 'temp')
                tmp_last_code = self.weather_settings.get_setting(self.cfg_path, 'weathvars', 'wcode')

        if tmp_last_temp and tmp_last_temp is not None:
            self.last_temp = tmp_last_temp
        else:
            self.last_temp = 0

        if tmp_last_code and tmp_last_code is not None:
            self.last_code = tmp_last_code
        else:
            self.last_code = 0

    def get_prev_weather_attr(self):
        """
        Returns the last weather code and last temp code from class attributes.

        :return: self.last_code, self.last_temp
        :rtype: int, int
        """
        return self.last_code, self.last_temp

    def get_location(self):
        """
        Retrieves last known location data if GPS available otherwise falls back to static location data.

        :return: current_long, current_lat
        :rtype: float, float
        """
        # checks if device location should be used:
        current_loc = None
        msg = ""
        if self.device_location:
            # Lets use the GPS on the device to get the current location or last successful location check
            current_loc = self.android.getLastKnownLocation(self.location_provider, self.location_request)
            msg = 'getLastKnownLocation detail: {}'.format(current_loc)
            self.logger.cli_log(msg, 'debug')
            self.location_source = "device"
            msg = 'Accessed GPS location data;'

        # If device location is not being used or the current location data returned empty
        if not self.device_location or current_loc is None:
            msg = 'Unable to access GPS location data;'
            current_loc = [{0}, {'passive': {'longitude': self.wedroid_settings['longitude'],
                                             'latitude': self.wedroid_settings['latitude']}}]
            self.location_source = "static"

        current_long = current_loc[1]['passive']['longitude']
        current_lat = current_loc[1]['passive']['latitude']

        # Log location data source
        msg = '{} using {} location data: latitude: {} longitude: {}'.format(msg, self.location_source, current_lat, current_long)
        self.logger.cli_log(msg, 'info')

        # If last known GPS failed or device location prohibited get stored locationdata.
        if current_loc:
            current_long = float(current_long)
            current_lat = float(current_lat)
            self.longitude = current_long
            self.latitude = current_lat
            return current_long, current_lat
        else:
            return False

    def get_observation_details(self, clat, clong):
        """
        Retrieves weather observation data and assigns values to class attributes and returns retrieved data.

        :param clong: Longitude
        :type clong: float
        :param clat: Latitude
        :type clat: float
        :return: Weather observation object
        :rtype: object or False
        """

        # If the last temp and code are not the defaults then set them before checking observation
        if self.temp != 0:
            self.last_temp = self.temp

        if self.wcode != 0:
            self.last_code = self.wcode

        try:
            # check observation object
            if self.owm is None:
                self.owm = self.connect_owm()
                # self.owm = pyowm.OWM(self.owm_api_key)
            # Weather_at_coords uses latitude and longitude
            self.observation = self.owm.weather_manager().weather_at_coords(clat, clong)

            observation = self.observation
            weather = observation.weather  # get_weather()
            # print(observation.to_dict())

            wind = weather.wind()
            if 'deg' in wind:
                self.wind_direction = self.degree_to_compass(wind['deg'])
            else:
                self.wind_direction = 'Undetermined'
            # Wind speed conversion from meter per second to mile per hour: unit x 2.2369
            self.wind_speed = Decimal(wind['speed'] * 2.2369).quantize(Decimal('1e-0'))

            # Standardised weather items
            sunset = weather.sunset_time()
            sunrise = weather.sunrise_time()
            sunset = self.time_utils.convert_todate(sunset)
            sunrise = self.time_utils.convert_todate(sunrise)

            # Check if DST is enabled and add an hour is so
            if self.time_utils.is_dst():
                sunset = self.time_utils.calculate_hours(sunset, '+', 1)
                sunrise = self.time_utils.calculate_hours(sunrise, '+', 1)

            self.sunset = sunset
            self.sunrise = sunrise
            self.day_state = self.time_utils.get_day_state(sunrise)

            temp = weather.temperature('celsius')['temp']
            self.temp = Decimal(temp).quantize(Decimal('1e-0'))
            self.status = weather.detailed_status
            self.wcode = str(weather.weather_code)
            # Extra Weather details
            # self.humidity = weather.humidity()

            return weather
        except pyowm.commons.exceptions.APIRequestError as error:
            self.logger.cli_log("OWM API access unauthorized; please review OWM access key.")
            self.logger.cli_log(error)
            return False
        except pyowm.commons.exceptions.APIResponseError as error:
            self.logger.cli_log("OWM API call timed out.")
            self.logger.cli_log(error)
            return False
        except Exception:
            self.logger.cli_log(self.logger.format_exception("stack"))
            return False

    def get_forecast(self, clat, clong, interval='3h', limit=None):
        """
        WIP: Fetches forecast for a period and summarises.

        :param clong: Longitude
        :type clong: float
        :param clat: Latitude
        :type clat: float
        :return:
        :rtype:
        """

        # Check
        if self.owm is None:
            self.owm = self.connect_owm()

        mgr = self.owm.weather_manager()
        forecaster = mgr.forecast_at_coords(clat, clong, interval, limit)  # this gives you a Forecaster object
        starts = self.time_utils.convert_todate(forecaster.when_starts())
        ends = self.time_utils.convert_todate(forecaster.when_ends())

        return forecaster

    def perform_temperature_test(self, temp):
        """
        Compares the passed in temperature with the previous observation if available and returns a announcement
        based on
        whether the temperature if raising, decreasing or freezing.

        :param temp: Temperature.
        :type temp: float
        :return: Temperature observation string.
        :rtype: str
        """
        if Decimal(temp) > Decimal(self.last_temp) and Decimal(temp) > 0:
            spk = self.other_vrm['temp-increase']
            spk = spk + str(temp)
        elif Decimal(self.last_temp) > Decimal(temp) > 0:
            if 2 >= Decimal(temp) > 0:
                spk = self.other_vrm['temp-approach-zero']
                spk = spk + str(temp)
            else:
                spk = self.other_vrm['temp-decrease']
                spk = spk + str(temp)
        elif Decimal(self.temp) <= 0:
            spk = self.other_vrm['temp-zero']
            spk = spk + str(temp)
        else:
            spk = self.other_vrm['temp-remains'] + str(temp)
        spk += self.other_vrm['temp-measurement']
        return spk

    def get_weather_report(self, last_code, weather_code):
        """
        Generates a weather report using the last weather code and the latest weather code.

        :param last_code: Last weather code.
        :type last_code: int
        :param weather_code: Latest weather code.
        :type weather_code: int
        :return: A weather report message.
        :rtype: str
        """
        weather_code = str(weather_code)
        last_code = str(last_code)
        # self.logkit.cli_log(last_code, weather_code)

        if last_code == weather_code:
            weather_part = self.weather_vrm[weather_code]["description"]
            # if weather code matches last code and contains approaching replace with ongoing
            if "approaching" in weather_part.lower() and weather_code not in ("801", "802", "803", "804"):
                weather_part = weather_part.lower()
                weather_part = weather_part.replace("approaching", "ongoing")
            msg = self.other_vrm['weather-nochange'] + str(weather_part)
        elif ("600" > last_code >= "500") and not ("600" > weather_code >= "500"):
            msg = self.other_vrm['rain-clear']
            msg += str(self.weather_vrm[weather_code]["description"])
        elif last_code == "701" and not weather_code == "701":
            msg = self.other_vrm['mist-clear']
            msg += str(self.weather_vrm[weather_code]["description"])
        else:
            msg = str(self.weather_vrm[weather_code]["description"])
        return msg

    def update_observation(self):
        """
        Saves weather data locally to weather.ini
        or sends weather data to Tasker for additional handling.
        """
        if self.wedroid_run_type == 'file':
            self.set_config_var()
        elif self.wedroid_run_type == 'tasker':
            self.set_observation_tasker_vars()

    def update_forecast(self):
        """
        Sends forecast data to Tasker for additional handling.
        """
        if self.wedroid_run_type == 'tasker':
            self.set_forecast_tasker_vars()

    def set_config_var(self):
        """
        Saves WeDroid weather related attributes to a .ini file. Can be used instead of Tasker integration for comparing
        current weather with the previous observation.
        """
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'wcode', self.wcode)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'sunrise', self.sunrise)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'sunset', self.sunset)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'temp', self.temp)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'now', self.now)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'wind_speed', self.wind_speed)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'wind_direction', self.wind_direction)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'humidity', self.humidity)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'day_state', self.day_state)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'time_msg', self.time_msg)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'weather_msg', self.weather_msg)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'temp_msg', self.temp_msg)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'wind_msg', self.wind_msg)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'sun_msg', self.sun_msg)
        # Avoid and interpolation error with config parser by removing percentage symbol from string.
        humidity_msg = self.humidity_msg.replace('%', '')
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'humidity_msg', humidity_msg)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'outburst_msg', self.outburst_msg)
        self.weather_settings.update_setting(self.cfg_path, 'weathvars', 'last_report', self.last_report)

    def run_cmd(self, am_args):
        """
        Uses Termux Activity Manager: `/data/data/com.termux/files/usr/bin/am` to broadcast intents to Tasker on
        Android.

        :return: True or False if the binary exists and the command ran.
        :rtype: bool
        """
        am_cmd = "/data/data/com.termux/files/usr/bin/am"

        if not os.path.exists(am_cmd):
            return False

        if not am_args:
            return False

        try:
            # subprocess.check_call(am_args)
            resi = subprocess.Popen(am_args, shell=True)
            return True
        except OSError as e:
            self.logger.cli_log(
                'Attempted to execute a program that does not exist in current environment: %s' % am_cmd,
                'error')
            self.logger.cli_log(e, 'debug')
            return False
        except subprocess.CalledProcessError as e:
            self.logger.cli_log('Sub program :<%s>, return not 0%s' % (am_cmd, e), 'error')
            self.logger.cli_log(e, 'debug')
            return False
        except Exception as e:
            self.logger.cli_log(e, 'error')
            return False

    def set_observation_tasker_vars(self):
        """
        Prepares current weather observation date and sends it to Tasker.
        """

        am_args = ("/data/data/com.termux/files/usr/bin/am broadcast "
                   "--user 0 "
                   "-a net.dinglisch.android.tasker.ACTION_TASK "
                   "--es task_name \"{}\" "
                "--esal varNames %wd_last_code,%wd_sunrise,%wd_sunset,%wd_last_temp,%wd_last_time,%wd_last_wind_speed,%wd_last_wind_direction,%wd_last_humidity,%wd_day_state,%wd_time_msg,%wd_weather_msg,%wd_temp_msg,%wd_wind_msg,%wd_sun_msg,%wd_humidity_msg,%wd_outburst_msg,%wd_announcement "
                   "--esal varValues \"{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\" ").format(
            self.tasker_task_name,
            self.wcode,
            self.sunrise,
            self.sunset,
            self.temp,
            self.now,
            self.wind_speed,
            self.wind_direction,
            self.humidity,
            self.day_state,
            self.time_msg,
            self.weather_msg,
            self.temp_msg,
            self.wind_msg,
            self.sun_msg,
            self.humidity_msg,
            self.outburst_msg,
            self.last_report)

        if am_args:
            self.run_cmd(am_args)
            return True
        else:
            return False

    def set_forecast_tasker_vars(self):
        """
        Prepares weather forecast date and sends it to Tasker.
        """

        am_args = ("/data/data/com.termux/files/usr/bin/am broadcast "
                   "--user 0 "
                   "-a net.dinglisch.android.tasker.ACTION_TASK "
                   "--es task_name \"{}\" "
                   "--esal varNames %wd_forecast_msg "
                   "--esal varValues \"{}\" ").format(
            self.tasker_task_name,
            self.forecast_msg)

        if am_args:
            self.run_cmd(am_args)
            return True
        else:
            return False

    def run_weather_observation(self):
        """
        Initiates a location check/update and then updates weather observations.

        :return: weather
        :rtype: object
        """
        clong, clat = self.get_location()
        weather = self.get_observation_details(clat, clong)
        self.last_weather_object = weather
        return self.last_code, self.wcode

    def run_weather_forecast(self, interval="3h", limit=4):
        """
        Initiates a location check/update and then updates the weather forecast.

        :return: forecaster
        :rtype: object
        """
        clong, clat = self.get_location()
        forecaster = self.get_forecast(clat, clong, interval, limit)
        self.last_weather_object = forecaster
        return forecaster

    def generate_weather_outburst(self):
        lc, wc = self.run_weather_observation()
        msg = self.weather_vrm.get(wc, self.other_vrm['unknown'])
        self.outburst_msg = msg
        return msg

    def generate_weather_announcement(self):
        """
        Initiates a location check/update, updates weather observations and builds a observation message based on
        message parts enabled.

        :return: Weather report
        :rtype: str
        """
        lc, wc = self.run_weather_observation()
        report = ""

        # Determine if we should announce the time
        if self.announce_time:
            msg = time.strftime(self.other_vrm['time-notification'])
            report = report + msg + ". "
            self.time_msg = msg

            if self.sl4a_gtts:
                self.android.ttsSpeak(msg)

        # Check weather change against previous
        msg = self.get_weather_report(lc, wc)

        if msg:
            report = report + msg + ". "
            self.weather_msg = msg

            if self.sl4a_gtts:
                self.android.ttsSpeak(msg)

        if lc is not False:
            # Should we announce the temperature?
            msg = self.perform_temperature_test(self.temp)
            self.temp_msg = msg

            # return early if "Unable to acquire forecast" already present in message
            if "Unable to acquire forecast" in report:
                return report

            # Temperature message addition
            if self.announce_temp:
                report = report + msg + ". "

                if self.sl4a_gtts:
                    self.android.ttsSpeak(msg)

            msg = self.other_vrm['wind'].format(self.wind_direction, self.wind_speed)
            self.wind_msg = msg

            # Wind direction/speed message addition
            if self.announce_wind:
                report = report + msg + ". "

                if self.sl4a_gtts:
                    self.android.ttsSpeak(msg)

            msg = self.other_vrm['humidity'].format(str(self.humidity))
            self.humidity_msg = msg

            # Humidty message addition
            if self.announce_humidty:
                report = report + msg + ". "

                if self.sl4a_gtts:
                    self.android.ttsSpeak(msg)

            self.now = self.time_utils.get_datetime_now()
            msg = self.generate_sun_status_message(self.now)
            self.sun_msg = msg

            # Sunrise and Sunset message additions
            if msg and self.announce_sun:
                report = report + msg + ". "

                if self.sl4a_gtts:
                    self.android.ttsSpeak(msg)
        # Default fallback message; a time observation
        else:
            msg = ""
            self.temp_msg = msg
            self.wind_msg = msg
            self.humidity_msg = msg
            self.now = self.time_utils.get_datetime_now()
            self.sun_msg = msg

        self.last_report = report
        self.update_observation()
        return report

    def generate_forecast_announcement(self, interval="3h", limit=4):
        forecaster = self.run_weather_forecast(interval, limit)
        msg = ""

        for entry in forecaster.forecast:
            if not entry.weather_code:
                continue
            wcode = str(entry.weather_code)
            # self.logger.cli_log(dir(entry))
            occurrence = self.time_utils.convert_todate(entry.reference_time()).strftime("%H:%M")
            prefix = "At"

            # switch if daily
            if interval == "daily":
                occurrence = self.time_utils.datetime_british(self.time_utils.convert_todate(entry.reference_time()), '%a the {th}')
                prefix = "On"

            msg += "{} {} {}. ".format(prefix, occurrence, self.weather_vrm[wcode]["title"])

        self.forecast_msg = self.other_vrm['forecast'].format(msg)
        self.update_forecast()
        return self.forecast_msg

    def friendly_sun_status(self, time_test, time_against, message):
        """
        Returns human friendly past, present or future message on the suns rise or set state

        :param datetime time_test: Tests this datetime value
        :param datetime time_against: Against this datetime value
        :param str message: String with placeholder for past, present or future status message
        :return: A friendly formatted time based message
        :rtype: str
        """
        pretty_date = self.time_utils.pretty_date(time_test, time_against)
        diff_msg = message.format(pretty_date)
        return diff_msg

    def generate_sun_status_message(self, test_time, time_range=None):
        """
        Compares passed in time to weather attribtues to determine if sunset/sunrise message should be include.
        Utilises a time range in and around the sunrise/sunset time to determine if the passed in time falls in to
        that category.

        :param time_range:
        :type time_range:
        :param test_time:
        :type test_time:
        :return:
        :rtype: str
        """
        if time_range is None:
            time_range = 1.5

        if self.sunrise and self.time_utils.time_within_range(self.sunrise, time_range, test_time):
            if self.sunrise < test_time:
                diff_msg = self.friendly_sun_status(self.sunrise, test_time, self.other_vrm['sunrise-past'])
            elif self.sunrise > test_time:
                diff_msg = self.friendly_sun_status(test_time, self.sunrise, self.other_vrm['sunrise-future'])
            else:
                return False
        elif self.sunset and self.time_utils.time_within_range(self.sunset, time_range, test_time):
            if self.sunset < test_time:
                diff_msg = self.friendly_sun_status(self.sunset, test_time, self.other_vrm['sunset-past'])
            elif self.sunset > test_time:
                diff_msg = self.friendly_sun_status(test_time, self.sunset, self.other_vrm['sunset-future'])
            else:
                return False
        else:
            return False

        return diff_msg

    def degree_to_compass(self, num):
        """
        Returns Compass direction from 16 co-ordinates based on Degree conversion.

        :param num: Degrees
        :type num: int
        :return: compass
        :rtype: str
        """
        val = int((num / 22.5) + .5)
        compass = [
            "North",
            "North northeast",
            "Northeast",
            "East northeast",
            "East",
            "East Southeast",
            "Southeast",
            "South southeast",
            "South",
            "South southwest",
            "Southwest",
            "West southwest",
            "West",
            "West northwest",
            "Northwest",
            "North northwest"
        ]
        return compass[(val % 16)]

    def get_weather_icon(self):
        """
        Retrieves the weather icon from OpenWeatherMaps based on the Weather Status code.

        :return: OWM Url for weather icon.
        :rtype: str
        """
        if self.wcode in self.weather_vrm and "icon" in self.weather_vrm[self.wcode]:
            icon = self.weather_vrm[self.wcode]["icon"]
            if self.wcode in ["800", "801", "802", "803", "804"]:
                if self.day_state in ["evening", "night"]:
                    icon += "n"
                else:
                    icon += "d"

            img_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
        else:
            img_url = ""

        return img_url

    def get_json(self, file_path):
        """
        Loads JSON formatted files.

        :param file_path: The JSON file name.
        :type file_path: str
        :param path: Optional path to JSON file location; defaults to WeDroid location.
        :type path: str
        :return: Returns a dictionary from JSON entries in a file.
        :rtype: dict
        """

        try:
            json_file = json.load(open(file_path))
            return json_file
        except FileNotFoundError as e:
            self.logger.cli_log("Exiting: Unable to find {}".format(file_path))
            exit()
        except JSONDecodeError as e:
            self.logger.cli_log("Exiting: Malformed JSON in {}".format(file_path))
            exit()

    def validate_json(self, data, validation_keys, validate_attributes=False):
        """
        Validates JSON file contents against a list of key names.

        :param data: dictionary JSON reference.
        :type data: dict
        :param validation_keys: List of key names to check exist.
        :type validation_keys: list
        :param validate_attributes: Set to true to validate key attributes.
        :type validate_attributes: bool
        :return:
        :rtype:
        """
        is_error = False
        for entry in validation_keys:
            # self.logger.cli_log("JSON entry: {}, {}".format(entry, validation_keys), "debug")

            if entry in data:
                # Validate weather attributes if set
                if validate_attributes:
                    if self.validate_weather_attributes(data[entry]):
                        continue
                    else:
                        is_error = True
                else:
                    continue
            else:
                is_error = True

            # Print entry error information
            if is_error:
                self.logger.cli_log("Error in JSON entry: {} ".format(entry))

        if is_error:
            self.logger.cli_log("Exiting critical JSON entries missing.")
            exit()
        else:
            return True

    def validate_weather_attributes(self, data):
        """
        Checks attributes for weather JSON entries to ensure requirements exist otherwise it exit the application.

        :param data:
        :type data:
        :return: Returns true on success, false if entry is missing.
        :rtype: bool
        """
        is_error = False
        validation_keys = ["title", "icon", "description"]

        for entry in validation_keys:
            if entry not in data:
                self.logger.cli_log("Missing JSON attribute: {} in {} ".format(entry, data))
                is_error = True

        if is_error:
            return False
        else:
            return True


def main():
    """
    WeDroid entry function for performing observations/forecasts.
    :return:
    """
    # Logging
    logger = LogKit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, help="Request type", default="observation")
    parser.add_argument("-lt", "--last_temp", type=float, help="Last weather temp", default="10.0")
    parser.add_argument("-lc", "--last_code", type=int, help="Last weather code", default="800")
    parser.add_argument("-v", "--verbose", help="Print object attributes for WeDroid", default=False,
                        type=bool, action=argparse.BooleanOptionalAction)
    # Forecast specific options:
    parser.add_argument("-i", "--interval", type=str,
                        help="Forecast interval time period formats include: 3h (minimum), 6h, daily", default="3h")
    parser.add_argument("-l", "--limit", type=int, help="Number of forecast results", default="6")
    parser.add_argument("-n", "--notification", help="Trigger a notification from WeDroid for observations",
                        default=False, type=bool, action=argparse.BooleanOptionalAction)
    # Config override
    parser.add_argument("-c", "--config", help="Override the path to the settings file",
                        default=None, type=str)
    args = parser.parse_args()

    request_type = args.type
    last_code = args.last_code
    last_temp = args.last_temp
    custom_config = args.config
    WEDROID_CONFIG = None

    # If custom config
    if custom_config and os.path.isfile(custom_config):
        WEDROID_CONFIG = custom_config

    wedroid = WeDroid(WEDROID_CONFIG)
    wedroid.set_prev_weather_attr(last_code, last_temp)
    report = None

    # Change the weather request type2
    if request_type == "observation":
        report = wedroid.generate_weather_announcement()
    elif request_type == "forecast":
        interval = args.interval
        limit = args.limit
        report = wedroid.generate_forecast_announcement(interval, limit)
    elif request_type == "outburst":
        report = wedroid.generate_weather_outburst()

    # Trigger webhook notifications for observation styled weather requests
    if request_type in ["observation", "outburst"]:
        notify = Notifications()
        notify.generate_notification(wedroid)

    # Exit if no valid report
    if not report:
        logger.cli_log("No observation was made")
        exit()

    logger.cli_log(report)

    # optionally print object attributes
    if 'verbose' in args and args.verbose:
        attrs = vars(wedroid)
        logger.cli_log('WeDroid Attributes: \n' + '\n'.join("    %s: %s" % item for item in attrs.items()), 'info')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

#  Copyright (c) 2019. Steven@oddineers.co.uk

import requests
import json
import traceback
from wedroid import logkit


class Notifications:
    def generate_notification(self, wedroid):
        # Return if object does not have an expected attribute
        if not hasattr(wedroid, 'location_source'):
            return False

        # Mattermost webhook example for posting results
        img_url = wedroid.get_weather_icon()

        source = ""
        if wedroid.location_source == "static":
            source = " (Default)"

        payload = {
            'username': wedroid.bot_name,
            'attachments': [
                {
                    "fallback": "The Weather",
                    "color": "#FF8000",
                    "pretext": "",
                    "text": "Brought to you by Pandora",
                    "author_name": "pandora",
                    #"author_icon": "https://oddineers.co.uk/",
                    "author_link": "https://oddineers.co.uk/",
                    "title": "The Weather",
                    "fields": [
                        {
                            "short": False,
                            "title": "Latest report",
                            "value": str(wedroid.last_report)
                        },
                        {
                            "short": True,
                            "title": "Temperature",
                            "value": str(wedroid.temp) + " &#176;C"
                        },
                        {
                            "short": True,
                            "title": "Weather Status",
                            "value": str(wedroid.status)
                        },
                        {
                            "short": True,
                            "title": "Wind speed",
                            "value": str(wedroid.wind_speed) + " mph"
                        },
                        {
                            "short": True,
                            "title": "Wind direction",
                            "value": str(wedroid.wind_direction)
                        },
                        {
                            "short": True,
                            "title": "State",
                            "value": str(wedroid.day_state)
                        },
                        {
                            "short": True,
                            "title": "Humidity",
                            "value": str(wedroid.humidity)
                        },
                        {
                            "short": True,
                            "title": "Sunrise",
                            "value": str(wedroid.sunrise)
                        },
                        {
                            "short": True,
                            "title": "Sunset",
                            "value": str(wedroid.sunset)
                        },
                        {
                            "short": True,
                            "title": "Longitude",
                            "value": str(wedroid.longitude)
                        },
                        {
                            "short": True,
                            "title": "Latitude",
                            "value": str(wedroid.latitude) + source
                        },
                        {
                            "short": True,
                            "title": "Weather Code",
                            "value": str(wedroid.wcode)
                        },
                    ],
                    "image_url": img_url,
                    "footer": "WeDroid v" + str(wedroid.version)
                }
            ]
        }
        self.post_message(wedroid.mattermost_url, payload)
    """

    """
    logkit = logkit.LogKit()

    def post_message(self, url, payload, headers=None):
        """
        POST a message to a url and optionally customise the request header.

        :param url: A Mattermost or Slack webhook
        :type url: str
        :param payload: Message contents.
        :type payload: dict
        :param headers: Define custom headers for the request; defaults to `'content-type': 'application/json'`
        :type headers: dict
        :return: Response status code on success.
        :rtype: int
        """
        if payload in ('', None):
            return self.logkit.cli_log('Empty payload provided.')

        if not isinstance(payload, dict):
            return self.logkit.cli_log('Payload expected as type: dict.')

        if url in ('', None):
            return self.logkit.cli_log('Invalid or empty notification url.')

        if isinstance(headers, dict):
            header = headers
        else:
            header = {'content-type': 'application/json'}

        try:
            response = requests.post(url, data=json.dumps(payload), headers=header)
            return response.status_code
        except Exception as e:
            self.logkit.cli_log(f"There was an error attempting url: {url}", 'error')
            self.logkit.cli_log(traceback.format_exc(), 'debug')
            return 400

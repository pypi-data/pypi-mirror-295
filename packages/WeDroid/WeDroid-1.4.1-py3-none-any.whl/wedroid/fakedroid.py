#  Copyright (c) 2020. Steven@oddineers.co.uk
from wedroid import logkit
from wedroid import termux


class FalseIntent:
    """
    Mirrors arguments from SL4A Android:makeIntent
    """
    def __init__(self, package, p2, p3, extras, result):
        self.package = package
        self.p2 = p2
        self.p3 = p3
        self.extras = extras
        self.result = result


class Android:
    """
    Fake Android class; functions are intended as monkey patched functions for use under non Android SL4A environments.
    Note:
    This was originally intended to allow WeDroid to more easily run across various OS's and when usage of WeDroid was
    primarily focused on Android via the SL4A project.
    Termux is now used for location acquisition with this Android class maintained to support older devices and SL4A.
    """
    def __init__(self):
        self.logger = logkit.LogKit()
        self.termux = termux.Termux()

    def ttsSpeak(self, speak: str):
        """
        Calls to ttsSpeak() are printed to the console.
        :param speak:
        :type str:
        :return: Void
        :rtype: None
        """
        self.logger.cli_log(speak, 'info')

    def getLastKnownLocation(self, provider: str = "gps", request: str = "once"):
        """
        Uses Android Termux emulator and the Termux-api package to access device location data in Python.

        :return: Returns location dict formatted similar to the SL4A Python 3 Android API.
        :rtype: dict
        """
        if provider not in ['gps', 'network', 'passive']:
            provider = "gps"
        if request not in ['once', 'last', 'updates']:
            request = "once"

        termux = self.termux.get_location(provider, request)

        if termux \
                and "longitude" in termux \
                and "latitude" in termux:
            location = [
                {'source': 'wedroid'},
                {
                    'passive': {
                        'longitude': termux['longitude'],
                        'latitude': termux['latitude']
                    }
                }
            ]
        else:
            location = None

        return location

    def makeIntent(self, package, p2, p3, extras):
        """
        Utilise the fake Intent class to safely pass the `makeIntent` data on non-Android based devices.

        :param package:
        :type package:
        :param p2:
        :type p2:
        :param p3:
        :type p3:
        :param extras:
        :type extras:
        :return: No intents supported message.
        :rtype: str
        """

        message = FalseIntent(package, p2, p3, extras, 'Fake Android module; no intents supported')
        result = message.result
        self.logger.cli_log(result)
        return result

    def sendBroadcastIntent(self, intent):
        """
        Fake `sendBroadcastIntent` functions print intent `contents` to console.

        :param intent:
        :type intent:
        :return:
        :rtype:
        """
        self.logger.cli_log(intent)
        pass

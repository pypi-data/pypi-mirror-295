#  Copyright (c) 2020. Steven@oddineers.co.uk
import json
import traceback
import subprocess
from wedroid import logkit


class Termux(object):
    logkit = logkit.LogKit()
    timeout = 30

    def get_location(self, provider: str = "gps", request: str = "once"):
        """
        Retrieves location data from Termux via the termux-location command.
        :param provider: Provider can be gps (default), network, passive
        :type provider: str
        :param request: Request can be once, last, updates
        :type request: str
        :return:
        :rtype:
        """
        if provider not in ['gps', 'network', 'passive']:
            provider = "gps"
        if request not in ['once', 'last', 'updates']:
            request = "once"
        cmd = f"termux-location -p {provider} -r {request}"
        data = None

        try:
            # Check if the command exists before popen
            resi = subprocess.check_output(cmd, shell=True, timeout=self.timeout)
            data = json.loads(resi)
            self.logkit.cli_log('Executed command: termux_location', 'info')
        except OSError as e:
            self.logkit.cli_log(
                'Attempted to execute a program that does not exist in current environment: %s' % cmd, 'error')
            pass
        except subprocess.CalledProcessError as e:
            self.logkit.cli_log('Sub program: <%s>, return not 0: %s' % (cmd, e), 'error')
            self.logkit.cli_log('Notice: Unable to find termux_location; Android Termux users please install '
                                'or update termux-api with `pkg install termux-api`', 'debug')
            self.logkit.cli_log(f"Error details: {traceback.format_exc()}", 'debug')
            pass
        except Exception as e:
            self.logkit.cli_log(e)
            pass
        finally:
            return data


if __name__ == '__main__':
    tmux = Termux()
    tmux.get_location()

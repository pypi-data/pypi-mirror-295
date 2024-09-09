import logging
import logging.config
import os
import sys
import traceback


# Single instance decorator
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class LogKit:
    def __init__(self, log_type="file"):
        if log_type == "file":
            self.log_cfg_file = os.path.dirname(os.path.abspath(__file__)) + '/log_config.ini'
            cfg_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../logs/')

            if not os.path.isdir(cfg_path):
                os.makedirs(cfg_path)

            self.logger = logging.getLogger('dev')
            logging.config.fileConfig(self.log_cfg_file)
            rfh = logging.handlers.RotatingFileHandler(cfg_path + '/app_log.txt', maxBytes=20000, backupCount=2)
            self.logger.addHandler(rfh)
            self.type = 'file'
        else:
            self.type = 'screen'

    def get_logger(self):
        return self.logger

    def set_log_level(self, level):
        return self.logger.setLevel(level)

    def format_exception(self, e="exception"):
        if e == "exception":
            exception_list = traceback.format_exc()
        else:
            exception_list = traceback.format_stack()

        exception_list = exception_list[:-2]
        exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
        exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        exception_str = "Traceback (most recent call last):\n"
        exception_str += "".join(exception_list)
        # Removing the last \n
        exception_str = exception_str[:-1]
        return str(exception_str)

    def clean_error(self, err, log_type='debug'):
        self.cli_log(str(err.args[0]) + " " + str(err.args[1]), log_type)

    def cli_log(self, message, log_type='info'):
        if self.type == "file":
            # Setup log rotation at 2MB per file with a max of 2 backup + 1 current (6 files).
            if log_type == 'critical':
                self.logger.critical(message)
            if log_type == 'error':
                self.logger.error(message)
            if log_type == 'warn':
                self.logger.warning(message)
            if log_type == 'info':
                self.logger.info(message)
            if log_type == 'debug':
                self.logger.debug(message)
        else:
            print(message)

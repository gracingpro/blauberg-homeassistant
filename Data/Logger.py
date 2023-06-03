import logging
import configparser

configfile = "config.ini"
config = configparser.ConfigParser()
config.read(configfile)
try:
    log_level = config.get("Log", "level")
except configparser.NoSectionError or configparser.NoOptionError:
    log_level = "INFO"


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_basic = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS_basic = {
        logging.DEBUG: green + format_basic + reset,
        logging.INFO: green + format_basic + reset,
        logging.WARNING: yellow + format_basic + reset,
        logging.ERROR: red + format_basic + reset,
        logging.CRITICAL: bold_red + format_basic + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS_basic.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


ch = logging.StreamHandler()
ch.setLevel(log_level)
ch.setFormatter(CustomFormatter())

logger = logging.getLogger('blauberg-homeassistant')
logger.setLevel(log_level)
logger.addHandler(ch)

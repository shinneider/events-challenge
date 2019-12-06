import logging
import logging.config
from config.settings import LOGGING


class Logger():
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger('crawler')

    @classmethod
    def _log(cls, msg, *args, **kwargs):
        return msg

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.log.debug(cls._log(msg, *args, **kwargs))

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.log.info(cls._log(msg, *args, **kwargs))

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.log.warning(cls._log(msg, *args, **kwargs))

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.log.error(cls._log(msg, *args, **kwargs))
    
    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls.log.critical(cls._log(msg, *args, **kwargs))


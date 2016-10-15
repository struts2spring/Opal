import os
import logging
import sys
from logging.handlers import RotatingFileHandler

try:
    if sys.platform == 'win32':
        import tempfile
        print tempfile.gettempdir()
        f = tempfile.TemporaryFile(mode='w+t')
        print 'temp.name:', f.name
        LOG_FILENAME = os.path.join(tempfile.gettempdir(),'opal' + ".log")
    else:
        LOG_FILENAME = os.path.join('/tmp','opal' + ".log")
#     LOG_FILENAME = os.path.join('tmp',os.path.splitext(__file__)[0] + ".log")
except:
    LOG_FILENAME =os.path.join( '/tmp',__file__ + ".log")

class Singleton(object):
    """
    Singleton interface:
    http://www.python.org/download/releases/2.2.3/descrintro/#__new__    
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass

class LoggerManager(Singleton):
    """
    Logger Manager.
    Handles all logging files.
    """
    def init(self, loggername):
        # define a Handler which writes INFO messages or higher to the sys.stderr
        self.console = logging.StreamHandler()
        self.console .setLevel(logging.INFO)
        self.logger = logging.getLogger(loggername)
        rhandler = None
        try:
            rhandler = RotatingFileHandler(
                    LOG_FILENAME,
                    mode='a',
                    maxBytes=10 * 1024 * 1024,
                    backupCount=5
                )
        except:
            raise IOError("Couldn't create/open file \"" + \
                          LOG_FILENAME + "\". Check permissions.")
        
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
#             fmt = '[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)-8s] %(message)s',
            fmt='[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)-8s] %(message)s',
            datefmt='%F %H:%M:%S'
        )
        self.console.setFormatter(formatter)
        rhandler.setFormatter(formatter)
        self.logger.addHandler(rhandler)
        self.logger.addHandler(self.console)

    def debug(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.debug(msg)

    def error(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.error(msg)

    def info(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.info(msg)

    def warning(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.warning(msg)

class Logger(object):
    """
    Logger object.
    """
    def __init__(self, loggername="root"):
        self.lm = LoggerManager(loggername)  # LoggerManager instance
        self.loggername = loggername  # logger name

    def debug(self, msg):
        self.lm.debug(self.loggername, msg)

    def error(self, msg):
        self.lm.error(self.loggername, msg)

    def info(self, msg):
        self.lm.info(self.loggername, msg)

    def warning(self, msg):
        self.lm.warning(self.loggername, msg)

if __name__ == '__main__':

    logger = Logger()
    logger.debug("this testname.")

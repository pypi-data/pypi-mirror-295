"""
Module docstring
"""

import abc
import logging
import sys
from contextlib import contextmanager
from io import StringIO
from logging import handlers
from typing import Union

import yaml

__all__ = ["Logger", "get_logger"]


class Singleton(type):
    """
    A singleton class for unique instantiation of the logger.
    """

    _instance = None

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(logging.Logger, metaclass=Singleton):
    """
    The class of the main logging channel.

    Methods
    -------
    from_config(cls)
        Instantiate the logger from a configuration file.
    get_child(name)
        Get a logger which is a descendant to the main logger.
    get_name(cls)
        Get the name of the logger.
    set_level(level)
        Set the lowest severity level to be be logged.

    See also
    --------
    logging.Logger: The base Logger class.
    """

    _name = "AIXD"
    _config = "logger.yaml"

    def __init__(self):
        super().__init__(self._name)

    def get_child(self, name):
        """
        Get a logger that is a descendant to the main logger.

        Parameters
        ----------
        name: str
            The name of the descendant logger.
        """

        return self.getChild(name)

    def set_verbosity(self, level):
        """
        Set the lower severity level to be logged.

        Parameters
        ----------
        level: (0, 10, 20, 30, 40, 50)
            The logging level numeric value, corresponding to notset, debug,
            info, warning, error and critical.
        """

        self.setLevel(level)

    @classmethod
    def get_name(cls):
        """
        Get the main logger name.
        """

        return cls._name

    @classmethod
    def from_config(cls):
        """
        Instantiate the logger using a configuration file.

        Returns
        -------
        logger: Logger
            The file-configured instance of the logger.

        Raises
        ------
        FileNotFoundError
            If the configuration file does not exist.
        """

        config_file = cls._config

        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file.read())

            logging.config.dictConfig(config)

            # ValueError: when a wrong value is specified as attribute
            # further config errors should be caught here

            # check the logger name, if different than the default
            name = cls.get_name()
            logger = logging.getLogger(name)

        except FileNotFoundError:
            raise FileNotFoundError("{} does not exist".format(config_file))

        return logger


class MemoryLogger:
    """
    The in-memory logger class for streaming logs to a memory channel which is
    instantiated and released using a context manager.

    Methods
    -------
    get_logs()
        Get the in-memory streamed logs.
    """

    def __init__(self, level=None):
        self.logger = get_logger()

        if level is None:
            level = self.logger.level

        self.level = level

    def __enter__(self):
        self._memory_log = StringIO()
        self._memory_handler = logging.StreamHandler(self._memory_log)
        self._memory_handler.setLevel(self.level)

        message_format = "%(asctime)s [%(levelname)s - %(name)s] %(message)s"
        date_format = "%d/%m/%Y %H:%M:%S"
        formatter = logging.Formatter(message_format, date_format)

        self._memory_handler.setFormatter(formatter)
        self.logger.addHandler(self._memory_handler)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.removeHandler(self._memory_handler)

    def get_logs(self):
        return self._memory_log.getvalue()


class Builder(abc.ABC):
    """
    An abstract interface for creating the parts of the logger.
    """

    def __init__(self):
        self.logger = Logger()
        self.logger.setLevel(logging.DEBUG)

        name = self.logger.get_name()
        logging.root.manager.loggerDict[name] = self.logger

    @abc.abstractmethod
    def add_handlers(self):
        pass

    @abc.abstractmethod
    def add_filters(self):
        pass

    @abc.abstractmethod
    def build(self):
        pass


class Basic(Builder):
    """
    A builder class that constructs a basic version of the logger. This basic
    version consists of two handlers, one streaming to the standard output
    stream and a second one streaming to a rotating log file.
    """

    def add_handlers(self):
        """
        Add the standard output stream and rotating log file handlers. The
        logging level is set to INFO for both handlers.
        """

        # Add a standard output stream handler

        level = logging.INFO
        msg_format = "[%(levelname)s - %(name)s] %(message)s"
        formatter = logging.Formatter(msg_format)

        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Add a rotating file handler

        level = logging.INFO
        msg_format = "%(asctime)s [%(levelname)s - %(name)s] %(message)s"
        date_format = "%d/%m/%Y %H:%M:%S"
        formatter = logging.Formatter(msg_format, date_format)

        logger_name = self.logger.get_name()
        file = "{}.log".format(logger_name)
        size = 200 * 1024 * 1024  # 200 Mbs
        backup = 2  # 2 files

        file_handler = handlers.RotatingFileHandler(file, maxBytes=size, backupCount=backup)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def add_filters(self):
        """
        Description
        """

        # to be implemented according to the module requirements

        pass

    def build(self):
        """
        Build the logger by assembling the handlers and filters.

        Returns
        -------
        logger: Logger
            The instantiated logger.
        """

        self.add_handlers()
        self.add_filters()

        return self.logger


def get_logger():
    """
    Return the main logger of the package. The logger is by default
    instantiated using the configuration file. If this does not exist or
    contains errors, the logger is instantiated using the Basic builder.

    Returns
    -------
    logger: logging.Logger
        The main package logger.

    See also
    --------
    Basic: The basic logger builder.
    """

    name = Logger.get_name()
    loggers = logging.root.manager.loggerDict.keys()

    if name not in loggers:
        try:
            logger = Logger.from_config()

        except FileNotFoundError:
            builder = Basic()
            logger = builder.build()

    else:
        logger = logging.getLogger(name)

    return logger


@contextmanager
def temporary_logger_level(logger: logging.Logger, new_level: Union[int, str]):
    """
    A context manager that temporarily sets the logging level of the logger. After exiting the context, the logging level is restored to its original value.
    """
    old_level = logger.level
    logger.setLevel(new_level)
    try:
        yield
    finally:
        logger.setLevel(old_level)

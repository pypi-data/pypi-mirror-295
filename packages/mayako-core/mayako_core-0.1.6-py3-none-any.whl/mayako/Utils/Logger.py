from enum import Enum
import logging
from logging.handlers import QueueHandler
from queue import Queue
import sys

class LoggingLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LoggingDestination(Enum):
    STDOUT = "STDOUT"
    QUEUE = "QUEUE"

LoggerType = logging.Logger

class Logger:
    # IMPORTANT: use LoggingLevel.INFO if you want to see events from the network such as BATTERY_INFO
    #instantiate this class in client with enable/disable logger => enable is sufficient i guess
    #only for loop events
    #for setup use execptions
    #https://stackoverflow.com/a/44401529
    _LOG_FORMAT:str = '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    #TODO: debug formater w
    _logger: LoggerType

    def init_logger(self, logging_level: LoggingLevel = LoggingLevel.INFO, destination: LoggingDestination = LoggingDestination.STDOUT, output_format: str = _LOG_FORMAT, queue: Queue = None) -> None:
        self._logging_level: LoggingLevel = logging_level
        self._destination = destination
        self._output_format = output_format
        self._queue = queue
        
        """ if self._logger:
            raise Exception("Logger instance already exists") """

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(LoggingLevel.DEBUG.name)

        self._handler = self._define_handler(self._destination, self._queue)
        self._handler.setLevel(self._logging_level.value)
        fmt = logging.Formatter(self._output_format)
        self._handler.setFormatter(fmt)

        self._logger.addHandler(self._handler)

    #need a place where we write the logs: file, std:out, network, whatever
    def _define_handler(self, destination: LoggingDestination, queue: Queue) -> logging.Handler:
        output: logging.Handler
        
        if destination == LoggingDestination.STDOUT:
            output = logging.StreamHandler(stream=sys.stdout)

        elif destination == LoggingDestination.QUEUE:
            if type(queue) is not Queue:
                raise TypeError(f"using {LoggingDestination.QUEUE} requires a queue")
            
            output = QueueHandler(queue)

        else:
            raise NotImplementedError(f"{destination.value} is not implemented")
        
        return output
    
    def get(self) -> LoggerType:
        return self._logger

LoggerInstance = Logger()
from typing import Dict, Callable, List

from .Utils.Logger import LoggerInstance, LoggerType


class Observable:

    _observers: Dict[str, List[Callable]]
    _logger: LoggerType

    def __init__(self):
        self._observers = {}
        self._logger = LoggerInstance.get()

    def subscribe(self, event: str, callback: Callable) -> None:
        if not callable(callback):
            raise TypeError(CERROR_MESSAGES.TYPE_MUST_BE_CALLABLE)

        try:
            self._observers[event].append(callback)
        except:
            self._observers[event] = [callback]

    def _notify_observers(self, event):
        if not event in self._observers.keys():
            return

        for callback in self._observers[event]:
            callback(self)
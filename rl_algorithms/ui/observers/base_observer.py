# ui/observers/base_observer.py
from abc import ABC, abstractmethod

class UIObserver(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict = None):
        pass
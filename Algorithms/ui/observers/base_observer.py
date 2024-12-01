from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass
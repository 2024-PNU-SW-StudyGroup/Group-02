# ui/observers/base_observer.py
from abc import ABC, abstractmethod

class UIObserver(ABC):
    """
    Abstract base class for UI observers in the visualization system.

    Methods
    -------
    update(event_type: str, data: dict = None)
        Abstract method to handle events and update the UI accordingly.
    """
    @abstractmethod
    def update(self, event_type: str, data: dict = None):
        """
        Abstract method to be implemented by subclasses for handling events.

        Parameters
        ----------
        event_type : str
            The type of the event being handled (e.g., 'algorithm_changed').
        data : dict, optional
            Additional data associated with the event (default is None).
        """
        pass
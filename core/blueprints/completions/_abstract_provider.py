from abc import ABC, abstractmethod


class CompletionProvider(ABC):
    
    def __init__(self, app):
        """
        Constructor that enforces setting an attribute.
        """
        self._app = app
        
        
    @abstractmethod
    def stream_completion(self, user, lm, **kwargs):
        """
        Abstract method stream completion. Implement logic for streaming here. You likely need the _app attribute here.
        """
        pass

    @abstractmethod
    def chunk_completion(self, user, lm, **kwargs):
        """
        Abstract method stream completion. Implement logic for chunk completion here.
        """
        pass
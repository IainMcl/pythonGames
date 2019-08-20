from abc import ABC

class ScreenObject(ABC):
    @abstractmethod
    def draw(self, win):
        pass


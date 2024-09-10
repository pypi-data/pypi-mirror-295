from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np


class BasePlatformCapture(ABC):
    """
    Abstract base class for platform-specific capture implementations.
    """

    @abstractmethod
    def capture_screen(self) -> np.ndarray:
        pass

    @abstractmethod
    def capture_region(self, region: Tuple[int, int, int, int]) -> np.ndarray:
        pass

    @abstractmethod
    def capture_window(self, window_title: str) -> np.ndarray:
        pass

    @abstractmethod
    def list_monitors(self) -> List[dict]:
        pass

    @abstractmethod
    def capture_monitor(self, monitor_id: int) -> np.ndarray:
        pass

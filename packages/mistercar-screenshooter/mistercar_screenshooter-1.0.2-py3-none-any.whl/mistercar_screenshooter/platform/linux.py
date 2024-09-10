from typing import List, Tuple
import numpy as np
from mss import mss
from mistercar_screenshooter.exceptions import CaptureError, WindowNotFoundError
from mistercar_screenshooter.platform.base import BasePlatformCapture


class LinuxCapture(BasePlatformCapture):
    """Linux-specific implementation of screen capture functionality."""

    def __init__(self):
        self.sct = mss()

    def capture_screen(self) -> np.ndarray:
        """Capture the entire screen."""
        try:
            monitor = self.sct.monitors[0]  # Full screen
            sct_img = self.sct.grab(monitor)
            return np.array(sct_img)
        except Exception as e:
            raise CaptureError(f"Failed to capture screen: {str(e)}")

    def capture_region(self, region: Tuple[int, int, int, int]) -> np.ndarray:
        """Capture a specific region of the screen."""
        try:
            sct_img = self.sct.grab(region)
            return np.array(sct_img)
        except Exception as e:
            raise CaptureError(f"Failed to capture region: {str(e)}")

    def capture_window(self, window_title: str) -> np.ndarray:
        """Capture a specific window."""
        # Note: This is a placeholder. Actual implementation would require
        # additional libraries like Xlib to find and capture specific windows.
        raise NotImplementedError("Window capture is not implemented for Linux")

    def list_monitors(self) -> List[dict]:
        """List all available monitors."""
        return self.sct.monitors[1:]  # Exclude the "all in one" monitor

    def capture_monitor(self, monitor_id: int) -> np.ndarray:
        """Capture a specific monitor."""
        try:
            monitor = self.sct.monitors[monitor_id]
            sct_img = self.sct.grab(monitor)
            return np.array(sct_img)
        except Exception as e:
            raise CaptureError(f"Failed to capture monitor: {str(e)}")

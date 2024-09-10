import ctypes
import ctypes.wintypes
from typing import List, Tuple, Any

import bettercam
import numpy as np
import win32gui
import win32ui

from mistercar_screenshooter.exceptions import WindowNotFoundError, CaptureError
from mistercar_screenshooter.platform.base import BasePlatformCapture


class WindowsCapture(BasePlatformCapture):
    """Windows-specific implementation of screen capture functionality."""

    def __init__(self):
        self.camera = bettercam.create(output_color="RGB")

    def capture_screen(self) -> np.ndarray:
        """Capture the entire screen."""
        try:
            return self.camera.grab()
        except Exception as e:
            raise CaptureError(f"Failed to capture screen: {str(e)}")

    def capture_region(self, region: Tuple[int, int, int, int]) -> np.ndarray:
        """Capture a specific region of the screen."""
        try:
            return self.camera.grab(region=region)
        except Exception as e:
            raise CaptureError(f"Failed to capture region: {str(e)}")

    def capture_window(self, window_title: str) -> np.ndarray:
        """Capture a specific window."""
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            if not hwnd:
                raise WindowNotFoundError(f"Window not found: {window_title}")

            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)

            result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
            if result == 0:
                raise CaptureError(f"Failed to capture window: {window_title}")

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            img = np.frombuffer(bmpstr, dtype=np.uint8).reshape(height, width, 4)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)

            return img[:, :, :3]  # Remove alpha channel

        except WindowNotFoundError:
            raise
        except Exception as e:
            raise CaptureError(f"Failed to capture window: {str(e)}")

    def list_monitors(self) -> List[dict]:
        """List all available monitors."""
        from mss import mss
        return mss().monitors[1:]  # # Exclude the "all in one" monitor

    def capture_monitor(self, monitor_id: int) -> np.ndarray:
        """Capture a specific monitor."""
        try:
            camera = bettercam.create(output_idx=monitor_id, output_color="RGB")
            return camera.grab()
        except Exception as e:
            raise CaptureError(f"Failed to capture monitor: {str(e)}")

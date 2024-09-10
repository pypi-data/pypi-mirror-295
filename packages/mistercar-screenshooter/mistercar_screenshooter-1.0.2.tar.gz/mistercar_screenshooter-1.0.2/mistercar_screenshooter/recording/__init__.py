from typing import Any
import platform
from mistercar_screenshooter.recording.frame_buffer import FrameBuffer
from mistercar_screenshooter.recording.bettercam_recorder import BetterCamRecorder


def create_recorder(capture_type: str, target: Any = None, target_fps: int = 60) -> FrameBuffer or BetterCamRecorder:
    """
    Create a Recorder object for background recording.

    Args:
        capture_type (str): Type of capture ('screen', 'region', 'window', or 'monitor')
        target (Any): Target for the capture (region tuple, window title, or monitor id)
        target_fps (int): Target FPS for the capture

    Returns:
        FrameBuffer or BetterCamRecorder: A Recorder object set up for the specified capture type.
    """
    if platform.system().lower() == "windows" and capture_type != "window":
        # Use BetterCam for Windows, except for window capture
        from mistercar_screenshooter.platform.windows import WindowsCapture
        camera = WindowsCapture().camera
        return BetterCamRecorder(camera, capture_type, target, target_fps)
    else:
        # Use FrameBuffer for non-Windows platforms and window capture on Windows
        if platform.system().lower() == "windows":
            from mistercar_screenshooter.platform.windows import WindowsCapture
            capture = WindowsCapture()
        elif platform.system().lower() == "linux":
            from mistercar_screenshooter.platform.linux import LinuxCapture
            capture = LinuxCapture()
        elif platform.system().lower() == "darwin":
            from mistercar_screenshooter.platform.macos import MacOSCapture
            capture = MacOSCapture()
        else:
            raise ValueError(f"Unsupported platform: {platform.system()}")

        if capture_type == "screen":
            def capture_func():
                return capture.capture_screen()
        elif capture_type == "region":
            def capture_func():
                return capture.capture_region(target)
        elif capture_type == "window":
            def capture_func():
                return capture.capture_window(target)
        elif capture_type == "monitor":
            def capture_func():
                return capture.capture_monitor(target)
        else:
            raise ValueError(f"Invalid capture type: {capture_type}")

        return FrameBuffer(capture_func, target_fps)

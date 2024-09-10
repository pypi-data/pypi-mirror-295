import platform
import time
from typing import Any, List, Tuple
import numpy as np
from mistercar_screenshooter.exceptions import UnsupportedPlatformError
from mistercar_screenshooter.recording import create_recorder, FrameBuffer, BetterCamRecorder
from mistercar_screenshooter.recording.video import VideoWriter


class ScreenCapture:
    """
    Main class for screen capture functionality across all platforms.
    """

    def __init__(self):
        """Initialize the ScreenCapture object with the appropriate platform-specific implementation."""
        system = platform.system().lower()
        if system == "windows":
            from mistercar_screenshooter.platform.windows import WindowsCapture
            self._impl = WindowsCapture()
        elif system == "linux":
            from mistercar_screenshooter.platform.linux import LinuxCapture
            self._impl = LinuxCapture()
        elif system == "darwin":
            from mistercar_screenshooter.platform.macos import MacOSCapture
            self._impl = MacOSCapture()
        else:
            raise UnsupportedPlatformError(f"Unsupported platform: {system}")

    def capture_screen(self) -> np.ndarray:
        """
        Capture the entire screen.

        Returns:
            np.ndarray: The captured screen image as a numpy array.
        """
        return self._impl.capture_screen()

    def capture_region(self, region: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Capture a specific region of the screen.

        Args:
            region (Tuple[int, int, int, int]): The region to capture (left, top, width, height).

        Returns:
            np.ndarray: The captured region image as a numpy array.
        """
        return self._impl.capture_region(region)

    def capture_window(self, window_title: str) -> np.ndarray:
        """
        Capture a specific window.

        Args:
            window_title (str): The title of the window to capture.

        Returns:
            np.ndarray: The captured window image as a numpy array.
        """
        return self._impl.capture_window(window_title)

    def list_monitors(self) -> List[dict]:
        """
        List all available monitors.

        Returns:
            List[dict]: A list of dictionaries containing information about each monitor.
        """
        return self._impl.list_monitors()

    def capture_monitor(self, monitor_id: int) -> np.ndarray:
        """
        Capture a specific monitor.

        Args:
            monitor_id (int): The ID of the monitor to capture.

        Returns:
            np.ndarray: The captured monitor image as a numpy array.
        """
        return self._impl.capture_monitor(monitor_id)

    def create_recorder(self, capture_type: str, target: Any = None, target_fps: int = 60) -> FrameBuffer or BetterCamRecorder:
        """
        Create a recorder object for background recording.

        Args:
            capture_type (str): Type of capture ('screen', 'region', 'window', or 'monitor')
            target (Any): Target for the capture (region tuple, window title, or monitor id)
            target_fps (int): Target FPS for the capture

        Returns:
            FrameBuffer or BetterCamRecorder: A recorder object set up for the specified capture type.
        """
        return create_recorder(capture_type, target, target_fps)

    def create_video_writer(self, filename: str, fps: int = 30, codec: str = "mp4v") -> VideoWriter:
        """
        Create a VideoWriter object for saving captures as a video file.

        Args:
            filename (str): Name of the output video file.
            fps (int): Frames per second for the output video.
            codec (str): Four-character code of codec used to compress the frames.

        Returns:
            VideoWriter: A VideoWriter object set up for the specified output.
        """
        return VideoWriter(filename, fps, codec)

    def record_video(self, filename: str, duration: float, capture_type: str = "screen",
                     target: Any = None, fps: int = 30):
        """
        Record a video for a specified duration.

        Args:
            filename (str): Name of the output video file.
            duration (float): Duration of the video in seconds.
            capture_type (str): Type of capture ('screen', 'region', 'window', or 'monitor')
            target (Any): Target for the capture (region tuple, window title, or monitor id)
            fps (int): Frames per second for the output video.
        """
        recorder = self.create_recorder(capture_type, target, fps)
        recorder.start()

        frames = []
        start_time = time.time()
        end_time = start_time + duration

        while time.time() < end_time:
            frame = recorder.get_latest_frame()
            if frame is not None:
                frames.append(frame)

        recorder.stop()

        if frames:
            with VideoWriter(filename, fps) as writer:
                writer.write(frames)

        print(f"Video saved with {len(frames)} frames.")

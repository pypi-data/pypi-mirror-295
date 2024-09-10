import cv2
import numpy as np
from typing import List


class VideoWriter:
    """
    Class for handling video writing functionality.
    """

    def __init__(self, filename: str, fps: int = 30, codec: str = "mp4v"):
        """
        Initialize the VideoWriter.

        Args:
            filename (str): Name of the output video file.
            fps (int): Frames per second for the output video.
            codec (str): Four-character code of codec used to compress the frames.
        """
        self.filename = filename
        self.fps = fps
        self.codec = codec
        self.writer = None
        self.frame_size = None

    def initialize(self, frame_size: tuple):
        """
        Initialize the cv2.VideoWriter object.
        Args:
            frame_size (tuple): The size of the video frames (width, height).
        """
        if self.writer is None:
            self.frame_size = frame_size
            fourcc = cv2.VideoWriter_fourcc(*self.codec)
            self.writer = cv2.VideoWriter(self.filename, fourcc, self.fps, self.frame_size)

    def write(self, frames: List[np.ndarray]):
        """
        Write a batch of frames to the video file.

        Args:
            frames (List[np.ndarray]): List of frames to write, in RGB format.
        """
        if not frames:
            return

        if self.writer is None:
            self.initialize((frames[0].shape[1], frames[0].shape[0]))

        for frame in frames:
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.writer.write(bgr_frame)

    def release(self):
        """
        Release the VideoWriter and finalize the video file.
        """
        if self.writer is not None:
            self.writer.release()
            self.writer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

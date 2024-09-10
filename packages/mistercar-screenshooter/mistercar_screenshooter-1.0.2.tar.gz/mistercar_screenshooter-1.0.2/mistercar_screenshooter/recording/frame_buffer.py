import threading
import time
from collections import deque
from typing import Callable, Optional, List
import numpy as np


class FrameBuffer:
    """
    Class for handling background frame capture and buffering.
    """

    def __init__(self, capture_func: Callable, fps: int = 30, buffer_size: int = 1000):
        self.capture_func = capture_func
        self.fps = fps
        self.buffer = deque(maxlen=buffer_size)
        self.running = False
        self.paused = False
        self.thread = None
        self.lock = threading.Lock()
        self.new_frame_event = threading.Event()

    def start(self):
        self.running = True
        self.paused = False
        self.thread = threading.Thread(target=self._record_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def get_latest_frame(self) -> Optional[np.ndarray]:
        self.new_frame_event.wait()
        self.new_frame_event.clear()
        with self.lock:
            return self.buffer[-1] if len(self.buffer) > 0 else None

    def get_latest_frames(self, n: int) -> List[np.ndarray]:
        with self.lock:
            return list(self.buffer)[-n:]

    def _record_loop(self):
        while self.running:
            if not self.paused:
                frame = self.capture_func()
                with self.lock:
                    self.buffer.append(frame)
                self.new_frame_event.set()
            time.sleep(1 / self.fps)

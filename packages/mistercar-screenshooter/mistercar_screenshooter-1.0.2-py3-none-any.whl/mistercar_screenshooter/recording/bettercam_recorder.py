from typing import Any
import numpy as np
import bettercam


class BetterCamRecorder:
    """
    Recorder class specifically for BetterCam on Windows.
    """

    def __init__(self, camera, capture_type: str, target: Any = None, target_fps: int = 60):
        self.camera = camera
        self.capture_type = capture_type
        self.target = target
        self.target_fps = target_fps

    def start(self):
        if self.capture_type == "region" and self.target:
            self.camera.start(region=self.target, video_mode=True, target_fps=self.target_fps)
        elif self.capture_type == "monitor" and self.target is not None:
            self.camera = bettercam.create(output_idx=self.target, output_color="RGB")
            self.camera.start(video_mode=True, target_fps=self.target_fps)
        else:
            self.camera.start(video_mode=True, target_fps=self.target_fps)

    def stop(self):
        self.camera.stop()

    def get_latest_frame(self) -> np.ndarray:
        return self.camera.get_latest_frame()

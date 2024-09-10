# 📸 **MisterCar ScreenShooter** 💥

🚀 A versatile, high-performance Python package for cross-platform screen capturing and recording. It offers functionality for full screen, region, window, and monitor capture, as well as video recording capabilities. 🎞️

## 🛠️ Installation

```bash
pip install mistercar_screenshooter
```

## 📚 Usage

Here's a comprehensive example demonstrating all the main features of screenshooter:

```python
from mistercar_screenshooter import ScreenCapture
import cv2
import time

# Create a ScreenCapture instance
sc = ScreenCapture()

# 1. Capture the entire screen
screen = sc.capture_screen()
cv2.imwrite("full_screen.png", cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))

# 2. Capture a specific region
region = sc.capture_region((100, 100, 500, 500))
cv2.imwrite("region.png", cv2.cvtColor(region, cv2.COLOR_RGB2BGR))

# 3. Capture a specific window (Windows only)
try:
    window = sc.capture_window("*Untitled - Notepad")
    cv2.imwrite("window.png", cv2.cvtColor(window, cv2.COLOR_RGB2BGR))
except NotImplementedError:
    print("Window capture is not supported on this platform.")

# 4. List and capture from multiple monitors
monitors = sc.list_monitors()
for i, monitor in enumerate(monitors):
    img = sc.capture_monitor(i)
    cv2.imwrite(f"monitor_{i}.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

# 5. Record a video
sc.record_video("output.mp4", duration=5, fps=60, capture_type="screen")

# 6. Use the recorder for continuous capture
recorder = sc.create_recorder("screen")
recorder.start()
start_time = time.time()
frame_count = 0
while time.time() - start_time < 5:  # Record for 5 seconds
    frame = recorder.get_latest_frame()
    # In a real application, you might process or save the frame here
    frame_count += 1
recorder.stop()
print(f"Captured {frame_count} frames in 5 seconds (approx. {frame_count / 5:.2f} FPS)")
```

This example covers all main functionalities:
1. 📷 Full screen capture
2. 🔍 Region capture
3. 🪟 Window capture (Windows only)
4. 🖥️🖥️ Multiple monitor support
5. 🎥 Video recording
6. 🔄 Continuous capture with the recorder

You can find this example as a runnable script in the `examples/demo.py` file in the repository.

## Platform-specific notes

### 🪟 Windows

On Windows, screenshooter uses the BetterCam library for high-performance screen capture. This provides several benefits:

- ⚡ High-speed capture (240Hz+ capable)
- 🎮 Ability to capture from Direct3D exclusive full-screen applications
- 🖼️ Automatic adjustment for scaled/stretched resolutions

### 🐧 Linux and 🍎 macOS

On Linux and macOS, screenshooter uses the MSS (Multiple Screen Shot) library for screen capture. While it doesn't offer the same level of performance as BetterCam on Windows, it provides a consistent cross-platform experience.

## 🙏 Acknowledgements

ScreenShooter is built upon these fantastic projects:

- 🖼️ [BetterCam](https://github.com/RootKit-Org/BetterCam): The world's fastest Python screenshot library for Windows.
- 🖥️ [MSS (Multiple Screen Shot)](https://github.com/BoboTiG/python-mss): An ultra fast cross-platform multiple screenshots module in pure Python using ctypes.

We're grateful to the maintainers and contributors of these projects for their excellent work!

## 🧪 Testing

To run the tests, install pytest and run:

```bash
pytest tests/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

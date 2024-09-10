import numpy as np
import cv2


def convert_to_rgb(image: np.ndarray) -> np.ndarray:
    """Convert an image to RGB format."""
    if image.shape[-1] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif image.shape[-1] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    else:
        raise ValueError("Unsupported image format")


def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize an image to the specified dimensions."""
    return cv2.resize(image, (width, height))

class ScreenshooterError(Exception):
    """Base exception for mistercar_screenshooter package."""
    pass


class CaptureError(ScreenshooterError):
    """Raised when a capture operation fails."""
    pass


class WindowNotFoundError(ScreenshooterError):
    """Raised when a specified window is not found."""
    pass


class UnsupportedPlatformError(ScreenshooterError):
    """Raised when the current platform is not supported."""
    pass

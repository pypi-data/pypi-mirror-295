"""anysynth root package."""

try:
    from anysynth import _version

    __version__ = _version.__version__
except Exception:
    __version__ = ""


__all__ = [
    "__version__",
]

"""
Plover Steno Engine Hooks Logger - A Plover extension to log out the contents of
steno engine hooks.
"""
from plover.engine import StenoEngine

from .steno_engine_hooks import Logger


class StenoEngineHooksLoggerExtension(Logger):
    """
    Plover entry point extension class to log the contents of steno engine
    hooks.
    """
    _engine: StenoEngine
    _log_marker: str

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine
        self._log_marker = "[STENO ENGINE HOOK (EXTENSION)]"

    def start(self) -> None:
        """
        Sets up steno engine hooks
        """
        for hook in self._HOOKS:
            self._engine.hook_connect(hook, getattr(self, f"_{hook}"))

    def stop(self) -> None:
        """
        Tears down the steno engine hooks
        """
        for hook in self._HOOKS:
            self._engine.hook_disconnect(hook, getattr(self, f"_{hook}"))

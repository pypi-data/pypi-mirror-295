"""
Plover Steno Engine Hooks Logger - A Plover GUI Tool to log out the contents of
steno engine hooks using Qt signals.
"""
from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Any,
    Dict,
    List
)

from plover import log
from plover.formatting import _Action
from plover.steno import Stroke
from plover.steno_dictionary import StenoDictionaryCollection


class Logger(ABC):
    """
    Contains implementation code for logging out contents of Plover steno engine
    hooks.
    """
    _HOOKS: list[str] = [
        "add_translation",
        "config_changed",
        "configure",
        "dictionaries_loaded",
        "focus",
        "lookup",
        "machine_state_changed",
        "output_changed",
        "quit",
        "send_backspaces",
        "send_key_combination",
        "send_string",
        "stroked",
        "suggestions",
        "translated",
    ]
    _log_marker: str

    @abstractmethod
    def __init__(self) -> None:
        self._log_marker = "[STENO ENGINE HOOK]"

    def _add_translation(self) -> None:
        """
        The Add Translation command was activated – open the Add Translation
        tool.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `add_translation()` called"
        )

    def _config_changed(self, config: Dict[str, Any]) -> None:
        """
        The configuration was changed, or it was loaded for the first time.
        `config` is a dictionary containing only the changed fields.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `config_changed(config: Dict[str, any])` called:\n"
            f"    `config`: {config}"
        )

    def _configure(self) -> None:
        """
        The Configure command was activated – open the configuration window.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `configure()` called"
        )

    def _dictionaries_loaded(
        self,
        dictionaries: StenoDictionaryCollection
    ) -> None:
        """
        The dictionaries were loaded, either when Plover starts up or the system
        is changed or when the engine is reset.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK "
            "`dictionaries_loaded(dictionaries: StenoDictionaryCollection)` "
            "called:\n"
            f"    `dictionaries`: {dictionaries}"
        )

    def _focus(self) -> None:
        """
        The Show command was activated – reopen Plover's main window and bring
        it to the front.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `focus()` called"
        )

    def _lookup(self) -> None:
        """
        The Lookup command was activated – open the Lookup tool.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `lookup()` called"
        )

    def _machine_state_changed(
        self,
        machine_type: str,
        machine_state: str
    ) -> None:
        """
        Either the machine type was changed by the user, or the connection state
        of the machine changed. `machine_type` is the name of the machine (e.g.
        Gemini PR), and `machine_state` is one of `stopped`, `initializing`,
        `connected` or `disconnected`.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK "
            "`machine_state_changed(machine_type: str, machine_state: str)` "
            "called:\n"
            f"    `machine_type`: {machine_type}\n"
            f"    `machine_state`: {machine_state}"
        )

    def _output_changed(self, enabled: bool) -> None:
        """
        The user requested to either enable or disable steno output. `enabled`
        is `True` if output is enabled, `False` otherwise.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `output_changed(enabled: bool)` called:\n"
            f"    `enabled`: {enabled}"
        )

    def _quit(self) -> None:
        """
        The Quit command was activated – wrap up any pending tasks and quit
        Plover.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `quit()` called"
        )

    def _send_backspaces(self, b: int) -> None:
        """
        Plover just sent backspaces over keyboard output. `b` is the number of
        backspaces sent.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `send_backspaces(b: int)` called:\n"
            f"    `b`: {b}"
        )

    def _send_key_combination(self, c: str) -> None:
        """
        Plover just sent a keyboard combination over keyboard output. `c` is a
        string representing the keyboard combination, for example `Alt_L(Tab)`
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `send_key_combination(c: str)` called:\n"
            f"    `c`: {c}"
        )

    def _send_string(self, s: str) -> None:
        """
        Plover just sent the string `s` over keyboard output.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `send_string(s: str)` called:\n"
            f"    `s`: {s}"
        )

    def _stroked(self, stroke: Stroke) -> None:
        """
        The user just sent a stroke.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `stroked(stroke: Stroke)` called:\n"
            f"    `stroke`: {stroke}"
        )

    def _suggestions(self) -> None:
        """
        The Suggestions command was activated – open the Suggestions tool.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK `suggestions()` called"
        )

    def _translated(self, old: List[_Action], new: List[_Action]) -> None:
        """
        A stroke was able to be translated.
        """
        log.info(
            f"{self._log_marker}\n"
            "HOOK "
            "`translated(old: List[_Action], new: List[_Action])` called:\n"
            f"    `old`: {old}\n"
            f"    `new`: {new}"
        )

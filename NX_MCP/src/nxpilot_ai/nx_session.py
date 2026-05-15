"""NX Open session wrapper — singleton that manages the NX connection."""

from __future__ import annotations

import logging
from typing import Any, List, Callable, Dict

logger = logging.getLogger("nxpilot_ai")


class Transaction:
    """Simple transaction wrapper for NX operations with rollback support."""

    def __init__(self, session: Any, name: str = "Transaction"):
        self._session = session
        self._name = name
        self._active = False
        self._rollback_actions: List[Callable[[], None]] = []
        self._completed = False

    def __enter__(self) -> "Transaction":
        """Start the transaction."""
        logger.info(f"Starting transaction: {self._name}")
        self._active = True
        # For NX, we can mark a save point or just track rollback actions manually
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """End transaction, rollback on exception."""
        if exc_type is not None and self._active:
            logger.error(f"Transaction failed: {self._name}, rolling back")
            self.rollback()
            return False
        elif self._active:
            self.commit()
        return False

    def add_rollback_action(self, action: Callable[[], None]) -> None:
        """Add an action to execute if transaction rolls back."""
        if self._active:
            self._rollback_actions.append(action)

    def commit(self) -> None:
        """Commit the transaction."""
        if self._active and not self._completed:
            logger.info(f"Committing transaction: {self._name}")
            self._completed = True
            self._rollback_actions = []
            self._active = False

    def rollback(self) -> None:
        """Rollback the transaction."""
        if self._active:
            logger.info(f"Rolling back transaction: {self._name}")
            # Execute rollback actions in reverse order
            for action in reversed(self._rollback_actions):
                try:
                    action()
                except Exception as e:
                    logger.warning(f"Rollback action failed: {e}")
            self._active = False


class NXSession:
    """Singleton wrapper around NXOpen.Session.

    Connects to a running NX instance. If NX is not available,
    tools will return descriptive errors instead of crashing.
    """

    _instance: NXSession | None = None

    def __init__(self) -> None:
        self._session: Any = None
        self._uf_session: Any = None
        self._connected = False
        self._object_cache: Dict[str, Any] = {}  # Cache for object lookups
        self._connect()

    def _connect(self) -> None:
        """Attempt to connect to the NX session."""
        try:
            import NXOpen

            self._session = NXOpen.Session.GetSession()
            self._connected = True
            logger.info("Connected to NX session")
        except Exception as e:
            self._connected = False
            self._session = None
            logger.warning("Could not connect to NX: %s", e)

    @classmethod
    def get_instance(cls) -> NXSession:
        """Get or create the singleton session."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton — used in tests."""
        cls._instance = None

    @property
    def is_connected(self) -> bool:
        """Whether we have a live NX connection."""
        return self._connected and self._session is not None

    @property
    def session(self) -> Any:
        """The raw NXOpen.Session object."""
        return self._session

    @property
    def work_part(self) -> Any | None:
        """The current work part, or None if not available."""
        if not self.is_connected:
            return None
        try:
            return self._session.Parts.Work
        except Exception:
            return None

    def create_transaction(self, name: str = "Transaction") -> Transaction:
        """Create a new transaction for this session."""
        return Transaction(self._session, name)

    def cache_object(self, key: str, obj: Any) -> None:
        """Cache an object by key."""
        self._object_cache[key] = obj
        logger.debug(f"Cached object with key: {key}")

    def get_cached_object(self, key: str) -> Any | None:
        """Get a cached object by key."""
        return self._object_cache.get(key)

    def clear_cache(self) -> None:
        """Clear the entire object cache."""
        self._object_cache.clear()
        logger.debug("Cleared object cache")

    @property
    def uf_session(self) -> Any | None:
        """The NXOpen.UF.UFSession, lazily initialized."""
        if not self.is_connected:
            return None
        if self._uf_session is None:
            try:
                import NXOpen.UF

                self._uf_session = NXOpen.UF.UFSession.GetUFSession()
            except Exception:
                pass
        return self._uf_session

    def require(self) -> Any:
        """Return the session or raise a clear error if not connected."""
        if not self.is_connected:
            raise RuntimeError(
                "NX is not connected. Start NX and ensure UGII_BASE_DIR is set correctly."
            )
        return self._session

    def require_work_part(self) -> Any:
        """Return the work part or raise a clear error."""
        part = self.work_part
        if part is None:
            raise RuntimeError(
                "No work part is open. Use nx_open_part or nx_create_part first."
            )
        return part

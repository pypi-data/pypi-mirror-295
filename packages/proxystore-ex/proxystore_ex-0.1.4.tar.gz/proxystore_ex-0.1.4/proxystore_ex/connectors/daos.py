"""DAOS Container connector implementation."""

from __future__ import annotations

import sys
import uuid
from types import TracebackType
from typing import Any
from typing import NamedTuple
from typing import Sequence

if sys.version_info >= (3, 11):  # pragma: >=3.11 cover
    from typing import Self
else:  # pragma: <3.11 cover
    from typing_extensions import Self

try:
    import pydaos
except ImportError as e:  # pragma: no cover
    if e.msg == "No module named 'pydaos'":
        import_error_message = """\
The pydaos package is not installed.

Check out the DAOS guide for installation instructions:
    https://extensions.proxystore.dev/latest/guides/daos/\
"""
        raise ImportError(import_error_message) from e
    else:
        raise


class DAOSKey(NamedTuple):
    """Key to object stored in a DAOS container.

    Attributes:
        pool: DAOS pool the container belongs to.
        container: Name of the DAOS container the dictionary with the object
            is in.
        namespace: Name of the DAOS dictionary the object is in.
        dict_key: Unique key in the DAOS dictionary.
    """

    pool: str
    container: str
    namespace: str
    dict_key: str


class DAOSConnector:
    """DAOS Container connector.

    Learn more about DAOS in Python
    [here](https://www.intel.com/content/www/us/en/developer/articles/case-study/unlock-the-power-of-daos-in-python-with-pydaos.html).

    Example:
        Assume we have a DAOS pool named "mypool." First, we create a new
        container in that pool named "kvstore" with type `PYTHON`.

        ```bash
        $ daos cont create mypool --type=PYTHON --label=kvstore
        ```

        Then we can create a connector.
        ```python
        from proxystore_ex.connectors.daos import DAOSConnector

        with DAOSConnector('mypool', 'kvstore', 'mynamespace') as connector:
            key = connector.put('value')
            assert connector.get(key) == 'value'
        ```

    Args:
        pool: DAOS pool label or UUID string.
        container: DAOS container label or UUID string.
        namespace: Name of the DAOS dictionary created in the DAOS container.
            All operations will be performed on this one dictionary so it can
            be thought of as a logically namespace separated from other
            applications interacting with this DAOS container.
        clear: Remove all keys from the DAOS dictionary named `namespace` when
            [`close()`][proxystore_ex.connectors.daos.DAOSConnector.close]
            is called. This will delete keys regardless of if they were
            created by ProxyStore or not.
    """

    def __init__(
        self,
        pool: str,
        container: str,
        namespace: str,
        clear: bool = False,
    ) -> None:
        self.pool = pool
        self.container = container
        self.namespace = namespace
        self.clear = clear

        self._container = pydaos.DCont(self.pool, self.container)
        try:
            self._dict = self._container.get(self.namespace)
        except pydaos.DObjNotFound:
            self._dict = self._container.dict(self.namespace)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(pool={self.pool}, '
            f'container={self.container}, namespace={self.namespace})'
        )

    def _validate_key(self, key: DAOSKey) -> None:
        if (
            key.pool != self.pool
            or key.container != self.container
            or key.namespace != self.namespace
        ):
            raise ValueError(
                'At least one of the pool, container, or namespace of the '
                f'key do not match the connector. Got {key} but expected '
                f'pool={self.pool}, container={self.container}, and '
                f'namespace={self.namespace}.',
            )

    def close(self, clear: bool | None = None) -> None:
        """Close the connector and clean up.

        Warning:
            Passing `clear=True` will result in **ALL** keys in the DAOS
            Dictionary being deleted regardless of if they were created by
            ProxyStore or not.

        Args:
            clear: Remove all keys in the DAOS dictionary. Overrides the
                default value of `clear` provided when the
                [`DAOSConnector`][proxystore_ex.connectors.daos.DAOSConnector]
                was instantiated.
        """
        if self.clear if clear is None else clear:
            for key in list(self._dict):
                del self._dict[key]
        # PyDAOS objects tend to call their close() on __del__.
        # This may cause issues, but we'll leave that to PyDAOS and trust
        # their choice.

    def config(self) -> dict[str, Any]:
        """Get the connector configuration.

        The configuration contains all the information needed to reconstruct
        the connector object.
        """
        return {
            'pool': self.pool,
            'container': self.container,
            'namespace': self.namespace,
            'clear': self.clear,
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> DAOSConnector:
        """Create a new connector instance from a configuration.

        Args:
            config: Configuration returned by `#!python .config()`.
        """
        return cls(**config)

    def evict(self, key: DAOSKey) -> None:
        """Evict the object associated with the key.

        Args:
            key: Key associated with object to evict.
        """
        self._validate_key(key)
        self._dict.pop(key.dict_key)

    def exists(self, key: DAOSKey) -> bool:
        """Check if an object associated with the key exists.

        Args:
            key: Key potentially associated with stored object.

        Returns:
            If an object associated with the key exists.
        """
        self._validate_key(key)
        return key.dict_key in self._dict

    def get(self, key: DAOSKey) -> bytes | None:
        """Get the serialized object associated with the key.

        Args:
            key: Key associated with the object to retrieve.

        Returns:
            Serialized object or `None` if the object does not exist.
        """
        self._validate_key(key)
        try:
            return self._dict.get(key.dict_key)
        except KeyError:
            return None

    def get_batch(self, keys: Sequence[DAOSKey]) -> list[bytes | None]:
        """Get a batch of serialized objects associated with the keys.

        Args:
            keys: Sequence of keys associated with objects to retrieve.

        Returns:
            List with same order as `keys` with the serialized objects or \
            `None` if the corresponding key does not have an associated object.
        """
        # Note: using DDict.bget() would be more efficient, but it will
        # error if any key is missing. So to maintain the semantics of
        # this method, we have to try each key individually.
        objs: list[bytes | None] = []
        for key in keys:
            self._validate_key(key)
            objs.append(self.get(key))
        return objs

    def new_key(self, obj: bytes | None = None) -> DAOSKey:
        """Create a new key.

        Args:
            obj: Optional object which the key will be associated with.
                Ignored in this implementation.

        Returns:
            Key which can be used to retrieve an object once \
            [`set()`][proxystore_ex.connectors.daos.DAOSConnector.set] \
            has been called on the key.
        """
        return DAOSKey(
            pool=self.pool,
            container=self.container,
            namespace=self.namespace,
            dict_key=str(uuid.uuid4()),
        )

    def put(self, obj: bytes) -> DAOSKey:
        """Put a serialized object in the store.

        Args:
            obj: Serialized object to put in the store.

        Returns:
            Key which can be used to retrieve the object.
        """
        key = DAOSKey(
            pool=self.pool,
            container=self.container,
            namespace=self.namespace,
            dict_key=str(uuid.uuid4()),
        )
        self._dict.put(key.dict_key, obj)
        return key

    def put_batch(self, objs: Sequence[bytes]) -> list[DAOSKey]:
        """Put a batch of serialized objects in the store.

        Args:
            objs: Sequence of serialized objects to put in the store.

        Returns:
            List of keys with the same order as `objs` which can be used to \
            retrieve the objects.
        """
        keys = [
            DAOSKey(
                pool=self.pool,
                container=self.container,
                namespace=self.namespace,
                dict_key=str(uuid.uuid4()),
            )
            for _ in objs
        ]
        self._dict.bput({key.dict_key: obj for key, obj in zip(keys, objs)})
        return keys

    def set(self, key: DAOSKey, obj: bytes) -> None:
        """Set the object associated with a key.

        Note:
            The [`Connector`][proxystore.connectors.protocols.Connector]
            provides write-once, read-many semantics. Thus,
            [`set()`][proxystore.connectors.protocols.DeferrableConnector.set]
            should only be called once per key, otherwise unexpected behavior
            can occur.

        Warning:
            This method is not required to be atomic and could therefore
            result in race conditions with calls to
            [`get()`][proxystore.connectors.protocols.Connector.get].

        Args:
            key: Key that the object will be associated with.
            obj: Object to associate with the key.
        """
        self._dict.put(key.dict_key, obj)

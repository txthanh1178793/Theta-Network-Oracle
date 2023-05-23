from __future__ import annotations

import abc
from typing import Dict, List, Optional, Tuple, Union

from core.utils import str_to_bytes32


class Entry(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> Dict[str, str]:
        ...

    @abc.abstractmethod
    def to_tuple(self) -> Dict[str, str]:
        ...

    def serialize_entries(self, entries: List[Entry]):
        serialized_entries = [
            entry.serialize() for entry in entries if issubclass(entry, Entry)
        ]
        return list(filter(lambda item: item is not None, serialized_entries))

    @staticmethod
    def flatten_entries(entries: List[SpotEntry]) -> List[int]:
        """This flattens entriees to tuples.  Useful when you need the raw felt array"""
        expanded = [entry.to_tuple() for entry in entries]
        flattened = [x for entry in expanded for x in entry]
        return [len(entries)] + flattened


class BaseEntry:
    timestamp: int
    source: str
    publisher: str

    def __init__(self, timestamp: int, source: str, publisher: str):
        self.timestamp = timestamp
        self.source = source
        self.publisher = publisher

class GenericEntry(Entry):
    base: BaseEntry
    key: str
    value: int

    def __init__(self,  timestamp: int, source: str, publisher: str, key: str, value: int):
        self.base = BaseEntry(timestamp, source, publisher)
        self.key = key
        self.value = value

    def serialize(self) -> Dict[str, str]:
        return {
            "base": {
                "timestamp": self.base.timestamp,
                "source": self.base.source,
                "publisher": self.base.publisher,
            },
            "key": self.key,
            "value": self.value,
        }

    def to_tuple(self):
        return (
            self.base.timestamp,
            self.base.source,
            self.base.publisher,
            self.key,
            self.value,
        )

    def __repr__(self):
        return f'GenericEntry(key="{self.key}", value={self.value}, timestamp={self.base.timestamp}, source="{self.base.source}", publisher="{self.base.publisher}")'

class SpotEntry(Entry):
    base: BaseEntry
    pair_id: str
    price: int
    volume: int

    def __init__(
        self,
        pair_id: str,
        price: int,
        timestamp: int,
        source: str,
        publisher: str,
        volume: Optional[int] = 0,
    ) -> None:
        self.base = BaseEntry(timestamp, source, publisher)
        self.pair_id = pair_id
        self.price = price
        self.volume = volume

    def __eq__(self, other):
        if isinstance(other, SpotEntry):
            return (
                self.pair_id == other.pair_id
                and self.price == other.price
                and self.base.timestamp == other.base.timestamp
                and self.base.source == other.base.source
                and self.base.publisher == other.base.publisher
                and self.volume == other.volume
            )
        if isinstance(other, Tuple) and len(other) == 4:
            return (
                self.pair_id == other.pair_id
                and self.price == other.price
                and self.base.timestamp == other.base.timestamp
                and self.base.source == other.base.source
                and self.base.publisher == other.base.publisher
                and self.volume == other.volume
            )
        return False

    def to_tuple(self):
        return (
            self.base.timestamp,
            self.base.source,
            self.base.publisher,
            self.pair_id,
            self.price,
            self.volume,
        )

    def serialize(self) -> Dict[str, str]:
        return {
            "base": {
                "timestamp": self.base.timestamp,
                "source": self.base.source,
                "publisher": self.base.publisher,
            },
            "pair_id": self.pair_id,
            "price": self.price,
            "volume": self.volume,
        }

    @staticmethod
    def from_dict(entry_dict: Dict[str, str]) -> "SpotEntry":
        return SpotEntry(
            entry_dict["base"]["pair_id"],
            entry_dict["price"],
            entry_dict["timestamp"],
            entry_dict["base"]["source"],
            entry_dict["base"]["publisher"],
        )

    @staticmethod
    def serialize_entries(entries: List[SpotEntry]) -> List[Dict[str, int]]:
        """serialize entries to a List of dictionaries"""
        # TODO log errors
        serialized_entries = [
            entry.serialize()
            for entry in entries
            # TODO  This needs to be much more resilient to publish errors
            if isinstance(entry, SpotEntry)
        ]
        return list(filter(lambda item: item is not None, serialized_entries))

    def __repr__(self):
        return f'SpotEntry(pair_id="{self.pair_id}", price={self.price}, timestamp={self.base.timestamp}, source="{self.base.source}", publisher="{self.base.publisher}, volume={self.volume})")'


class FutureEntry(Entry):
    timestamp: int
    source: str
    publisher: str
    pair_id: str
    price: int
    expiry_timestamp: int

    def __init__(self, timestamp, source, publisher, pair_id, price, expiry_timestamp):
        if type(pair_id) == str:
            pair_id = str_to_felt(pair_id)

        if type(publisher) == str:
            publisher = str_to_felt(publisher)

        if type(source) == str:
            source = str_to_felt(source)

        if type(expiry_timestamp) == str:
            expiry_timestamp = str_to_felt(expiry_timestamp)

        self.base = BaseEntry(timestamp, source, publisher)
        self.pair_id = pair_id
        self.price = price
        self.expiry_timestamp = expiry_timestamp

    def __eq__(self, other):
        if isinstance(other, FutureEntry):
            return (
                self.pair_id == other.pair_id
                and self.price == other.price
                and self.base.timestamp == other.base.timestamp
                and self.base.source == other.base.source
                and self.base.publisher == other.base.publisher
                and self.expiry_timestamp == other.expiry_timestamp
            )
        if isinstance(other, Tuple) and len(other) == 4:
            return (
                self.pair_id == other.pair_id
                and self.price == other.price
                and self.base.timestamp == other.base.timestamp
                and self.base.source == other.base.source
                and self.base.publisher == other.base.publisher
                and self.expiry_timestamp == other.expiry_timestamp
            )
        return False

    def to_tuple(self):
        return (
            self.base.timestamp,
            self.base.source,
            self.base.publisher,
            self.pair_id,
            self.price,
            self.expiry_timestamp,
        )

    def serialize(self) -> Dict[str, str]:
        return {
            "base": {
                "timestamp": self.base.timestamp,
                "source": self.base.source,
                "publisher": self.base.publisher,
            },
            "pair_id": self.pair_id,
            "price": self.price,
            "expiry_timestamp": self.expiry_timestamp,
        }

    @staticmethod
    def serialize_entries(entries: List[FutureEntry]) -> List[Dict[str, int]]:
        """serialize entries to a List of dictionaries"""
        # TODO (rlkelly): log errors
        serialized_entries = [
            entry.serialize()
            for entry in entries
            # TODO (rlkelly): This needs to be much more resilient to publish errors
            if isinstance(entry, FutureEntry)
        ]
        return list(filter(lambda item: item is not None, serialized_entries))

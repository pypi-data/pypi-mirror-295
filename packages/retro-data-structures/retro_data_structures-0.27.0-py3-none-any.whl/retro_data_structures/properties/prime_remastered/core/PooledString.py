# Generated file
import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from .AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PooledString(BaseProperty):
    index: int = -1
    size_or_str: typing.Union[int, bytes] = b""

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None) -> typing_extensions.Self:
        a, b = struct.unpack('<lL', data.read(8))
        if a == -1:
            b = data.read(b)
        return cls(a, b)

    def to_stream(self, data: typing.BinaryIO) -> None:
        a, b = self.index, self.size_or_str
        if a == -1:
            b = len(b)
        data.write(struct.pack('<lL', a, b))
        if a == -1:
            data.write(self.size_or_str)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        return cls(data["index"], data["size_or_str"])

    def to_json(self) -> json_util.JsonObject:
        return {
            "index": self.index,
            "size_or_str": self.size_or_str,
        }

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

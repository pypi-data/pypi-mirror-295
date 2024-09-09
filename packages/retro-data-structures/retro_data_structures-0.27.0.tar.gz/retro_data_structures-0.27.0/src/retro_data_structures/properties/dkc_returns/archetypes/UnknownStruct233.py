# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.field_reflection import FieldReflection

if typing.TYPE_CHECKING:
    class UnknownStruct233Json(typing_extensions.TypedDict):
        unknown: float
        bomb_locator: str
    

@dataclasses.dataclass()
class UnknownStruct233(BaseProperty):
    unknown: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9ccd4a05, original_name='Unknown'
        ),
    })
    bomb_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xa1afdb3f, original_name='BombLocator'
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        property_count = struct.unpack(">H", data.read(2))[0]
        if (result := cls._fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 2:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ccd4a05
        unknown = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa1afdb3f
        bomb_locator = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(unknown, bomb_locator)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x9c\xcdJ\x05')  # 0x9ccd4a05
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xa1\xaf\xdb?')  # 0xa1afdb3f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.bomb_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct233Json", data)
        return cls(
            unknown=json_data['unknown'],
            bomb_locator=json_data['bomb_locator'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'bomb_locator': self.bomb_locator,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9ccd4a05: ('unknown', _decode_unknown),
    0xa1afdb3f: ('bomb_locator', _decode_bomb_locator),
}

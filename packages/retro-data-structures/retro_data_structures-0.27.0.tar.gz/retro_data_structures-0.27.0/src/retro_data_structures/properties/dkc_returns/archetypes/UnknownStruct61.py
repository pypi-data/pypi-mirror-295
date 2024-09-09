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
    class UnknownStruct61Json(typing_extensions.TypedDict):
        number_of_bombs: int
        horizontal_spread: float
        unknown_0xf228ec53: float
        unknown_0xd91227f1: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xf8d8d976, 0x8c29e91c, 0xf228ec53, 0xd91227f1)


@dataclasses.dataclass()
class UnknownStruct61(BaseProperty):
    number_of_bombs: int = dataclasses.field(default=6, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf8d8d976, original_name='NumberOfBombs'
        ),
    })
    horizontal_spread: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8c29e91c, original_name='HorizontalSpread'
        ),
    })
    unknown_0xf228ec53: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf228ec53, original_name='Unknown'
        ),
    })
    unknown_0xd91227f1: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd91227f1, original_name='Unknown'
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
        if property_count != 4:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(40))
        assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xf8\xd8\xd9v')  # 0xf8d8d976
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_bombs))

        data.write(b'\x8c)\xe9\x1c')  # 0x8c29e91c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_spread))

        data.write(b'\xf2(\xecS')  # 0xf228ec53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf228ec53))

        data.write(b"\xd9\x12'\xf1")  # 0xd91227f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd91227f1))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct61Json", data)
        return cls(
            number_of_bombs=json_data['number_of_bombs'],
            horizontal_spread=json_data['horizontal_spread'],
            unknown_0xf228ec53=json_data['unknown_0xf228ec53'],
            unknown_0xd91227f1=json_data['unknown_0xd91227f1'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_bombs': self.number_of_bombs,
            'horizontal_spread': self.horizontal_spread,
            'unknown_0xf228ec53': self.unknown_0xf228ec53,
            'unknown_0xd91227f1': self.unknown_0xd91227f1,
        }


def _decode_number_of_bombs(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_horizontal_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf228ec53(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd91227f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8d8d976: ('number_of_bombs', _decode_number_of_bombs),
    0x8c29e91c: ('horizontal_spread', _decode_horizontal_spread),
    0xf228ec53: ('unknown_0xf228ec53', _decode_unknown_0xf228ec53),
    0xd91227f1: ('unknown_0xd91227f1', _decode_unknown_0xd91227f1),
}

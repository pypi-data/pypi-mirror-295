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
    class UnknownStruct70Json(typing_extensions.TypedDict):
        unknown_0x3b6740f1: float
        unknown_0x8130b0d8: float
        ignore_upper_lower_bounds: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x3b6740f1, 0x8130b0d8, 0x685952e3)


@dataclasses.dataclass()
class UnknownStruct70(BaseProperty):
    unknown_0x3b6740f1: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3b6740f1, original_name='Unknown'
        ),
    })
    unknown_0x8130b0d8: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8130b0d8, original_name='Unknown'
        ),
    })
    ignore_upper_lower_bounds: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x685952e3, original_name='IgnoreUpperLowerBounds'
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
        if property_count != 3:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(27))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b';g@\xf1')  # 0x3b6740f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b6740f1))

        data.write(b'\x810\xb0\xd8')  # 0x8130b0d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8130b0d8))

        data.write(b'hYR\xe3')  # 0x685952e3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_upper_lower_bounds))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct70Json", data)
        return cls(
            unknown_0x3b6740f1=json_data['unknown_0x3b6740f1'],
            unknown_0x8130b0d8=json_data['unknown_0x8130b0d8'],
            ignore_upper_lower_bounds=json_data['ignore_upper_lower_bounds'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x3b6740f1': self.unknown_0x3b6740f1,
            'unknown_0x8130b0d8': self.unknown_0x8130b0d8,
            'ignore_upper_lower_bounds': self.ignore_upper_lower_bounds,
        }


def _decode_unknown_0x3b6740f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8130b0d8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_upper_lower_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3b6740f1: ('unknown_0x3b6740f1', _decode_unknown_0x3b6740f1),
    0x8130b0d8: ('unknown_0x8130b0d8', _decode_unknown_0x8130b0d8),
    0x685952e3: ('ignore_upper_lower_bounds', _decode_ignore_upper_lower_bounds),
}

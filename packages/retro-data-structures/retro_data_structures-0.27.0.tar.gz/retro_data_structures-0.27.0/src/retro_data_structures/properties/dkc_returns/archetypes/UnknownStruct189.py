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
    class UnknownStruct189Json(typing_extensions.TypedDict):
        unknown_0xe84a887b: float
        unknown_0x8a58a7f8: int
        stun_duration: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xe84a887b, 0x8a58a7f8, 0x2d8db31d)


@dataclasses.dataclass()
class UnknownStruct189(BaseProperty):
    unknown_0xe84a887b: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe84a887b, original_name='Unknown'
        ),
    })
    unknown_0x8a58a7f8: int = dataclasses.field(default=2, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8a58a7f8, original_name='Unknown'
        ),
    })
    stun_duration: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d8db31d, original_name='StunDuration'
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
            _FAST_FORMAT = struct.Struct('>LHfLHlLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(30))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xe8J\x88{')  # 0xe84a887b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe84a887b))

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct189Json", data)
        return cls(
            unknown_0xe84a887b=json_data['unknown_0xe84a887b'],
            unknown_0x8a58a7f8=json_data['unknown_0x8a58a7f8'],
            stun_duration=json_data['stun_duration'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xe84a887b': self.unknown_0xe84a887b,
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'stun_duration': self.stun_duration,
        }


def _decode_unknown_0xe84a887b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe84a887b: ('unknown_0xe84a887b', _decode_unknown_0xe84a887b),
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
}

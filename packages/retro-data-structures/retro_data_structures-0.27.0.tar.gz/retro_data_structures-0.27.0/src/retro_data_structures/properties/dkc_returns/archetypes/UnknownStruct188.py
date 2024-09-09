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
    class UnknownStruct188Json(typing_extensions.TypedDict):
        unknown_0xe84a887b: float
        unknown_0x8a58a7f8: int
        unknown_0x1d18ec45: bool
        stun_duration: float
        unknown_0x634415f0: float
        unknown_0x82090854: float
        unknown_0x0c7f57a5: float
        unknown_0x1a75dce7: float
        unknown_0x89c8bb60: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xe84a887b, 0x8a58a7f8, 0x1d18ec45, 0x2d8db31d, 0x634415f0, 0x82090854, 0xc7f57a5, 0x1a75dce7, 0x89c8bb60)


@dataclasses.dataclass()
class UnknownStruct188(BaseProperty):
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
    unknown_0x1d18ec45: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1d18ec45, original_name='Unknown'
        ),
    })
    stun_duration: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d8db31d, original_name='StunDuration'
        ),
    })
    unknown_0x634415f0: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x634415f0, original_name='Unknown'
        ),
    })
    unknown_0x82090854: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x82090854, original_name='Unknown'
        ),
    })
    unknown_0x0c7f57a5: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0c7f57a5, original_name='Unknown'
        ),
    })
    unknown_0x1a75dce7: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1a75dce7, original_name='Unknown'
        ),
    })
    unknown_0x89c8bb60: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x89c8bb60, original_name='Unknown'
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
        if property_count != 9:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHlLH?LHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(87))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xe8J\x88{')  # 0xe84a887b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe84a887b))

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'\x1d\x18\xecE')  # 0x1d18ec45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1d18ec45))

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

        data.write(b'cD\x15\xf0')  # 0x634415f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x634415f0))

        data.write(b'\x82\t\x08T')  # 0x82090854
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x82090854))

        data.write(b'\x0c\x7fW\xa5')  # 0xc7f57a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0c7f57a5))

        data.write(b'\x1au\xdc\xe7')  # 0x1a75dce7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1a75dce7))

        data.write(b'\x89\xc8\xbb`')  # 0x89c8bb60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x89c8bb60))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct188Json", data)
        return cls(
            unknown_0xe84a887b=json_data['unknown_0xe84a887b'],
            unknown_0x8a58a7f8=json_data['unknown_0x8a58a7f8'],
            unknown_0x1d18ec45=json_data['unknown_0x1d18ec45'],
            stun_duration=json_data['stun_duration'],
            unknown_0x634415f0=json_data['unknown_0x634415f0'],
            unknown_0x82090854=json_data['unknown_0x82090854'],
            unknown_0x0c7f57a5=json_data['unknown_0x0c7f57a5'],
            unknown_0x1a75dce7=json_data['unknown_0x1a75dce7'],
            unknown_0x89c8bb60=json_data['unknown_0x89c8bb60'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xe84a887b': self.unknown_0xe84a887b,
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'unknown_0x1d18ec45': self.unknown_0x1d18ec45,
            'stun_duration': self.stun_duration,
            'unknown_0x634415f0': self.unknown_0x634415f0,
            'unknown_0x82090854': self.unknown_0x82090854,
            'unknown_0x0c7f57a5': self.unknown_0x0c7f57a5,
            'unknown_0x1a75dce7': self.unknown_0x1a75dce7,
            'unknown_0x89c8bb60': self.unknown_0x89c8bb60,
        }


def _decode_unknown_0xe84a887b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1d18ec45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x634415f0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x82090854(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0c7f57a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1a75dce7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x89c8bb60(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe84a887b: ('unknown_0xe84a887b', _decode_unknown_0xe84a887b),
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0x1d18ec45: ('unknown_0x1d18ec45', _decode_unknown_0x1d18ec45),
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
    0x634415f0: ('unknown_0x634415f0', _decode_unknown_0x634415f0),
    0x82090854: ('unknown_0x82090854', _decode_unknown_0x82090854),
    0xc7f57a5: ('unknown_0x0c7f57a5', _decode_unknown_0x0c7f57a5),
    0x1a75dce7: ('unknown_0x1a75dce7', _decode_unknown_0x1a75dce7),
    0x89c8bb60: ('unknown_0x89c8bb60', _decode_unknown_0x89c8bb60),
}

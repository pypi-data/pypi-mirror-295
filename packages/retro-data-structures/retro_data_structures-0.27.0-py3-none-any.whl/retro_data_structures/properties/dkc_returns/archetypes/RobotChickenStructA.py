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
    class RobotChickenStructAJson(typing_extensions.TypedDict):
        unknown_0x86982e06: int
        grid_dist_min: int
        grid_dist_max: int
        unknown_0x3c182e6d: int
        unknown_0x5bdf89c0: int
        unknown_0xd8828f28: int
        unknown_0xd387b254: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x86982e06, 0xcf0adc96, 0x8a089f14, 0x3c182e6d, 0x5bdf89c0, 0xd8828f28, 0xd387b254)


@dataclasses.dataclass()
class RobotChickenStructA(BaseProperty):
    unknown_0x86982e06: int = dataclasses.field(default=5, metadata={
        'reflection': FieldReflection[int](
            int, id=0x86982e06, original_name='Unknown'
        ),
    })
    grid_dist_min: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0xcf0adc96, original_name='GridDistMin'
        ),
    })
    grid_dist_max: int = dataclasses.field(default=7, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8a089f14, original_name='GridDistMax'
        ),
    })
    unknown_0x3c182e6d: int = dataclasses.field(default=33, metadata={
        'reflection': FieldReflection[int](
            int, id=0x3c182e6d, original_name='Unknown'
        ),
    })
    unknown_0x5bdf89c0: int = dataclasses.field(default=33, metadata={
        'reflection': FieldReflection[int](
            int, id=0x5bdf89c0, original_name='Unknown'
        ),
    })
    unknown_0xd8828f28: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xd8828f28, original_name='Unknown'
        ),
    })
    unknown_0xd387b254: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xd387b254, original_name='Unknown'
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
        if property_count != 7:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHlLHlLHl')
    
        dec = _FAST_FORMAT.unpack(data.read(70))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x86\x98.\x06')  # 0x86982e06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x86982e06))

        data.write(b'\xcf\n\xdc\x96')  # 0xcf0adc96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grid_dist_min))

        data.write(b'\x8a\x08\x9f\x14')  # 0x8a089f14
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grid_dist_max))

        data.write(b'<\x18.m')  # 0x3c182e6d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x3c182e6d))

        data.write(b'[\xdf\x89\xc0')  # 0x5bdf89c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x5bdf89c0))

        data.write(b'\xd8\x82\x8f(')  # 0xd8828f28
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd8828f28))

        data.write(b'\xd3\x87\xb2T')  # 0xd387b254
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd387b254))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("RobotChickenStructAJson", data)
        return cls(
            unknown_0x86982e06=json_data['unknown_0x86982e06'],
            grid_dist_min=json_data['grid_dist_min'],
            grid_dist_max=json_data['grid_dist_max'],
            unknown_0x3c182e6d=json_data['unknown_0x3c182e6d'],
            unknown_0x5bdf89c0=json_data['unknown_0x5bdf89c0'],
            unknown_0xd8828f28=json_data['unknown_0xd8828f28'],
            unknown_0xd387b254=json_data['unknown_0xd387b254'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x86982e06': self.unknown_0x86982e06,
            'grid_dist_min': self.grid_dist_min,
            'grid_dist_max': self.grid_dist_max,
            'unknown_0x3c182e6d': self.unknown_0x3c182e6d,
            'unknown_0x5bdf89c0': self.unknown_0x5bdf89c0,
            'unknown_0xd8828f28': self.unknown_0xd8828f28,
            'unknown_0xd387b254': self.unknown_0xd387b254,
        }


def _decode_unknown_0x86982e06(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grid_dist_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grid_dist_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3c182e6d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x5bdf89c0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd8828f28(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd387b254(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x86982e06: ('unknown_0x86982e06', _decode_unknown_0x86982e06),
    0xcf0adc96: ('grid_dist_min', _decode_grid_dist_min),
    0x8a089f14: ('grid_dist_max', _decode_grid_dist_max),
    0x3c182e6d: ('unknown_0x3c182e6d', _decode_unknown_0x3c182e6d),
    0x5bdf89c0: ('unknown_0x5bdf89c0', _decode_unknown_0x5bdf89c0),
    0xd8828f28: ('unknown_0xd8828f28', _decode_unknown_0xd8828f28),
    0xd387b254: ('unknown_0xd387b254', _decode_unknown_0xd387b254),
}

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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class UnknownStruct134Json(typing_extensions.TypedDict):
        unknown_0x51e5c747: bool
        unknown_0x4046688f: bool
        replace_bounds: bool
        min_point: json_util.JsonValue
        max_point: json_util.JsonValue
    

_FAST_FORMAT = None
_FAST_IDS = (0x51e5c747, 0x4046688f, 0x99037e15, 0x48d6716b, 0xf1f0ea1a)


@dataclasses.dataclass()
class UnknownStruct134(BaseProperty):
    unknown_0x51e5c747: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x51e5c747, original_name='Unknown'
        ),
    })
    unknown_0x4046688f: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4046688f, original_name='Unknown'
        ),
    })
    replace_bounds: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x99037e15, original_name='ReplaceBounds'
        ),
    })
    min_point: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x48d6716b, original_name='MinPoint', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    max_point: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xf1f0ea1a, original_name='MaxPoint', from_json=Vector.from_json, to_json=Vector.to_json
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
        if property_count != 5:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LHfffLHfff')
    
        dec = _FAST_FORMAT.unpack(data.read(57))
        assert (dec[0], dec[3], dec[6], dec[9], dec[14]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            Vector(*dec[11:14]),
            Vector(*dec[16:19]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'Q\xe5\xc7G')  # 0x51e5c747
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x51e5c747))

        data.write(b'@Fh\x8f')  # 0x4046688f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4046688f))

        data.write(b'\x99\x03~\x15')  # 0x99037e15
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.replace_bounds))

        data.write(b'H\xd6qk')  # 0x48d6716b
        data.write(b'\x00\x0c')  # size
        self.min_point.to_stream(data)

        data.write(b'\xf1\xf0\xea\x1a')  # 0xf1f0ea1a
        data.write(b'\x00\x0c')  # size
        self.max_point.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct134Json", data)
        return cls(
            unknown_0x51e5c747=json_data['unknown_0x51e5c747'],
            unknown_0x4046688f=json_data['unknown_0x4046688f'],
            replace_bounds=json_data['replace_bounds'],
            min_point=Vector.from_json(json_data['min_point']),
            max_point=Vector.from_json(json_data['max_point']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x51e5c747': self.unknown_0x51e5c747,
            'unknown_0x4046688f': self.unknown_0x4046688f,
            'replace_bounds': self.replace_bounds,
            'min_point': self.min_point.to_json(),
            'max_point': self.max_point.to_json(),
        }


def _decode_unknown_0x51e5c747(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4046688f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_replace_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_min_point(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_max_point(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x51e5c747: ('unknown_0x51e5c747', _decode_unknown_0x51e5c747),
    0x4046688f: ('unknown_0x4046688f', _decode_unknown_0x4046688f),
    0x99037e15: ('replace_bounds', _decode_replace_bounds),
    0x48d6716b: ('min_point', _decode_min_point),
    0xf1f0ea1a: ('max_point', _decode_max_point),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct246 import UnknownStruct246

if typing.TYPE_CHECKING:
    class UnknownStruct247Json(typing_extensions.TypedDict):
        unknown_struct246: json_util.JsonObject
        radius: float
        is_moving_target: bool
        unknown_0x1ede41df: bool
        unknown_0xbde22b8e: float
        ignoring_duration: float
    

@dataclasses.dataclass()
class UnknownStruct247(BaseProperty):
    unknown_struct246: UnknownStruct246 = dataclasses.field(default_factory=UnknownStruct246, metadata={
        'reflection': FieldReflection[UnknownStruct246](
            UnknownStruct246, id=0x93a412dd, original_name='UnknownStruct246', from_json=UnknownStruct246.from_json, to_json=UnknownStruct246.to_json
        ),
    })
    radius: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x78c507eb, original_name='Radius'
        ),
    })
    is_moving_target: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x84ac8dc6, original_name='IsMovingTarget'
        ),
    })
    unknown_0x1ede41df: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1ede41df, original_name='Unknown'
        ),
    })
    unknown_0xbde22b8e: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbde22b8e, original_name='Unknown'
        ),
    })
    ignoring_duration: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb902b5a1, original_name='IgnoringDuration'
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
        if property_count != 6:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x93a412dd
        unknown_struct246 = UnknownStruct246.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x78c507eb
        radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x84ac8dc6
        is_moving_target = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1ede41df
        unknown_0x1ede41df = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbde22b8e
        unknown_0xbde22b8e = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb902b5a1
        ignoring_duration = struct.unpack('>f', data.read(4))[0]
    
        return cls(unknown_struct246, radius, is_moving_target, unknown_0x1ede41df, unknown_0xbde22b8e, ignoring_duration)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x93\xa4\x12\xdd')  # 0x93a412dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct246.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\x84\xac\x8d\xc6')  # 0x84ac8dc6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_moving_target))

        data.write(b'\x1e\xdeA\xdf')  # 0x1ede41df
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1ede41df))

        data.write(b'\xbd\xe2+\x8e')  # 0xbde22b8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbde22b8e))

        data.write(b'\xb9\x02\xb5\xa1')  # 0xb902b5a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ignoring_duration))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct247Json", data)
        return cls(
            unknown_struct246=UnknownStruct246.from_json(json_data['unknown_struct246']),
            radius=json_data['radius'],
            is_moving_target=json_data['is_moving_target'],
            unknown_0x1ede41df=json_data['unknown_0x1ede41df'],
            unknown_0xbde22b8e=json_data['unknown_0xbde22b8e'],
            ignoring_duration=json_data['ignoring_duration'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct246': self.unknown_struct246.to_json(),
            'radius': self.radius,
            'is_moving_target': self.is_moving_target,
            'unknown_0x1ede41df': self.unknown_0x1ede41df,
            'unknown_0xbde22b8e': self.unknown_0xbde22b8e,
            'ignoring_duration': self.ignoring_duration,
        }


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_moving_target(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x1ede41df(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbde22b8e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignoring_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x93a412dd: ('unknown_struct246', UnknownStruct246.from_stream),
    0x78c507eb: ('radius', _decode_radius),
    0x84ac8dc6: ('is_moving_target', _decode_is_moving_target),
    0x1ede41df: ('unknown_0x1ede41df', _decode_unknown_0x1ede41df),
    0xbde22b8e: ('unknown_0xbde22b8e', _decode_unknown_0xbde22b8e),
    0xb902b5a1: ('ignoring_duration', _decode_ignoring_duration),
}

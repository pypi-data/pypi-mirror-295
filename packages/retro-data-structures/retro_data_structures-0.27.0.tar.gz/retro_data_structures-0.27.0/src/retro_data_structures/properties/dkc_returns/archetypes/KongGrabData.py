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
    class KongGrabDataJson(typing_extensions.TypedDict):
        grab_front_range: json_util.JsonValue
        grab_air_front_range: json_util.JsonValue
        grab_side_range: json_util.JsonValue
        grab_side_offset: float
        throw_velocity: json_util.JsonValue
        left_locator: str
        right_locator: str
        turn_locator: str
        allow_held_object_ceiling_adjust: bool
    

@dataclasses.dataclass()
class KongGrabData(BaseProperty):
    grab_front_range: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.5, y=2.25, z=1.25), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x797fa862, original_name='GrabFrontRange', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    grab_air_front_range: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.5, y=2.25, z=2.5), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xe91a3395, original_name='GrabAirFrontRange', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    grab_side_range: Vector = dataclasses.field(default_factory=lambda: Vector(x=3.0, y=1.899999976158142, z=1.25), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x43fdb8d0, original_name='GrabSideRange', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    grab_side_offset: float = dataclasses.field(default=-0.6000000238418579, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb55ebd3d, original_name='GrabSideOffset'
        ),
    })
    throw_velocity: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=25.0, z=5.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xecaa2f72, original_name='ThrowVelocity', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    left_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x54bc48a1, original_name='LeftLocator'
        ),
    })
    right_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xdb6cd2ca, original_name='RightLocator'
        ),
    })
    turn_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x3941bc07, original_name='TurnLocator'
        ),
    })
    allow_held_object_ceiling_adjust: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x02d6a990, original_name='AllowHeldObjectCeilingAdjust'
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x797fa862
        grab_front_range = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe91a3395
        grab_air_front_range = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43fdb8d0
        grab_side_range = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb55ebd3d
        grab_side_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xecaa2f72
        throw_velocity = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x54bc48a1
        left_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb6cd2ca
        right_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3941bc07
        turn_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x02d6a990
        allow_held_object_ceiling_adjust = struct.unpack('>?', data.read(1))[0]
    
        return cls(grab_front_range, grab_air_front_range, grab_side_range, grab_side_offset, throw_velocity, left_locator, right_locator, turn_locator, allow_held_object_ceiling_adjust)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'y\x7f\xa8b')  # 0x797fa862
        data.write(b'\x00\x0c')  # size
        self.grab_front_range.to_stream(data)

        data.write(b'\xe9\x1a3\x95')  # 0xe91a3395
        data.write(b'\x00\x0c')  # size
        self.grab_air_front_range.to_stream(data)

        data.write(b'C\xfd\xb8\xd0')  # 0x43fdb8d0
        data.write(b'\x00\x0c')  # size
        self.grab_side_range.to_stream(data)

        data.write(b'\xb5^\xbd=')  # 0xb55ebd3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_side_offset))

        data.write(b'\xec\xaa/r')  # 0xecaa2f72
        data.write(b'\x00\x0c')  # size
        self.throw_velocity.to_stream(data)

        data.write(b'T\xbcH\xa1')  # 0x54bc48a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.left_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdbl\xd2\xca')  # 0xdb6cd2ca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.right_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9A\xbc\x07')  # 0x3941bc07
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.turn_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\xd6\xa9\x90')  # 0x2d6a990
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_held_object_ceiling_adjust))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("KongGrabDataJson", data)
        return cls(
            grab_front_range=Vector.from_json(json_data['grab_front_range']),
            grab_air_front_range=Vector.from_json(json_data['grab_air_front_range']),
            grab_side_range=Vector.from_json(json_data['grab_side_range']),
            grab_side_offset=json_data['grab_side_offset'],
            throw_velocity=Vector.from_json(json_data['throw_velocity']),
            left_locator=json_data['left_locator'],
            right_locator=json_data['right_locator'],
            turn_locator=json_data['turn_locator'],
            allow_held_object_ceiling_adjust=json_data['allow_held_object_ceiling_adjust'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'grab_front_range': self.grab_front_range.to_json(),
            'grab_air_front_range': self.grab_air_front_range.to_json(),
            'grab_side_range': self.grab_side_range.to_json(),
            'grab_side_offset': self.grab_side_offset,
            'throw_velocity': self.throw_velocity.to_json(),
            'left_locator': self.left_locator,
            'right_locator': self.right_locator,
            'turn_locator': self.turn_locator,
            'allow_held_object_ceiling_adjust': self.allow_held_object_ceiling_adjust,
        }


def _decode_grab_front_range(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_grab_air_front_range(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_grab_side_range(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_grab_side_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_throw_velocity(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_left_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_right_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_turn_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_allow_held_object_ceiling_adjust(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x797fa862: ('grab_front_range', _decode_grab_front_range),
    0xe91a3395: ('grab_air_front_range', _decode_grab_air_front_range),
    0x43fdb8d0: ('grab_side_range', _decode_grab_side_range),
    0xb55ebd3d: ('grab_side_offset', _decode_grab_side_offset),
    0xecaa2f72: ('throw_velocity', _decode_throw_velocity),
    0x54bc48a1: ('left_locator', _decode_left_locator),
    0xdb6cd2ca: ('right_locator', _decode_right_locator),
    0x3941bc07: ('turn_locator', _decode_turn_locator),
    0x2d6a990: ('allow_held_object_ceiling_adjust', _decode_allow_held_object_ceiling_adjust),
}

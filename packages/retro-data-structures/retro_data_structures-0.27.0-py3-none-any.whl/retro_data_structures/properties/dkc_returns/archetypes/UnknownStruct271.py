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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct270 import UnknownStruct270

if typing.TYPE_CHECKING:
    class UnknownStruct271Json(typing_extensions.TypedDict):
        unknown_struct270: json_util.JsonObject
        unknown: float
        collision_offset: float
        sink_speed: float
        rise_speed: float
        kill_threshold: float
    

@dataclasses.dataclass()
class UnknownStruct271(BaseProperty):
    unknown_struct270: UnknownStruct270 = dataclasses.field(default_factory=UnknownStruct270, metadata={
        'reflection': FieldReflection[UnknownStruct270](
            UnknownStruct270, id=0x719066eb, original_name='UnknownStruct270', from_json=UnknownStruct270.from_json, to_json=UnknownStruct270.to_json
        ),
    })
    unknown: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfba6a1d6, original_name='Unknown'
        ),
    })
    collision_offset: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb4828a9f, original_name='CollisionOffset'
        ),
    })
    sink_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3139c165, original_name='SinkSpeed'
        ),
    })
    rise_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6cf7e707, original_name='RiseSpeed'
        ),
    })
    kill_threshold: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf41a57e6, original_name='KillThreshold'
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
        assert property_id == 0x719066eb
        unknown_struct270 = UnknownStruct270.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfba6a1d6
        unknown = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb4828a9f
        collision_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3139c165
        sink_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6cf7e707
        rise_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf41a57e6
        kill_threshold = struct.unpack('>f', data.read(4))[0]
    
        return cls(unknown_struct270, unknown, collision_offset, sink_speed, rise_speed, kill_threshold)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'q\x90f\xeb')  # 0x719066eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct270.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb\xa6\xa1\xd6')  # 0xfba6a1d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xb4\x82\x8a\x9f')  # 0xb4828a9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_offset))

        data.write(b'19\xc1e')  # 0x3139c165
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sink_speed))

        data.write(b'l\xf7\xe7\x07')  # 0x6cf7e707
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rise_speed))

        data.write(b'\xf4\x1aW\xe6')  # 0xf41a57e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.kill_threshold))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct271Json", data)
        return cls(
            unknown_struct270=UnknownStruct270.from_json(json_data['unknown_struct270']),
            unknown=json_data['unknown'],
            collision_offset=json_data['collision_offset'],
            sink_speed=json_data['sink_speed'],
            rise_speed=json_data['rise_speed'],
            kill_threshold=json_data['kill_threshold'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct270': self.unknown_struct270.to_json(),
            'unknown': self.unknown,
            'collision_offset': self.collision_offset,
            'sink_speed': self.sink_speed,
            'rise_speed': self.rise_speed,
            'kill_threshold': self.kill_threshold,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sink_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rise_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_kill_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x719066eb: ('unknown_struct270', UnknownStruct270.from_stream),
    0xfba6a1d6: ('unknown', _decode_unknown),
    0xb4828a9f: ('collision_offset', _decode_collision_offset),
    0x3139c165: ('sink_speed', _decode_sink_speed),
    0x6cf7e707: ('rise_speed', _decode_rise_speed),
    0xf41a57e6: ('kill_threshold', _decode_kill_threshold),
}

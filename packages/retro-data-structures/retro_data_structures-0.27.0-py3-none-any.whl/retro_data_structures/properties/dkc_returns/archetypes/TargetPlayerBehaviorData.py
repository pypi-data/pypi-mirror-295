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
    class TargetPlayerBehaviorDataJson(typing_extensions.TypedDict):
        mode: int
        start_targeting_range: float
        stop_targeting_range: float
        rotation_speed: float
        telegraph_loops: bool
        telegraph_time: float
        min_target_distance: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xb8f60f9a, 0x1165a51e, 0xfa57398b, 0x11cd076f, 0x5ea80f07, 0x8e6bbef1, 0xfa6a5761)


@dataclasses.dataclass()
class TargetPlayerBehaviorData(BaseProperty):
    mode: int = dataclasses.field(default=1638556020, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb8f60f9a, original_name='Mode'
        ),
    })  # Choice
    start_targeting_range: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1165a51e, original_name='StartTargetingRange'
        ),
    })
    stop_targeting_range: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfa57398b, original_name='StopTargetingRange'
        ),
    })
    rotation_speed: float = dataclasses.field(default=1440.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x11cd076f, original_name='RotationSpeed'
        ),
    })
    telegraph_loops: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5ea80f07, original_name='TelegraphLoops'
        ),
    })
    telegraph_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8e6bbef1, original_name='TelegraphTime'
        ),
    })
    min_target_distance: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfa6a5761, original_name='MinTargetDistance'
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
            _FAST_FORMAT = struct.Struct('>LHLLHfLHfLHfLH?LHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(67))
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

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mode))

        data.write(b'\x11e\xa5\x1e')  # 0x1165a51e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_targeting_range))

        data.write(b'\xfaW9\x8b')  # 0xfa57398b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_targeting_range))

        data.write(b'\x11\xcd\x07o')  # 0x11cd076f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_speed))

        data.write(b'^\xa8\x0f\x07')  # 0x5ea80f07
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.telegraph_loops))

        data.write(b'\x8ek\xbe\xf1')  # 0x8e6bbef1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.telegraph_time))

        data.write(b'\xfajWa')  # 0xfa6a5761
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_target_distance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TargetPlayerBehaviorDataJson", data)
        return cls(
            mode=json_data['mode'],
            start_targeting_range=json_data['start_targeting_range'],
            stop_targeting_range=json_data['stop_targeting_range'],
            rotation_speed=json_data['rotation_speed'],
            telegraph_loops=json_data['telegraph_loops'],
            telegraph_time=json_data['telegraph_time'],
            min_target_distance=json_data['min_target_distance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'mode': self.mode,
            'start_targeting_range': self.start_targeting_range,
            'stop_targeting_range': self.stop_targeting_range,
            'rotation_speed': self.rotation_speed,
            'telegraph_loops': self.telegraph_loops,
            'telegraph_time': self.telegraph_time,
            'min_target_distance': self.min_target_distance,
        }


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_start_targeting_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stop_targeting_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_telegraph_loops(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_telegraph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_target_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb8f60f9a: ('mode', _decode_mode),
    0x1165a51e: ('start_targeting_range', _decode_start_targeting_range),
    0xfa57398b: ('stop_targeting_range', _decode_stop_targeting_range),
    0x11cd076f: ('rotation_speed', _decode_rotation_speed),
    0x5ea80f07: ('telegraph_loops', _decode_telegraph_loops),
    0x8e6bbef1: ('telegraph_time', _decode_telegraph_time),
    0xfa6a5761: ('min_target_distance', _decode_min_target_distance),
}

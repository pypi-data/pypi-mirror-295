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
    class SlideBehaviorDataJson(typing_extensions.TypedDict):
        slope_detection_angle: float
        slide_detection_angle: float
        slide_friction: float
        slow_friction: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x4e7def7e, 0x6591a3a9, 0xc28b285e, 0xced6fccf)


@dataclasses.dataclass()
class SlideBehaviorData(BaseProperty):
    slope_detection_angle: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4e7def7e, original_name='SlopeDetectionAngle'
        ),
    })
    slide_detection_angle: float = dataclasses.field(default=54.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6591a3a9, original_name='SlideDetectionAngle'
        ),
    })
    slide_friction: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc28b285e, original_name='SlideFriction'
        ),
    })
    slow_friction: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xced6fccf, original_name='SlowFriction'
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
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')
    
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

        data.write(b'N}\xef~')  # 0x4e7def7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slope_detection_angle))

        data.write(b'e\x91\xa3\xa9')  # 0x6591a3a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_detection_angle))

        data.write(b'\xc2\x8b(^')  # 0xc28b285e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_friction))

        data.write(b'\xce\xd6\xfc\xcf')  # 0xced6fccf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slow_friction))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SlideBehaviorDataJson", data)
        return cls(
            slope_detection_angle=json_data['slope_detection_angle'],
            slide_detection_angle=json_data['slide_detection_angle'],
            slide_friction=json_data['slide_friction'],
            slow_friction=json_data['slow_friction'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'slope_detection_angle': self.slope_detection_angle,
            'slide_detection_angle': self.slide_detection_angle,
            'slide_friction': self.slide_friction,
            'slow_friction': self.slow_friction,
        }


def _decode_slope_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slow_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4e7def7e: ('slope_detection_angle', _decode_slope_detection_angle),
    0x6591a3a9: ('slide_detection_angle', _decode_slide_detection_angle),
    0xc28b285e: ('slide_friction', _decode_slide_friction),
    0xced6fccf: ('slow_friction', _decode_slow_friction),
}

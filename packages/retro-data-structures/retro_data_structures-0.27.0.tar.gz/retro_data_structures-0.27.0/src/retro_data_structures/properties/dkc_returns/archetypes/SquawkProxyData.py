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
    class SquawkProxyDataJson(typing_extensions.TypedDict):
        auto_player_detection_far_radius: float
        auto_player_detection_near_radius: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xcd5113dc, 0xc706d790)


@dataclasses.dataclass()
class SquawkProxyData(BaseProperty):
    auto_player_detection_far_radius: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcd5113dc, original_name='AutoPlayerDetectionFarRadius'
        ),
    })
    auto_player_detection_near_radius: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc706d790, original_name='AutoPlayerDetectionNearRadius'
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
        if property_count != 2:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(20))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xcdQ\x13\xdc')  # 0xcd5113dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_player_detection_far_radius))

        data.write(b'\xc7\x06\xd7\x90')  # 0xc706d790
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_player_detection_near_radius))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SquawkProxyDataJson", data)
        return cls(
            auto_player_detection_far_radius=json_data['auto_player_detection_far_radius'],
            auto_player_detection_near_radius=json_data['auto_player_detection_near_radius'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'auto_player_detection_far_radius': self.auto_player_detection_far_radius,
            'auto_player_detection_near_radius': self.auto_player_detection_near_radius,
        }


def _decode_auto_player_detection_far_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_player_detection_near_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcd5113dc: ('auto_player_detection_far_radius', _decode_auto_player_detection_far_radius),
    0xc706d790: ('auto_player_detection_near_radius', _decode_auto_player_detection_near_radius),
}

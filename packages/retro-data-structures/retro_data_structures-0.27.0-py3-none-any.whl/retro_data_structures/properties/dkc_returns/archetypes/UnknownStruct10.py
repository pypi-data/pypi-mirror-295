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
    class UnknownStruct10Json(typing_extensions.TypedDict):
        max_speed_x: float
        tracking_speed_x: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x206dea2e, 0xa57469d3)


@dataclasses.dataclass()
class UnknownStruct10(BaseProperty):
    max_speed_x: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x206dea2e, original_name='MaxSpeedX'
        ),
    })
    tracking_speed_x: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa57469d3, original_name='TrackingSpeedX'
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

        data.write(b' m\xea.')  # 0x206dea2e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_speed_x))

        data.write(b'\xa5ti\xd3')  # 0xa57469d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tracking_speed_x))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct10Json", data)
        return cls(
            max_speed_x=json_data['max_speed_x'],
            tracking_speed_x=json_data['tracking_speed_x'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'max_speed_x': self.max_speed_x,
            'tracking_speed_x': self.tracking_speed_x,
        }


def _decode_max_speed_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tracking_speed_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x206dea2e: ('max_speed_x', _decode_max_speed_x),
    0xa57469d3: ('tracking_speed_x', _decode_tracking_speed_x),
}

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
    class RambiControllerDataJson(typing_extensions.TypedDict):
        flee_speed_percentage: float
        maintain_direction_time: float
        off_screen_turn_around_distance: float
        despawn_timer: float
        despawn_distance: float
        far_despawn_distance: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x49bfc1b, 0x4466016e, 0x7ff6b094, 0xbc2f0b41, 0xe7655628, 0xebe02cd7)


@dataclasses.dataclass()
class RambiControllerData(BaseProperty):
    flee_speed_percentage: float = dataclasses.field(default=50.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x049bfc1b, original_name='FleeSpeedPercentage'
        ),
    })
    maintain_direction_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4466016e, original_name='MaintainDirectionTime'
        ),
    })
    off_screen_turn_around_distance: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7ff6b094, original_name='OffScreenTurnAroundDistance'
        ),
    })
    despawn_timer: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbc2f0b41, original_name='DespawnTimer'
        ),
    })
    despawn_distance: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe7655628, original_name='DespawnDistance'
        ),
    })
    far_despawn_distance: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xebe02cd7, original_name='FarDespawnDistance'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(60))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x04\x9b\xfc\x1b')  # 0x49bfc1b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flee_speed_percentage))

        data.write(b'Df\x01n')  # 0x4466016e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maintain_direction_time))

        data.write(b'\x7f\xf6\xb0\x94')  # 0x7ff6b094
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.off_screen_turn_around_distance))

        data.write(b'\xbc/\x0bA')  # 0xbc2f0b41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.despawn_timer))

        data.write(b'\xe7eV(')  # 0xe7655628
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.despawn_distance))

        data.write(b'\xeb\xe0,\xd7')  # 0xebe02cd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.far_despawn_distance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("RambiControllerDataJson", data)
        return cls(
            flee_speed_percentage=json_data['flee_speed_percentage'],
            maintain_direction_time=json_data['maintain_direction_time'],
            off_screen_turn_around_distance=json_data['off_screen_turn_around_distance'],
            despawn_timer=json_data['despawn_timer'],
            despawn_distance=json_data['despawn_distance'],
            far_despawn_distance=json_data['far_despawn_distance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'flee_speed_percentage': self.flee_speed_percentage,
            'maintain_direction_time': self.maintain_direction_time,
            'off_screen_turn_around_distance': self.off_screen_turn_around_distance,
            'despawn_timer': self.despawn_timer,
            'despawn_distance': self.despawn_distance,
            'far_despawn_distance': self.far_despawn_distance,
        }


def _decode_flee_speed_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maintain_direction_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_off_screen_turn_around_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_despawn_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_despawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_far_despawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x49bfc1b: ('flee_speed_percentage', _decode_flee_speed_percentage),
    0x4466016e: ('maintain_direction_time', _decode_maintain_direction_time),
    0x7ff6b094: ('off_screen_turn_around_distance', _decode_off_screen_turn_around_distance),
    0xbc2f0b41: ('despawn_timer', _decode_despawn_timer),
    0xe7655628: ('despawn_distance', _decode_despawn_distance),
    0xebe02cd7: ('far_despawn_distance', _decode_far_despawn_distance),
}

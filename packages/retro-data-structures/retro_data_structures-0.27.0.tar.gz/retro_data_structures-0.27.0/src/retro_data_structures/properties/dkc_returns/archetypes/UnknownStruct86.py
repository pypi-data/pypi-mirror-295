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
import retro_data_structures.enums.dkc_returns as enums

if typing.TYPE_CHECKING:
    class UnknownStruct86Json(typing_extensions.TypedDict):
        unknown: bool
        movement_speed: float
        locomotion_speed: int
        start_turn_distance: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x52f2ec16, 0x416f15e8, 0x8cebeb1e, 0xf572256b)


@dataclasses.dataclass()
class UnknownStruct86(BaseProperty):
    unknown: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x52f2ec16, original_name='Unknown'
        ),
    })
    movement_speed: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x416f15e8, original_name='MovementSpeed'
        ),
    })
    locomotion_speed: enums.LocomotionSpeed = dataclasses.field(default=enums.LocomotionSpeed.Unknown1, metadata={
        'reflection': FieldReflection[enums.LocomotionSpeed](
            enums.LocomotionSpeed, id=0x8cebeb1e, original_name='LocomotionSpeed', from_json=enums.LocomotionSpeed.from_json, to_json=enums.LocomotionSpeed.to_json
        ),
    })
    start_turn_distance: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf572256b, original_name='StartTurnDistance'
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
            _FAST_FORMAT = struct.Struct('>LH?LHfLHLLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(37))
        assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            enums.LocomotionSpeed(dec[8]),
            dec[11],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'R\xf2\xec\x16')  # 0x52f2ec16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'Ao\x15\xe8')  # 0x416f15e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_speed))

        data.write(b'\x8c\xeb\xeb\x1e')  # 0x8cebeb1e
        data.write(b'\x00\x04')  # size
        self.locomotion_speed.to_stream(data)

        data.write(b'\xf5r%k')  # 0xf572256b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_turn_distance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct86Json", data)
        return cls(
            unknown=json_data['unknown'],
            movement_speed=json_data['movement_speed'],
            locomotion_speed=enums.LocomotionSpeed.from_json(json_data['locomotion_speed']),
            start_turn_distance=json_data['start_turn_distance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'movement_speed': self.movement_speed,
            'locomotion_speed': self.locomotion_speed.to_json(),
            'start_turn_distance': self.start_turn_distance,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_movement_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_locomotion_speed(data: typing.BinaryIO, property_size: int):
    return enums.LocomotionSpeed.from_stream(data)


def _decode_start_turn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x52f2ec16: ('unknown', _decode_unknown),
    0x416f15e8: ('movement_speed', _decode_movement_speed),
    0x8cebeb1e: ('locomotion_speed', _decode_locomotion_speed),
    0xf572256b: ('start_turn_distance', _decode_start_turn_distance),
}

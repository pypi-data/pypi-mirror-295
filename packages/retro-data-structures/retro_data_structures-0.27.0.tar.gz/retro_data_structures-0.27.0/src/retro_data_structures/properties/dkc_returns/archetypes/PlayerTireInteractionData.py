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
    class PlayerTireInteractionDataJson(typing_extensions.TypedDict):
        pre_tire_jump_buffer: float
        pre_tire_jump_buffer_sd: float
        programmatic_turn_speed: float
        bump_into_tire_wall_min_speed: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x3e65410c, 0x784d143f, 0xcf03cb0c, 0x3a32dfcb)


@dataclasses.dataclass()
class PlayerTireInteractionData(BaseProperty):
    pre_tire_jump_buffer: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3e65410c, original_name='PreTireJumpBuffer'
        ),
    })
    pre_tire_jump_buffer_sd: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x784d143f, original_name='PreTireJumpBufferSD'
        ),
    })
    programmatic_turn_speed: float = dataclasses.field(default=450.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcf03cb0c, original_name='ProgrammaticTurnSpeed'
        ),
    })
    bump_into_tire_wall_min_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3a32dfcb, original_name='BumpIntoTireWallMinSpeed'
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

        data.write(b'>eA\x0c')  # 0x3e65410c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_tire_jump_buffer))

        data.write(b'xM\x14?')  # 0x784d143f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_tire_jump_buffer_sd))

        data.write(b'\xcf\x03\xcb\x0c')  # 0xcf03cb0c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.programmatic_turn_speed))

        data.write(b':2\xdf\xcb')  # 0x3a32dfcb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bump_into_tire_wall_min_speed))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerTireInteractionDataJson", data)
        return cls(
            pre_tire_jump_buffer=json_data['pre_tire_jump_buffer'],
            pre_tire_jump_buffer_sd=json_data['pre_tire_jump_buffer_sd'],
            programmatic_turn_speed=json_data['programmatic_turn_speed'],
            bump_into_tire_wall_min_speed=json_data['bump_into_tire_wall_min_speed'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'pre_tire_jump_buffer': self.pre_tire_jump_buffer,
            'pre_tire_jump_buffer_sd': self.pre_tire_jump_buffer_sd,
            'programmatic_turn_speed': self.programmatic_turn_speed,
            'bump_into_tire_wall_min_speed': self.bump_into_tire_wall_min_speed,
        }


def _decode_pre_tire_jump_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pre_tire_jump_buffer_sd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_programmatic_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bump_into_tire_wall_min_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3e65410c: ('pre_tire_jump_buffer', _decode_pre_tire_jump_buffer),
    0x784d143f: ('pre_tire_jump_buffer_sd', _decode_pre_tire_jump_buffer_sd),
    0xcf03cb0c: ('programmatic_turn_speed', _decode_programmatic_turn_speed),
    0x3a32dfcb: ('bump_into_tire_wall_min_speed', _decode_bump_into_tire_wall_min_speed),
}

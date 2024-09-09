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
    class PlayerMovementParametersJson(typing_extensions.TypedDict):
        minimum_walk_speed: float
        maximum_run_speed: float
        acceleration: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x1ff79060, 0x950a7b96, 0x39fb7978)


@dataclasses.dataclass()
class PlayerMovementParameters(BaseProperty):
    minimum_walk_speed: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1ff79060, original_name='MinimumWalkSpeed'
        ),
    })
    maximum_run_speed: float = dataclasses.field(default=9.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x950a7b96, original_name='MaximumRunSpeed'
        ),
    })
    acceleration: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39fb7978, original_name='Acceleration'
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
        if property_count != 3:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(30))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x1f\xf7\x90`')  # 0x1ff79060
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_walk_speed))

        data.write(b'\x95\n{\x96')  # 0x950a7b96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_run_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerMovementParametersJson", data)
        return cls(
            minimum_walk_speed=json_data['minimum_walk_speed'],
            maximum_run_speed=json_data['maximum_run_speed'],
            acceleration=json_data['acceleration'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'minimum_walk_speed': self.minimum_walk_speed,
            'maximum_run_speed': self.maximum_run_speed,
            'acceleration': self.acceleration,
        }


def _decode_minimum_walk_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_run_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1ff79060: ('minimum_walk_speed', _decode_minimum_walk_speed),
    0x950a7b96: ('maximum_run_speed', _decode_maximum_run_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
}

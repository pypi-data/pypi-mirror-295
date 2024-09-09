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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class UnknownStruct196Json(typing_extensions.TypedDict):
        launch_direction: int
        unknown: json_util.JsonValue
        initial_velocity: float
        gravity: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x1f7ef449, 0xc0025200, 0x81473093, 0x2f2ae3e5)


@dataclasses.dataclass()
class UnknownStruct196(BaseProperty):
    launch_direction: enums.LaunchDirection = dataclasses.field(default=enums.LaunchDirection.Unknown1, metadata={
        'reflection': FieldReflection[enums.LaunchDirection](
            enums.LaunchDirection, id=0x1f7ef449, original_name='LaunchDirection', from_json=enums.LaunchDirection.from_json, to_json=enums.LaunchDirection.to_json
        ),
    })
    unknown: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xc0025200, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    initial_velocity: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x81473093, original_name='InitialVelocity'
        ),
    })
    gravity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
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
            _FAST_FORMAT = struct.Struct('>LHLLHfffLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(48))
        assert (dec[0], dec[3], dec[8], dec[11]) == _FAST_IDS
        return cls(
            enums.LaunchDirection(dec[2]),
            Vector(*dec[5:8]),
            dec[10],
            dec[13],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x1f~\xf4I')  # 0x1f7ef449
        data.write(b'\x00\x04')  # size
        self.launch_direction.to_stream(data)

        data.write(b'\xc0\x02R\x00')  # 0xc0025200
        data.write(b'\x00\x0c')  # size
        self.unknown.to_stream(data)

        data.write(b'\x81G0\x93')  # 0x81473093
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_velocity))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct196Json", data)
        return cls(
            launch_direction=enums.LaunchDirection.from_json(json_data['launch_direction']),
            unknown=Vector.from_json(json_data['unknown']),
            initial_velocity=json_data['initial_velocity'],
            gravity=json_data['gravity'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'launch_direction': self.launch_direction.to_json(),
            'unknown': self.unknown.to_json(),
            'initial_velocity': self.initial_velocity,
            'gravity': self.gravity,
        }


def _decode_launch_direction(data: typing.BinaryIO, property_size: int):
    return enums.LaunchDirection.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_initial_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1f7ef449: ('launch_direction', _decode_launch_direction),
    0xc0025200: ('unknown', _decode_unknown),
    0x81473093: ('initial_velocity', _decode_initial_velocity),
    0x2f2ae3e5: ('gravity', _decode_gravity),
}

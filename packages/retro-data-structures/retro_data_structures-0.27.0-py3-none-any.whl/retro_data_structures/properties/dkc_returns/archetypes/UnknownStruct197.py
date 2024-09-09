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
    class UnknownStruct197Json(typing_extensions.TypedDict):
        physics_target_type: int
        unknown_0xef531185: float
        unknown_0x0e6e350f: int
        gravity: float
        arc_height: float
        flight_time: float
        only_target_active: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x38f20661, 0xef531185, 0xe6e350f, 0x2f2ae3e5, 0x2150aa96, 0xfbd9fb93, 0x364f0b8)


@dataclasses.dataclass()
class UnknownStruct197(BaseProperty):
    physics_target_type: enums.PhysicsTargetType = dataclasses.field(default=enums.PhysicsTargetType.Unknown2, metadata={
        'reflection': FieldReflection[enums.PhysicsTargetType](
            enums.PhysicsTargetType, id=0x38f20661, original_name='PhysicsTargetType', from_json=enums.PhysicsTargetType.from_json, to_json=enums.PhysicsTargetType.to_json
        ),
    })
    unknown_0xef531185: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xef531185, original_name='Unknown'
        ),
    })
    unknown_0x0e6e350f: int = dataclasses.field(default=3294124709, metadata={
        'reflection': FieldReflection[int](
            int, id=0x0e6e350f, original_name='Unknown'
        ),
    })  # Choice
    gravity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    arc_height: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2150aa96, original_name='ArcHeight'
        ),
    })
    flight_time: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfbd9fb93, original_name='FlightTime'
        ),
    })
    only_target_active: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0364f0b8, original_name='OnlyTargetActive'
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
            _FAST_FORMAT = struct.Struct('>LHLLHfLHLLHfLHfLHfLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(67))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) == _FAST_IDS
        return cls(
            enums.PhysicsTargetType(dec[2]),
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

        data.write(b'8\xf2\x06a')  # 0x38f20661
        data.write(b'\x00\x04')  # size
        self.physics_target_type.to_stream(data)

        data.write(b'\xefS\x11\x85')  # 0xef531185
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xef531185))

        data.write(b'\x0en5\x0f')  # 0xe6e350f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x0e6e350f))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'!P\xaa\x96')  # 0x2150aa96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.arc_height))

        data.write(b'\xfb\xd9\xfb\x93')  # 0xfbd9fb93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_time))

        data.write(b'\x03d\xf0\xb8')  # 0x364f0b8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.only_target_active))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct197Json", data)
        return cls(
            physics_target_type=enums.PhysicsTargetType.from_json(json_data['physics_target_type']),
            unknown_0xef531185=json_data['unknown_0xef531185'],
            unknown_0x0e6e350f=json_data['unknown_0x0e6e350f'],
            gravity=json_data['gravity'],
            arc_height=json_data['arc_height'],
            flight_time=json_data['flight_time'],
            only_target_active=json_data['only_target_active'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'physics_target_type': self.physics_target_type.to_json(),
            'unknown_0xef531185': self.unknown_0xef531185,
            'unknown_0x0e6e350f': self.unknown_0x0e6e350f,
            'gravity': self.gravity,
            'arc_height': self.arc_height,
            'flight_time': self.flight_time,
            'only_target_active': self.only_target_active,
        }


def _decode_physics_target_type(data: typing.BinaryIO, property_size: int):
    return enums.PhysicsTargetType.from_stream(data)


def _decode_unknown_0xef531185(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0e6e350f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arc_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_only_target_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x38f20661: ('physics_target_type', _decode_physics_target_type),
    0xef531185: ('unknown_0xef531185', _decode_unknown_0xef531185),
    0xe6e350f: ('unknown_0x0e6e350f', _decode_unknown_0x0e6e350f),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x2150aa96: ('arc_height', _decode_arc_height),
    0xfbd9fb93: ('flight_time', _decode_flight_time),
    0x364f0b8: ('only_target_active', _decode_only_target_active),
}

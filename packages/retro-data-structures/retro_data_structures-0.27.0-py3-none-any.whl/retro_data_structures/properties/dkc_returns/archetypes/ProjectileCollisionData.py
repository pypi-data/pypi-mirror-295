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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class ProjectileCollisionDataJson(typing_extensions.TypedDict):
        unknown_0xa9f8a74f: int
        collision_type: int
        sphere_radius: float
        unknown_0xfef3d2da: json_util.JsonValue
        unknown_0x2918609b: json_util.JsonValue
    

_FAST_FORMAT = None
_FAST_IDS = (0xa9f8a74f, 0xb674ea3d, 0xf3d6e959, 0xfef3d2da, 0x2918609b)


@dataclasses.dataclass()
class ProjectileCollisionData(BaseProperty):
    unknown_0xa9f8a74f: int = dataclasses.field(default=64, metadata={
        'reflection': FieldReflection[int](
            int, id=0xa9f8a74f, original_name='Unknown'
        ),
    })
    collision_type: int = dataclasses.field(default=988868003, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb674ea3d, original_name='CollisionType'
        ),
    })  # Choice
    sphere_radius: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf3d6e959, original_name='SphereRadius'
        ),
    })
    unknown_0xfef3d2da: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xfef3d2da, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_0x2918609b: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x2918609b, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
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
        if property_count != 5:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHlLHLLHfLHfffLHfff')
    
        dec = _FAST_FORMAT.unpack(data.read(66))
        assert (dec[0], dec[3], dec[6], dec[9], dec[14]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            Vector(*dec[11:14]),
            Vector(*dec[16:19]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xa9\xf8\xa7O')  # 0xa9f8a74f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa9f8a74f))

        data.write(b'\xb6t\xea=')  # 0xb674ea3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.collision_type))

        data.write(b'\xf3\xd6\xe9Y')  # 0xf3d6e959
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sphere_radius))

        data.write(b'\xfe\xf3\xd2\xda')  # 0xfef3d2da
        data.write(b'\x00\x0c')  # size
        self.unknown_0xfef3d2da.to_stream(data)

        data.write(b')\x18`\x9b')  # 0x2918609b
        data.write(b'\x00\x0c')  # size
        self.unknown_0x2918609b.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ProjectileCollisionDataJson", data)
        return cls(
            unknown_0xa9f8a74f=json_data['unknown_0xa9f8a74f'],
            collision_type=json_data['collision_type'],
            sphere_radius=json_data['sphere_radius'],
            unknown_0xfef3d2da=Vector.from_json(json_data['unknown_0xfef3d2da']),
            unknown_0x2918609b=Vector.from_json(json_data['unknown_0x2918609b']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xa9f8a74f': self.unknown_0xa9f8a74f,
            'collision_type': self.collision_type,
            'sphere_radius': self.sphere_radius,
            'unknown_0xfef3d2da': self.unknown_0xfef3d2da.to_json(),
            'unknown_0x2918609b': self.unknown_0x2918609b.to_json(),
        }


def _decode_unknown_0xa9f8a74f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_collision_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sphere_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfef3d2da(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x2918609b(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa9f8a74f: ('unknown_0xa9f8a74f', _decode_unknown_0xa9f8a74f),
    0xb674ea3d: ('collision_type', _decode_collision_type),
    0xf3d6e959: ('sphere_radius', _decode_sphere_radius),
    0xfef3d2da: ('unknown_0xfef3d2da', _decode_unknown_0xfef3d2da),
    0x2918609b: ('unknown_0x2918609b', _decode_unknown_0x2918609b),
}

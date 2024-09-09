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
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence

if typing.TYPE_CHECKING:
    class UnknownStruct76Json(typing_extensions.TypedDict):
        motion_type: json_util.JsonObject
        use_vertical_motion: bool
        convergence: json_util.JsonObject
        collision_type: int
    

@dataclasses.dataclass()
class UnknownStruct76(BaseProperty):
    motion_type: Convergence = dataclasses.field(default_factory=Convergence, metadata={
        'reflection': FieldReflection[Convergence](
            Convergence, id=0xc1547af3, original_name='MotionType', from_json=Convergence.from_json, to_json=Convergence.to_json
        ),
    })
    use_vertical_motion: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7d0bca87, original_name='UseVerticalMotion'
        ),
    })
    convergence: Convergence = dataclasses.field(default_factory=Convergence, metadata={
        'reflection': FieldReflection[Convergence](
            Convergence, id=0xd9a90ec3, original_name='Convergence', from_json=Convergence.from_json, to_json=Convergence.to_json
        ),
    })
    collision_type: enums.CollisionType = dataclasses.field(default=enums.CollisionType.Unknown1, metadata={
        'reflection': FieldReflection[enums.CollisionType](
            enums.CollisionType, id=0xb674ea3d, original_name='CollisionType', from_json=enums.CollisionType.from_json, to_json=enums.CollisionType.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc1547af3
        motion_type = Convergence.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7d0bca87
        use_vertical_motion = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9a90ec3
        convergence = Convergence.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb674ea3d
        collision_type = enums.CollisionType.from_stream(data)
    
        return cls(motion_type, use_vertical_motion, convergence, collision_type)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xc1Tz\xf3')  # 0xc1547af3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\x0b\xca\x87')  # 0x7d0bca87
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_vertical_motion))

        data.write(b'\xd9\xa9\x0e\xc3')  # 0xd9a90ec3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6t\xea=')  # 0xb674ea3d
        data.write(b'\x00\x04')  # size
        self.collision_type.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct76Json", data)
        return cls(
            motion_type=Convergence.from_json(json_data['motion_type']),
            use_vertical_motion=json_data['use_vertical_motion'],
            convergence=Convergence.from_json(json_data['convergence']),
            collision_type=enums.CollisionType.from_json(json_data['collision_type']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'motion_type': self.motion_type.to_json(),
            'use_vertical_motion': self.use_vertical_motion,
            'convergence': self.convergence.to_json(),
            'collision_type': self.collision_type.to_json(),
        }


def _decode_use_vertical_motion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_collision_type(data: typing.BinaryIO, property_size: int):
    return enums.CollisionType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc1547af3: ('motion_type', Convergence.from_stream),
    0x7d0bca87: ('use_vertical_motion', _decode_use_vertical_motion),
    0xd9a90ec3: ('convergence', Convergence.from_stream),
    0xb674ea3d: ('collision_type', _decode_collision_type),
}

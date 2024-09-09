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
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileBounceData import ProjectileBounceData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileCollisionData import ProjectileCollisionData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileData import ProjectileData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileMotionData import ProjectileMotionData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileRenderData import ProjectileRenderData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct205 import UnknownStruct205
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class UnknownStruct206Json(typing_extensions.TypedDict):
        actor_information: json_util.JsonObject
        projectile_data: json_util.JsonObject
        projectile_render_data: json_util.JsonObject
        projectile_collision_data: json_util.JsonObject
        projectile_motion_data: json_util.JsonObject
        can_bounce: bool
        projectile_bounce_data: json_util.JsonObject
        scale: json_util.JsonValue
        unknown_struct205: json_util.JsonObject
        unknown: float
    

@dataclasses.dataclass()
class UnknownStruct206(BaseProperty):
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    projectile_data: ProjectileData = dataclasses.field(default_factory=ProjectileData, metadata={
        'reflection': FieldReflection[ProjectileData](
            ProjectileData, id=0xa5cc2982, original_name='ProjectileData', from_json=ProjectileData.from_json, to_json=ProjectileData.to_json
        ),
    })
    projectile_render_data: ProjectileRenderData = dataclasses.field(default_factory=ProjectileRenderData, metadata={
        'reflection': FieldReflection[ProjectileRenderData](
            ProjectileRenderData, id=0xd90dab09, original_name='ProjectileRenderData', from_json=ProjectileRenderData.from_json, to_json=ProjectileRenderData.to_json
        ),
    })
    projectile_collision_data: ProjectileCollisionData = dataclasses.field(default_factory=ProjectileCollisionData, metadata={
        'reflection': FieldReflection[ProjectileCollisionData](
            ProjectileCollisionData, id=0x58d9785f, original_name='ProjectileCollisionData', from_json=ProjectileCollisionData.from_json, to_json=ProjectileCollisionData.to_json
        ),
    })
    projectile_motion_data: ProjectileMotionData = dataclasses.field(default_factory=ProjectileMotionData, metadata={
        'reflection': FieldReflection[ProjectileMotionData](
            ProjectileMotionData, id=0x90dcef98, original_name='ProjectileMotionData', from_json=ProjectileMotionData.from_json, to_json=ProjectileMotionData.to_json
        ),
    })
    can_bounce: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcc4284a2, original_name='CanBounce'
        ),
    })
    projectile_bounce_data: ProjectileBounceData = dataclasses.field(default_factory=ProjectileBounceData, metadata={
        'reflection': FieldReflection[ProjectileBounceData](
            ProjectileBounceData, id=0x50a7e94b, original_name='ProjectileBounceData', from_json=ProjectileBounceData.from_json, to_json=ProjectileBounceData.to_json
        ),
    })
    scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xf726e5da, original_name='Scale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_struct205: UnknownStruct205 = dataclasses.field(default_factory=UnknownStruct205, metadata={
        'reflection': FieldReflection[UnknownStruct205](
            UnknownStruct205, id=0xea0f134d, original_name='UnknownStruct205', from_json=UnknownStruct205.from_json, to_json=UnknownStruct205.to_json
        ),
    })
    unknown: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3180d4f3, original_name='Unknown'
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
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa5cc2982
        projectile_data = ProjectileData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd90dab09
        projectile_render_data = ProjectileRenderData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x58d9785f
        projectile_collision_data = ProjectileCollisionData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x90dcef98
        projectile_motion_data = ProjectileMotionData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcc4284a2
        can_bounce = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50a7e94b
        projectile_bounce_data = ProjectileBounceData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf726e5da
        scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xea0f134d
        unknown_struct205 = UnknownStruct205.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3180d4f3
        unknown = struct.unpack('>f', data.read(4))[0]
    
        return cls(actor_information, projectile_data, projectile_render_data, projectile_collision_data, projectile_motion_data, can_bounce, projectile_bounce_data, scale, unknown_struct205, unknown)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\xcc)\x82')  # 0xa5cc2982
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd9\r\xab\t')  # 0xd90dab09
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_render_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\xd9x_')  # 0x58d9785f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_collision_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90\xdc\xef\x98')  # 0x90dcef98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_motion_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xccB\x84\xa2')  # 0xcc4284a2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_bounce))

        data.write(b'P\xa7\xe9K')  # 0x50a7e94b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_bounce_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7&\xe5\xda')  # 0xf726e5da
        data.write(b'\x00\x0c')  # size
        self.scale.to_stream(data)

        data.write(b'\xea\x0f\x13M')  # 0xea0f134d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct205.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\x80\xd4\xf3')  # 0x3180d4f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct206Json", data)
        return cls(
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            projectile_data=ProjectileData.from_json(json_data['projectile_data']),
            projectile_render_data=ProjectileRenderData.from_json(json_data['projectile_render_data']),
            projectile_collision_data=ProjectileCollisionData.from_json(json_data['projectile_collision_data']),
            projectile_motion_data=ProjectileMotionData.from_json(json_data['projectile_motion_data']),
            can_bounce=json_data['can_bounce'],
            projectile_bounce_data=ProjectileBounceData.from_json(json_data['projectile_bounce_data']),
            scale=Vector.from_json(json_data['scale']),
            unknown_struct205=UnknownStruct205.from_json(json_data['unknown_struct205']),
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'actor_information': self.actor_information.to_json(),
            'projectile_data': self.projectile_data.to_json(),
            'projectile_render_data': self.projectile_render_data.to_json(),
            'projectile_collision_data': self.projectile_collision_data.to_json(),
            'projectile_motion_data': self.projectile_motion_data.to_json(),
            'can_bounce': self.can_bounce,
            'projectile_bounce_data': self.projectile_bounce_data.to_json(),
            'scale': self.scale.to_json(),
            'unknown_struct205': self.unknown_struct205.to_json(),
            'unknown': self.unknown,
        }


def _decode_can_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0xa5cc2982: ('projectile_data', ProjectileData.from_stream),
    0xd90dab09: ('projectile_render_data', ProjectileRenderData.from_stream),
    0x58d9785f: ('projectile_collision_data', ProjectileCollisionData.from_stream),
    0x90dcef98: ('projectile_motion_data', ProjectileMotionData.from_stream),
    0xcc4284a2: ('can_bounce', _decode_can_bounce),
    0x50a7e94b: ('projectile_bounce_data', ProjectileBounceData.from_stream),
    0xf726e5da: ('scale', _decode_scale),
    0xea0f134d: ('unknown_struct205', UnknownStruct205.from_stream),
    0x3180d4f3: ('unknown', _decode_unknown),
}

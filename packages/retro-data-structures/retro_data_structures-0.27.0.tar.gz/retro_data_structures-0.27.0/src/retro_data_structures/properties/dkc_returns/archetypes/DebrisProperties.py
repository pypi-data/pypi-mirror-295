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
from retro_data_structures.properties.dkc_returns.archetypes.DebrisPropertiesOrientationEnum import DebrisPropertiesOrientationEnum
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct17 import UnknownStruct17
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class DebrisPropertiesJson(typing_extensions.TypedDict):
        cone_spread_yaw: float
        cone_spread_pitch: float
        initial_direction: json_util.JsonValue
        position_offset: json_util.JsonValue
        transform_position_offset: bool
        minimum_speed: float
        maximum_speed: float
        minimum_spin_speed: json_util.JsonValue
        maximum_spin_speed: json_util.JsonValue
        minimum_lifetime: float
        maximum_lifetime: float
        disable_collision_time: float
        fade_in_end_percentage: float
        fade_out_start_percentage: float
        start_color: json_util.JsonValue
        middle_color: json_util.JsonValue
        end_color: json_util.JsonValue
        unknown_0xd79690b4: bool
        unknown_0x0145d02d: bool
        scale_start_percentage: float
        final_scale: json_util.JsonValue
        unknown_0x417f4a91: float
        friction: float
        gravity: float
        disable_physics_threshold: float
        model: int
        model_pivot_point: json_util.JsonValue
        created_sound: int
        bounce_sound: int
        max_bounce_sounds: int
        unknown_0x76c79503: float
        unknown_0x310dfac8: float
        unknown_0x5e9f5215: float
        unknown_0x39743618: float
        unknown_0x33e0fbb4: float
        unknown_0xe82e7ed7: float
        unknown_0x855ee21b: float
        particle_system1: int
        particle_system1_scale: json_util.JsonValue
        particle_system1_uses_global_translation: bool
        particle_system1_uses_global_orientation: bool
        particle_system1_wait_for_particles_to_die: bool
        particle_system1_orientation: json_util.JsonObject
        particle_system2: int
        particle_system2_scale: json_util.JsonValue
        particle_system2_uses_global_translation: bool
        particle_system2_uses_global_orientation: bool
        particle_system2_wait_for_particles_to_die: bool
        particle_system2_orientation: json_util.JsonObject
        bounce_particle_effect: int
        bounce_particle_scale: json_util.JsonValue
        bounce_effect_transform: json_util.JsonObject
        is_collider: bool
        unknown_0xe73b9eb0: bool
        die_on_collision: bool
        unknown_0x8723498a: bool
        unknown_0x0f2c673e: int
        collide_with_characters: bool
        unknown_0x8ec68a96: bool
        fixed_bounce_speed_x: float
        fixed_bounce_speed_y: float
        unknown_0xbfd82a19: bool
        unknown_0x723d42d6: bool
        unknown_0x4edb1d0e: bool
        unknown_0xbf496273: bool
        unknown_0xf83c1c1f: bool
        unknown_0x88b1af46: bool
        render_in_foreground: bool
        allow_silhouette: bool
        unknown_0xe5eced02: bool
    

@dataclasses.dataclass()
class DebrisProperties(BaseProperty):
    cone_spread_yaw: float = dataclasses.field(default=180.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5c3c4a57, original_name='ConeSpreadYaw'
        ),
    })
    cone_spread_pitch: float = dataclasses.field(default=180.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa79fc55f, original_name='ConeSpreadPitch'
        ),
    })
    initial_direction: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x01a0dfe6, original_name='InitialDirection', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    position_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xef90f09d, original_name='PositionOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    transform_position_offset: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc4b1e6a1, original_name='TransformPositionOffset'
        ),
    })
    minimum_speed: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0185263e, original_name='MinimumSpeed'
        ),
    })
    maximum_speed: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x140ef2cc, original_name='MaximumSpeed'
        ),
    })
    minimum_spin_speed: Vector = dataclasses.field(default_factory=lambda: Vector(x=-1.0, y=-1.0, z=-1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xf78c8ac7, original_name='MinimumSpinSpeed', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    maximum_spin_speed: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xb69bb541, original_name='MaximumSpinSpeed', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    minimum_lifetime: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd6594622, original_name='MinimumLifetime'
        ),
    })
    maximum_lifetime: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xff27bb3a, original_name='MaximumLifetime'
        ),
    })
    disable_collision_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6b571ba5, original_name='DisableCollisionTime'
        ),
    })
    fade_in_end_percentage: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x50051a17, original_name='FadeInEndPercentage'
        ),
    })
    fade_out_start_percentage: float = dataclasses.field(default=80.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6353c409, original_name='FadeOutStartPercentage'
        ),
    })
    start_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x3a5634d8, original_name='StartColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    middle_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x7c6ebe98, original_name='MiddleColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    end_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x5af5867d, original_name='EndColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    unknown_0xd79690b4: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd79690b4, original_name='Unknown'
        ),
    })
    unknown_0x0145d02d: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0145d02d, original_name='Unknown'
        ),
    })
    scale_start_percentage: float = dataclasses.field(default=80.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x886e7c9f, original_name='ScaleStartPercentage'
        ),
    })
    final_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x80c22a0a, original_name='FinalScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_0x417f4a91: float = dataclasses.field(default=0.375, metadata={
        'reflection': FieldReflection[float](
            float, id=0x417f4a91, original_name='Unknown'
        ),
    })
    friction: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x16b72d49, original_name='Friction'
        ),
    })
    gravity: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    disable_physics_threshold: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x295f05b7, original_name='DisablePhysicsThreshold'
        ),
    })
    model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc27ffa8f, original_name='Model'
        ),
    })
    model_pivot_point: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xeedbb07e, original_name='ModelPivotPoint', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    created_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x93f8e0b0, original_name='CreatedSound'
        ),
    })
    bounce_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf1925576, original_name='BounceSound'
        ),
    })
    max_bounce_sounds: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x991202c3, original_name='MaxBounceSounds'
        ),
    })
    unknown_0x76c79503: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x76c79503, original_name='Unknown'
        ),
    })
    unknown_0x310dfac8: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x310dfac8, original_name='Unknown'
        ),
    })
    unknown_0x5e9f5215: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5e9f5215, original_name='Unknown'
        ),
    })
    unknown_0x39743618: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39743618, original_name='Unknown'
        ),
    })
    unknown_0x33e0fbb4: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x33e0fbb4, original_name='Unknown'
        ),
    })
    unknown_0xe82e7ed7: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe82e7ed7, original_name='Unknown'
        ),
    })
    unknown_0x855ee21b: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x855ee21b, original_name='Unknown'
        ),
    })
    particle_system1: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x478d0aa3, original_name='ParticleSystem1'
        ),
    })
    particle_system1_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x19a6f71f, original_name='ParticleSystem1Scale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    particle_system1_uses_global_translation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3b03a01e, original_name='ParticleSystem1UsesGlobalTranslation'
        ),
    })
    particle_system1_uses_global_orientation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdb1fa61c, original_name='ParticleSystem1UsesGlobalOrientation'
        ),
    })
    particle_system1_wait_for_particles_to_die: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3bdd2fed, original_name='ParticleSystem1WaitForParticlesToDie'
        ),
    })
    particle_system1_orientation: DebrisPropertiesOrientationEnum = dataclasses.field(default_factory=DebrisPropertiesOrientationEnum, metadata={
        'reflection': FieldReflection[DebrisPropertiesOrientationEnum](
            DebrisPropertiesOrientationEnum, id=0xf5dd4690, original_name='ParticleSystem1Orientation', from_json=DebrisPropertiesOrientationEnum.from_json, to_json=DebrisPropertiesOrientationEnum.to_json
        ),
    })
    particle_system2: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc119780d, original_name='ParticleSystem2'
        ),
    })
    particle_system2_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x6e3825ef, original_name='ParticleSystem2Scale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    particle_system2_uses_global_translation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc9544de6, original_name='ParticleSystem2UsesGlobalTranslation'
        ),
    })
    particle_system2_uses_global_orientation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x29484be4, original_name='ParticleSystem2UsesGlobalOrientation'
        ),
    })
    particle_system2_wait_for_particles_to_die: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc98ac215, original_name='ParticleSystem2WaitForParticlesToDie'
        ),
    })
    particle_system2_orientation: DebrisPropertiesOrientationEnum = dataclasses.field(default_factory=DebrisPropertiesOrientationEnum, metadata={
        'reflection': FieldReflection[DebrisPropertiesOrientationEnum](
            DebrisPropertiesOrientationEnum, id=0x3ce95d9d, original_name='ParticleSystem2Orientation', from_json=DebrisPropertiesOrientationEnum.from_json, to_json=DebrisPropertiesOrientationEnum.to_json
        ),
    })
    bounce_particle_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x217c37c2, original_name='BounceParticleEffect'
        ),
    })
    bounce_particle_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x60d6bf8e, original_name='BounceParticleScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    bounce_effect_transform: UnknownStruct17 = dataclasses.field(default_factory=UnknownStruct17, metadata={
        'reflection': FieldReflection[UnknownStruct17](
            UnknownStruct17, id=0xce59ebff, original_name='BounceEffectTransform', from_json=UnknownStruct17.from_json, to_json=UnknownStruct17.to_json
        ),
    })
    is_collider: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2c7b18dd, original_name='IsCollider'
        ),
    })
    unknown_0xe73b9eb0: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe73b9eb0, original_name='Unknown'
        ),
    })
    die_on_collision: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0d7fad55, original_name='DieOnCollision'
        ),
    })
    unknown_0x8723498a: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8723498a, original_name='Unknown'
        ),
    })
    unknown_0x0f2c673e: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x0f2c673e, original_name='Unknown'
        ),
    })
    collide_with_characters: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x55d8ace3, original_name='CollideWithCharacters'
        ),
    })
    unknown_0x8ec68a96: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8ec68a96, original_name='Unknown'
        ),
    })
    fixed_bounce_speed_x: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9bd94326, original_name='FixedBounceSpeedX'
        ),
    })
    fixed_bounce_speed_y: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x50859083, original_name='FixedBounceSpeedY'
        ),
    })
    unknown_0xbfd82a19: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbfd82a19, original_name='Unknown'
        ),
    })
    unknown_0x723d42d6: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x723d42d6, original_name='Unknown'
        ),
    })
    unknown_0x4edb1d0e: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4edb1d0e, original_name='Unknown'
        ),
    })
    unknown_0xbf496273: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbf496273, original_name='Unknown'
        ),
    })
    unknown_0xf83c1c1f: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf83c1c1f, original_name='Unknown'
        ),
    })
    unknown_0x88b1af46: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x88b1af46, original_name='Unknown'
        ),
    })
    render_in_foreground: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa6aa06d5, original_name='RenderInForeground'
        ),
    })
    allow_silhouette: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x32375e0e, original_name='AllowSilhouette'
        ),
    })
    unknown_0xe5eced02: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe5eced02, original_name='Unknown'
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
        if property_count != 70:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5c3c4a57
        cone_spread_yaw = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa79fc55f
        cone_spread_pitch = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x01a0dfe6
        initial_direction = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xef90f09d
        position_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc4b1e6a1
        transform_position_offset = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0185263e
        minimum_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x140ef2cc
        maximum_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf78c8ac7
        minimum_spin_speed = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb69bb541
        maximum_spin_speed = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd6594622
        minimum_lifetime = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xff27bb3a
        maximum_lifetime = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b571ba5
        disable_collision_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50051a17
        fade_in_end_percentage = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6353c409
        fade_out_start_percentage = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a5634d8
        start_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c6ebe98
        middle_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5af5867d
        end_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd79690b4
        unknown_0xd79690b4 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0145d02d
        unknown_0x0145d02d = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x886e7c9f
        scale_start_percentage = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x80c22a0a
        final_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x417f4a91
        unknown_0x417f4a91 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x16b72d49
        friction = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x295f05b7
        disable_physics_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc27ffa8f
        model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeedbb07e
        model_pivot_point = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x93f8e0b0
        created_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf1925576
        bounce_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x991202c3
        max_bounce_sounds = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76c79503
        unknown_0x76c79503 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x310dfac8
        unknown_0x310dfac8 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e9f5215
        unknown_0x5e9f5215 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x39743618
        unknown_0x39743618 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x33e0fbb4
        unknown_0x33e0fbb4 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe82e7ed7
        unknown_0xe82e7ed7 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x855ee21b
        unknown_0x855ee21b = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x478d0aa3
        particle_system1 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x19a6f71f
        particle_system1_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3b03a01e
        particle_system1_uses_global_translation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb1fa61c
        particle_system1_uses_global_orientation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3bdd2fed
        particle_system1_wait_for_particles_to_die = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5dd4690
        particle_system1_orientation = DebrisPropertiesOrientationEnum.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc119780d
        particle_system2 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6e3825ef
        particle_system2_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc9544de6
        particle_system2_uses_global_translation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x29484be4
        particle_system2_uses_global_orientation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc98ac215
        particle_system2_wait_for_particles_to_die = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3ce95d9d
        particle_system2_orientation = DebrisPropertiesOrientationEnum.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x217c37c2
        bounce_particle_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60d6bf8e
        bounce_particle_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xce59ebff
        bounce_effect_transform = UnknownStruct17.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2c7b18dd
        is_collider = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe73b9eb0
        unknown_0xe73b9eb0 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0d7fad55
        die_on_collision = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8723498a
        unknown_0x8723498a = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0f2c673e
        unknown_0x0f2c673e = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x55d8ace3
        collide_with_characters = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ec68a96
        unknown_0x8ec68a96 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9bd94326
        fixed_bounce_speed_x = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50859083
        fixed_bounce_speed_y = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbfd82a19
        unknown_0xbfd82a19 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x723d42d6
        unknown_0x723d42d6 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4edb1d0e
        unknown_0x4edb1d0e = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf496273
        unknown_0xbf496273 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf83c1c1f
        unknown_0xf83c1c1f = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x88b1af46
        unknown_0x88b1af46 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa6aa06d5
        render_in_foreground = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x32375e0e
        allow_silhouette = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe5eced02
        unknown_0xe5eced02 = struct.unpack('>?', data.read(1))[0]
    
        return cls(cone_spread_yaw, cone_spread_pitch, initial_direction, position_offset, transform_position_offset, minimum_speed, maximum_speed, minimum_spin_speed, maximum_spin_speed, minimum_lifetime, maximum_lifetime, disable_collision_time, fade_in_end_percentage, fade_out_start_percentage, start_color, middle_color, end_color, unknown_0xd79690b4, unknown_0x0145d02d, scale_start_percentage, final_scale, unknown_0x417f4a91, friction, gravity, disable_physics_threshold, model, model_pivot_point, created_sound, bounce_sound, max_bounce_sounds, unknown_0x76c79503, unknown_0x310dfac8, unknown_0x5e9f5215, unknown_0x39743618, unknown_0x33e0fbb4, unknown_0xe82e7ed7, unknown_0x855ee21b, particle_system1, particle_system1_scale, particle_system1_uses_global_translation, particle_system1_uses_global_orientation, particle_system1_wait_for_particles_to_die, particle_system1_orientation, particle_system2, particle_system2_scale, particle_system2_uses_global_translation, particle_system2_uses_global_orientation, particle_system2_wait_for_particles_to_die, particle_system2_orientation, bounce_particle_effect, bounce_particle_scale, bounce_effect_transform, is_collider, unknown_0xe73b9eb0, die_on_collision, unknown_0x8723498a, unknown_0x0f2c673e, collide_with_characters, unknown_0x8ec68a96, fixed_bounce_speed_x, fixed_bounce_speed_y, unknown_0xbfd82a19, unknown_0x723d42d6, unknown_0x4edb1d0e, unknown_0xbf496273, unknown_0xf83c1c1f, unknown_0x88b1af46, render_in_foreground, allow_silhouette, unknown_0xe5eced02)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00F')  # 70 properties

        data.write(b'\\<JW')  # 0x5c3c4a57
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cone_spread_yaw))

        data.write(b'\xa7\x9f\xc5_')  # 0xa79fc55f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cone_spread_pitch))

        data.write(b'\x01\xa0\xdf\xe6')  # 0x1a0dfe6
        data.write(b'\x00\x0c')  # size
        self.initial_direction.to_stream(data)

        data.write(b'\xef\x90\xf0\x9d')  # 0xef90f09d
        data.write(b'\x00\x0c')  # size
        self.position_offset.to_stream(data)

        data.write(b'\xc4\xb1\xe6\xa1')  # 0xc4b1e6a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.transform_position_offset))

        data.write(b'\x01\x85&>')  # 0x185263e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_speed))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

        data.write(b'\xf7\x8c\x8a\xc7')  # 0xf78c8ac7
        data.write(b'\x00\x0c')  # size
        self.minimum_spin_speed.to_stream(data)

        data.write(b'\xb6\x9b\xb5A')  # 0xb69bb541
        data.write(b'\x00\x0c')  # size
        self.maximum_spin_speed.to_stream(data)

        data.write(b'\xd6YF"')  # 0xd6594622
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_lifetime))

        data.write(b"\xff'\xbb:")  # 0xff27bb3a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_lifetime))

        data.write(b'kW\x1b\xa5')  # 0x6b571ba5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_collision_time))

        data.write(b'P\x05\x1a\x17')  # 0x50051a17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_end_percentage))

        data.write(b'cS\xc4\t')  # 0x6353c409
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_start_percentage))

        data.write(b':V4\xd8')  # 0x3a5634d8
        data.write(b'\x00\x10')  # size
        self.start_color.to_stream(data)

        data.write(b'|n\xbe\x98')  # 0x7c6ebe98
        data.write(b'\x00\x10')  # size
        self.middle_color.to_stream(data)

        data.write(b'Z\xf5\x86}')  # 0x5af5867d
        data.write(b'\x00\x10')  # size
        self.end_color.to_stream(data)

        data.write(b'\xd7\x96\x90\xb4')  # 0xd79690b4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd79690b4))

        data.write(b'\x01E\xd0-')  # 0x145d02d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0145d02d))

        data.write(b'\x88n|\x9f')  # 0x886e7c9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scale_start_percentage))

        data.write(b'\x80\xc2*\n')  # 0x80c22a0a
        data.write(b'\x00\x0c')  # size
        self.final_scale.to_stream(data)

        data.write(b'A\x7fJ\x91')  # 0x417f4a91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x417f4a91))

        data.write(b'\x16\xb7-I')  # 0x16b72d49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.friction))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b')_\x05\xb7')  # 0x295f05b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_physics_threshold))

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\xee\xdb\xb0~')  # 0xeedbb07e
        data.write(b'\x00\x0c')  # size
        self.model_pivot_point.to_stream(data)

        data.write(b'\x93\xf8\xe0\xb0')  # 0x93f8e0b0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.created_sound))

        data.write(b'\xf1\x92Uv')  # 0xf1925576
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_sound))

        data.write(b'\x99\x12\x02\xc3')  # 0x991202c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_bounce_sounds))

        data.write(b'v\xc7\x95\x03')  # 0x76c79503
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76c79503))

        data.write(b'1\r\xfa\xc8')  # 0x310dfac8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x310dfac8))

        data.write(b'^\x9fR\x15')  # 0x5e9f5215
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5e9f5215))

        data.write(b'9t6\x18')  # 0x39743618
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x39743618))

        data.write(b'3\xe0\xfb\xb4')  # 0x33e0fbb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x33e0fbb4))

        data.write(b'\xe8.~\xd7')  # 0xe82e7ed7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe82e7ed7))

        data.write(b'\x85^\xe2\x1b')  # 0x855ee21b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x855ee21b))

        data.write(b'G\x8d\n\xa3')  # 0x478d0aa3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.particle_system1))

        data.write(b'\x19\xa6\xf7\x1f')  # 0x19a6f71f
        data.write(b'\x00\x0c')  # size
        self.particle_system1_scale.to_stream(data)

        data.write(b';\x03\xa0\x1e')  # 0x3b03a01e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_translation))

        data.write(b'\xdb\x1f\xa6\x1c')  # 0xdb1fa61c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_orientation))

        data.write(b';\xdd/\xed')  # 0x3bdd2fed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_wait_for_particles_to_die))

        data.write(b'\xf5\xddF\x90')  # 0xf5dd4690
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.particle_system1_orientation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1\x19x\r')  # 0xc119780d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.particle_system2))

        data.write(b'n8%\xef')  # 0x6e3825ef
        data.write(b'\x00\x0c')  # size
        self.particle_system2_scale.to_stream(data)

        data.write(b'\xc9TM\xe6')  # 0xc9544de6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system2_uses_global_translation))

        data.write(b')HK\xe4')  # 0x29484be4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system2_uses_global_orientation))

        data.write(b'\xc9\x8a\xc2\x15')  # 0xc98ac215
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system2_wait_for_particles_to_die))

        data.write(b'<\xe9]\x9d')  # 0x3ce95d9d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.particle_system2_orientation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!|7\xc2')  # 0x217c37c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_particle_effect))

        data.write(b'`\xd6\xbf\x8e')  # 0x60d6bf8e
        data.write(b'\x00\x0c')  # size
        self.bounce_particle_scale.to_stream(data)

        data.write(b'\xceY\xeb\xff')  # 0xce59ebff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bounce_effect_transform.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',{\x18\xdd')  # 0x2c7b18dd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_collider))

        data.write(b'\xe7;\x9e\xb0')  # 0xe73b9eb0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe73b9eb0))

        data.write(b'\r\x7f\xadU')  # 0xd7fad55
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.die_on_collision))

        data.write(b'\x87#I\x8a')  # 0x8723498a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8723498a))

        data.write(b'\x0f,g>')  # 0xf2c673e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x0f2c673e))

        data.write(b'U\xd8\xac\xe3')  # 0x55d8ace3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.collide_with_characters))

        data.write(b'\x8e\xc6\x8a\x96')  # 0x8ec68a96
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8ec68a96))

        data.write(b'\x9b\xd9C&')  # 0x9bd94326
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_bounce_speed_x))

        data.write(b'P\x85\x90\x83')  # 0x50859083
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_bounce_speed_y))

        data.write(b'\xbf\xd8*\x19')  # 0xbfd82a19
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbfd82a19))

        data.write(b'r=B\xd6')  # 0x723d42d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x723d42d6))

        data.write(b'N\xdb\x1d\x0e')  # 0x4edb1d0e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4edb1d0e))

        data.write(b'\xbfIbs')  # 0xbf496273
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbf496273))

        data.write(b'\xf8<\x1c\x1f')  # 0xf83c1c1f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf83c1c1f))

        data.write(b'\x88\xb1\xafF')  # 0x88b1af46
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x88b1af46))

        data.write(b'\xa6\xaa\x06\xd5')  # 0xa6aa06d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_in_foreground))

        data.write(b'27^\x0e')  # 0x32375e0e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_silhouette))

        data.write(b'\xe5\xec\xed\x02')  # 0xe5eced02
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe5eced02))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("DebrisPropertiesJson", data)
        return cls(
            cone_spread_yaw=json_data['cone_spread_yaw'],
            cone_spread_pitch=json_data['cone_spread_pitch'],
            initial_direction=Vector.from_json(json_data['initial_direction']),
            position_offset=Vector.from_json(json_data['position_offset']),
            transform_position_offset=json_data['transform_position_offset'],
            minimum_speed=json_data['minimum_speed'],
            maximum_speed=json_data['maximum_speed'],
            minimum_spin_speed=Vector.from_json(json_data['minimum_spin_speed']),
            maximum_spin_speed=Vector.from_json(json_data['maximum_spin_speed']),
            minimum_lifetime=json_data['minimum_lifetime'],
            maximum_lifetime=json_data['maximum_lifetime'],
            disable_collision_time=json_data['disable_collision_time'],
            fade_in_end_percentage=json_data['fade_in_end_percentage'],
            fade_out_start_percentage=json_data['fade_out_start_percentage'],
            start_color=Color.from_json(json_data['start_color']),
            middle_color=Color.from_json(json_data['middle_color']),
            end_color=Color.from_json(json_data['end_color']),
            unknown_0xd79690b4=json_data['unknown_0xd79690b4'],
            unknown_0x0145d02d=json_data['unknown_0x0145d02d'],
            scale_start_percentage=json_data['scale_start_percentage'],
            final_scale=Vector.from_json(json_data['final_scale']),
            unknown_0x417f4a91=json_data['unknown_0x417f4a91'],
            friction=json_data['friction'],
            gravity=json_data['gravity'],
            disable_physics_threshold=json_data['disable_physics_threshold'],
            model=json_data['model'],
            model_pivot_point=Vector.from_json(json_data['model_pivot_point']),
            created_sound=json_data['created_sound'],
            bounce_sound=json_data['bounce_sound'],
            max_bounce_sounds=json_data['max_bounce_sounds'],
            unknown_0x76c79503=json_data['unknown_0x76c79503'],
            unknown_0x310dfac8=json_data['unknown_0x310dfac8'],
            unknown_0x5e9f5215=json_data['unknown_0x5e9f5215'],
            unknown_0x39743618=json_data['unknown_0x39743618'],
            unknown_0x33e0fbb4=json_data['unknown_0x33e0fbb4'],
            unknown_0xe82e7ed7=json_data['unknown_0xe82e7ed7'],
            unknown_0x855ee21b=json_data['unknown_0x855ee21b'],
            particle_system1=json_data['particle_system1'],
            particle_system1_scale=Vector.from_json(json_data['particle_system1_scale']),
            particle_system1_uses_global_translation=json_data['particle_system1_uses_global_translation'],
            particle_system1_uses_global_orientation=json_data['particle_system1_uses_global_orientation'],
            particle_system1_wait_for_particles_to_die=json_data['particle_system1_wait_for_particles_to_die'],
            particle_system1_orientation=DebrisPropertiesOrientationEnum.from_json(json_data['particle_system1_orientation']),
            particle_system2=json_data['particle_system2'],
            particle_system2_scale=Vector.from_json(json_data['particle_system2_scale']),
            particle_system2_uses_global_translation=json_data['particle_system2_uses_global_translation'],
            particle_system2_uses_global_orientation=json_data['particle_system2_uses_global_orientation'],
            particle_system2_wait_for_particles_to_die=json_data['particle_system2_wait_for_particles_to_die'],
            particle_system2_orientation=DebrisPropertiesOrientationEnum.from_json(json_data['particle_system2_orientation']),
            bounce_particle_effect=json_data['bounce_particle_effect'],
            bounce_particle_scale=Vector.from_json(json_data['bounce_particle_scale']),
            bounce_effect_transform=UnknownStruct17.from_json(json_data['bounce_effect_transform']),
            is_collider=json_data['is_collider'],
            unknown_0xe73b9eb0=json_data['unknown_0xe73b9eb0'],
            die_on_collision=json_data['die_on_collision'],
            unknown_0x8723498a=json_data['unknown_0x8723498a'],
            unknown_0x0f2c673e=json_data['unknown_0x0f2c673e'],
            collide_with_characters=json_data['collide_with_characters'],
            unknown_0x8ec68a96=json_data['unknown_0x8ec68a96'],
            fixed_bounce_speed_x=json_data['fixed_bounce_speed_x'],
            fixed_bounce_speed_y=json_data['fixed_bounce_speed_y'],
            unknown_0xbfd82a19=json_data['unknown_0xbfd82a19'],
            unknown_0x723d42d6=json_data['unknown_0x723d42d6'],
            unknown_0x4edb1d0e=json_data['unknown_0x4edb1d0e'],
            unknown_0xbf496273=json_data['unknown_0xbf496273'],
            unknown_0xf83c1c1f=json_data['unknown_0xf83c1c1f'],
            unknown_0x88b1af46=json_data['unknown_0x88b1af46'],
            render_in_foreground=json_data['render_in_foreground'],
            allow_silhouette=json_data['allow_silhouette'],
            unknown_0xe5eced02=json_data['unknown_0xe5eced02'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'cone_spread_yaw': self.cone_spread_yaw,
            'cone_spread_pitch': self.cone_spread_pitch,
            'initial_direction': self.initial_direction.to_json(),
            'position_offset': self.position_offset.to_json(),
            'transform_position_offset': self.transform_position_offset,
            'minimum_speed': self.minimum_speed,
            'maximum_speed': self.maximum_speed,
            'minimum_spin_speed': self.minimum_spin_speed.to_json(),
            'maximum_spin_speed': self.maximum_spin_speed.to_json(),
            'minimum_lifetime': self.minimum_lifetime,
            'maximum_lifetime': self.maximum_lifetime,
            'disable_collision_time': self.disable_collision_time,
            'fade_in_end_percentage': self.fade_in_end_percentage,
            'fade_out_start_percentage': self.fade_out_start_percentage,
            'start_color': self.start_color.to_json(),
            'middle_color': self.middle_color.to_json(),
            'end_color': self.end_color.to_json(),
            'unknown_0xd79690b4': self.unknown_0xd79690b4,
            'unknown_0x0145d02d': self.unknown_0x0145d02d,
            'scale_start_percentage': self.scale_start_percentage,
            'final_scale': self.final_scale.to_json(),
            'unknown_0x417f4a91': self.unknown_0x417f4a91,
            'friction': self.friction,
            'gravity': self.gravity,
            'disable_physics_threshold': self.disable_physics_threshold,
            'model': self.model,
            'model_pivot_point': self.model_pivot_point.to_json(),
            'created_sound': self.created_sound,
            'bounce_sound': self.bounce_sound,
            'max_bounce_sounds': self.max_bounce_sounds,
            'unknown_0x76c79503': self.unknown_0x76c79503,
            'unknown_0x310dfac8': self.unknown_0x310dfac8,
            'unknown_0x5e9f5215': self.unknown_0x5e9f5215,
            'unknown_0x39743618': self.unknown_0x39743618,
            'unknown_0x33e0fbb4': self.unknown_0x33e0fbb4,
            'unknown_0xe82e7ed7': self.unknown_0xe82e7ed7,
            'unknown_0x855ee21b': self.unknown_0x855ee21b,
            'particle_system1': self.particle_system1,
            'particle_system1_scale': self.particle_system1_scale.to_json(),
            'particle_system1_uses_global_translation': self.particle_system1_uses_global_translation,
            'particle_system1_uses_global_orientation': self.particle_system1_uses_global_orientation,
            'particle_system1_wait_for_particles_to_die': self.particle_system1_wait_for_particles_to_die,
            'particle_system1_orientation': self.particle_system1_orientation.to_json(),
            'particle_system2': self.particle_system2,
            'particle_system2_scale': self.particle_system2_scale.to_json(),
            'particle_system2_uses_global_translation': self.particle_system2_uses_global_translation,
            'particle_system2_uses_global_orientation': self.particle_system2_uses_global_orientation,
            'particle_system2_wait_for_particles_to_die': self.particle_system2_wait_for_particles_to_die,
            'particle_system2_orientation': self.particle_system2_orientation.to_json(),
            'bounce_particle_effect': self.bounce_particle_effect,
            'bounce_particle_scale': self.bounce_particle_scale.to_json(),
            'bounce_effect_transform': self.bounce_effect_transform.to_json(),
            'is_collider': self.is_collider,
            'unknown_0xe73b9eb0': self.unknown_0xe73b9eb0,
            'die_on_collision': self.die_on_collision,
            'unknown_0x8723498a': self.unknown_0x8723498a,
            'unknown_0x0f2c673e': self.unknown_0x0f2c673e,
            'collide_with_characters': self.collide_with_characters,
            'unknown_0x8ec68a96': self.unknown_0x8ec68a96,
            'fixed_bounce_speed_x': self.fixed_bounce_speed_x,
            'fixed_bounce_speed_y': self.fixed_bounce_speed_y,
            'unknown_0xbfd82a19': self.unknown_0xbfd82a19,
            'unknown_0x723d42d6': self.unknown_0x723d42d6,
            'unknown_0x4edb1d0e': self.unknown_0x4edb1d0e,
            'unknown_0xbf496273': self.unknown_0xbf496273,
            'unknown_0xf83c1c1f': self.unknown_0xf83c1c1f,
            'unknown_0x88b1af46': self.unknown_0x88b1af46,
            'render_in_foreground': self.render_in_foreground,
            'allow_silhouette': self.allow_silhouette,
            'unknown_0xe5eced02': self.unknown_0xe5eced02,
        }


def _decode_cone_spread_yaw(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cone_spread_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_direction(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_position_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_transform_position_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_spin_speed(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_maximum_spin_speed(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_minimum_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_collision_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_end_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_start_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_middle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_end_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xd79690b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0145d02d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_start_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_final_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x417f4a91(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_physics_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_model_pivot_point(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_created_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_max_bounce_sounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x76c79503(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x310dfac8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5e9f5215(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x39743618(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x33e0fbb4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe82e7ed7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x855ee21b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_particle_system1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_particle_system1_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_particle_system1_uses_global_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_uses_global_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_wait_for_particles_to_die(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_particle_system2_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_particle_system2_uses_global_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system2_uses_global_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system2_wait_for_particles_to_die(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bounce_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bounce_particle_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_is_collider(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe73b9eb0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_die_on_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x8723498a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0f2c673e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_collide_with_characters(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x8ec68a96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fixed_bounce_speed_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_bounce_speed_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbfd82a19(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x723d42d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4edb1d0e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbf496273(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf83c1c1f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x88b1af46(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_in_foreground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_silhouette(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe5eced02(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5c3c4a57: ('cone_spread_yaw', _decode_cone_spread_yaw),
    0xa79fc55f: ('cone_spread_pitch', _decode_cone_spread_pitch),
    0x1a0dfe6: ('initial_direction', _decode_initial_direction),
    0xef90f09d: ('position_offset', _decode_position_offset),
    0xc4b1e6a1: ('transform_position_offset', _decode_transform_position_offset),
    0x185263e: ('minimum_speed', _decode_minimum_speed),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
    0xf78c8ac7: ('minimum_spin_speed', _decode_minimum_spin_speed),
    0xb69bb541: ('maximum_spin_speed', _decode_maximum_spin_speed),
    0xd6594622: ('minimum_lifetime', _decode_minimum_lifetime),
    0xff27bb3a: ('maximum_lifetime', _decode_maximum_lifetime),
    0x6b571ba5: ('disable_collision_time', _decode_disable_collision_time),
    0x50051a17: ('fade_in_end_percentage', _decode_fade_in_end_percentage),
    0x6353c409: ('fade_out_start_percentage', _decode_fade_out_start_percentage),
    0x3a5634d8: ('start_color', _decode_start_color),
    0x7c6ebe98: ('middle_color', _decode_middle_color),
    0x5af5867d: ('end_color', _decode_end_color),
    0xd79690b4: ('unknown_0xd79690b4', _decode_unknown_0xd79690b4),
    0x145d02d: ('unknown_0x0145d02d', _decode_unknown_0x0145d02d),
    0x886e7c9f: ('scale_start_percentage', _decode_scale_start_percentage),
    0x80c22a0a: ('final_scale', _decode_final_scale),
    0x417f4a91: ('unknown_0x417f4a91', _decode_unknown_0x417f4a91),
    0x16b72d49: ('friction', _decode_friction),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x295f05b7: ('disable_physics_threshold', _decode_disable_physics_threshold),
    0xc27ffa8f: ('model', _decode_model),
    0xeedbb07e: ('model_pivot_point', _decode_model_pivot_point),
    0x93f8e0b0: ('created_sound', _decode_created_sound),
    0xf1925576: ('bounce_sound', _decode_bounce_sound),
    0x991202c3: ('max_bounce_sounds', _decode_max_bounce_sounds),
    0x76c79503: ('unknown_0x76c79503', _decode_unknown_0x76c79503),
    0x310dfac8: ('unknown_0x310dfac8', _decode_unknown_0x310dfac8),
    0x5e9f5215: ('unknown_0x5e9f5215', _decode_unknown_0x5e9f5215),
    0x39743618: ('unknown_0x39743618', _decode_unknown_0x39743618),
    0x33e0fbb4: ('unknown_0x33e0fbb4', _decode_unknown_0x33e0fbb4),
    0xe82e7ed7: ('unknown_0xe82e7ed7', _decode_unknown_0xe82e7ed7),
    0x855ee21b: ('unknown_0x855ee21b', _decode_unknown_0x855ee21b),
    0x478d0aa3: ('particle_system1', _decode_particle_system1),
    0x19a6f71f: ('particle_system1_scale', _decode_particle_system1_scale),
    0x3b03a01e: ('particle_system1_uses_global_translation', _decode_particle_system1_uses_global_translation),
    0xdb1fa61c: ('particle_system1_uses_global_orientation', _decode_particle_system1_uses_global_orientation),
    0x3bdd2fed: ('particle_system1_wait_for_particles_to_die', _decode_particle_system1_wait_for_particles_to_die),
    0xf5dd4690: ('particle_system1_orientation', DebrisPropertiesOrientationEnum.from_stream),
    0xc119780d: ('particle_system2', _decode_particle_system2),
    0x6e3825ef: ('particle_system2_scale', _decode_particle_system2_scale),
    0xc9544de6: ('particle_system2_uses_global_translation', _decode_particle_system2_uses_global_translation),
    0x29484be4: ('particle_system2_uses_global_orientation', _decode_particle_system2_uses_global_orientation),
    0xc98ac215: ('particle_system2_wait_for_particles_to_die', _decode_particle_system2_wait_for_particles_to_die),
    0x3ce95d9d: ('particle_system2_orientation', DebrisPropertiesOrientationEnum.from_stream),
    0x217c37c2: ('bounce_particle_effect', _decode_bounce_particle_effect),
    0x60d6bf8e: ('bounce_particle_scale', _decode_bounce_particle_scale),
    0xce59ebff: ('bounce_effect_transform', UnknownStruct17.from_stream),
    0x2c7b18dd: ('is_collider', _decode_is_collider),
    0xe73b9eb0: ('unknown_0xe73b9eb0', _decode_unknown_0xe73b9eb0),
    0xd7fad55: ('die_on_collision', _decode_die_on_collision),
    0x8723498a: ('unknown_0x8723498a', _decode_unknown_0x8723498a),
    0xf2c673e: ('unknown_0x0f2c673e', _decode_unknown_0x0f2c673e),
    0x55d8ace3: ('collide_with_characters', _decode_collide_with_characters),
    0x8ec68a96: ('unknown_0x8ec68a96', _decode_unknown_0x8ec68a96),
    0x9bd94326: ('fixed_bounce_speed_x', _decode_fixed_bounce_speed_x),
    0x50859083: ('fixed_bounce_speed_y', _decode_fixed_bounce_speed_y),
    0xbfd82a19: ('unknown_0xbfd82a19', _decode_unknown_0xbfd82a19),
    0x723d42d6: ('unknown_0x723d42d6', _decode_unknown_0x723d42d6),
    0x4edb1d0e: ('unknown_0x4edb1d0e', _decode_unknown_0x4edb1d0e),
    0xbf496273: ('unknown_0xbf496273', _decode_unknown_0xbf496273),
    0xf83c1c1f: ('unknown_0xf83c1c1f', _decode_unknown_0xf83c1c1f),
    0x88b1af46: ('unknown_0x88b1af46', _decode_unknown_0x88b1af46),
    0xa6aa06d5: ('render_in_foreground', _decode_render_in_foreground),
    0x32375e0e: ('allow_silhouette', _decode_allow_silhouette),
    0xe5eced02: ('unknown_0xe5eced02', _decode_unknown_0xe5eced02),
}

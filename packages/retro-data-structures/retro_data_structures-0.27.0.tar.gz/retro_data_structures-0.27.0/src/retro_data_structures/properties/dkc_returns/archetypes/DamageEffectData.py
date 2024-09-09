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
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.dkc_returns.archetypes.LightParameters import LightParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class DamageEffectDataJson(typing_extensions.TypedDict):
        bounds: json_util.JsonValue
        apply_damage_to_any_vulnerable_actor: bool
        damage: json_util.JsonObject
        duration: float
        turn_damage_off_delay_after_emitter_shut_down: float
        draw_debug_box_multiplier: float
        force_delete_multiplier: float
        speed: float
        use_terrain_alignment: bool
        terrain_search_up_distance: float
        override_terrain_search_radius: bool
        terrain_search_radius: float
        terrain_alignment_rotation_speed: float
        terrain_alignment_speed_k: float
        use_terrain_neighbor_influences: bool
        align_velocity_with_surface: bool
        align_effect: bool
        can_be_blown_out: bool
        particle: int
        time_scale: float
        model_scale: json_util.JsonValue
        sound: int
        kill_sound_when_effect_ends: bool
        use_alternate_damage_effect: bool
        use_lighting: bool
        lighting: json_util.JsonObject
    

@dataclasses.dataclass()
class DamageEffectData(BaseProperty):
    bounds: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x3bbeeed2, original_name='Bounds', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    apply_damage_to_any_vulnerable_actor: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x418d52d4, original_name='ApplyDamageToAnyVulnerableActor'
        ),
    })
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0x337f9524, original_name='Damage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    duration: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8b51e23f, original_name='Duration'
        ),
    })
    turn_damage_off_delay_after_emitter_shut_down: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf3112ad9, original_name='TurnDamageOffDelayAfterEmitterShutDown'
        ),
    })
    draw_debug_box_multiplier: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd1ef7248, original_name='DrawDebugBoxMultiplier'
        ),
    })
    force_delete_multiplier: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa93de032, original_name='ForceDeleteMultiplier'
        ),
    })
    speed: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6392404e, original_name='Speed'
        ),
    })
    use_terrain_alignment: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6117e78f, original_name='UseTerrainAlignment'
        ),
    })
    terrain_search_up_distance: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xdb1c71c2, original_name='TerrainSearchUpDistance'
        ),
    })
    override_terrain_search_radius: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x23ee6c1d, original_name='OverrideTerrainSearchRadius'
        ),
    })
    terrain_search_radius: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2331d418, original_name='TerrainSearchRadius'
        ),
    })
    terrain_alignment_rotation_speed: float = dataclasses.field(default=360.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa884e63f, original_name='TerrainAlignmentRotationSpeed'
        ),
    })
    terrain_alignment_speed_k: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe4076e11, original_name='TerrainAlignmentSpeedK'
        ),
    })
    use_terrain_neighbor_influences: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa863bae2, original_name='UseTerrainNeighborInfluences'
        ),
    })
    align_velocity_with_surface: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd1e5b042, original_name='AlignVelocityWithSurface'
        ),
    })
    align_effect: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x441d8647, original_name='AlignEffect'
        ),
    })
    can_be_blown_out: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd5417338, original_name='CanBeBlownOut'
        ),
    })
    particle: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6d1ce525, original_name='Particle'
        ),
    })
    time_scale: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3edf746b, original_name='TimeScale'
        ),
    })
    model_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xea6d6548, original_name='ModelScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa55dacf6, original_name='Sound'
        ),
    })
    kill_sound_when_effect_ends: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x78a661ef, original_name='KillSoundWhenEffectEnds'
        ),
    })
    use_alternate_damage_effect: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf0993bfe, original_name='UseAlternateDamageEffect'
        ),
    })
    use_lighting: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x818d8dae, original_name='UseLighting'
        ),
    })
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters, metadata={
        'reflection': FieldReflection[LightParameters](
            LightParameters, id=0xb028db0e, original_name='Lighting', from_json=LightParameters.from_json, to_json=LightParameters.to_json
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
        if property_count != 26:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3bbeeed2
        bounds = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x418d52d4
        apply_damage_to_any_vulnerable_actor = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x337f9524
        damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8b51e23f
        duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf3112ad9
        turn_damage_off_delay_after_emitter_shut_down = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1ef7248
        draw_debug_box_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa93de032
        force_delete_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6392404e
        speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6117e78f
        use_terrain_alignment = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb1c71c2
        terrain_search_up_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x23ee6c1d
        override_terrain_search_radius = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2331d418
        terrain_search_radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa884e63f
        terrain_alignment_rotation_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe4076e11
        terrain_alignment_speed_k = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa863bae2
        use_terrain_neighbor_influences = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1e5b042
        align_velocity_with_surface = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x441d8647
        align_effect = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd5417338
        can_be_blown_out = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6d1ce525
        particle = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3edf746b
        time_scale = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xea6d6548
        model_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa55dacf6
        sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x78a661ef
        kill_sound_when_effect_ends = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0993bfe
        use_alternate_damage_effect = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x818d8dae
        use_lighting = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb028db0e
        lighting = LightParameters.from_stream(data, property_size)
    
        return cls(bounds, apply_damage_to_any_vulnerable_actor, damage, duration, turn_damage_off_delay_after_emitter_shut_down, draw_debug_box_multiplier, force_delete_multiplier, speed, use_terrain_alignment, terrain_search_up_distance, override_terrain_search_radius, terrain_search_radius, terrain_alignment_rotation_speed, terrain_alignment_speed_k, use_terrain_neighbor_influences, align_velocity_with_surface, align_effect, can_be_blown_out, particle, time_scale, model_scale, sound, kill_sound_when_effect_ends, use_alternate_damage_effect, use_lighting, lighting)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1a')  # 26 properties

        data.write(b';\xbe\xee\xd2')  # 0x3bbeeed2
        data.write(b'\x00\x0c')  # size
        self.bounds.to_stream(data)

        data.write(b'A\x8dR\xd4')  # 0x418d52d4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_damage_to_any_vulnerable_actor))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\xf3\x11*\xd9')  # 0xf3112ad9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_damage_off_delay_after_emitter_shut_down))

        data.write(b'\xd1\xefrH')  # 0xd1ef7248
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.draw_debug_box_multiplier))

        data.write(b'\xa9=\xe02')  # 0xa93de032
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.force_delete_multiplier))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'a\x17\xe7\x8f')  # 0x6117e78f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_terrain_alignment))

        data.write(b'\xdb\x1cq\xc2')  # 0xdb1c71c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_search_up_distance))

        data.write(b'#\xeel\x1d')  # 0x23ee6c1d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override_terrain_search_radius))

        data.write(b'#1\xd4\x18')  # 0x2331d418
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_search_radius))

        data.write(b'\xa8\x84\xe6?')  # 0xa884e63f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_rotation_speed))

        data.write(b'\xe4\x07n\x11')  # 0xe4076e11
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_speed_k))

        data.write(b'\xa8c\xba\xe2')  # 0xa863bae2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_terrain_neighbor_influences))

        data.write(b'\xd1\xe5\xb0B')  # 0xd1e5b042
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.align_velocity_with_surface))

        data.write(b'D\x1d\x86G')  # 0x441d8647
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.align_effect))

        data.write(b'\xd5As8')  # 0xd5417338
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_be_blown_out))

        data.write(b'm\x1c\xe5%')  # 0x6d1ce525
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.particle))

        data.write(b'>\xdftk')  # 0x3edf746b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_scale))

        data.write(b'\xeameH')  # 0xea6d6548
        data.write(b'\x00\x0c')  # size
        self.model_scale.to_stream(data)

        data.write(b'\xa5]\xac\xf6')  # 0xa55dacf6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound))

        data.write(b'x\xa6a\xef')  # 0x78a661ef
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.kill_sound_when_effect_ends))

        data.write(b'\xf0\x99;\xfe')  # 0xf0993bfe
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_alternate_damage_effect))

        data.write(b'\x81\x8d\x8d\xae')  # 0x818d8dae
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_lighting))

        data.write(b'\xb0(\xdb\x0e')  # 0xb028db0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lighting.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("DamageEffectDataJson", data)
        return cls(
            bounds=Vector.from_json(json_data['bounds']),
            apply_damage_to_any_vulnerable_actor=json_data['apply_damage_to_any_vulnerable_actor'],
            damage=DamageInfo.from_json(json_data['damage']),
            duration=json_data['duration'],
            turn_damage_off_delay_after_emitter_shut_down=json_data['turn_damage_off_delay_after_emitter_shut_down'],
            draw_debug_box_multiplier=json_data['draw_debug_box_multiplier'],
            force_delete_multiplier=json_data['force_delete_multiplier'],
            speed=json_data['speed'],
            use_terrain_alignment=json_data['use_terrain_alignment'],
            terrain_search_up_distance=json_data['terrain_search_up_distance'],
            override_terrain_search_radius=json_data['override_terrain_search_radius'],
            terrain_search_radius=json_data['terrain_search_radius'],
            terrain_alignment_rotation_speed=json_data['terrain_alignment_rotation_speed'],
            terrain_alignment_speed_k=json_data['terrain_alignment_speed_k'],
            use_terrain_neighbor_influences=json_data['use_terrain_neighbor_influences'],
            align_velocity_with_surface=json_data['align_velocity_with_surface'],
            align_effect=json_data['align_effect'],
            can_be_blown_out=json_data['can_be_blown_out'],
            particle=json_data['particle'],
            time_scale=json_data['time_scale'],
            model_scale=Vector.from_json(json_data['model_scale']),
            sound=json_data['sound'],
            kill_sound_when_effect_ends=json_data['kill_sound_when_effect_ends'],
            use_alternate_damage_effect=json_data['use_alternate_damage_effect'],
            use_lighting=json_data['use_lighting'],
            lighting=LightParameters.from_json(json_data['lighting']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'bounds': self.bounds.to_json(),
            'apply_damage_to_any_vulnerable_actor': self.apply_damage_to_any_vulnerable_actor,
            'damage': self.damage.to_json(),
            'duration': self.duration,
            'turn_damage_off_delay_after_emitter_shut_down': self.turn_damage_off_delay_after_emitter_shut_down,
            'draw_debug_box_multiplier': self.draw_debug_box_multiplier,
            'force_delete_multiplier': self.force_delete_multiplier,
            'speed': self.speed,
            'use_terrain_alignment': self.use_terrain_alignment,
            'terrain_search_up_distance': self.terrain_search_up_distance,
            'override_terrain_search_radius': self.override_terrain_search_radius,
            'terrain_search_radius': self.terrain_search_radius,
            'terrain_alignment_rotation_speed': self.terrain_alignment_rotation_speed,
            'terrain_alignment_speed_k': self.terrain_alignment_speed_k,
            'use_terrain_neighbor_influences': self.use_terrain_neighbor_influences,
            'align_velocity_with_surface': self.align_velocity_with_surface,
            'align_effect': self.align_effect,
            'can_be_blown_out': self.can_be_blown_out,
            'particle': self.particle,
            'time_scale': self.time_scale,
            'model_scale': self.model_scale.to_json(),
            'sound': self.sound,
            'kill_sound_when_effect_ends': self.kill_sound_when_effect_ends,
            'use_alternate_damage_effect': self.use_alternate_damage_effect,
            'use_lighting': self.use_lighting,
            'lighting': self.lighting.to_json(),
        }


def _decode_bounds(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_apply_damage_to_any_vulnerable_actor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_damage_off_delay_after_emitter_shut_down(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_draw_debug_box_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_force_delete_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_terrain_alignment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_terrain_search_up_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_override_terrain_search_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_terrain_search_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_rotation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_speed_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_terrain_neighbor_influences(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_align_velocity_with_surface(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_align_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_be_blown_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_time_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_kill_sound_when_effect_ends(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_alternate_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_lighting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3bbeeed2: ('bounds', _decode_bounds),
    0x418d52d4: ('apply_damage_to_any_vulnerable_actor', _decode_apply_damage_to_any_vulnerable_actor),
    0x337f9524: ('damage', DamageInfo.from_stream),
    0x8b51e23f: ('duration', _decode_duration),
    0xf3112ad9: ('turn_damage_off_delay_after_emitter_shut_down', _decode_turn_damage_off_delay_after_emitter_shut_down),
    0xd1ef7248: ('draw_debug_box_multiplier', _decode_draw_debug_box_multiplier),
    0xa93de032: ('force_delete_multiplier', _decode_force_delete_multiplier),
    0x6392404e: ('speed', _decode_speed),
    0x6117e78f: ('use_terrain_alignment', _decode_use_terrain_alignment),
    0xdb1c71c2: ('terrain_search_up_distance', _decode_terrain_search_up_distance),
    0x23ee6c1d: ('override_terrain_search_radius', _decode_override_terrain_search_radius),
    0x2331d418: ('terrain_search_radius', _decode_terrain_search_radius),
    0xa884e63f: ('terrain_alignment_rotation_speed', _decode_terrain_alignment_rotation_speed),
    0xe4076e11: ('terrain_alignment_speed_k', _decode_terrain_alignment_speed_k),
    0xa863bae2: ('use_terrain_neighbor_influences', _decode_use_terrain_neighbor_influences),
    0xd1e5b042: ('align_velocity_with_surface', _decode_align_velocity_with_surface),
    0x441d8647: ('align_effect', _decode_align_effect),
    0xd5417338: ('can_be_blown_out', _decode_can_be_blown_out),
    0x6d1ce525: ('particle', _decode_particle),
    0x3edf746b: ('time_scale', _decode_time_scale),
    0xea6d6548: ('model_scale', _decode_model_scale),
    0xa55dacf6: ('sound', _decode_sound),
    0x78a661ef: ('kill_sound_when_effect_ends', _decode_kill_sound_when_effect_ends),
    0xf0993bfe: ('use_alternate_damage_effect', _decode_use_alternate_damage_effect),
    0x818d8dae: ('use_lighting', _decode_use_lighting),
    0xb028db0e: ('lighting', LightParameters.from_stream),
}

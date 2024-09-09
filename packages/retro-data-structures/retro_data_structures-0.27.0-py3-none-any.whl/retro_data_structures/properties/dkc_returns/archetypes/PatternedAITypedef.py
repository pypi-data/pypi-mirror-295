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
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class PatternedAITypedefJson(typing_extensions.TypedDict):
        mass: float
        vulnerability: json_util.JsonObject
        contact_damage: json_util.JsonObject
        damage_wait_time: float
        health: json_util.JsonObject
        collision_radius: float
        collision_height: float
        collision_offset: json_util.JsonValue
        step_up_height: float
        step_down_height: float
        character_animation_information: json_util.JsonObject
        fsmc_0x1749405b: int
        fsmc_0x1b21eeb2: int
        path_mesh_index: int
        unknown_0x39a6dec3: float
        unknown_0x47de2455: bool
        creature_death_particle_effect: int
        unknown_0xc88ad680: int
        caud: int
        creature_death_particle_effect_uses_creature_orientation: bool
        ground_pound_slap_detection_radius: float
        speed: float
        turn_speed: float
        unknown_0x6d892893: bool
        detection_range: float
        detection_height_range: float
        detection_angle: float
        min_attack_range: float
        max_attack_range: float
        average_attack_time: float
        attack_time_variation: float
    

@dataclasses.dataclass()
class PatternedAITypedef(BaseProperty):
    mass: float = dataclasses.field(default=150.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x75dbb375, original_name='Mass'
        ),
    })
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability, metadata={
        'reflection': FieldReflection[DamageVulnerability](
            DamageVulnerability, id=0x7b71ae90, original_name='Vulnerability', from_json=DamageVulnerability.from_json, to_json=DamageVulnerability.to_json
        ),
    })
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0xd756416e, original_name='ContactDamage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    damage_wait_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe0cdc7e3, original_name='DamageWaitTime'
        ),
    })
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo, metadata={
        'reflection': FieldReflection[HealthInfo](
            HealthInfo, id=0xcf90d15e, original_name='Health', from_json=HealthInfo.from_json, to_json=HealthInfo.to_json
        ),
    })
    collision_radius: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8a6ab139, original_name='CollisionRadius'
        ),
    })
    collision_height: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3011b5df, original_name='CollisionHeight'
        ),
    })
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x2e686c2a, original_name='CollisionOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    step_up_height: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd9355674, original_name='StepUpHeight'
        ),
    })
    step_down_height: float = dataclasses.field(default=0.1599999964237213, metadata={
        'reflection': FieldReflection[float](
            float, id=0x88ea81db, original_name='StepDownHeight'
        ),
    })
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa244c9d8, original_name='CharacterAnimationInformation', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    fsmc_0x1749405b: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FSMC'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1749405b, original_name='FSMC'
        ),
    })
    fsmc_0x1b21eeb2: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FSMC'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1b21eeb2, original_name='FSMC'
        ),
    })
    path_mesh_index: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x98169634, original_name='PathMeshIndex'
        ),
    })
    unknown_0x39a6dec3: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39a6dec3, original_name='Unknown'
        ),
    })
    unknown_0x47de2455: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x47de2455, original_name='Unknown'
        ),
    })
    creature_death_particle_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xdfe74895, original_name='CreatureDeathParticleEffect'
        ),
    })
    unknown_0xc88ad680: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc88ad680, original_name='Unknown'
        ),
    })
    caud: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x64c22667, original_name='CAUD'
        ),
    })
    creature_death_particle_effect_uses_creature_orientation: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xfd8a9692, original_name='CreatureDeathParticleEffectUsesCreatureOrientation'
        ),
    })
    ground_pound_slap_detection_radius: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe0644402, original_name='GroundPoundSlapDetectionRadius'
        ),
    })
    speed: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6392404e, original_name='Speed'
        ),
    })
    turn_speed: float = dataclasses.field(default=120.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x020c78bb, original_name='TurnSpeed'
        ),
    })
    unknown_0x6d892893: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6d892893, original_name='Unknown'
        ),
    })
    detection_range: float = dataclasses.field(default=100.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8db77ee4, original_name='DetectionRange'
        ),
    })
    detection_height_range: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x513f04b8, original_name='DetectionHeightRange'
        ),
    })
    detection_angle: float = dataclasses.field(default=60.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x83dfc40f, original_name='DetectionAngle'
        ),
    })
    min_attack_range: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x58434916, original_name='MinAttackRange'
        ),
    })
    max_attack_range: float = dataclasses.field(default=11.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xff77c96f, original_name='MaxAttackRange'
        ),
    })
    average_attack_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb0cfe015, original_name='AverageAttackTime'
        ),
    })
    attack_time_variation: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc80e329b, original_name='AttackTimeVariation'
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
        if property_count != 31:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x75dbb375
        mass = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b71ae90
        vulnerability = DamageVulnerability.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd756416e
        contact_damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe0cdc7e3
        damage_wait_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcf90d15e
        health = HealthInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8a6ab139
        collision_radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3011b5df
        collision_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e686c2a
        collision_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9355674
        step_up_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x88ea81db
        step_down_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa244c9d8
        character_animation_information = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1749405b
        fsmc_0x1749405b = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b21eeb2
        fsmc_0x1b21eeb2 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x98169634
        path_mesh_index = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x39a6dec3
        unknown_0x39a6dec3 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47de2455
        unknown_0x47de2455 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdfe74895
        creature_death_particle_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc88ad680
        unknown_0xc88ad680 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x64c22667
        caud = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfd8a9692
        creature_death_particle_effect_uses_creature_orientation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe0644402
        ground_pound_slap_detection_radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6392404e
        speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x020c78bb
        turn_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6d892893
        unknown_0x6d892893 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8db77ee4
        detection_range = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x513f04b8
        detection_height_range = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x83dfc40f
        detection_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x58434916
        min_attack_range = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xff77c96f
        max_attack_range = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0cfe015
        average_attack_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc80e329b
        attack_time_variation = struct.unpack('>f', data.read(4))[0]
    
        return cls(mass, vulnerability, contact_damage, damage_wait_time, health, collision_radius, collision_height, collision_offset, step_up_height, step_down_height, character_animation_information, fsmc_0x1749405b, fsmc_0x1b21eeb2, path_mesh_index, unknown_0x39a6dec3, unknown_0x47de2455, creature_death_particle_effect, unknown_0xc88ad680, caud, creature_death_particle_effect_uses_creature_orientation, ground_pound_slap_detection_radius, speed, turn_speed, unknown_0x6d892893, detection_range, detection_height_range, detection_angle, min_attack_range, max_attack_range, average_attack_time, attack_time_variation)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0\xcd\xc7\xe3')  # 0xe0cdc7e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_wait_time))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8aj\xb19')  # 0x8a6ab139
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_radius))

        data.write(b'0\x11\xb5\xdf')  # 0x3011b5df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_height))

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xd95Vt')  # 0xd9355674
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.step_up_height))

        data.write(b'\x88\xea\x81\xdb')  # 0x88ea81db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.step_down_height))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17I@[')  # 0x1749405b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fsmc_0x1749405b))

        data.write(b'\x1b!\xee\xb2')  # 0x1b21eeb2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fsmc_0x1b21eeb2))

        data.write(b'\x98\x16\x964')  # 0x98169634
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.path_mesh_index))

        data.write(b'9\xa6\xde\xc3')  # 0x39a6dec3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x39a6dec3))

        data.write(b'G\xde$U')  # 0x47de2455
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x47de2455))

        data.write(b'\xdf\xe7H\x95')  # 0xdfe74895
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.creature_death_particle_effect))

        data.write(b'\xc8\x8a\xd6\x80')  # 0xc88ad680
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xc88ad680))

        data.write(b'd\xc2&g')  # 0x64c22667
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xfd\x8a\x96\x92')  # 0xfd8a9692
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.creature_death_particle_effect_uses_creature_orientation))

        data.write(b'\xe0dD\x02')  # 0xe0644402
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_slap_detection_radius))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'\x02\x0cx\xbb')  # 0x20c78bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed))

        data.write(b'm\x89(\x93')  # 0x6d892893
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6d892893))

        data.write(b'\x8d\xb7~\xe4')  # 0x8db77ee4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_range))

        data.write(b'Q?\x04\xb8')  # 0x513f04b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_height_range))

        data.write(b'\x83\xdf\xc4\x0f')  # 0x83dfc40f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_angle))

        data.write(b'XCI\x16')  # 0x58434916
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_range))

        data.write(b'\xffw\xc9o')  # 0xff77c96f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_range))

        data.write(b'\xb0\xcf\xe0\x15')  # 0xb0cfe015
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.average_attack_time))

        data.write(b'\xc8\x0e2\x9b')  # 0xc80e329b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_time_variation))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PatternedAITypedefJson", data)
        return cls(
            mass=json_data['mass'],
            vulnerability=DamageVulnerability.from_json(json_data['vulnerability']),
            contact_damage=DamageInfo.from_json(json_data['contact_damage']),
            damage_wait_time=json_data['damage_wait_time'],
            health=HealthInfo.from_json(json_data['health']),
            collision_radius=json_data['collision_radius'],
            collision_height=json_data['collision_height'],
            collision_offset=Vector.from_json(json_data['collision_offset']),
            step_up_height=json_data['step_up_height'],
            step_down_height=json_data['step_down_height'],
            character_animation_information=AnimationParameters.from_json(json_data['character_animation_information']),
            fsmc_0x1749405b=json_data['fsmc_0x1749405b'],
            fsmc_0x1b21eeb2=json_data['fsmc_0x1b21eeb2'],
            path_mesh_index=json_data['path_mesh_index'],
            unknown_0x39a6dec3=json_data['unknown_0x39a6dec3'],
            unknown_0x47de2455=json_data['unknown_0x47de2455'],
            creature_death_particle_effect=json_data['creature_death_particle_effect'],
            unknown_0xc88ad680=json_data['unknown_0xc88ad680'],
            caud=json_data['caud'],
            creature_death_particle_effect_uses_creature_orientation=json_data['creature_death_particle_effect_uses_creature_orientation'],
            ground_pound_slap_detection_radius=json_data['ground_pound_slap_detection_radius'],
            speed=json_data['speed'],
            turn_speed=json_data['turn_speed'],
            unknown_0x6d892893=json_data['unknown_0x6d892893'],
            detection_range=json_data['detection_range'],
            detection_height_range=json_data['detection_height_range'],
            detection_angle=json_data['detection_angle'],
            min_attack_range=json_data['min_attack_range'],
            max_attack_range=json_data['max_attack_range'],
            average_attack_time=json_data['average_attack_time'],
            attack_time_variation=json_data['attack_time_variation'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'mass': self.mass,
            'vulnerability': self.vulnerability.to_json(),
            'contact_damage': self.contact_damage.to_json(),
            'damage_wait_time': self.damage_wait_time,
            'health': self.health.to_json(),
            'collision_radius': self.collision_radius,
            'collision_height': self.collision_height,
            'collision_offset': self.collision_offset.to_json(),
            'step_up_height': self.step_up_height,
            'step_down_height': self.step_down_height,
            'character_animation_information': self.character_animation_information.to_json(),
            'fsmc_0x1749405b': self.fsmc_0x1749405b,
            'fsmc_0x1b21eeb2': self.fsmc_0x1b21eeb2,
            'path_mesh_index': self.path_mesh_index,
            'unknown_0x39a6dec3': self.unknown_0x39a6dec3,
            'unknown_0x47de2455': self.unknown_0x47de2455,
            'creature_death_particle_effect': self.creature_death_particle_effect,
            'unknown_0xc88ad680': self.unknown_0xc88ad680,
            'caud': self.caud,
            'creature_death_particle_effect_uses_creature_orientation': self.creature_death_particle_effect_uses_creature_orientation,
            'ground_pound_slap_detection_radius': self.ground_pound_slap_detection_radius,
            'speed': self.speed,
            'turn_speed': self.turn_speed,
            'unknown_0x6d892893': self.unknown_0x6d892893,
            'detection_range': self.detection_range,
            'detection_height_range': self.detection_height_range,
            'detection_angle': self.detection_angle,
            'min_attack_range': self.min_attack_range,
            'max_attack_range': self.max_attack_range,
            'average_attack_time': self.average_attack_time,
            'attack_time_variation': self.attack_time_variation,
        }


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_wait_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_step_up_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_step_down_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fsmc_0x1749405b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fsmc_0x1b21eeb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_path_mesh_index(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x39a6dec3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x47de2455(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_creature_death_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xc88ad680(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_creature_death_particle_effect_uses_creature_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ground_pound_slap_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d892893(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_detection_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_height_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_average_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_time_variation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x75dbb375: ('mass', _decode_mass),
    0x7b71ae90: ('vulnerability', DamageVulnerability.from_stream),
    0xd756416e: ('contact_damage', DamageInfo.from_stream),
    0xe0cdc7e3: ('damage_wait_time', _decode_damage_wait_time),
    0xcf90d15e: ('health', HealthInfo.from_stream),
    0x8a6ab139: ('collision_radius', _decode_collision_radius),
    0x3011b5df: ('collision_height', _decode_collision_height),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xd9355674: ('step_up_height', _decode_step_up_height),
    0x88ea81db: ('step_down_height', _decode_step_down_height),
    0xa244c9d8: ('character_animation_information', AnimationParameters.from_stream),
    0x1749405b: ('fsmc_0x1749405b', _decode_fsmc_0x1749405b),
    0x1b21eeb2: ('fsmc_0x1b21eeb2', _decode_fsmc_0x1b21eeb2),
    0x98169634: ('path_mesh_index', _decode_path_mesh_index),
    0x39a6dec3: ('unknown_0x39a6dec3', _decode_unknown_0x39a6dec3),
    0x47de2455: ('unknown_0x47de2455', _decode_unknown_0x47de2455),
    0xdfe74895: ('creature_death_particle_effect', _decode_creature_death_particle_effect),
    0xc88ad680: ('unknown_0xc88ad680', _decode_unknown_0xc88ad680),
    0x64c22667: ('caud', _decode_caud),
    0xfd8a9692: ('creature_death_particle_effect_uses_creature_orientation', _decode_creature_death_particle_effect_uses_creature_orientation),
    0xe0644402: ('ground_pound_slap_detection_radius', _decode_ground_pound_slap_detection_radius),
    0x6392404e: ('speed', _decode_speed),
    0x20c78bb: ('turn_speed', _decode_turn_speed),
    0x6d892893: ('unknown_0x6d892893', _decode_unknown_0x6d892893),
    0x8db77ee4: ('detection_range', _decode_detection_range),
    0x513f04b8: ('detection_height_range', _decode_detection_height_range),
    0x83dfc40f: ('detection_angle', _decode_detection_angle),
    0x58434916: ('min_attack_range', _decode_min_attack_range),
    0xff77c96f: ('max_attack_range', _decode_max_attack_range),
    0xb0cfe015: ('average_attack_time', _decode_average_attack_time),
    0xc80e329b: ('attack_time_variation', _decode_attack_time_variation),
}

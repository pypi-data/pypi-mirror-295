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
from retro_data_structures.properties.dkc_returns.archetypes.AdditiveTouchAttackBehaviorData import AdditiveTouchAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.AreaAttackBehaviorData import AreaAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.BopJumpBehaviorData import BopJumpBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.DamagedBehaviorData import DamagedBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.DrivenIntoGroundBehaviorData import DrivenIntoGroundBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FleeBehaviorData import FleeBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FollowPathControlBehaviorData import FollowPathControlBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FollowSurfaceBehaviorData import FollowSurfaceBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.FollowWaypointsBehaviorData import FollowWaypointsBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.GrabPlayerBehaviorData import GrabPlayerBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.GrabbedBehaviorData import GrabbedBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.IdleBehaviorData import IdleBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.OneShotBehaviorData import OneShotBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileAttackBehaviorData import ProjectileAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileBehaviorData import ProjectileBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SeekerBehaviorData import SeekerBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SeparateAndReformBehaviorData import SeparateAndReformBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SlideBehaviorData import SlideBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SpawnBehaviorData import SpawnBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.StackableBlockBehaviorData import StackableBlockBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.StunnedByBopBehaviorData import StunnedByBopBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.StunnedByContactRuleData import StunnedByContactRuleData
from retro_data_structures.properties.dkc_returns.archetypes.StunnedByGroundPoundBehaviorData import StunnedByGroundPoundBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SwingLineBehaviorData import SwingLineBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.SwoopBehaviorData import SwoopBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.TargetPlayerBehaviorData import TargetPlayerBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.TouchAttackBehaviorData import TouchAttackBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct109 import UnknownStruct109
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct115 import UnknownStruct115
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct116 import UnknownStruct116
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct118 import UnknownStruct118
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct119 import UnknownStruct119
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct122 import UnknownStruct122
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct128 import UnknownStruct128
from retro_data_structures.properties.dkc_returns.archetypes.VerticalFlightBehaviorData import VerticalFlightBehaviorData
from retro_data_structures.properties.dkc_returns.archetypes.WanderBehaviorData import WanderBehaviorData

if typing.TYPE_CHECKING:
    class BehaviorDataJson(typing_extensions.TypedDict):
        behavior_type: int
        damaged: json_util.JsonObject
        stunned_by_ground_pound: json_util.JsonObject
        stunned_by_bop: json_util.JsonObject
        touch_attack: json_util.JsonObject
        projectile_attack: json_util.JsonObject
        follow_waypoints: json_util.JsonObject
        grabbed: json_util.JsonObject
        flee: json_util.JsonObject
        wander: json_util.JsonObject
        follow_surface: json_util.JsonObject
        bop_jump: json_util.JsonObject
        idle: json_util.JsonObject
        unknown_struct109: json_util.JsonObject
        projectile: json_util.JsonObject
        vertical_flight: json_util.JsonObject
        stackable_block: json_util.JsonObject
        spawn: json_util.JsonObject
        swoop: json_util.JsonObject
        unknown_struct115: json_util.JsonObject
        unknown_struct116: json_util.JsonObject
        slide: json_util.JsonObject
        unknown_struct118: json_util.JsonObject
        unknown_struct119: json_util.JsonObject
        swing_line: json_util.JsonObject
        grab_player: json_util.JsonObject
        additive_touch_attack: json_util.JsonObject
        unknown_struct122: json_util.JsonObject
        stunned_by_contact_rule: json_util.JsonObject
        driven_into_ground: json_util.JsonObject
        one_shot: json_util.JsonObject
        target_player: json_util.JsonObject
        unknown: json_util.JsonObject
        area_attack: json_util.JsonObject
        unknown_struct128: json_util.JsonObject
        separate_and_reform: json_util.JsonObject
        additive_projectile_attack: json_util.JsonObject
        seeker: json_util.JsonObject
        follow_path_control: json_util.JsonObject
    

@dataclasses.dataclass()
class BehaviorData(BaseProperty):
    behavior_type: enums.BehaviorType = dataclasses.field(default=enums.BehaviorType.Unknown1, metadata={
        'reflection': FieldReflection[enums.BehaviorType](
            enums.BehaviorType, id=0x6403daed, original_name='BehaviorType', from_json=enums.BehaviorType.from_json, to_json=enums.BehaviorType.to_json
        ),
    })
    damaged: DamagedBehaviorData = dataclasses.field(default_factory=DamagedBehaviorData, metadata={
        'reflection': FieldReflection[DamagedBehaviorData](
            DamagedBehaviorData, id=0xd5110050, original_name='Damaged', from_json=DamagedBehaviorData.from_json, to_json=DamagedBehaviorData.to_json
        ),
    })
    stunned_by_ground_pound: StunnedByGroundPoundBehaviorData = dataclasses.field(default_factory=StunnedByGroundPoundBehaviorData, metadata={
        'reflection': FieldReflection[StunnedByGroundPoundBehaviorData](
            StunnedByGroundPoundBehaviorData, id=0xa792725d, original_name='StunnedByGroundPound', from_json=StunnedByGroundPoundBehaviorData.from_json, to_json=StunnedByGroundPoundBehaviorData.to_json
        ),
    })
    stunned_by_bop: StunnedByBopBehaviorData = dataclasses.field(default_factory=StunnedByBopBehaviorData, metadata={
        'reflection': FieldReflection[StunnedByBopBehaviorData](
            StunnedByBopBehaviorData, id=0x33ea54af, original_name='StunnedByBop', from_json=StunnedByBopBehaviorData.from_json, to_json=StunnedByBopBehaviorData.to_json
        ),
    })
    touch_attack: TouchAttackBehaviorData = dataclasses.field(default_factory=TouchAttackBehaviorData, metadata={
        'reflection': FieldReflection[TouchAttackBehaviorData](
            TouchAttackBehaviorData, id=0x50f0d548, original_name='TouchAttack', from_json=TouchAttackBehaviorData.from_json, to_json=TouchAttackBehaviorData.to_json
        ),
    })
    projectile_attack: ProjectileAttackBehaviorData = dataclasses.field(default_factory=ProjectileAttackBehaviorData, metadata={
        'reflection': FieldReflection[ProjectileAttackBehaviorData](
            ProjectileAttackBehaviorData, id=0x3ff111b9, original_name='ProjectileAttack', from_json=ProjectileAttackBehaviorData.from_json, to_json=ProjectileAttackBehaviorData.to_json
        ),
    })
    follow_waypoints: FollowWaypointsBehaviorData = dataclasses.field(default_factory=FollowWaypointsBehaviorData, metadata={
        'reflection': FieldReflection[FollowWaypointsBehaviorData](
            FollowWaypointsBehaviorData, id=0x6d2c073f, original_name='FollowWaypoints', from_json=FollowWaypointsBehaviorData.from_json, to_json=FollowWaypointsBehaviorData.to_json
        ),
    })
    grabbed: GrabbedBehaviorData = dataclasses.field(default_factory=GrabbedBehaviorData, metadata={
        'reflection': FieldReflection[GrabbedBehaviorData](
            GrabbedBehaviorData, id=0x24ff7572, original_name='Grabbed', from_json=GrabbedBehaviorData.from_json, to_json=GrabbedBehaviorData.to_json
        ),
    })
    flee: FleeBehaviorData = dataclasses.field(default_factory=FleeBehaviorData, metadata={
        'reflection': FieldReflection[FleeBehaviorData](
            FleeBehaviorData, id=0x799fe4f9, original_name='Flee', from_json=FleeBehaviorData.from_json, to_json=FleeBehaviorData.to_json
        ),
    })
    wander: WanderBehaviorData = dataclasses.field(default_factory=WanderBehaviorData, metadata={
        'reflection': FieldReflection[WanderBehaviorData](
            WanderBehaviorData, id=0x8c4949cf, original_name='Wander', from_json=WanderBehaviorData.from_json, to_json=WanderBehaviorData.to_json
        ),
    })
    follow_surface: FollowSurfaceBehaviorData = dataclasses.field(default_factory=FollowSurfaceBehaviorData, metadata={
        'reflection': FieldReflection[FollowSurfaceBehaviorData](
            FollowSurfaceBehaviorData, id=0x9344ed81, original_name='FollowSurface', from_json=FollowSurfaceBehaviorData.from_json, to_json=FollowSurfaceBehaviorData.to_json
        ),
    })
    bop_jump: BopJumpBehaviorData = dataclasses.field(default_factory=BopJumpBehaviorData, metadata={
        'reflection': FieldReflection[BopJumpBehaviorData](
            BopJumpBehaviorData, id=0xf764a9d2, original_name='BopJump', from_json=BopJumpBehaviorData.from_json, to_json=BopJumpBehaviorData.to_json
        ),
    })
    idle: IdleBehaviorData = dataclasses.field(default_factory=IdleBehaviorData, metadata={
        'reflection': FieldReflection[IdleBehaviorData](
            IdleBehaviorData, id=0x1b97c54d, original_name='Idle', from_json=IdleBehaviorData.from_json, to_json=IdleBehaviorData.to_json
        ),
    })
    unknown_struct109: UnknownStruct109 = dataclasses.field(default_factory=UnknownStruct109, metadata={
        'reflection': FieldReflection[UnknownStruct109](
            UnknownStruct109, id=0x4a54cb95, original_name='UnknownStruct109', from_json=UnknownStruct109.from_json, to_json=UnknownStruct109.to_json
        ),
    })
    projectile: ProjectileBehaviorData = dataclasses.field(default_factory=ProjectileBehaviorData, metadata={
        'reflection': FieldReflection[ProjectileBehaviorData](
            ProjectileBehaviorData, id=0x9bd0d08a, original_name='Projectile', from_json=ProjectileBehaviorData.from_json, to_json=ProjectileBehaviorData.to_json
        ),
    })
    vertical_flight: VerticalFlightBehaviorData = dataclasses.field(default_factory=VerticalFlightBehaviorData, metadata={
        'reflection': FieldReflection[VerticalFlightBehaviorData](
            VerticalFlightBehaviorData, id=0xec689e56, original_name='VerticalFlight', from_json=VerticalFlightBehaviorData.from_json, to_json=VerticalFlightBehaviorData.to_json
        ),
    })
    stackable_block: StackableBlockBehaviorData = dataclasses.field(default_factory=StackableBlockBehaviorData, metadata={
        'reflection': FieldReflection[StackableBlockBehaviorData](
            StackableBlockBehaviorData, id=0xabf0e7c3, original_name='StackableBlock', from_json=StackableBlockBehaviorData.from_json, to_json=StackableBlockBehaviorData.to_json
        ),
    })
    spawn: SpawnBehaviorData = dataclasses.field(default_factory=SpawnBehaviorData, metadata={
        'reflection': FieldReflection[SpawnBehaviorData](
            SpawnBehaviorData, id=0xb3e150a1, original_name='Spawn', from_json=SpawnBehaviorData.from_json, to_json=SpawnBehaviorData.to_json
        ),
    })
    swoop: SwoopBehaviorData = dataclasses.field(default_factory=SwoopBehaviorData, metadata={
        'reflection': FieldReflection[SwoopBehaviorData](
            SwoopBehaviorData, id=0xe5139db0, original_name='Swoop', from_json=SwoopBehaviorData.from_json, to_json=SwoopBehaviorData.to_json
        ),
    })
    unknown_struct115: UnknownStruct115 = dataclasses.field(default_factory=UnknownStruct115, metadata={
        'reflection': FieldReflection[UnknownStruct115](
            UnknownStruct115, id=0x3a5925d6, original_name='UnknownStruct115', from_json=UnknownStruct115.from_json, to_json=UnknownStruct115.to_json
        ),
    })
    unknown_struct116: UnknownStruct116 = dataclasses.field(default_factory=UnknownStruct116, metadata={
        'reflection': FieldReflection[UnknownStruct116](
            UnknownStruct116, id=0xde440d53, original_name='UnknownStruct116', from_json=UnknownStruct116.from_json, to_json=UnknownStruct116.to_json
        ),
    })
    slide: SlideBehaviorData = dataclasses.field(default_factory=SlideBehaviorData, metadata={
        'reflection': FieldReflection[SlideBehaviorData](
            SlideBehaviorData, id=0x6c80d03a, original_name='Slide', from_json=SlideBehaviorData.from_json, to_json=SlideBehaviorData.to_json
        ),
    })
    unknown_struct118: UnknownStruct118 = dataclasses.field(default_factory=UnknownStruct118, metadata={
        'reflection': FieldReflection[UnknownStruct118](
            UnknownStruct118, id=0xe233135a, original_name='UnknownStruct118', from_json=UnknownStruct118.from_json, to_json=UnknownStruct118.to_json
        ),
    })
    unknown_struct119: UnknownStruct119 = dataclasses.field(default_factory=UnknownStruct119, metadata={
        'reflection': FieldReflection[UnknownStruct119](
            UnknownStruct119, id=0x4699b820, original_name='UnknownStruct119', from_json=UnknownStruct119.from_json, to_json=UnknownStruct119.to_json
        ),
    })
    swing_line: SwingLineBehaviorData = dataclasses.field(default_factory=SwingLineBehaviorData, metadata={
        'reflection': FieldReflection[SwingLineBehaviorData](
            SwingLineBehaviorData, id=0xea2c12f9, original_name='SwingLine', from_json=SwingLineBehaviorData.from_json, to_json=SwingLineBehaviorData.to_json
        ),
    })
    grab_player: GrabPlayerBehaviorData = dataclasses.field(default_factory=GrabPlayerBehaviorData, metadata={
        'reflection': FieldReflection[GrabPlayerBehaviorData](
            GrabPlayerBehaviorData, id=0x32da6aa8, original_name='GrabPlayer', from_json=GrabPlayerBehaviorData.from_json, to_json=GrabPlayerBehaviorData.to_json
        ),
    })
    additive_touch_attack: AdditiveTouchAttackBehaviorData = dataclasses.field(default_factory=AdditiveTouchAttackBehaviorData, metadata={
        'reflection': FieldReflection[AdditiveTouchAttackBehaviorData](
            AdditiveTouchAttackBehaviorData, id=0xc962cb9c, original_name='AdditiveTouchAttack', from_json=AdditiveTouchAttackBehaviorData.from_json, to_json=AdditiveTouchAttackBehaviorData.to_json
        ),
    })
    unknown_struct122: UnknownStruct122 = dataclasses.field(default_factory=UnknownStruct122, metadata={
        'reflection': FieldReflection[UnknownStruct122](
            UnknownStruct122, id=0x0f6e5327, original_name='UnknownStruct122', from_json=UnknownStruct122.from_json, to_json=UnknownStruct122.to_json
        ),
    })
    stunned_by_contact_rule: StunnedByContactRuleData = dataclasses.field(default_factory=StunnedByContactRuleData, metadata={
        'reflection': FieldReflection[StunnedByContactRuleData](
            StunnedByContactRuleData, id=0xe2c2f5ef, original_name='StunnedByContactRule', from_json=StunnedByContactRuleData.from_json, to_json=StunnedByContactRuleData.to_json
        ),
    })
    driven_into_ground: DrivenIntoGroundBehaviorData = dataclasses.field(default_factory=DrivenIntoGroundBehaviorData, metadata={
        'reflection': FieldReflection[DrivenIntoGroundBehaviorData](
            DrivenIntoGroundBehaviorData, id=0x5192ccec, original_name='DrivenIntoGround', from_json=DrivenIntoGroundBehaviorData.from_json, to_json=DrivenIntoGroundBehaviorData.to_json
        ),
    })
    one_shot: OneShotBehaviorData = dataclasses.field(default_factory=OneShotBehaviorData, metadata={
        'reflection': FieldReflection[OneShotBehaviorData](
            OneShotBehaviorData, id=0xafcade60, original_name='OneShot', from_json=OneShotBehaviorData.from_json, to_json=OneShotBehaviorData.to_json
        ),
    })
    target_player: TargetPlayerBehaviorData = dataclasses.field(default_factory=TargetPlayerBehaviorData, metadata={
        'reflection': FieldReflection[TargetPlayerBehaviorData](
            TargetPlayerBehaviorData, id=0x749a68a1, original_name='TargetPlayer', from_json=TargetPlayerBehaviorData.from_json, to_json=TargetPlayerBehaviorData.to_json
        ),
    })
    unknown: DrivenIntoGroundBehaviorData = dataclasses.field(default_factory=DrivenIntoGroundBehaviorData, metadata={
        'reflection': FieldReflection[DrivenIntoGroundBehaviorData](
            DrivenIntoGroundBehaviorData, id=0x02cc6f52, original_name='Unknown', from_json=DrivenIntoGroundBehaviorData.from_json, to_json=DrivenIntoGroundBehaviorData.to_json
        ),
    })
    area_attack: AreaAttackBehaviorData = dataclasses.field(default_factory=AreaAttackBehaviorData, metadata={
        'reflection': FieldReflection[AreaAttackBehaviorData](
            AreaAttackBehaviorData, id=0xe37f3561, original_name='AreaAttack', from_json=AreaAttackBehaviorData.from_json, to_json=AreaAttackBehaviorData.to_json
        ),
    })
    unknown_struct128: UnknownStruct128 = dataclasses.field(default_factory=UnknownStruct128, metadata={
        'reflection': FieldReflection[UnknownStruct128](
            UnknownStruct128, id=0xa1f091b2, original_name='UnknownStruct128', from_json=UnknownStruct128.from_json, to_json=UnknownStruct128.to_json
        ),
    })
    separate_and_reform: SeparateAndReformBehaviorData = dataclasses.field(default_factory=SeparateAndReformBehaviorData, metadata={
        'reflection': FieldReflection[SeparateAndReformBehaviorData](
            SeparateAndReformBehaviorData, id=0x0638fc2b, original_name='SeparateAndReform', from_json=SeparateAndReformBehaviorData.from_json, to_json=SeparateAndReformBehaviorData.to_json
        ),
    })
    additive_projectile_attack: ProjectileAttackBehaviorData = dataclasses.field(default_factory=ProjectileAttackBehaviorData, metadata={
        'reflection': FieldReflection[ProjectileAttackBehaviorData](
            ProjectileAttackBehaviorData, id=0x311759a0, original_name='AdditiveProjectileAttack', from_json=ProjectileAttackBehaviorData.from_json, to_json=ProjectileAttackBehaviorData.to_json
        ),
    })
    seeker: SeekerBehaviorData = dataclasses.field(default_factory=SeekerBehaviorData, metadata={
        'reflection': FieldReflection[SeekerBehaviorData](
            SeekerBehaviorData, id=0x5fce6a84, original_name='Seeker', from_json=SeekerBehaviorData.from_json, to_json=SeekerBehaviorData.to_json
        ),
    })
    follow_path_control: FollowPathControlBehaviorData = dataclasses.field(default_factory=FollowPathControlBehaviorData, metadata={
        'reflection': FieldReflection[FollowPathControlBehaviorData](
            FollowPathControlBehaviorData, id=0xeed66e6d, original_name='FollowPathControl', from_json=FollowPathControlBehaviorData.from_json, to_json=FollowPathControlBehaviorData.to_json
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
        if property_count != 39:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6403daed
        behavior_type = enums.BehaviorType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd5110050
        damaged = DamagedBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa792725d
        stunned_by_ground_pound = StunnedByGroundPoundBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x33ea54af
        stunned_by_bop = StunnedByBopBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50f0d548
        touch_attack = TouchAttackBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3ff111b9
        projectile_attack = ProjectileAttackBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6d2c073f
        follow_waypoints = FollowWaypointsBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x24ff7572
        grabbed = GrabbedBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x799fe4f9
        flee = FleeBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8c4949cf
        wander = WanderBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9344ed81
        follow_surface = FollowSurfaceBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf764a9d2
        bop_jump = BopJumpBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b97c54d
        idle = IdleBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4a54cb95
        unknown_struct109 = UnknownStruct109.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9bd0d08a
        projectile = ProjectileBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xec689e56
        vertical_flight = VerticalFlightBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xabf0e7c3
        stackable_block = StackableBlockBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3e150a1
        spawn = SpawnBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe5139db0
        swoop = SwoopBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a5925d6
        unknown_struct115 = UnknownStruct115.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xde440d53
        unknown_struct116 = UnknownStruct116.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6c80d03a
        slide = SlideBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe233135a
        unknown_struct118 = UnknownStruct118.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4699b820
        unknown_struct119 = UnknownStruct119.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xea2c12f9
        swing_line = SwingLineBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x32da6aa8
        grab_player = GrabPlayerBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc962cb9c
        additive_touch_attack = AdditiveTouchAttackBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0f6e5327
        unknown_struct122 = UnknownStruct122.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2c2f5ef
        stunned_by_contact_rule = StunnedByContactRuleData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5192ccec
        driven_into_ground = DrivenIntoGroundBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xafcade60
        one_shot = OneShotBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x749a68a1
        target_player = TargetPlayerBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x02cc6f52
        unknown = DrivenIntoGroundBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe37f3561
        area_attack = AreaAttackBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa1f091b2
        unknown_struct128 = UnknownStruct128.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0638fc2b
        separate_and_reform = SeparateAndReformBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x311759a0
        additive_projectile_attack = ProjectileAttackBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5fce6a84
        seeker = SeekerBehaviorData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeed66e6d
        follow_path_control = FollowPathControlBehaviorData.from_stream(data, property_size)
    
        return cls(behavior_type, damaged, stunned_by_ground_pound, stunned_by_bop, touch_attack, projectile_attack, follow_waypoints, grabbed, flee, wander, follow_surface, bop_jump, idle, unknown_struct109, projectile, vertical_flight, stackable_block, spawn, swoop, unknown_struct115, unknown_struct116, slide, unknown_struct118, unknown_struct119, swing_line, grab_player, additive_touch_attack, unknown_struct122, stunned_by_contact_rule, driven_into_ground, one_shot, target_player, unknown, area_attack, unknown_struct128, separate_and_reform, additive_projectile_attack, seeker, follow_path_control)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b"\x00'")  # 39 properties

        data.write(b'd\x03\xda\xed')  # 0x6403daed
        data.write(b'\x00\x04')  # size
        self.behavior_type.to_stream(data)

        data.write(b'\xd5\x11\x00P')  # 0xd5110050
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damaged.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x92r]')  # 0xa792725d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned_by_ground_pound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\xeaT\xaf')  # 0x33ea54af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned_by_bop.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\xf0\xd5H')  # 0x50f0d548
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.touch_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\xf1\x11\xb9')  # 0x3ff111b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm,\x07?')  # 0x6d2c073f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.follow_waypoints.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xffur')  # 0x24ff7572
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grabbed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x9f\xe4\xf9')  # 0x799fe4f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flee.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8cII\xcf')  # 0x8c4949cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.wander.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93D\xed\x81')  # 0x9344ed81
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.follow_surface.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7d\xa9\xd2')  # 0xf764a9d2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bop_jump.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\x97\xc5M')  # 0x1b97c54d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.idle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'JT\xcb\x95')  # 0x4a54cb95
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct109.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\xd0\xd0\x8a')  # 0x9bd0d08a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xech\x9eV')  # 0xec689e56
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vertical_flight.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab\xf0\xe7\xc3')  # 0xabf0e7c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stackable_block.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xe1P\xa1')  # 0xb3e150a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spawn.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x13\x9d\xb0')  # 0xe5139db0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swoop.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':Y%\xd6')  # 0x3a5925d6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct115.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdeD\rS')  # 0xde440d53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct116.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\x80\xd0:')  # 0x6c80d03a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe23\x13Z')  # 0xe233135a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct118.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\x99\xb8 ')  # 0x4699b820
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct119.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea,\x12\xf9')  # 0xea2c12f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swing_line.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\xdaj\xa8')  # 0x32da6aa8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grab_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9b\xcb\x9c')  # 0xc962cb9c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.additive_touch_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\x0fnS'")  # 0xf6e5327
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct122.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\xc2\xf5\xef')  # 0xe2c2f5ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned_by_contact_rule.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x92\xcc\xec')  # 0x5192ccec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.driven_into_ground.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf\xca\xde`')  # 0xafcade60
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.one_shot.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\x9ah\xa1')  # 0x749a68a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\xccoR')  # 0x2cc6f52
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x7f5a')  # 0xe37f3561
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1\xf0\x91\xb2')  # 0xa1f091b2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct128.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x068\xfc+')  # 0x638fc2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.separate_and_reform.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\x17Y\xa0')  # 0x311759a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.additive_projectile_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\xcej\x84')  # 0x5fce6a84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seeker.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xee\xd6nm')  # 0xeed66e6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.follow_path_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BehaviorDataJson", data)
        return cls(
            behavior_type=enums.BehaviorType.from_json(json_data['behavior_type']),
            damaged=DamagedBehaviorData.from_json(json_data['damaged']),
            stunned_by_ground_pound=StunnedByGroundPoundBehaviorData.from_json(json_data['stunned_by_ground_pound']),
            stunned_by_bop=StunnedByBopBehaviorData.from_json(json_data['stunned_by_bop']),
            touch_attack=TouchAttackBehaviorData.from_json(json_data['touch_attack']),
            projectile_attack=ProjectileAttackBehaviorData.from_json(json_data['projectile_attack']),
            follow_waypoints=FollowWaypointsBehaviorData.from_json(json_data['follow_waypoints']),
            grabbed=GrabbedBehaviorData.from_json(json_data['grabbed']),
            flee=FleeBehaviorData.from_json(json_data['flee']),
            wander=WanderBehaviorData.from_json(json_data['wander']),
            follow_surface=FollowSurfaceBehaviorData.from_json(json_data['follow_surface']),
            bop_jump=BopJumpBehaviorData.from_json(json_data['bop_jump']),
            idle=IdleBehaviorData.from_json(json_data['idle']),
            unknown_struct109=UnknownStruct109.from_json(json_data['unknown_struct109']),
            projectile=ProjectileBehaviorData.from_json(json_data['projectile']),
            vertical_flight=VerticalFlightBehaviorData.from_json(json_data['vertical_flight']),
            stackable_block=StackableBlockBehaviorData.from_json(json_data['stackable_block']),
            spawn=SpawnBehaviorData.from_json(json_data['spawn']),
            swoop=SwoopBehaviorData.from_json(json_data['swoop']),
            unknown_struct115=UnknownStruct115.from_json(json_data['unknown_struct115']),
            unknown_struct116=UnknownStruct116.from_json(json_data['unknown_struct116']),
            slide=SlideBehaviorData.from_json(json_data['slide']),
            unknown_struct118=UnknownStruct118.from_json(json_data['unknown_struct118']),
            unknown_struct119=UnknownStruct119.from_json(json_data['unknown_struct119']),
            swing_line=SwingLineBehaviorData.from_json(json_data['swing_line']),
            grab_player=GrabPlayerBehaviorData.from_json(json_data['grab_player']),
            additive_touch_attack=AdditiveTouchAttackBehaviorData.from_json(json_data['additive_touch_attack']),
            unknown_struct122=UnknownStruct122.from_json(json_data['unknown_struct122']),
            stunned_by_contact_rule=StunnedByContactRuleData.from_json(json_data['stunned_by_contact_rule']),
            driven_into_ground=DrivenIntoGroundBehaviorData.from_json(json_data['driven_into_ground']),
            one_shot=OneShotBehaviorData.from_json(json_data['one_shot']),
            target_player=TargetPlayerBehaviorData.from_json(json_data['target_player']),
            unknown=DrivenIntoGroundBehaviorData.from_json(json_data['unknown']),
            area_attack=AreaAttackBehaviorData.from_json(json_data['area_attack']),
            unknown_struct128=UnknownStruct128.from_json(json_data['unknown_struct128']),
            separate_and_reform=SeparateAndReformBehaviorData.from_json(json_data['separate_and_reform']),
            additive_projectile_attack=ProjectileAttackBehaviorData.from_json(json_data['additive_projectile_attack']),
            seeker=SeekerBehaviorData.from_json(json_data['seeker']),
            follow_path_control=FollowPathControlBehaviorData.from_json(json_data['follow_path_control']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'behavior_type': self.behavior_type.to_json(),
            'damaged': self.damaged.to_json(),
            'stunned_by_ground_pound': self.stunned_by_ground_pound.to_json(),
            'stunned_by_bop': self.stunned_by_bop.to_json(),
            'touch_attack': self.touch_attack.to_json(),
            'projectile_attack': self.projectile_attack.to_json(),
            'follow_waypoints': self.follow_waypoints.to_json(),
            'grabbed': self.grabbed.to_json(),
            'flee': self.flee.to_json(),
            'wander': self.wander.to_json(),
            'follow_surface': self.follow_surface.to_json(),
            'bop_jump': self.bop_jump.to_json(),
            'idle': self.idle.to_json(),
            'unknown_struct109': self.unknown_struct109.to_json(),
            'projectile': self.projectile.to_json(),
            'vertical_flight': self.vertical_flight.to_json(),
            'stackable_block': self.stackable_block.to_json(),
            'spawn': self.spawn.to_json(),
            'swoop': self.swoop.to_json(),
            'unknown_struct115': self.unknown_struct115.to_json(),
            'unknown_struct116': self.unknown_struct116.to_json(),
            'slide': self.slide.to_json(),
            'unknown_struct118': self.unknown_struct118.to_json(),
            'unknown_struct119': self.unknown_struct119.to_json(),
            'swing_line': self.swing_line.to_json(),
            'grab_player': self.grab_player.to_json(),
            'additive_touch_attack': self.additive_touch_attack.to_json(),
            'unknown_struct122': self.unknown_struct122.to_json(),
            'stunned_by_contact_rule': self.stunned_by_contact_rule.to_json(),
            'driven_into_ground': self.driven_into_ground.to_json(),
            'one_shot': self.one_shot.to_json(),
            'target_player': self.target_player.to_json(),
            'unknown': self.unknown.to_json(),
            'area_attack': self.area_attack.to_json(),
            'unknown_struct128': self.unknown_struct128.to_json(),
            'separate_and_reform': self.separate_and_reform.to_json(),
            'additive_projectile_attack': self.additive_projectile_attack.to_json(),
            'seeker': self.seeker.to_json(),
            'follow_path_control': self.follow_path_control.to_json(),
        }


def _decode_behavior_type(data: typing.BinaryIO, property_size: int):
    return enums.BehaviorType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6403daed: ('behavior_type', _decode_behavior_type),
    0xd5110050: ('damaged', DamagedBehaviorData.from_stream),
    0xa792725d: ('stunned_by_ground_pound', StunnedByGroundPoundBehaviorData.from_stream),
    0x33ea54af: ('stunned_by_bop', StunnedByBopBehaviorData.from_stream),
    0x50f0d548: ('touch_attack', TouchAttackBehaviorData.from_stream),
    0x3ff111b9: ('projectile_attack', ProjectileAttackBehaviorData.from_stream),
    0x6d2c073f: ('follow_waypoints', FollowWaypointsBehaviorData.from_stream),
    0x24ff7572: ('grabbed', GrabbedBehaviorData.from_stream),
    0x799fe4f9: ('flee', FleeBehaviorData.from_stream),
    0x8c4949cf: ('wander', WanderBehaviorData.from_stream),
    0x9344ed81: ('follow_surface', FollowSurfaceBehaviorData.from_stream),
    0xf764a9d2: ('bop_jump', BopJumpBehaviorData.from_stream),
    0x1b97c54d: ('idle', IdleBehaviorData.from_stream),
    0x4a54cb95: ('unknown_struct109', UnknownStruct109.from_stream),
    0x9bd0d08a: ('projectile', ProjectileBehaviorData.from_stream),
    0xec689e56: ('vertical_flight', VerticalFlightBehaviorData.from_stream),
    0xabf0e7c3: ('stackable_block', StackableBlockBehaviorData.from_stream),
    0xb3e150a1: ('spawn', SpawnBehaviorData.from_stream),
    0xe5139db0: ('swoop', SwoopBehaviorData.from_stream),
    0x3a5925d6: ('unknown_struct115', UnknownStruct115.from_stream),
    0xde440d53: ('unknown_struct116', UnknownStruct116.from_stream),
    0x6c80d03a: ('slide', SlideBehaviorData.from_stream),
    0xe233135a: ('unknown_struct118', UnknownStruct118.from_stream),
    0x4699b820: ('unknown_struct119', UnknownStruct119.from_stream),
    0xea2c12f9: ('swing_line', SwingLineBehaviorData.from_stream),
    0x32da6aa8: ('grab_player', GrabPlayerBehaviorData.from_stream),
    0xc962cb9c: ('additive_touch_attack', AdditiveTouchAttackBehaviorData.from_stream),
    0xf6e5327: ('unknown_struct122', UnknownStruct122.from_stream),
    0xe2c2f5ef: ('stunned_by_contact_rule', StunnedByContactRuleData.from_stream),
    0x5192ccec: ('driven_into_ground', DrivenIntoGroundBehaviorData.from_stream),
    0xafcade60: ('one_shot', OneShotBehaviorData.from_stream),
    0x749a68a1: ('target_player', TargetPlayerBehaviorData.from_stream),
    0x2cc6f52: ('unknown', DrivenIntoGroundBehaviorData.from_stream),
    0xe37f3561: ('area_attack', AreaAttackBehaviorData.from_stream),
    0xa1f091b2: ('unknown_struct128', UnknownStruct128.from_stream),
    0x638fc2b: ('separate_and_reform', SeparateAndReformBehaviorData.from_stream),
    0x311759a0: ('additive_projectile_attack', ProjectileAttackBehaviorData.from_stream),
    0x5fce6a84: ('seeker', SeekerBehaviorData.from_stream),
    0xeed66e6d: ('follow_path_control', FollowPathControlBehaviorData.from_stream),
}

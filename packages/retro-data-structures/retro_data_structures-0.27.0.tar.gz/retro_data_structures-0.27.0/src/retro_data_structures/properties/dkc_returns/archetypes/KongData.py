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
from retro_data_structures.properties.dkc_returns.archetypes.KongGrabData import KongGrabData
from retro_data_structures.properties.dkc_returns.archetypes.KongGroundPoundData import KongGroundPoundData
from retro_data_structures.properties.dkc_returns.archetypes.KongRunningSlapData import KongRunningSlapData
from retro_data_structures.properties.dkc_returns.archetypes.KongSlideData import KongSlideData
from retro_data_structures.properties.dkc_returns.archetypes.KongStalledDescentData import KongStalledDescentData
from retro_data_structures.properties.dkc_returns.archetypes.KongSwingData import KongSwingData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAttachmentsData import PlayerAttachmentsData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerBarrelCannonData import PlayerBarrelCannonData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerBasicMovementData import PlayerBasicMovementData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerBopAnimThresholds import PlayerBopAnimThresholds
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCling2Data import PlayerCling2Data
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCommonData import PlayerCommonData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCrouchData import PlayerCrouchData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCrushData import PlayerCrushData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerFireReactionData import PlayerFireReactionData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerHeadTrackingData import PlayerHeadTrackingData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerJumpAnimWeights import PlayerJumpAnimWeights
from retro_data_structures.properties.dkc_returns.archetypes.PlayerJumpData import PlayerJumpData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMeleeData import PlayerMeleeData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountData import PlayerMountData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountRiderList import PlayerMountRiderList
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardData import PlayerMultiKillRewardData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerOffscreenIndicator import PlayerOffscreenIndicator
from retro_data_structures.properties.dkc_returns.archetypes.PlayerPeanutGunData import PlayerPeanutGunData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerPeriodicAdditiveAnimationData import PlayerPeriodicAdditiveAnimationData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerRiseFromTheGraveData import PlayerRiseFromTheGraveData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerShieldData import PlayerShieldData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerSlaveData import PlayerSlaveData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerSplineAdvancementData import PlayerSplineAdvancementData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTarInteractionData import PlayerTarInteractionData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTeleportData import PlayerTeleportData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTerrainAlignmentData import PlayerTerrainAlignmentData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerTireInteractionData import PlayerTireInteractionData
from retro_data_structures.properties.dkc_returns.archetypes.RambiControllerData import RambiControllerData

if typing.TYPE_CHECKING:
    class KongDataJson(typing_extensions.TypedDict):
        common: json_util.JsonObject
        basic_movement: json_util.JsonObject
        jump_data: json_util.JsonObject
        jump_animation_weights: json_util.JsonObject
        jump_bop_animation_thresholds: json_util.JsonObject
        spline_advancement: json_util.JsonObject
        rambi_controller_data: json_util.JsonObject
        attachments_data: json_util.JsonObject
        barrel_cannon_data: json_util.JsonObject
        cling2_data: json_util.JsonObject
        kong_ground_pound_data: json_util.JsonObject
        kong_cling_slap_data: json_util.JsonObject
        kong_running_slap_data: json_util.JsonObject
        kong_swing_data: json_util.JsonObject
        kong_slide_data: json_util.JsonObject
        kong_stalled_descent_data: json_util.JsonObject
        kong_grab_data: json_util.JsonObject
        head_tracking_data: json_util.JsonObject
        melee_data: json_util.JsonObject
        mount_data: json_util.JsonObject
        rider_list_data: json_util.JsonObject
        periodic_additive_animation_data: json_util.JsonObject
        slave_data: json_util.JsonObject
        offscreen_data: json_util.JsonObject
        tar_interaction_data: json_util.JsonObject
        teleport_data: json_util.JsonObject
        tire_interaction_data: json_util.JsonObject
        peanut_gun_data: json_util.JsonObject
        crouch_data: json_util.JsonObject
        fire_reaction: json_util.JsonObject
        crush_data: json_util.JsonObject
        multi_kill_reward_data: json_util.JsonObject
        rise_from_the_grave_data: json_util.JsonObject
        terrain_alignment_data: json_util.JsonObject
        shield_data: json_util.JsonObject
    

@dataclasses.dataclass()
class KongData(BaseProperty):
    common: PlayerCommonData = dataclasses.field(default_factory=PlayerCommonData, metadata={
        'reflection': FieldReflection[PlayerCommonData](
            PlayerCommonData, id=0x3c38498d, original_name='Common', from_json=PlayerCommonData.from_json, to_json=PlayerCommonData.to_json
        ),
    })
    basic_movement: PlayerBasicMovementData = dataclasses.field(default_factory=PlayerBasicMovementData, metadata={
        'reflection': FieldReflection[PlayerBasicMovementData](
            PlayerBasicMovementData, id=0x7fb7e8b1, original_name='BasicMovement', from_json=PlayerBasicMovementData.from_json, to_json=PlayerBasicMovementData.to_json
        ),
    })
    jump_data: PlayerJumpData = dataclasses.field(default_factory=PlayerJumpData, metadata={
        'reflection': FieldReflection[PlayerJumpData](
            PlayerJumpData, id=0xf07bec6d, original_name='JumpData', from_json=PlayerJumpData.from_json, to_json=PlayerJumpData.to_json
        ),
    })
    jump_animation_weights: PlayerJumpAnimWeights = dataclasses.field(default_factory=PlayerJumpAnimWeights, metadata={
        'reflection': FieldReflection[PlayerJumpAnimWeights](
            PlayerJumpAnimWeights, id=0xf3d8dcb1, original_name='JumpAnimationWeights', from_json=PlayerJumpAnimWeights.from_json, to_json=PlayerJumpAnimWeights.to_json
        ),
    })
    jump_bop_animation_thresholds: PlayerBopAnimThresholds = dataclasses.field(default_factory=PlayerBopAnimThresholds, metadata={
        'reflection': FieldReflection[PlayerBopAnimThresholds](
            PlayerBopAnimThresholds, id=0x5e1168ac, original_name='JumpBopAnimationThresholds', from_json=PlayerBopAnimThresholds.from_json, to_json=PlayerBopAnimThresholds.to_json
        ),
    })
    spline_advancement: PlayerSplineAdvancementData = dataclasses.field(default_factory=PlayerSplineAdvancementData, metadata={
        'reflection': FieldReflection[PlayerSplineAdvancementData](
            PlayerSplineAdvancementData, id=0x5d89056a, original_name='SplineAdvancement', from_json=PlayerSplineAdvancementData.from_json, to_json=PlayerSplineAdvancementData.to_json
        ),
    })
    rambi_controller_data: RambiControllerData = dataclasses.field(default_factory=RambiControllerData, metadata={
        'reflection': FieldReflection[RambiControllerData](
            RambiControllerData, id=0xe03287ae, original_name='RambiControllerData', from_json=RambiControllerData.from_json, to_json=RambiControllerData.to_json
        ),
    })
    attachments_data: PlayerAttachmentsData = dataclasses.field(default_factory=PlayerAttachmentsData, metadata={
        'reflection': FieldReflection[PlayerAttachmentsData](
            PlayerAttachmentsData, id=0x9f1ef2f3, original_name='AttachmentsData', from_json=PlayerAttachmentsData.from_json, to_json=PlayerAttachmentsData.to_json
        ),
    })
    barrel_cannon_data: PlayerBarrelCannonData = dataclasses.field(default_factory=PlayerBarrelCannonData, metadata={
        'reflection': FieldReflection[PlayerBarrelCannonData](
            PlayerBarrelCannonData, id=0xbbca7365, original_name='BarrelCannonData', from_json=PlayerBarrelCannonData.from_json, to_json=PlayerBarrelCannonData.to_json
        ),
    })
    cling2_data: PlayerCling2Data = dataclasses.field(default_factory=PlayerCling2Data, metadata={
        'reflection': FieldReflection[PlayerCling2Data](
            PlayerCling2Data, id=0xf9b150fc, original_name='Cling2Data', from_json=PlayerCling2Data.from_json, to_json=PlayerCling2Data.to_json
        ),
    })
    kong_ground_pound_data: KongGroundPoundData = dataclasses.field(default_factory=KongGroundPoundData, metadata={
        'reflection': FieldReflection[KongGroundPoundData](
            KongGroundPoundData, id=0x856f56a7, original_name='KongGroundPoundData', from_json=KongGroundPoundData.from_json, to_json=KongGroundPoundData.to_json
        ),
    })
    kong_cling_slap_data: KongGroundPoundData = dataclasses.field(default_factory=KongGroundPoundData, metadata={
        'reflection': FieldReflection[KongGroundPoundData](
            KongGroundPoundData, id=0xf5e908d1, original_name='KongClingSlapData', from_json=KongGroundPoundData.from_json, to_json=KongGroundPoundData.to_json
        ),
    })
    kong_running_slap_data: KongRunningSlapData = dataclasses.field(default_factory=KongRunningSlapData, metadata={
        'reflection': FieldReflection[KongRunningSlapData](
            KongRunningSlapData, id=0x36453107, original_name='KongRunningSlapData', from_json=KongRunningSlapData.from_json, to_json=KongRunningSlapData.to_json
        ),
    })
    kong_swing_data: KongSwingData = dataclasses.field(default_factory=KongSwingData, metadata={
        'reflection': FieldReflection[KongSwingData](
            KongSwingData, id=0xf7878a5a, original_name='KongSwingData', from_json=KongSwingData.from_json, to_json=KongSwingData.to_json
        ),
    })
    kong_slide_data: KongSlideData = dataclasses.field(default_factory=KongSlideData, metadata={
        'reflection': FieldReflection[KongSlideData](
            KongSlideData, id=0x60c43eaf, original_name='KongSlideData', from_json=KongSlideData.from_json, to_json=KongSlideData.to_json
        ),
    })
    kong_stalled_descent_data: KongStalledDescentData = dataclasses.field(default_factory=KongStalledDescentData, metadata={
        'reflection': FieldReflection[KongStalledDescentData](
            KongStalledDescentData, id=0xe38134fc, original_name='KongStalledDescentData', from_json=KongStalledDescentData.from_json, to_json=KongStalledDescentData.to_json
        ),
    })
    kong_grab_data: KongGrabData = dataclasses.field(default_factory=KongGrabData, metadata={
        'reflection': FieldReflection[KongGrabData](
            KongGrabData, id=0x75586c2b, original_name='KongGrabData', from_json=KongGrabData.from_json, to_json=KongGrabData.to_json
        ),
    })
    head_tracking_data: PlayerHeadTrackingData = dataclasses.field(default_factory=PlayerHeadTrackingData, metadata={
        'reflection': FieldReflection[PlayerHeadTrackingData](
            PlayerHeadTrackingData, id=0x4d6c99eb, original_name='HeadTrackingData', from_json=PlayerHeadTrackingData.from_json, to_json=PlayerHeadTrackingData.to_json
        ),
    })
    melee_data: PlayerMeleeData = dataclasses.field(default_factory=PlayerMeleeData, metadata={
        'reflection': FieldReflection[PlayerMeleeData](
            PlayerMeleeData, id=0xf2b15344, original_name='MeleeData', from_json=PlayerMeleeData.from_json, to_json=PlayerMeleeData.to_json
        ),
    })
    mount_data: PlayerMountData = dataclasses.field(default_factory=PlayerMountData, metadata={
        'reflection': FieldReflection[PlayerMountData](
            PlayerMountData, id=0x978e5bd8, original_name='MountData', from_json=PlayerMountData.from_json, to_json=PlayerMountData.to_json
        ),
    })
    rider_list_data: PlayerMountRiderList = dataclasses.field(default_factory=PlayerMountRiderList, metadata={
        'reflection': FieldReflection[PlayerMountRiderList](
            PlayerMountRiderList, id=0x7f681411, original_name='RiderListData', from_json=PlayerMountRiderList.from_json, to_json=PlayerMountRiderList.to_json
        ),
    })
    periodic_additive_animation_data: PlayerPeriodicAdditiveAnimationData = dataclasses.field(default_factory=PlayerPeriodicAdditiveAnimationData, metadata={
        'reflection': FieldReflection[PlayerPeriodicAdditiveAnimationData](
            PlayerPeriodicAdditiveAnimationData, id=0x249dc50a, original_name='PeriodicAdditiveAnimationData', from_json=PlayerPeriodicAdditiveAnimationData.from_json, to_json=PlayerPeriodicAdditiveAnimationData.to_json
        ),
    })
    slave_data: PlayerSlaveData = dataclasses.field(default_factory=PlayerSlaveData, metadata={
        'reflection': FieldReflection[PlayerSlaveData](
            PlayerSlaveData, id=0x29c83997, original_name='SlaveData', from_json=PlayerSlaveData.from_json, to_json=PlayerSlaveData.to_json
        ),
    })
    offscreen_data: PlayerOffscreenIndicator = dataclasses.field(default_factory=PlayerOffscreenIndicator, metadata={
        'reflection': FieldReflection[PlayerOffscreenIndicator](
            PlayerOffscreenIndicator, id=0x74b21331, original_name='OffscreenData', from_json=PlayerOffscreenIndicator.from_json, to_json=PlayerOffscreenIndicator.to_json
        ),
    })
    tar_interaction_data: PlayerTarInteractionData = dataclasses.field(default_factory=PlayerTarInteractionData, metadata={
        'reflection': FieldReflection[PlayerTarInteractionData](
            PlayerTarInteractionData, id=0xc3260ca9, original_name='TarInteractionData', from_json=PlayerTarInteractionData.from_json, to_json=PlayerTarInteractionData.to_json
        ),
    })
    teleport_data: PlayerTeleportData = dataclasses.field(default_factory=PlayerTeleportData, metadata={
        'reflection': FieldReflection[PlayerTeleportData](
            PlayerTeleportData, id=0xa7117cdd, original_name='TeleportData', from_json=PlayerTeleportData.from_json, to_json=PlayerTeleportData.to_json
        ),
    })
    tire_interaction_data: PlayerTireInteractionData = dataclasses.field(default_factory=PlayerTireInteractionData, metadata={
        'reflection': FieldReflection[PlayerTireInteractionData](
            PlayerTireInteractionData, id=0xe31814db, original_name='TireInteractionData', from_json=PlayerTireInteractionData.from_json, to_json=PlayerTireInteractionData.to_json
        ),
    })
    peanut_gun_data: PlayerPeanutGunData = dataclasses.field(default_factory=PlayerPeanutGunData, metadata={
        'reflection': FieldReflection[PlayerPeanutGunData](
            PlayerPeanutGunData, id=0x8870d3dd, original_name='PeanutGunData', from_json=PlayerPeanutGunData.from_json, to_json=PlayerPeanutGunData.to_json
        ),
    })
    crouch_data: PlayerCrouchData = dataclasses.field(default_factory=PlayerCrouchData, metadata={
        'reflection': FieldReflection[PlayerCrouchData](
            PlayerCrouchData, id=0x2d712fbe, original_name='CrouchData', from_json=PlayerCrouchData.from_json, to_json=PlayerCrouchData.to_json
        ),
    })
    fire_reaction: PlayerFireReactionData = dataclasses.field(default_factory=PlayerFireReactionData, metadata={
        'reflection': FieldReflection[PlayerFireReactionData](
            PlayerFireReactionData, id=0xfa1f4263, original_name='FireReaction', from_json=PlayerFireReactionData.from_json, to_json=PlayerFireReactionData.to_json
        ),
    })
    crush_data: PlayerCrushData = dataclasses.field(default_factory=PlayerCrushData, metadata={
        'reflection': FieldReflection[PlayerCrushData](
            PlayerCrushData, id=0x8abb25c4, original_name='CrushData', from_json=PlayerCrushData.from_json, to_json=PlayerCrushData.to_json
        ),
    })
    multi_kill_reward_data: PlayerMultiKillRewardData = dataclasses.field(default_factory=PlayerMultiKillRewardData, metadata={
        'reflection': FieldReflection[PlayerMultiKillRewardData](
            PlayerMultiKillRewardData, id=0x98efc863, original_name='MultiKillRewardData', from_json=PlayerMultiKillRewardData.from_json, to_json=PlayerMultiKillRewardData.to_json
        ),
    })
    rise_from_the_grave_data: PlayerRiseFromTheGraveData = dataclasses.field(default_factory=PlayerRiseFromTheGraveData, metadata={
        'reflection': FieldReflection[PlayerRiseFromTheGraveData](
            PlayerRiseFromTheGraveData, id=0x39b0b057, original_name='RiseFromTheGraveData', from_json=PlayerRiseFromTheGraveData.from_json, to_json=PlayerRiseFromTheGraveData.to_json
        ),
    })
    terrain_alignment_data: PlayerTerrainAlignmentData = dataclasses.field(default_factory=PlayerTerrainAlignmentData, metadata={
        'reflection': FieldReflection[PlayerTerrainAlignmentData](
            PlayerTerrainAlignmentData, id=0x1bd6769f, original_name='TerrainAlignmentData', from_json=PlayerTerrainAlignmentData.from_json, to_json=PlayerTerrainAlignmentData.to_json
        ),
    })
    shield_data: PlayerShieldData = dataclasses.field(default_factory=PlayerShieldData, metadata={
        'reflection': FieldReflection[PlayerShieldData](
            PlayerShieldData, id=0xb2d0a449, original_name='ShieldData', from_json=PlayerShieldData.from_json, to_json=PlayerShieldData.to_json
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
        if property_count != 35:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3c38498d
        common = PlayerCommonData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7fb7e8b1
        basic_movement = PlayerBasicMovementData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf07bec6d
        jump_data = PlayerJumpData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf3d8dcb1
        jump_animation_weights = PlayerJumpAnimWeights.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e1168ac
        jump_bop_animation_thresholds = PlayerBopAnimThresholds.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5d89056a
        spline_advancement = PlayerSplineAdvancementData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe03287ae
        rambi_controller_data = RambiControllerData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9f1ef2f3
        attachments_data = PlayerAttachmentsData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbca7365
        barrel_cannon_data = PlayerBarrelCannonData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf9b150fc
        cling2_data = PlayerCling2Data.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x856f56a7
        kong_ground_pound_data = KongGroundPoundData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5e908d1
        kong_cling_slap_data = KongGroundPoundData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36453107
        kong_running_slap_data = KongRunningSlapData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf7878a5a
        kong_swing_data = KongSwingData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60c43eaf
        kong_slide_data = KongSlideData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe38134fc
        kong_stalled_descent_data = KongStalledDescentData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x75586c2b
        kong_grab_data = KongGrabData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4d6c99eb
        head_tracking_data = PlayerHeadTrackingData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf2b15344
        melee_data = PlayerMeleeData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x978e5bd8
        mount_data = PlayerMountData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f681411
        rider_list_data = PlayerMountRiderList.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x249dc50a
        periodic_additive_animation_data = PlayerPeriodicAdditiveAnimationData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x29c83997
        slave_data = PlayerSlaveData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x74b21331
        offscreen_data = PlayerOffscreenIndicator.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc3260ca9
        tar_interaction_data = PlayerTarInteractionData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa7117cdd
        teleport_data = PlayerTeleportData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe31814db
        tire_interaction_data = PlayerTireInteractionData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8870d3dd
        peanut_gun_data = PlayerPeanutGunData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2d712fbe
        crouch_data = PlayerCrouchData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfa1f4263
        fire_reaction = PlayerFireReactionData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8abb25c4
        crush_data = PlayerCrushData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x98efc863
        multi_kill_reward_data = PlayerMultiKillRewardData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x39b0b057
        rise_from_the_grave_data = PlayerRiseFromTheGraveData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1bd6769f
        terrain_alignment_data = PlayerTerrainAlignmentData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb2d0a449
        shield_data = PlayerShieldData.from_stream(data, property_size)
    
        return cls(common, basic_movement, jump_data, jump_animation_weights, jump_bop_animation_thresholds, spline_advancement, rambi_controller_data, attachments_data, barrel_cannon_data, cling2_data, kong_ground_pound_data, kong_cling_slap_data, kong_running_slap_data, kong_swing_data, kong_slide_data, kong_stalled_descent_data, kong_grab_data, head_tracking_data, melee_data, mount_data, rider_list_data, periodic_additive_animation_data, slave_data, offscreen_data, tar_interaction_data, teleport_data, tire_interaction_data, peanut_gun_data, crouch_data, fire_reaction, crush_data, multi_kill_reward_data, rise_from_the_grave_data, terrain_alignment_data, shield_data)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00#')  # 35 properties

        data.write(b'<8I\x8d')  # 0x3c38498d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.common.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xb7\xe8\xb1')  # 0x7fb7e8b1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.basic_movement.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0{\xecm')  # 0xf07bec6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xd8\xdc\xb1')  # 0xf3d8dcb1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_animation_weights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\x11h\xac')  # 0x5e1168ac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_bop_animation_thresholds.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\x89\x05j')  # 0x5d89056a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline_advancement.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe02\x87\xae')  # 0xe03287ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rambi_controller_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9f\x1e\xf2\xf3')  # 0x9f1ef2f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachments_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xcase')  # 0xbbca7365
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.barrel_cannon_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xb1P\xfc')  # 0xf9b150fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cling2_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85oV\xa7')  # 0x856f56a7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_ground_pound_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\xe9\x08\xd1')  # 0xf5e908d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_cling_slap_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6E1\x07')  # 0x36453107
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_running_slap_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\x87\x8aZ')  # 0xf7878a5a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_swing_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'`\xc4>\xaf')  # 0x60c43eaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_slide_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x814\xfc')  # 0xe38134fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_stalled_descent_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'uXl+')  # 0x75586c2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_grab_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Ml\x99\xeb')  # 0x4d6c99eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.head_tracking_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2\xb1SD')  # 0xf2b15344
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\x8e[\xd8')  # 0x978e5bd8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mount_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7fh\x14\x11')  # 0x7f681411
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider_list_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\x9d\xc5\n')  # 0x249dc50a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.periodic_additive_animation_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')\xc89\x97')  # 0x29c83997
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slave_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\xb2\x131')  # 0x74b21331
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offscreen_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3&\x0c\xa9')  # 0xc3260ca9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar_interaction_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7\x11|\xdd')  # 0xa7117cdd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.teleport_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\x18\x14\xdb')  # 0xe31814db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tire_interaction_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88p\xd3\xdd')  # 0x8870d3dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.peanut_gun_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-q/\xbe')  # 0x2d712fbe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.crouch_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x1fBc')  # 0xfa1f4263
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fire_reaction.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8a\xbb%\xc4')  # 0x8abb25c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.crush_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xef\xc8c')  # 0x98efc863
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.multi_kill_reward_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9\xb0\xb0W')  # 0x39b0b057
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rise_from_the_grave_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\xd6v\x9f')  # 0x1bd6769f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.terrain_alignment_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\xd0\xa4I')  # 0xb2d0a449
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("KongDataJson", data)
        return cls(
            common=PlayerCommonData.from_json(json_data['common']),
            basic_movement=PlayerBasicMovementData.from_json(json_data['basic_movement']),
            jump_data=PlayerJumpData.from_json(json_data['jump_data']),
            jump_animation_weights=PlayerJumpAnimWeights.from_json(json_data['jump_animation_weights']),
            jump_bop_animation_thresholds=PlayerBopAnimThresholds.from_json(json_data['jump_bop_animation_thresholds']),
            spline_advancement=PlayerSplineAdvancementData.from_json(json_data['spline_advancement']),
            rambi_controller_data=RambiControllerData.from_json(json_data['rambi_controller_data']),
            attachments_data=PlayerAttachmentsData.from_json(json_data['attachments_data']),
            barrel_cannon_data=PlayerBarrelCannonData.from_json(json_data['barrel_cannon_data']),
            cling2_data=PlayerCling2Data.from_json(json_data['cling2_data']),
            kong_ground_pound_data=KongGroundPoundData.from_json(json_data['kong_ground_pound_data']),
            kong_cling_slap_data=KongGroundPoundData.from_json(json_data['kong_cling_slap_data']),
            kong_running_slap_data=KongRunningSlapData.from_json(json_data['kong_running_slap_data']),
            kong_swing_data=KongSwingData.from_json(json_data['kong_swing_data']),
            kong_slide_data=KongSlideData.from_json(json_data['kong_slide_data']),
            kong_stalled_descent_data=KongStalledDescentData.from_json(json_data['kong_stalled_descent_data']),
            kong_grab_data=KongGrabData.from_json(json_data['kong_grab_data']),
            head_tracking_data=PlayerHeadTrackingData.from_json(json_data['head_tracking_data']),
            melee_data=PlayerMeleeData.from_json(json_data['melee_data']),
            mount_data=PlayerMountData.from_json(json_data['mount_data']),
            rider_list_data=PlayerMountRiderList.from_json(json_data['rider_list_data']),
            periodic_additive_animation_data=PlayerPeriodicAdditiveAnimationData.from_json(json_data['periodic_additive_animation_data']),
            slave_data=PlayerSlaveData.from_json(json_data['slave_data']),
            offscreen_data=PlayerOffscreenIndicator.from_json(json_data['offscreen_data']),
            tar_interaction_data=PlayerTarInteractionData.from_json(json_data['tar_interaction_data']),
            teleport_data=PlayerTeleportData.from_json(json_data['teleport_data']),
            tire_interaction_data=PlayerTireInteractionData.from_json(json_data['tire_interaction_data']),
            peanut_gun_data=PlayerPeanutGunData.from_json(json_data['peanut_gun_data']),
            crouch_data=PlayerCrouchData.from_json(json_data['crouch_data']),
            fire_reaction=PlayerFireReactionData.from_json(json_data['fire_reaction']),
            crush_data=PlayerCrushData.from_json(json_data['crush_data']),
            multi_kill_reward_data=PlayerMultiKillRewardData.from_json(json_data['multi_kill_reward_data']),
            rise_from_the_grave_data=PlayerRiseFromTheGraveData.from_json(json_data['rise_from_the_grave_data']),
            terrain_alignment_data=PlayerTerrainAlignmentData.from_json(json_data['terrain_alignment_data']),
            shield_data=PlayerShieldData.from_json(json_data['shield_data']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'common': self.common.to_json(),
            'basic_movement': self.basic_movement.to_json(),
            'jump_data': self.jump_data.to_json(),
            'jump_animation_weights': self.jump_animation_weights.to_json(),
            'jump_bop_animation_thresholds': self.jump_bop_animation_thresholds.to_json(),
            'spline_advancement': self.spline_advancement.to_json(),
            'rambi_controller_data': self.rambi_controller_data.to_json(),
            'attachments_data': self.attachments_data.to_json(),
            'barrel_cannon_data': self.barrel_cannon_data.to_json(),
            'cling2_data': self.cling2_data.to_json(),
            'kong_ground_pound_data': self.kong_ground_pound_data.to_json(),
            'kong_cling_slap_data': self.kong_cling_slap_data.to_json(),
            'kong_running_slap_data': self.kong_running_slap_data.to_json(),
            'kong_swing_data': self.kong_swing_data.to_json(),
            'kong_slide_data': self.kong_slide_data.to_json(),
            'kong_stalled_descent_data': self.kong_stalled_descent_data.to_json(),
            'kong_grab_data': self.kong_grab_data.to_json(),
            'head_tracking_data': self.head_tracking_data.to_json(),
            'melee_data': self.melee_data.to_json(),
            'mount_data': self.mount_data.to_json(),
            'rider_list_data': self.rider_list_data.to_json(),
            'periodic_additive_animation_data': self.periodic_additive_animation_data.to_json(),
            'slave_data': self.slave_data.to_json(),
            'offscreen_data': self.offscreen_data.to_json(),
            'tar_interaction_data': self.tar_interaction_data.to_json(),
            'teleport_data': self.teleport_data.to_json(),
            'tire_interaction_data': self.tire_interaction_data.to_json(),
            'peanut_gun_data': self.peanut_gun_data.to_json(),
            'crouch_data': self.crouch_data.to_json(),
            'fire_reaction': self.fire_reaction.to_json(),
            'crush_data': self.crush_data.to_json(),
            'multi_kill_reward_data': self.multi_kill_reward_data.to_json(),
            'rise_from_the_grave_data': self.rise_from_the_grave_data.to_json(),
            'terrain_alignment_data': self.terrain_alignment_data.to_json(),
            'shield_data': self.shield_data.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3c38498d: ('common', PlayerCommonData.from_stream),
    0x7fb7e8b1: ('basic_movement', PlayerBasicMovementData.from_stream),
    0xf07bec6d: ('jump_data', PlayerJumpData.from_stream),
    0xf3d8dcb1: ('jump_animation_weights', PlayerJumpAnimWeights.from_stream),
    0x5e1168ac: ('jump_bop_animation_thresholds', PlayerBopAnimThresholds.from_stream),
    0x5d89056a: ('spline_advancement', PlayerSplineAdvancementData.from_stream),
    0xe03287ae: ('rambi_controller_data', RambiControllerData.from_stream),
    0x9f1ef2f3: ('attachments_data', PlayerAttachmentsData.from_stream),
    0xbbca7365: ('barrel_cannon_data', PlayerBarrelCannonData.from_stream),
    0xf9b150fc: ('cling2_data', PlayerCling2Data.from_stream),
    0x856f56a7: ('kong_ground_pound_data', KongGroundPoundData.from_stream),
    0xf5e908d1: ('kong_cling_slap_data', KongGroundPoundData.from_stream),
    0x36453107: ('kong_running_slap_data', KongRunningSlapData.from_stream),
    0xf7878a5a: ('kong_swing_data', KongSwingData.from_stream),
    0x60c43eaf: ('kong_slide_data', KongSlideData.from_stream),
    0xe38134fc: ('kong_stalled_descent_data', KongStalledDescentData.from_stream),
    0x75586c2b: ('kong_grab_data', KongGrabData.from_stream),
    0x4d6c99eb: ('head_tracking_data', PlayerHeadTrackingData.from_stream),
    0xf2b15344: ('melee_data', PlayerMeleeData.from_stream),
    0x978e5bd8: ('mount_data', PlayerMountData.from_stream),
    0x7f681411: ('rider_list_data', PlayerMountRiderList.from_stream),
    0x249dc50a: ('periodic_additive_animation_data', PlayerPeriodicAdditiveAnimationData.from_stream),
    0x29c83997: ('slave_data', PlayerSlaveData.from_stream),
    0x74b21331: ('offscreen_data', PlayerOffscreenIndicator.from_stream),
    0xc3260ca9: ('tar_interaction_data', PlayerTarInteractionData.from_stream),
    0xa7117cdd: ('teleport_data', PlayerTeleportData.from_stream),
    0xe31814db: ('tire_interaction_data', PlayerTireInteractionData.from_stream),
    0x8870d3dd: ('peanut_gun_data', PlayerPeanutGunData.from_stream),
    0x2d712fbe: ('crouch_data', PlayerCrouchData.from_stream),
    0xfa1f4263: ('fire_reaction', PlayerFireReactionData.from_stream),
    0x8abb25c4: ('crush_data', PlayerCrushData.from_stream),
    0x98efc863: ('multi_kill_reward_data', PlayerMultiKillRewardData.from_stream),
    0x39b0b057: ('rise_from_the_grave_data', PlayerRiseFromTheGraveData.from_stream),
    0x1bd6769f: ('terrain_alignment_data', PlayerTerrainAlignmentData.from_stream),
    0xb2d0a449: ('shield_data', PlayerShieldData.from_stream),
}

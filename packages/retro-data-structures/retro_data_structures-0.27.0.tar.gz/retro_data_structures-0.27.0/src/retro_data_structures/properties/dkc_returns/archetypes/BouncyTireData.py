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
from retro_data_structures.properties.dkc_returns.archetypes.BouncyTireJumpHeights import BouncyTireJumpHeights
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class BouncyTireDataJson(typing_extensions.TypedDict):
        animation: json_util.JsonObject
        idle_animation: int
        spring_animation: int
        left_jiggle_animation: int
        right_jiggle_animation: int
        bounce_height: float
        normal_jump_heights: json_util.JsonObject
        tar_inhibited_jump_heights: json_util.JsonObject
        high_jump_max_velocity_x: float
        mass: float
        rider_stop_speed_threshold: float
        bounce_detection_angle: float
        bounce_sound_effect: int
        jump_sound_effect: int
        collision_model: int
        is_stationary: bool
        should_cancel_players_momentum: bool
        unknown_0x592fc47e: bool
        should_absorb_shadows: bool
        unknown_0x9d837da5: bool
        air_control_disabled_duration_on_low_bounce: float
        air_control_disabled_duration_on_high_bounce: float
        air_control_scalar_on_high_bounce: float
        air_control_scalar_on_low_bounce: float
    

@dataclasses.dataclass()
class BouncyTireData(BaseProperty):
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa3d63f44, original_name='Animation', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    idle_animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xa2a5b38f, original_name='IdleAnimation'
        ),
    })
    spring_animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x0d584a11, original_name='SpringAnimation'
        ),
    })
    left_jiggle_animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xcb1931f5, original_name='LeftJiggleAnimation'
        ),
    })
    right_jiggle_animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6462907a, original_name='RightJiggleAnimation'
        ),
    })
    bounce_height: float = dataclasses.field(default=3.140199899673462, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f524fd4, original_name='BounceHeight'
        ),
    })
    normal_jump_heights: BouncyTireJumpHeights = dataclasses.field(default_factory=BouncyTireJumpHeights, metadata={
        'reflection': FieldReflection[BouncyTireJumpHeights](
            BouncyTireJumpHeights, id=0x19287737, original_name='NormalJumpHeights', from_json=BouncyTireJumpHeights.from_json, to_json=BouncyTireJumpHeights.to_json
        ),
    })
    tar_inhibited_jump_heights: BouncyTireJumpHeights = dataclasses.field(default_factory=BouncyTireJumpHeights, metadata={
        'reflection': FieldReflection[BouncyTireJumpHeights](
            BouncyTireJumpHeights, id=0x6a3afc9e, original_name='TarInhibitedJumpHeights', from_json=BouncyTireJumpHeights.from_json, to_json=BouncyTireJumpHeights.to_json
        ),
    })
    high_jump_max_velocity_x: float = dataclasses.field(default=9.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x83a5293a, original_name='HighJumpMaxVelocityX'
        ),
    })
    mass: float = dataclasses.field(default=80.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x75dbb375, original_name='Mass'
        ),
    })
    rider_stop_speed_threshold: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4f6a5403, original_name='RiderStopSpeedThreshold'
        ),
    })
    bounce_detection_angle: float = dataclasses.field(default=45.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa8e46ea2, original_name='BounceDetectionAngle'
        ),
    })
    bounce_sound_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x69156fbe, original_name='BounceSoundEffect'
        ),
    })
    jump_sound_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc00904c2, original_name='JumpSoundEffect'
        ),
    })
    collision_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['DCLN'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0fc966dc, original_name='CollisionModel'
        ),
    })
    is_stationary: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xab2e56f4, original_name='IsStationary'
        ),
    })
    should_cancel_players_momentum: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x74920e0e, original_name='ShouldCancelPlayersMomentum'
        ),
    })
    unknown_0x592fc47e: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x592fc47e, original_name='Unknown'
        ),
    })
    should_absorb_shadows: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x82d11331, original_name='ShouldAbsorbShadows'
        ),
    })
    unknown_0x9d837da5: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9d837da5, original_name='Unknown'
        ),
    })
    air_control_disabled_duration_on_low_bounce: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3d04e592, original_name='AirControlDisabledDurationOnLowBounce'
        ),
    })
    air_control_disabled_duration_on_high_bounce: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3595d977, original_name='AirControlDisabledDurationOnHighBounce'
        ),
    })
    air_control_scalar_on_high_bounce: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd5505ea4, original_name='AirControlScalarOnHighBounce'
        ),
    })
    air_control_scalar_on_low_bounce: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d6a2898, original_name='AirControlScalarOnLowBounce'
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
        if property_count != 24:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa3d63f44
        animation = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa2a5b38f
        idle_animation = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0d584a11
        spring_animation = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcb1931f5
        left_jiggle_animation = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6462907a
        right_jiggle_animation = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f524fd4
        bounce_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x19287737
        normal_jump_heights = BouncyTireJumpHeights.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a3afc9e
        tar_inhibited_jump_heights = BouncyTireJumpHeights.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x83a5293a
        high_jump_max_velocity_x = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x75dbb375
        mass = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4f6a5403
        rider_stop_speed_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa8e46ea2
        bounce_detection_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x69156fbe
        bounce_sound_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc00904c2
        jump_sound_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0fc966dc
        collision_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab2e56f4
        is_stationary = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x74920e0e
        should_cancel_players_momentum = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x592fc47e
        unknown_0x592fc47e = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82d11331
        should_absorb_shadows = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9d837da5
        unknown_0x9d837da5 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3d04e592
        air_control_disabled_duration_on_low_bounce = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3595d977
        air_control_disabled_duration_on_high_bounce = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd5505ea4
        air_control_scalar_on_high_bounce = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2d6a2898
        air_control_scalar_on_low_bounce = struct.unpack('>f', data.read(4))[0]
    
        return cls(animation, idle_animation, spring_animation, left_jiggle_animation, right_jiggle_animation, bounce_height, normal_jump_heights, tar_inhibited_jump_heights, high_jump_max_velocity_x, mass, rider_stop_speed_threshold, bounce_detection_angle, bounce_sound_effect, jump_sound_effect, collision_model, is_stationary, should_cancel_players_momentum, unknown_0x592fc47e, should_absorb_shadows, unknown_0x9d837da5, air_control_disabled_duration_on_low_bounce, air_control_disabled_duration_on_high_bounce, air_control_scalar_on_high_bounce, air_control_scalar_on_low_bounce)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\xa5\xb3\x8f')  # 0xa2a5b38f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.idle_animation))

        data.write(b'\rXJ\x11')  # 0xd584a11
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.spring_animation))

        data.write(b'\xcb\x191\xf5')  # 0xcb1931f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.left_jiggle_animation))

        data.write(b'db\x90z')  # 0x6462907a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.right_jiggle_animation))

        data.write(b'/RO\xd4')  # 0x2f524fd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_height))

        data.write(b'\x19(w7')  # 0x19287737
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_jump_heights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j:\xfc\x9e')  # 0x6a3afc9e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar_inhibited_jump_heights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83\xa5):')  # 0x83a5293a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.high_jump_max_velocity_x))

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'OjT\x03')  # 0x4f6a5403
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rider_stop_speed_threshold))

        data.write(b'\xa8\xe4n\xa2')  # 0xa8e46ea2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_detection_angle))

        data.write(b'i\x15o\xbe')  # 0x69156fbe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_sound_effect))

        data.write(b'\xc0\t\x04\xc2')  # 0xc00904c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jump_sound_effect))

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'\xab.V\xf4')  # 0xab2e56f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_stationary))

        data.write(b't\x92\x0e\x0e')  # 0x74920e0e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_cancel_players_momentum))

        data.write(b'Y/\xc4~')  # 0x592fc47e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x592fc47e))

        data.write(b'\x82\xd1\x131')  # 0x82d11331
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_absorb_shadows))

        data.write(b'\x9d\x83}\xa5')  # 0x9d837da5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9d837da5))

        data.write(b'=\x04\xe5\x92')  # 0x3d04e592
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_disabled_duration_on_low_bounce))

        data.write(b'5\x95\xd9w')  # 0x3595d977
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_disabled_duration_on_high_bounce))

        data.write(b'\xd5P^\xa4')  # 0xd5505ea4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_scalar_on_high_bounce))

        data.write(b'-j(\x98')  # 0x2d6a2898
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_scalar_on_low_bounce))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BouncyTireDataJson", data)
        return cls(
            animation=AnimationParameters.from_json(json_data['animation']),
            idle_animation=json_data['idle_animation'],
            spring_animation=json_data['spring_animation'],
            left_jiggle_animation=json_data['left_jiggle_animation'],
            right_jiggle_animation=json_data['right_jiggle_animation'],
            bounce_height=json_data['bounce_height'],
            normal_jump_heights=BouncyTireJumpHeights.from_json(json_data['normal_jump_heights']),
            tar_inhibited_jump_heights=BouncyTireJumpHeights.from_json(json_data['tar_inhibited_jump_heights']),
            high_jump_max_velocity_x=json_data['high_jump_max_velocity_x'],
            mass=json_data['mass'],
            rider_stop_speed_threshold=json_data['rider_stop_speed_threshold'],
            bounce_detection_angle=json_data['bounce_detection_angle'],
            bounce_sound_effect=json_data['bounce_sound_effect'],
            jump_sound_effect=json_data['jump_sound_effect'],
            collision_model=json_data['collision_model'],
            is_stationary=json_data['is_stationary'],
            should_cancel_players_momentum=json_data['should_cancel_players_momentum'],
            unknown_0x592fc47e=json_data['unknown_0x592fc47e'],
            should_absorb_shadows=json_data['should_absorb_shadows'],
            unknown_0x9d837da5=json_data['unknown_0x9d837da5'],
            air_control_disabled_duration_on_low_bounce=json_data['air_control_disabled_duration_on_low_bounce'],
            air_control_disabled_duration_on_high_bounce=json_data['air_control_disabled_duration_on_high_bounce'],
            air_control_scalar_on_high_bounce=json_data['air_control_scalar_on_high_bounce'],
            air_control_scalar_on_low_bounce=json_data['air_control_scalar_on_low_bounce'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'animation': self.animation.to_json(),
            'idle_animation': self.idle_animation,
            'spring_animation': self.spring_animation,
            'left_jiggle_animation': self.left_jiggle_animation,
            'right_jiggle_animation': self.right_jiggle_animation,
            'bounce_height': self.bounce_height,
            'normal_jump_heights': self.normal_jump_heights.to_json(),
            'tar_inhibited_jump_heights': self.tar_inhibited_jump_heights.to_json(),
            'high_jump_max_velocity_x': self.high_jump_max_velocity_x,
            'mass': self.mass,
            'rider_stop_speed_threshold': self.rider_stop_speed_threshold,
            'bounce_detection_angle': self.bounce_detection_angle,
            'bounce_sound_effect': self.bounce_sound_effect,
            'jump_sound_effect': self.jump_sound_effect,
            'collision_model': self.collision_model,
            'is_stationary': self.is_stationary,
            'should_cancel_players_momentum': self.should_cancel_players_momentum,
            'unknown_0x592fc47e': self.unknown_0x592fc47e,
            'should_absorb_shadows': self.should_absorb_shadows,
            'unknown_0x9d837da5': self.unknown_0x9d837da5,
            'air_control_disabled_duration_on_low_bounce': self.air_control_disabled_duration_on_low_bounce,
            'air_control_disabled_duration_on_high_bounce': self.air_control_disabled_duration_on_high_bounce,
            'air_control_scalar_on_high_bounce': self.air_control_scalar_on_high_bounce,
            'air_control_scalar_on_low_bounce': self.air_control_scalar_on_low_bounce,
        }


def _decode_idle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spring_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_left_jiggle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_right_jiggle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bounce_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_high_jump_max_velocity_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rider_stop_speed_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_jump_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_is_stationary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_should_cancel_players_momentum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x592fc47e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_should_absorb_shadows(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x9d837da5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_air_control_disabled_duration_on_low_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_control_disabled_duration_on_high_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_control_scalar_on_high_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_control_scalar_on_low_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa3d63f44: ('animation', AnimationParameters.from_stream),
    0xa2a5b38f: ('idle_animation', _decode_idle_animation),
    0xd584a11: ('spring_animation', _decode_spring_animation),
    0xcb1931f5: ('left_jiggle_animation', _decode_left_jiggle_animation),
    0x6462907a: ('right_jiggle_animation', _decode_right_jiggle_animation),
    0x2f524fd4: ('bounce_height', _decode_bounce_height),
    0x19287737: ('normal_jump_heights', BouncyTireJumpHeights.from_stream),
    0x6a3afc9e: ('tar_inhibited_jump_heights', BouncyTireJumpHeights.from_stream),
    0x83a5293a: ('high_jump_max_velocity_x', _decode_high_jump_max_velocity_x),
    0x75dbb375: ('mass', _decode_mass),
    0x4f6a5403: ('rider_stop_speed_threshold', _decode_rider_stop_speed_threshold),
    0xa8e46ea2: ('bounce_detection_angle', _decode_bounce_detection_angle),
    0x69156fbe: ('bounce_sound_effect', _decode_bounce_sound_effect),
    0xc00904c2: ('jump_sound_effect', _decode_jump_sound_effect),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xab2e56f4: ('is_stationary', _decode_is_stationary),
    0x74920e0e: ('should_cancel_players_momentum', _decode_should_cancel_players_momentum),
    0x592fc47e: ('unknown_0x592fc47e', _decode_unknown_0x592fc47e),
    0x82d11331: ('should_absorb_shadows', _decode_should_absorb_shadows),
    0x9d837da5: ('unknown_0x9d837da5', _decode_unknown_0x9d837da5),
    0x3d04e592: ('air_control_disabled_duration_on_low_bounce', _decode_air_control_disabled_duration_on_low_bounce),
    0x3595d977: ('air_control_disabled_duration_on_high_bounce', _decode_air_control_disabled_duration_on_high_bounce),
    0xd5505ea4: ('air_control_scalar_on_high_bounce', _decode_air_control_scalar_on_high_bounce),
    0x2d6a2898: ('air_control_scalar_on_low_bounce', _decode_air_control_scalar_on_low_bounce),
}

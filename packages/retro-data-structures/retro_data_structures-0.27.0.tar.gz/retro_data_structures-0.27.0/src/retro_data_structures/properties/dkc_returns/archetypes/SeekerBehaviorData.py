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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class SeekerBehaviorDataJson(typing_extensions.TypedDict):
        mode: int
        seek_when_behavior_inactive: bool
        attack_range_squared: float
        speed: float
        acceleration: float
        deceleration: float
        turn_speed_radians: float
        hover_speed_threshold: float
        ignore_all_but_player: bool
        ignore_all_during_death: bool
        suicide_on_player_touch: bool
        disable_collision_time_after_creation: float
        life_time: float
        max_distance_from_origin_squared: float
        targeting_time: float
        telegraph_time: float
        pause_time: float
        stop_distance_squared: float
        stop_speed: float
        flight_sound: int
        flight_sound_low_pass_filter: json_util.JsonObject
        flight_sound_pitch: json_util.JsonObject
        flight_sound_volume: json_util.JsonObject
        maximum_speed_for_audio_inverse: float
        flight_sound_deceleration_k: float
    

@dataclasses.dataclass()
class SeekerBehaviorData(BaseProperty):
    mode: int = dataclasses.field(default=3821732504, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb8f60f9a, original_name='Mode'
        ),
    })  # Choice
    seek_when_behavior_inactive: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x745a8f03, original_name='SeekWhenBehaviorInactive'
        ),
    })
    attack_range_squared: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xde5bfc61, original_name='AttackRangeSquared'
        ),
    })
    speed: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6392404e, original_name='Speed'
        ),
    })
    acceleration: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39fb7978, original_name='Acceleration'
        ),
    })
    deceleration: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9ec4fc10, original_name='Deceleration'
        ),
    })
    turn_speed_radians: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x589a76ff, original_name='TurnSpeedRadians'
        ),
    })
    hover_speed_threshold: float = dataclasses.field(default=0.30000001192092896, metadata={
        'reflection': FieldReflection[float](
            float, id=0x332b5518, original_name='HoverSpeedThreshold'
        ),
    })
    ignore_all_but_player: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xab0f5158, original_name='IgnoreAllButPlayer'
        ),
    })
    ignore_all_during_death: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x884973d2, original_name='IgnoreAllDuringDeath'
        ),
    })
    suicide_on_player_touch: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbac80e1f, original_name='SuicideOnPlayerTouch'
        ),
    })
    disable_collision_time_after_creation: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbec99005, original_name='DisableCollisionTimeAfterCreation'
        ),
    })
    life_time: float = dataclasses.field(default=120.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb02de555, original_name='LifeTime'
        ),
    })
    max_distance_from_origin_squared: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0928580f, original_name='MaxDistanceFromOriginSquared'
        ),
    })
    targeting_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd94c3954, original_name='TargetingTime'
        ),
    })
    telegraph_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8e6bbef1, original_name='TelegraphTime'
        ),
    })
    pause_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6b08f2f2, original_name='PauseTime'
        ),
    })
    stop_distance_squared: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x48b45911, original_name='StopDistanceSquared'
        ),
    })
    stop_speed: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd4600821, original_name='StopSpeed'
        ),
    })
    flight_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe1e66b24, original_name='FlightSound'
        ),
    })
    flight_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xb413c45f, original_name='FlightSoundLowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    flight_sound_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x76c7464c, original_name='FlightSoundPitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    flight_sound_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x10e05aaf, original_name='FlightSoundVolume', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    maximum_speed_for_audio_inverse: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbda0b3f2, original_name='MaximumSpeedForAudioInverse'
        ),
    })
    flight_sound_deceleration_k: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7a7df6e3, original_name='FlightSoundDecelerationK'
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
        if property_count != 25:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb8f60f9a
        mode = struct.unpack(">L", data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x745a8f03
        seek_when_behavior_inactive = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xde5bfc61
        attack_range_squared = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6392404e
        speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x39fb7978
        acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ec4fc10
        deceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x589a76ff
        turn_speed_radians = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x332b5518
        hover_speed_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab0f5158
        ignore_all_but_player = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x884973d2
        ignore_all_during_death = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbac80e1f
        suicide_on_player_touch = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbec99005
        disable_collision_time_after_creation = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb02de555
        life_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0928580f
        max_distance_from_origin_squared = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd94c3954
        targeting_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8e6bbef1
        telegraph_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b08f2f2
        pause_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x48b45911
        stop_distance_squared = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd4600821
        stop_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe1e66b24
        flight_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb413c45f
        flight_sound_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76c7464c
        flight_sound_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x10e05aaf
        flight_sound_volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbda0b3f2
        maximum_speed_for_audio_inverse = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7a7df6e3
        flight_sound_deceleration_k = struct.unpack('>f', data.read(4))[0]
    
        return cls(mode, seek_when_behavior_inactive, attack_range_squared, speed, acceleration, deceleration, turn_speed_radians, hover_speed_threshold, ignore_all_but_player, ignore_all_during_death, suicide_on_player_touch, disable_collision_time_after_creation, life_time, max_distance_from_origin_squared, targeting_time, telegraph_time, pause_time, stop_distance_squared, stop_speed, flight_sound, flight_sound_low_pass_filter, flight_sound_pitch, flight_sound_volume, maximum_speed_for_audio_inverse, flight_sound_deceleration_k)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mode))

        data.write(b'tZ\x8f\x03')  # 0x745a8f03
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.seek_when_behavior_inactive))

        data.write(b'\xde[\xfca')  # 0xde5bfc61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range_squared))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'X\x9av\xff')  # 0x589a76ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed_radians))

        data.write(b'3+U\x18')  # 0x332b5518
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_speed_threshold))

        data.write(b'\xab\x0fQX')  # 0xab0f5158
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_all_but_player))

        data.write(b'\x88Is\xd2')  # 0x884973d2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_all_during_death))

        data.write(b'\xba\xc8\x0e\x1f')  # 0xbac80e1f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.suicide_on_player_touch))

        data.write(b'\xbe\xc9\x90\x05')  # 0xbec99005
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_collision_time_after_creation))

        data.write(b'\xb0-\xe5U')  # 0xb02de555
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.life_time))

        data.write(b'\t(X\x0f')  # 0x928580f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_distance_from_origin_squared))

        data.write(b'\xd9L9T')  # 0xd94c3954
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.targeting_time))

        data.write(b'\x8ek\xbe\xf1')  # 0x8e6bbef1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.telegraph_time))

        data.write(b'k\x08\xf2\xf2')  # 0x6b08f2f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause_time))

        data.write(b'H\xb4Y\x11')  # 0x48b45911
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_distance_squared))

        data.write(b'\xd4`\x08!')  # 0xd4600821
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_speed))

        data.write(b'\xe1\xe6k$')  # 0xe1e66b24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flight_sound))

        data.write(b'\xb4\x13\xc4_')  # 0xb413c45f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xc7FL')  # 0x76c7464c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\xe0Z\xaf')  # 0x10e05aaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\xa0\xb3\xf2')  # 0xbda0b3f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed_for_audio_inverse))

        data.write(b'z}\xf6\xe3')  # 0x7a7df6e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_sound_deceleration_k))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SeekerBehaviorDataJson", data)
        return cls(
            mode=json_data['mode'],
            seek_when_behavior_inactive=json_data['seek_when_behavior_inactive'],
            attack_range_squared=json_data['attack_range_squared'],
            speed=json_data['speed'],
            acceleration=json_data['acceleration'],
            deceleration=json_data['deceleration'],
            turn_speed_radians=json_data['turn_speed_radians'],
            hover_speed_threshold=json_data['hover_speed_threshold'],
            ignore_all_but_player=json_data['ignore_all_but_player'],
            ignore_all_during_death=json_data['ignore_all_during_death'],
            suicide_on_player_touch=json_data['suicide_on_player_touch'],
            disable_collision_time_after_creation=json_data['disable_collision_time_after_creation'],
            life_time=json_data['life_time'],
            max_distance_from_origin_squared=json_data['max_distance_from_origin_squared'],
            targeting_time=json_data['targeting_time'],
            telegraph_time=json_data['telegraph_time'],
            pause_time=json_data['pause_time'],
            stop_distance_squared=json_data['stop_distance_squared'],
            stop_speed=json_data['stop_speed'],
            flight_sound=json_data['flight_sound'],
            flight_sound_low_pass_filter=Spline.from_json(json_data['flight_sound_low_pass_filter']),
            flight_sound_pitch=Spline.from_json(json_data['flight_sound_pitch']),
            flight_sound_volume=Spline.from_json(json_data['flight_sound_volume']),
            maximum_speed_for_audio_inverse=json_data['maximum_speed_for_audio_inverse'],
            flight_sound_deceleration_k=json_data['flight_sound_deceleration_k'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'mode': self.mode,
            'seek_when_behavior_inactive': self.seek_when_behavior_inactive,
            'attack_range_squared': self.attack_range_squared,
            'speed': self.speed,
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'turn_speed_radians': self.turn_speed_radians,
            'hover_speed_threshold': self.hover_speed_threshold,
            'ignore_all_but_player': self.ignore_all_but_player,
            'ignore_all_during_death': self.ignore_all_during_death,
            'suicide_on_player_touch': self.suicide_on_player_touch,
            'disable_collision_time_after_creation': self.disable_collision_time_after_creation,
            'life_time': self.life_time,
            'max_distance_from_origin_squared': self.max_distance_from_origin_squared,
            'targeting_time': self.targeting_time,
            'telegraph_time': self.telegraph_time,
            'pause_time': self.pause_time,
            'stop_distance_squared': self.stop_distance_squared,
            'stop_speed': self.stop_speed,
            'flight_sound': self.flight_sound,
            'flight_sound_low_pass_filter': self.flight_sound_low_pass_filter.to_json(),
            'flight_sound_pitch': self.flight_sound_pitch.to_json(),
            'flight_sound_volume': self.flight_sound_volume.to_json(),
            'maximum_speed_for_audio_inverse': self.maximum_speed_for_audio_inverse,
            'flight_sound_deceleration_k': self.flight_sound_deceleration_k,
        }


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_seek_when_behavior_inactive(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_attack_range_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed_radians(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_speed_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_all_but_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_all_during_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_suicide_on_player_touch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_collision_time_after_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_distance_from_origin_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_targeting_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_telegraph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pause_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stop_distance_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stop_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_maximum_speed_for_audio_inverse(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound_deceleration_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb8f60f9a: ('mode', _decode_mode),
    0x745a8f03: ('seek_when_behavior_inactive', _decode_seek_when_behavior_inactive),
    0xde5bfc61: ('attack_range_squared', _decode_attack_range_squared),
    0x6392404e: ('speed', _decode_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x589a76ff: ('turn_speed_radians', _decode_turn_speed_radians),
    0x332b5518: ('hover_speed_threshold', _decode_hover_speed_threshold),
    0xab0f5158: ('ignore_all_but_player', _decode_ignore_all_but_player),
    0x884973d2: ('ignore_all_during_death', _decode_ignore_all_during_death),
    0xbac80e1f: ('suicide_on_player_touch', _decode_suicide_on_player_touch),
    0xbec99005: ('disable_collision_time_after_creation', _decode_disable_collision_time_after_creation),
    0xb02de555: ('life_time', _decode_life_time),
    0x928580f: ('max_distance_from_origin_squared', _decode_max_distance_from_origin_squared),
    0xd94c3954: ('targeting_time', _decode_targeting_time),
    0x8e6bbef1: ('telegraph_time', _decode_telegraph_time),
    0x6b08f2f2: ('pause_time', _decode_pause_time),
    0x48b45911: ('stop_distance_squared', _decode_stop_distance_squared),
    0xd4600821: ('stop_speed', _decode_stop_speed),
    0xe1e66b24: ('flight_sound', _decode_flight_sound),
    0xb413c45f: ('flight_sound_low_pass_filter', Spline.from_stream),
    0x76c7464c: ('flight_sound_pitch', Spline.from_stream),
    0x10e05aaf: ('flight_sound_volume', Spline.from_stream),
    0xbda0b3f2: ('maximum_speed_for_audio_inverse', _decode_maximum_speed_for_audio_inverse),
    0x7a7df6e3: ('flight_sound_deceleration_k', _decode_flight_sound_deceleration_k),
}

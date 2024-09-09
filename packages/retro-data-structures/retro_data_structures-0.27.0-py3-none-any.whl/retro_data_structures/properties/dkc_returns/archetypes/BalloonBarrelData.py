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
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class BalloonBarrelDataJson(typing_extensions.TypedDict):
        balloon_character: json_util.JsonObject
        balloon_attach_locator: str
        barrel_attach_locator: str
        downward_velocity: float
        shake_animation_repeat_time: float
        min_horizontal_motion_time: float
        max_horizontal_motion_time: float
        min_horizontal_motion_velocity: float
        max_horizontal_motion_velocity: float
        horizontal_motion_acceleration: float
        seek_downward_velocity: float
        seek_mode_chase_rate: float
        seek_minimum_chase_velocity: float
        shake_input_stop_time: float
        shake_input_resume_time: float
        shake_input_time: float
        shake_input_speed: json_util.JsonObject
        shake_input_target_height_adjust: float
        gravity_multiplier: float
        extra_downward_collision: float
        start_offset: float
        below_screen_offset: float
        texture_set: int
        pop_effect: int
        pop_sound: int
        shake_sound: int
        offscreen_disappear_sound: int
    

@dataclasses.dataclass()
class BalloonBarrelData(BaseProperty):
    balloon_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xf8b3abe0, original_name='BalloonCharacter', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    balloon_attach_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x82de5e29, original_name='BalloonAttachLocator'
        ),
    })
    barrel_attach_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x1644af87, original_name='BarrelAttachLocator'
        ),
    })
    downward_velocity: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xddb16979, original_name='DownwardVelocity'
        ),
    })
    shake_animation_repeat_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2b201845, original_name='ShakeAnimationRepeatTime'
        ),
    })
    min_horizontal_motion_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbf75e71f, original_name='MinHorizontalMotionTime'
        ),
    })
    max_horizontal_motion_time: float = dataclasses.field(default=2.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe87bb75c, original_name='MaxHorizontalMotionTime'
        ),
    })
    min_horizontal_motion_velocity: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9545f9ef, original_name='MinHorizontalMotionVelocity'
        ),
    })
    max_horizontal_motion_velocity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1bd4c955, original_name='MaxHorizontalMotionVelocity'
        ),
    })
    horizontal_motion_acceleration: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x64acdf7b, original_name='HorizontalMotionAcceleration'
        ),
    })
    seek_downward_velocity: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcd6e33a5, original_name='SeekDownwardVelocity'
        ),
    })
    seek_mode_chase_rate: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc3cdafcb, original_name='SeekModeChaseRate'
        ),
    })
    seek_minimum_chase_velocity: float = dataclasses.field(default=2.200000047683716, metadata={
        'reflection': FieldReflection[float](
            float, id=0x88befdeb, original_name='SeekMinimumChaseVelocity'
        ),
    })
    shake_input_stop_time: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x228ee623, original_name='ShakeInputStopTime'
        ),
    })
    shake_input_resume_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7e31967c, original_name='ShakeInputResumeTime'
        ),
    })
    shake_input_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xdcb3f50e, original_name='ShakeInputTime'
        ),
    })
    shake_input_speed: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xbd917023, original_name='ShakeInputSpeed', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    shake_input_target_height_adjust: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7c8454bd, original_name='ShakeInputTargetHeightAdjust'
        ),
    })
    gravity_multiplier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42ac42ea, original_name='GravityMultiplier'
        ),
    })
    extra_downward_collision: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9a27ddc3, original_name='ExtraDownwardCollision'
        ),
    })
    start_offset: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x409618b6, original_name='StartOffset'
        ),
    })
    below_screen_offset: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0eefa478, original_name='BelowScreenOffset'
        ),
    })
    texture_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6b40acef, original_name='TextureSet'
        ),
    })
    pop_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2672e0bf, original_name='PopEffect'
        ),
    })
    pop_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe4cd14f9, original_name='PopSound'
        ),
    })
    shake_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1a422994, original_name='ShakeSound'
        ),
    })
    offscreen_disappear_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x59cd8dee, original_name='OffscreenDisappearSound'
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
        if property_count != 27:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf8b3abe0
        balloon_character = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82de5e29
        balloon_attach_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1644af87
        barrel_attach_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xddb16979
        downward_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2b201845
        shake_animation_repeat_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf75e71f
        min_horizontal_motion_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe87bb75c
        max_horizontal_motion_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9545f9ef
        min_horizontal_motion_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1bd4c955
        max_horizontal_motion_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x64acdf7b
        horizontal_motion_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcd6e33a5
        seek_downward_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc3cdafcb
        seek_mode_chase_rate = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x88befdeb
        seek_minimum_chase_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x228ee623
        shake_input_stop_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e31967c
        shake_input_resume_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdcb3f50e
        shake_input_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbd917023
        shake_input_speed = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c8454bd
        shake_input_target_height_adjust = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x42ac42ea
        gravity_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a27ddc3
        extra_downward_collision = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x409618b6
        start_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0eefa478
        below_screen_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b40acef
        texture_set = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2672e0bf
        pop_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe4cd14f9
        pop_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1a422994
        shake_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59cd8dee
        offscreen_disappear_sound = struct.unpack(">Q", data.read(8))[0]
    
        return cls(balloon_character, balloon_attach_locator, barrel_attach_locator, downward_velocity, shake_animation_repeat_time, min_horizontal_motion_time, max_horizontal_motion_time, min_horizontal_motion_velocity, max_horizontal_motion_velocity, horizontal_motion_acceleration, seek_downward_velocity, seek_mode_chase_rate, seek_minimum_chase_velocity, shake_input_stop_time, shake_input_resume_time, shake_input_time, shake_input_speed, shake_input_target_height_adjust, gravity_multiplier, extra_downward_collision, start_offset, below_screen_offset, texture_set, pop_effect, pop_sound, shake_sound, offscreen_disappear_sound)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'\xf8\xb3\xab\xe0')  # 0xf8b3abe0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balloon_character.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x82\xde^)')  # 0x82de5e29
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.balloon_attach_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16D\xaf\x87')  # 0x1644af87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.barrel_attach_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd\xb1iy')  # 0xddb16979
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.downward_velocity))

        data.write(b'+ \x18E')  # 0x2b201845
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shake_animation_repeat_time))

        data.write(b'\xbfu\xe7\x1f')  # 0xbf75e71f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_horizontal_motion_time))

        data.write(b'\xe8{\xb7\\')  # 0xe87bb75c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_horizontal_motion_time))

        data.write(b'\x95E\xf9\xef')  # 0x9545f9ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_horizontal_motion_velocity))

        data.write(b'\x1b\xd4\xc9U')  # 0x1bd4c955
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_horizontal_motion_velocity))

        data.write(b'd\xac\xdf{')  # 0x64acdf7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_motion_acceleration))

        data.write(b'\xcdn3\xa5')  # 0xcd6e33a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.seek_downward_velocity))

        data.write(b'\xc3\xcd\xaf\xcb')  # 0xc3cdafcb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.seek_mode_chase_rate))

        data.write(b'\x88\xbe\xfd\xeb')  # 0x88befdeb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.seek_minimum_chase_velocity))

        data.write(b'"\x8e\xe6#')  # 0x228ee623
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shake_input_stop_time))

        data.write(b'~1\x96|')  # 0x7e31967c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shake_input_resume_time))

        data.write(b'\xdc\xb3\xf5\x0e')  # 0xdcb3f50e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shake_input_time))

        data.write(b'\xbd\x91p#')  # 0xbd917023
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shake_input_speed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\x84T\xbd')  # 0x7c8454bd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shake_input_target_height_adjust))

        data.write(b'B\xacB\xea')  # 0x42ac42ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_multiplier))

        data.write(b"\x9a'\xdd\xc3")  # 0x9a27ddc3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.extra_downward_collision))

        data.write(b'@\x96\x18\xb6')  # 0x409618b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_offset))

        data.write(b'\x0e\xef\xa4x')  # 0xeefa478
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.below_screen_offset))

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'&r\xe0\xbf')  # 0x2672e0bf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pop_effect))

        data.write(b'\xe4\xcd\x14\xf9')  # 0xe4cd14f9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pop_sound))

        data.write(b'\x1aB)\x94')  # 0x1a422994
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shake_sound))

        data.write(b'Y\xcd\x8d\xee')  # 0x59cd8dee
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.offscreen_disappear_sound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BalloonBarrelDataJson", data)
        return cls(
            balloon_character=AnimationParameters.from_json(json_data['balloon_character']),
            balloon_attach_locator=json_data['balloon_attach_locator'],
            barrel_attach_locator=json_data['barrel_attach_locator'],
            downward_velocity=json_data['downward_velocity'],
            shake_animation_repeat_time=json_data['shake_animation_repeat_time'],
            min_horizontal_motion_time=json_data['min_horizontal_motion_time'],
            max_horizontal_motion_time=json_data['max_horizontal_motion_time'],
            min_horizontal_motion_velocity=json_data['min_horizontal_motion_velocity'],
            max_horizontal_motion_velocity=json_data['max_horizontal_motion_velocity'],
            horizontal_motion_acceleration=json_data['horizontal_motion_acceleration'],
            seek_downward_velocity=json_data['seek_downward_velocity'],
            seek_mode_chase_rate=json_data['seek_mode_chase_rate'],
            seek_minimum_chase_velocity=json_data['seek_minimum_chase_velocity'],
            shake_input_stop_time=json_data['shake_input_stop_time'],
            shake_input_resume_time=json_data['shake_input_resume_time'],
            shake_input_time=json_data['shake_input_time'],
            shake_input_speed=Spline.from_json(json_data['shake_input_speed']),
            shake_input_target_height_adjust=json_data['shake_input_target_height_adjust'],
            gravity_multiplier=json_data['gravity_multiplier'],
            extra_downward_collision=json_data['extra_downward_collision'],
            start_offset=json_data['start_offset'],
            below_screen_offset=json_data['below_screen_offset'],
            texture_set=json_data['texture_set'],
            pop_effect=json_data['pop_effect'],
            pop_sound=json_data['pop_sound'],
            shake_sound=json_data['shake_sound'],
            offscreen_disappear_sound=json_data['offscreen_disappear_sound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'balloon_character': self.balloon_character.to_json(),
            'balloon_attach_locator': self.balloon_attach_locator,
            'barrel_attach_locator': self.barrel_attach_locator,
            'downward_velocity': self.downward_velocity,
            'shake_animation_repeat_time': self.shake_animation_repeat_time,
            'min_horizontal_motion_time': self.min_horizontal_motion_time,
            'max_horizontal_motion_time': self.max_horizontal_motion_time,
            'min_horizontal_motion_velocity': self.min_horizontal_motion_velocity,
            'max_horizontal_motion_velocity': self.max_horizontal_motion_velocity,
            'horizontal_motion_acceleration': self.horizontal_motion_acceleration,
            'seek_downward_velocity': self.seek_downward_velocity,
            'seek_mode_chase_rate': self.seek_mode_chase_rate,
            'seek_minimum_chase_velocity': self.seek_minimum_chase_velocity,
            'shake_input_stop_time': self.shake_input_stop_time,
            'shake_input_resume_time': self.shake_input_resume_time,
            'shake_input_time': self.shake_input_time,
            'shake_input_speed': self.shake_input_speed.to_json(),
            'shake_input_target_height_adjust': self.shake_input_target_height_adjust,
            'gravity_multiplier': self.gravity_multiplier,
            'extra_downward_collision': self.extra_downward_collision,
            'start_offset': self.start_offset,
            'below_screen_offset': self.below_screen_offset,
            'texture_set': self.texture_set,
            'pop_effect': self.pop_effect,
            'pop_sound': self.pop_sound,
            'shake_sound': self.shake_sound,
            'offscreen_disappear_sound': self.offscreen_disappear_sound,
        }


def _decode_balloon_attach_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_barrel_attach_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_downward_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shake_animation_repeat_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_horizontal_motion_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_horizontal_motion_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_horizontal_motion_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_horizontal_motion_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_motion_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_seek_downward_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_seek_mode_chase_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_seek_minimum_chase_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shake_input_stop_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shake_input_resume_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shake_input_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shake_input_target_height_adjust(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_extra_downward_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_below_screen_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_pop_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_pop_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shake_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_offscreen_disappear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8b3abe0: ('balloon_character', AnimationParameters.from_stream),
    0x82de5e29: ('balloon_attach_locator', _decode_balloon_attach_locator),
    0x1644af87: ('barrel_attach_locator', _decode_barrel_attach_locator),
    0xddb16979: ('downward_velocity', _decode_downward_velocity),
    0x2b201845: ('shake_animation_repeat_time', _decode_shake_animation_repeat_time),
    0xbf75e71f: ('min_horizontal_motion_time', _decode_min_horizontal_motion_time),
    0xe87bb75c: ('max_horizontal_motion_time', _decode_max_horizontal_motion_time),
    0x9545f9ef: ('min_horizontal_motion_velocity', _decode_min_horizontal_motion_velocity),
    0x1bd4c955: ('max_horizontal_motion_velocity', _decode_max_horizontal_motion_velocity),
    0x64acdf7b: ('horizontal_motion_acceleration', _decode_horizontal_motion_acceleration),
    0xcd6e33a5: ('seek_downward_velocity', _decode_seek_downward_velocity),
    0xc3cdafcb: ('seek_mode_chase_rate', _decode_seek_mode_chase_rate),
    0x88befdeb: ('seek_minimum_chase_velocity', _decode_seek_minimum_chase_velocity),
    0x228ee623: ('shake_input_stop_time', _decode_shake_input_stop_time),
    0x7e31967c: ('shake_input_resume_time', _decode_shake_input_resume_time),
    0xdcb3f50e: ('shake_input_time', _decode_shake_input_time),
    0xbd917023: ('shake_input_speed', Spline.from_stream),
    0x7c8454bd: ('shake_input_target_height_adjust', _decode_shake_input_target_height_adjust),
    0x42ac42ea: ('gravity_multiplier', _decode_gravity_multiplier),
    0x9a27ddc3: ('extra_downward_collision', _decode_extra_downward_collision),
    0x409618b6: ('start_offset', _decode_start_offset),
    0xeefa478: ('below_screen_offset', _decode_below_screen_offset),
    0x6b40acef: ('texture_set', _decode_texture_set),
    0x2672e0bf: ('pop_effect', _decode_pop_effect),
    0xe4cd14f9: ('pop_sound', _decode_pop_sound),
    0x1a422994: ('shake_sound', _decode_shake_sound),
    0x59cd8dee: ('offscreen_disappear_sound', _decode_offscreen_disappear_sound),
}

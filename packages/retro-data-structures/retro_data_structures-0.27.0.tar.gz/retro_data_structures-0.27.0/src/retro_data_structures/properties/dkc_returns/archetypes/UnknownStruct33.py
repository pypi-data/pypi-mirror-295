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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct33Json(typing_extensions.TypedDict):
        rotates_about: int
        start_orientation: int
        idle_orientation: int
        rotational_acceleration: float
        max_rotational_velocity: float
        maximum_tilt: float
        maximum_tilt_right_threshold: float
        maximum_tilt_left_threshold: float
        balanced_threshold: float
        begin_tilt_damp_angle_threshold: float
        tilt_velocity_percentage: json_util.JsonObject
        begin_balanced_damp_angle_threshold: float
        balanced_velocity_percentage: json_util.JsonObject
        rotate_sound: int
        rotate_stop_balanced_sound: int
        rotate_stop_tilted_sound: int
        rotate_sound_ratio_change_factor: float
        rotate_sound_low_pass_filter: json_util.JsonObject
        rotate_sound_pitch: json_util.JsonObject
        rotate_sound_volume: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct33(BaseProperty):
    rotates_about: enums.RotatesAbout = dataclasses.field(default=enums.RotatesAbout.Unknown2, metadata={
        'reflection': FieldReflection[enums.RotatesAbout](
            enums.RotatesAbout, id=0x2f827982, original_name='RotatesAbout', from_json=enums.RotatesAbout.from_json, to_json=enums.RotatesAbout.to_json
        ),
    })
    start_orientation: enums.StartOrientation = dataclasses.field(default=enums.StartOrientation.Unknown1, metadata={
        'reflection': FieldReflection[enums.StartOrientation](
            enums.StartOrientation, id=0x74cecbeb, original_name='StartOrientation', from_json=enums.StartOrientation.from_json, to_json=enums.StartOrientation.to_json
        ),
    })
    idle_orientation: enums.IdleOrientation = dataclasses.field(default=enums.IdleOrientation.Unknown1, metadata={
        'reflection': FieldReflection[enums.IdleOrientation](
            enums.IdleOrientation, id=0x23a9add2, original_name='IdleOrientation', from_json=enums.IdleOrientation.from_json, to_json=enums.IdleOrientation.to_json
        ),
    })
    rotational_acceleration: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x48e58214, original_name='RotationalAcceleration'
        ),
    })
    max_rotational_velocity: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5de325e7, original_name='MaxRotationalVelocity'
        ),
    })
    maximum_tilt: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb14c9474, original_name='MaximumTilt'
        ),
    })
    maximum_tilt_right_threshold: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f1bebad, original_name='MaximumTiltRightThreshold'
        ),
    })
    maximum_tilt_left_threshold: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7f852bb9, original_name='MaximumTiltLeftThreshold'
        ),
    })
    balanced_threshold: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfafb3bfe, original_name='BalancedThreshold'
        ),
    })
    begin_tilt_damp_angle_threshold: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbe0f5bab, original_name='BeginTiltDampAngleThreshold'
        ),
    })
    tilt_velocity_percentage: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xaea70dd9, original_name='TiltVelocityPercentage', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    begin_balanced_damp_angle_threshold: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8abc25f2, original_name='BeginBalancedDampAngleThreshold'
        ),
    })
    balanced_velocity_percentage: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x59299e65, original_name='BalancedVelocityPercentage', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rotate_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd54a5bd8, original_name='RotateSound'
        ),
    })
    rotate_stop_balanced_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4b4818ee, original_name='RotateStopBalancedSound'
        ),
    })
    rotate_stop_tilted_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4a9b4299, original_name='RotateStopTiltedSound'
        ),
    })
    rotate_sound_ratio_change_factor: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2e2c202d, original_name='RotateSoundRatioChangeFactor'
        ),
    })
    rotate_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x15cc25fd, original_name='RotateSoundLowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rotate_sound_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x9169cc59, original_name='RotateSoundPitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rotate_sound_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x7dda10ce, original_name='RotateSoundVolume', from_json=Spline.from_json, to_json=Spline.to_json
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
        if property_count != 20:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f827982
        rotates_about = enums.RotatesAbout.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x74cecbeb
        start_orientation = enums.StartOrientation.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x23a9add2
        idle_orientation = enums.IdleOrientation.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x48e58214
        rotational_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5de325e7
        max_rotational_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb14c9474
        maximum_tilt = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f1bebad
        maximum_tilt_right_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f852bb9
        maximum_tilt_left_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfafb3bfe
        balanced_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbe0f5bab
        begin_tilt_damp_angle_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaea70dd9
        tilt_velocity_percentage = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8abc25f2
        begin_balanced_damp_angle_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59299e65
        balanced_velocity_percentage = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd54a5bd8
        rotate_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4b4818ee
        rotate_stop_balanced_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4a9b4299
        rotate_stop_tilted_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e2c202d
        rotate_sound_ratio_change_factor = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x15cc25fd
        rotate_sound_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9169cc59
        rotate_sound_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7dda10ce
        rotate_sound_volume = Spline.from_stream(data, property_size)
    
        return cls(rotates_about, start_orientation, idle_orientation, rotational_acceleration, max_rotational_velocity, maximum_tilt, maximum_tilt_right_threshold, maximum_tilt_left_threshold, balanced_threshold, begin_tilt_damp_angle_threshold, tilt_velocity_percentage, begin_balanced_damp_angle_threshold, balanced_velocity_percentage, rotate_sound, rotate_stop_balanced_sound, rotate_stop_tilted_sound, rotate_sound_ratio_change_factor, rotate_sound_low_pass_filter, rotate_sound_pitch, rotate_sound_volume)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'/\x82y\x82')  # 0x2f827982
        data.write(b'\x00\x04')  # size
        self.rotates_about.to_stream(data)

        data.write(b't\xce\xcb\xeb')  # 0x74cecbeb
        data.write(b'\x00\x04')  # size
        self.start_orientation.to_stream(data)

        data.write(b'#\xa9\xad\xd2')  # 0x23a9add2
        data.write(b'\x00\x04')  # size
        self.idle_orientation.to_stream(data)

        data.write(b'H\xe5\x82\x14')  # 0x48e58214
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotational_acceleration))

        data.write(b']\xe3%\xe7')  # 0x5de325e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_rotational_velocity))

        data.write(b'\xb1L\x94t')  # 0xb14c9474
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_tilt))

        data.write(b'/\x1b\xeb\xad')  # 0x2f1bebad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_tilt_right_threshold))

        data.write(b'\x7f\x85+\xb9')  # 0x7f852bb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_tilt_left_threshold))

        data.write(b'\xfa\xfb;\xfe')  # 0xfafb3bfe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.balanced_threshold))

        data.write(b'\xbe\x0f[\xab')  # 0xbe0f5bab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.begin_tilt_damp_angle_threshold))

        data.write(b'\xae\xa7\r\xd9')  # 0xaea70dd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tilt_velocity_percentage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8a\xbc%\xf2')  # 0x8abc25f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.begin_balanced_damp_angle_threshold))

        data.write(b'Y)\x9ee')  # 0x59299e65
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balanced_velocity_percentage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd5J[\xd8')  # 0xd54a5bd8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rotate_sound))

        data.write(b'KH\x18\xee')  # 0x4b4818ee
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rotate_stop_balanced_sound))

        data.write(b'J\x9bB\x99')  # 0x4a9b4299
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rotate_stop_tilted_sound))

        data.write(b'., -')  # 0x2e2c202d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotate_sound_ratio_change_factor))

        data.write(b'\x15\xcc%\xfd')  # 0x15cc25fd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotate_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91i\xccY')  # 0x9169cc59
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotate_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\xda\x10\xce')  # 0x7dda10ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotate_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct33Json", data)
        return cls(
            rotates_about=enums.RotatesAbout.from_json(json_data['rotates_about']),
            start_orientation=enums.StartOrientation.from_json(json_data['start_orientation']),
            idle_orientation=enums.IdleOrientation.from_json(json_data['idle_orientation']),
            rotational_acceleration=json_data['rotational_acceleration'],
            max_rotational_velocity=json_data['max_rotational_velocity'],
            maximum_tilt=json_data['maximum_tilt'],
            maximum_tilt_right_threshold=json_data['maximum_tilt_right_threshold'],
            maximum_tilt_left_threshold=json_data['maximum_tilt_left_threshold'],
            balanced_threshold=json_data['balanced_threshold'],
            begin_tilt_damp_angle_threshold=json_data['begin_tilt_damp_angle_threshold'],
            tilt_velocity_percentage=Spline.from_json(json_data['tilt_velocity_percentage']),
            begin_balanced_damp_angle_threshold=json_data['begin_balanced_damp_angle_threshold'],
            balanced_velocity_percentage=Spline.from_json(json_data['balanced_velocity_percentage']),
            rotate_sound=json_data['rotate_sound'],
            rotate_stop_balanced_sound=json_data['rotate_stop_balanced_sound'],
            rotate_stop_tilted_sound=json_data['rotate_stop_tilted_sound'],
            rotate_sound_ratio_change_factor=json_data['rotate_sound_ratio_change_factor'],
            rotate_sound_low_pass_filter=Spline.from_json(json_data['rotate_sound_low_pass_filter']),
            rotate_sound_pitch=Spline.from_json(json_data['rotate_sound_pitch']),
            rotate_sound_volume=Spline.from_json(json_data['rotate_sound_volume']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'rotates_about': self.rotates_about.to_json(),
            'start_orientation': self.start_orientation.to_json(),
            'idle_orientation': self.idle_orientation.to_json(),
            'rotational_acceleration': self.rotational_acceleration,
            'max_rotational_velocity': self.max_rotational_velocity,
            'maximum_tilt': self.maximum_tilt,
            'maximum_tilt_right_threshold': self.maximum_tilt_right_threshold,
            'maximum_tilt_left_threshold': self.maximum_tilt_left_threshold,
            'balanced_threshold': self.balanced_threshold,
            'begin_tilt_damp_angle_threshold': self.begin_tilt_damp_angle_threshold,
            'tilt_velocity_percentage': self.tilt_velocity_percentage.to_json(),
            'begin_balanced_damp_angle_threshold': self.begin_balanced_damp_angle_threshold,
            'balanced_velocity_percentage': self.balanced_velocity_percentage.to_json(),
            'rotate_sound': self.rotate_sound,
            'rotate_stop_balanced_sound': self.rotate_stop_balanced_sound,
            'rotate_stop_tilted_sound': self.rotate_stop_tilted_sound,
            'rotate_sound_ratio_change_factor': self.rotate_sound_ratio_change_factor,
            'rotate_sound_low_pass_filter': self.rotate_sound_low_pass_filter.to_json(),
            'rotate_sound_pitch': self.rotate_sound_pitch.to_json(),
            'rotate_sound_volume': self.rotate_sound_volume.to_json(),
        }


def _decode_rotates_about(data: typing.BinaryIO, property_size: int):
    return enums.RotatesAbout.from_stream(data)


def _decode_start_orientation(data: typing.BinaryIO, property_size: int):
    return enums.StartOrientation.from_stream(data)


def _decode_idle_orientation(data: typing.BinaryIO, property_size: int):
    return enums.IdleOrientation.from_stream(data)


def _decode_rotational_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_rotational_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_tilt(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_tilt_right_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_tilt_left_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_balanced_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_begin_tilt_damp_angle_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_begin_balanced_damp_angle_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotate_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rotate_stop_balanced_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rotate_stop_tilted_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rotate_sound_ratio_change_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2f827982: ('rotates_about', _decode_rotates_about),
    0x74cecbeb: ('start_orientation', _decode_start_orientation),
    0x23a9add2: ('idle_orientation', _decode_idle_orientation),
    0x48e58214: ('rotational_acceleration', _decode_rotational_acceleration),
    0x5de325e7: ('max_rotational_velocity', _decode_max_rotational_velocity),
    0xb14c9474: ('maximum_tilt', _decode_maximum_tilt),
    0x2f1bebad: ('maximum_tilt_right_threshold', _decode_maximum_tilt_right_threshold),
    0x7f852bb9: ('maximum_tilt_left_threshold', _decode_maximum_tilt_left_threshold),
    0xfafb3bfe: ('balanced_threshold', _decode_balanced_threshold),
    0xbe0f5bab: ('begin_tilt_damp_angle_threshold', _decode_begin_tilt_damp_angle_threshold),
    0xaea70dd9: ('tilt_velocity_percentage', Spline.from_stream),
    0x8abc25f2: ('begin_balanced_damp_angle_threshold', _decode_begin_balanced_damp_angle_threshold),
    0x59299e65: ('balanced_velocity_percentage', Spline.from_stream),
    0xd54a5bd8: ('rotate_sound', _decode_rotate_sound),
    0x4b4818ee: ('rotate_stop_balanced_sound', _decode_rotate_stop_balanced_sound),
    0x4a9b4299: ('rotate_stop_tilted_sound', _decode_rotate_stop_tilted_sound),
    0x2e2c202d: ('rotate_sound_ratio_change_factor', _decode_rotate_sound_ratio_change_factor),
    0x15cc25fd: ('rotate_sound_low_pass_filter', Spline.from_stream),
    0x9169cc59: ('rotate_sound_pitch', Spline.from_stream),
    0x7dda10ce: ('rotate_sound_volume', Spline.from_stream),
}

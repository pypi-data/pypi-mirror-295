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
from retro_data_structures.properties.dkc_returns.archetypes.MaterialSoundPair import MaterialSoundPair
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class KongSlideDataJson(typing_extensions.TypedDict):
        slope_detection_angle: float
        slide_no_jump_angle: float
        slide_detection_angle: float
        scramble_detection_angle: float
        scramble_speed: float
        tar_scramble_speed: float
        slide_breaking_speed: float
        max_slide_speed: float
        scramble_recovery_acceleration: float
        slide_speedup_acceleration: float
        slide_slowdown_acceleration: float
        planar_slide_recovery_speed: float
        slide_sound: int
        slide_sound_ratio_change_factor: float
        slide_sound_low_pass_filter: json_util.JsonObject
        slide_sound_pitch: json_util.JsonObject
        slide_sound_volume: json_util.JsonObject
        num_material_sounds: int
        material_sound0: json_util.JsonObject
        material_sound1: json_util.JsonObject
        material_sound2: json_util.JsonObject
        material_sound3: json_util.JsonObject
        material_sound4: json_util.JsonObject
        material_sound5: json_util.JsonObject
        material_sound6: json_util.JsonObject
        material_sound7: json_util.JsonObject
        material_sound8: json_util.JsonObject
        material_sound9: json_util.JsonObject
    

@dataclasses.dataclass()
class KongSlideData(BaseProperty):
    slope_detection_angle: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4e7def7e, original_name='SlopeDetectionAngle'
        ),
    })
    slide_no_jump_angle: float = dataclasses.field(default=70.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x18aa5c74, original_name='SlideNoJumpAngle'
        ),
    })
    slide_detection_angle: float = dataclasses.field(default=54.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6591a3a9, original_name='SlideDetectionAngle'
        ),
    })
    scramble_detection_angle: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8f7fdd6f, original_name='ScrambleDetectionAngle'
        ),
    })
    scramble_speed: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x43849900, original_name='ScrambleSpeed'
        ),
    })
    tar_scramble_speed: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8e7ea4fc, original_name='TarScrambleSpeed'
        ),
    })
    slide_breaking_speed: float = dataclasses.field(default=7.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8f3b9328, original_name='SlideBreakingSpeed'
        ),
    })
    max_slide_speed: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4c6ec511, original_name='MaxSlideSpeed'
        ),
    })
    scramble_recovery_acceleration: float = dataclasses.field(default=40.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7335084d, original_name='ScrambleRecoveryAcceleration'
        ),
    })
    slide_speedup_acceleration: float = dataclasses.field(default=40.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7600a6c5, original_name='SlideSpeedupAcceleration'
        ),
    })
    slide_slowdown_acceleration: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8f73e73d, original_name='SlideSlowdownAcceleration'
        ),
    })
    planar_slide_recovery_speed: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xce007890, original_name='PlanarSlideRecoverySpeed'
        ),
    })
    slide_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2b79ea93, original_name='SlideSound'
        ),
    })
    slide_sound_ratio_change_factor: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xba30aaca, original_name='SlideSoundRatioChangeFactor'
        ),
    })
    slide_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xd9ca50c2, original_name='SlideSoundLowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    slide_sound_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x84951ec7, original_name='SlideSoundPitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    slide_sound_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x6a78525f, original_name='SlideSoundVolume', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    num_material_sounds: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xd7c19141, original_name='NumMaterialSounds'
        ),
    })
    material_sound0: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0x576d9946, original_name='MaterialSound0', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound1: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0xb83f2fa7, original_name='MaterialSound1', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound2: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0x52b9f2c5, original_name='MaterialSound2', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound3: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0xbdeb4424, original_name='MaterialSound3', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound4: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0x5cc54e40, original_name='MaterialSound4', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound5: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0xb397f8a1, original_name='MaterialSound5', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound6: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0x591125c3, original_name='MaterialSound6', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound7: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0xb6439322, original_name='MaterialSound7', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound8: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0x403c374a, original_name='MaterialSound8', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
        ),
    })
    material_sound9: MaterialSoundPair = dataclasses.field(default_factory=MaterialSoundPair, metadata={
        'reflection': FieldReflection[MaterialSoundPair](
            MaterialSoundPair, id=0xaf6e81ab, original_name='MaterialSound9', from_json=MaterialSoundPair.from_json, to_json=MaterialSoundPair.to_json
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
        if property_count != 28:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4e7def7e
        slope_detection_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x18aa5c74
        slide_no_jump_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6591a3a9
        slide_detection_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f7fdd6f
        scramble_detection_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43849900
        scramble_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8e7ea4fc
        tar_scramble_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f3b9328
        slide_breaking_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4c6ec511
        max_slide_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7335084d
        scramble_recovery_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7600a6c5
        slide_speedup_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f73e73d
        slide_slowdown_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xce007890
        planar_slide_recovery_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2b79ea93
        slide_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xba30aaca
        slide_sound_ratio_change_factor = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9ca50c2
        slide_sound_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x84951ec7
        slide_sound_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a78525f
        slide_sound_volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd7c19141
        num_material_sounds = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x576d9946
        material_sound0 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb83f2fa7
        material_sound1 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x52b9f2c5
        material_sound2 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbdeb4424
        material_sound3 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5cc54e40
        material_sound4 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb397f8a1
        material_sound5 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x591125c3
        material_sound6 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb6439322
        material_sound7 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x403c374a
        material_sound8 = MaterialSoundPair.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaf6e81ab
        material_sound9 = MaterialSoundPair.from_stream(data, property_size)
    
        return cls(slope_detection_angle, slide_no_jump_angle, slide_detection_angle, scramble_detection_angle, scramble_speed, tar_scramble_speed, slide_breaking_speed, max_slide_speed, scramble_recovery_acceleration, slide_speedup_acceleration, slide_slowdown_acceleration, planar_slide_recovery_speed, slide_sound, slide_sound_ratio_change_factor, slide_sound_low_pass_filter, slide_sound_pitch, slide_sound_volume, num_material_sounds, material_sound0, material_sound1, material_sound2, material_sound3, material_sound4, material_sound5, material_sound6, material_sound7, material_sound8, material_sound9)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1c')  # 28 properties

        data.write(b'N}\xef~')  # 0x4e7def7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slope_detection_angle))

        data.write(b'\x18\xaa\\t')  # 0x18aa5c74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_no_jump_angle))

        data.write(b'e\x91\xa3\xa9')  # 0x6591a3a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_detection_angle))

        data.write(b'\x8f\x7f\xddo')  # 0x8f7fdd6f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scramble_detection_angle))

        data.write(b'C\x84\x99\x00')  # 0x43849900
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scramble_speed))

        data.write(b'\x8e~\xa4\xfc')  # 0x8e7ea4fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tar_scramble_speed))

        data.write(b'\x8f;\x93(')  # 0x8f3b9328
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_breaking_speed))

        data.write(b'Ln\xc5\x11')  # 0x4c6ec511
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_slide_speed))

        data.write(b's5\x08M')  # 0x7335084d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scramble_recovery_acceleration))

        data.write(b'v\x00\xa6\xc5')  # 0x7600a6c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_speedup_acceleration))

        data.write(b'\x8fs\xe7=')  # 0x8f73e73d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_slowdown_acceleration))

        data.write(b'\xce\x00x\x90')  # 0xce007890
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.planar_slide_recovery_speed))

        data.write(b'+y\xea\x93')  # 0x2b79ea93
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.slide_sound))

        data.write(b'\xba0\xaa\xca')  # 0xba30aaca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_sound_ratio_change_factor))

        data.write(b'\xd9\xcaP\xc2')  # 0xd9ca50c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84\x95\x1e\xc7')  # 0x84951ec7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jxR_')  # 0x6a78525f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slide_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7\xc1\x91A')  # 0xd7c19141
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_material_sounds))

        data.write(b'Wm\x99F')  # 0x576d9946
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8?/\xa7')  # 0xb83f2fa7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'R\xb9\xf2\xc5')  # 0x52b9f2c5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\xebD$')  # 0xbdeb4424
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\xc5N@')  # 0x5cc54e40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\x97\xf8\xa1')  # 0xb397f8a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x11%\xc3')  # 0x591125c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6C\x93"')  # 0xb6439322
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@<7J')  # 0x403c374a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xafn\x81\xab')  # 0xaf6e81ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sound9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("KongSlideDataJson", data)
        return cls(
            slope_detection_angle=json_data['slope_detection_angle'],
            slide_no_jump_angle=json_data['slide_no_jump_angle'],
            slide_detection_angle=json_data['slide_detection_angle'],
            scramble_detection_angle=json_data['scramble_detection_angle'],
            scramble_speed=json_data['scramble_speed'],
            tar_scramble_speed=json_data['tar_scramble_speed'],
            slide_breaking_speed=json_data['slide_breaking_speed'],
            max_slide_speed=json_data['max_slide_speed'],
            scramble_recovery_acceleration=json_data['scramble_recovery_acceleration'],
            slide_speedup_acceleration=json_data['slide_speedup_acceleration'],
            slide_slowdown_acceleration=json_data['slide_slowdown_acceleration'],
            planar_slide_recovery_speed=json_data['planar_slide_recovery_speed'],
            slide_sound=json_data['slide_sound'],
            slide_sound_ratio_change_factor=json_data['slide_sound_ratio_change_factor'],
            slide_sound_low_pass_filter=Spline.from_json(json_data['slide_sound_low_pass_filter']),
            slide_sound_pitch=Spline.from_json(json_data['slide_sound_pitch']),
            slide_sound_volume=Spline.from_json(json_data['slide_sound_volume']),
            num_material_sounds=json_data['num_material_sounds'],
            material_sound0=MaterialSoundPair.from_json(json_data['material_sound0']),
            material_sound1=MaterialSoundPair.from_json(json_data['material_sound1']),
            material_sound2=MaterialSoundPair.from_json(json_data['material_sound2']),
            material_sound3=MaterialSoundPair.from_json(json_data['material_sound3']),
            material_sound4=MaterialSoundPair.from_json(json_data['material_sound4']),
            material_sound5=MaterialSoundPair.from_json(json_data['material_sound5']),
            material_sound6=MaterialSoundPair.from_json(json_data['material_sound6']),
            material_sound7=MaterialSoundPair.from_json(json_data['material_sound7']),
            material_sound8=MaterialSoundPair.from_json(json_data['material_sound8']),
            material_sound9=MaterialSoundPair.from_json(json_data['material_sound9']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'slope_detection_angle': self.slope_detection_angle,
            'slide_no_jump_angle': self.slide_no_jump_angle,
            'slide_detection_angle': self.slide_detection_angle,
            'scramble_detection_angle': self.scramble_detection_angle,
            'scramble_speed': self.scramble_speed,
            'tar_scramble_speed': self.tar_scramble_speed,
            'slide_breaking_speed': self.slide_breaking_speed,
            'max_slide_speed': self.max_slide_speed,
            'scramble_recovery_acceleration': self.scramble_recovery_acceleration,
            'slide_speedup_acceleration': self.slide_speedup_acceleration,
            'slide_slowdown_acceleration': self.slide_slowdown_acceleration,
            'planar_slide_recovery_speed': self.planar_slide_recovery_speed,
            'slide_sound': self.slide_sound,
            'slide_sound_ratio_change_factor': self.slide_sound_ratio_change_factor,
            'slide_sound_low_pass_filter': self.slide_sound_low_pass_filter.to_json(),
            'slide_sound_pitch': self.slide_sound_pitch.to_json(),
            'slide_sound_volume': self.slide_sound_volume.to_json(),
            'num_material_sounds': self.num_material_sounds,
            'material_sound0': self.material_sound0.to_json(),
            'material_sound1': self.material_sound1.to_json(),
            'material_sound2': self.material_sound2.to_json(),
            'material_sound3': self.material_sound3.to_json(),
            'material_sound4': self.material_sound4.to_json(),
            'material_sound5': self.material_sound5.to_json(),
            'material_sound6': self.material_sound6.to_json(),
            'material_sound7': self.material_sound7.to_json(),
            'material_sound8': self.material_sound8.to_json(),
            'material_sound9': self.material_sound9.to_json(),
        }


def _decode_slope_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_no_jump_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scramble_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scramble_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tar_scramble_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_breaking_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_slide_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scramble_recovery_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_speedup_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_slowdown_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_planar_slide_recovery_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_slide_sound_ratio_change_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_num_material_sounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4e7def7e: ('slope_detection_angle', _decode_slope_detection_angle),
    0x18aa5c74: ('slide_no_jump_angle', _decode_slide_no_jump_angle),
    0x6591a3a9: ('slide_detection_angle', _decode_slide_detection_angle),
    0x8f7fdd6f: ('scramble_detection_angle', _decode_scramble_detection_angle),
    0x43849900: ('scramble_speed', _decode_scramble_speed),
    0x8e7ea4fc: ('tar_scramble_speed', _decode_tar_scramble_speed),
    0x8f3b9328: ('slide_breaking_speed', _decode_slide_breaking_speed),
    0x4c6ec511: ('max_slide_speed', _decode_max_slide_speed),
    0x7335084d: ('scramble_recovery_acceleration', _decode_scramble_recovery_acceleration),
    0x7600a6c5: ('slide_speedup_acceleration', _decode_slide_speedup_acceleration),
    0x8f73e73d: ('slide_slowdown_acceleration', _decode_slide_slowdown_acceleration),
    0xce007890: ('planar_slide_recovery_speed', _decode_planar_slide_recovery_speed),
    0x2b79ea93: ('slide_sound', _decode_slide_sound),
    0xba30aaca: ('slide_sound_ratio_change_factor', _decode_slide_sound_ratio_change_factor),
    0xd9ca50c2: ('slide_sound_low_pass_filter', Spline.from_stream),
    0x84951ec7: ('slide_sound_pitch', Spline.from_stream),
    0x6a78525f: ('slide_sound_volume', Spline.from_stream),
    0xd7c19141: ('num_material_sounds', _decode_num_material_sounds),
    0x576d9946: ('material_sound0', MaterialSoundPair.from_stream),
    0xb83f2fa7: ('material_sound1', MaterialSoundPair.from_stream),
    0x52b9f2c5: ('material_sound2', MaterialSoundPair.from_stream),
    0xbdeb4424: ('material_sound3', MaterialSoundPair.from_stream),
    0x5cc54e40: ('material_sound4', MaterialSoundPair.from_stream),
    0xb397f8a1: ('material_sound5', MaterialSoundPair.from_stream),
    0x591125c3: ('material_sound6', MaterialSoundPair.from_stream),
    0xb6439322: ('material_sound7', MaterialSoundPair.from_stream),
    0x403c374a: ('material_sound8', MaterialSoundPair.from_stream),
    0xaf6e81ab: ('material_sound9', MaterialSoundPair.from_stream),
}

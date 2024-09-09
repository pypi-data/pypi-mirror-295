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
from retro_data_structures.properties.dkc_returns.archetypes.MaterialType import MaterialType
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class MineCartMaterialSoundsJson(typing_extensions.TypedDict):
        material: json_util.JsonObject
        rolling_sound: int
        rolling_sound_low_pass_filter: json_util.JsonObject
        rolling_sound_pitch: json_util.JsonObject
        rolling_sound_volume: json_util.JsonObject
        rolling_sound2: int
        rolling_sound2_low_pass_filter: json_util.JsonObject
        rolling_sound2_pitch: json_util.JsonObject
        rolling_sound2_volume: json_util.JsonObject
        jump_sound: int
        land_sound: int
    

@dataclasses.dataclass()
class MineCartMaterialSounds(BaseProperty):
    material: MaterialType = dataclasses.field(default_factory=MaterialType, metadata={
        'reflection': FieldReflection[MaterialType](
            MaterialType, id=0xd72e09e1, original_name='Material', from_json=MaterialType.from_json, to_json=MaterialType.to_json
        ),
    })
    rolling_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x36b1add6, original_name='RollingSound'
        ),
    })
    rolling_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xefe4798f, original_name='RollingSoundLowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rolling_sound_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x96d4f78b, original_name='RollingSoundPitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rolling_sound_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x15001e0d, original_name='RollingSoundVolume', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rolling_sound2: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe3a63100, original_name='RollingSound2'
        ),
    })
    rolling_sound2_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x3b016cfa, original_name='RollingSound2LowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rolling_sound2_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x00c95a55, original_name='RollingSound2Pitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    rolling_sound2_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x74fdfc73, original_name='RollingSound2Volume', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    jump_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xebe660af, original_name='JumpSound'
        ),
    })
    land_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0e2b82ec, original_name='LandSound'
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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd72e09e1
        material = MaterialType.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36b1add6
        rolling_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xefe4798f
        rolling_sound_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x96d4f78b
        rolling_sound_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x15001e0d
        rolling_sound_volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe3a63100
        rolling_sound2 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3b016cfa
        rolling_sound2_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00c95a55
        rolling_sound2_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x74fdfc73
        rolling_sound2_volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xebe660af
        jump_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0e2b82ec
        land_sound = struct.unpack(">Q", data.read(8))[0]
    
        return cls(material, rolling_sound, rolling_sound_low_pass_filter, rolling_sound_pitch, rolling_sound_volume, rolling_sound2, rolling_sound2_low_pass_filter, rolling_sound2_pitch, rolling_sound2_volume, jump_sound, land_sound)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xd7.\t\xe1')  # 0xd72e09e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xb1\xad\xd6')  # 0x36b1add6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rolling_sound))

        data.write(b'\xef\xe4y\x8f')  # 0xefe4798f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96\xd4\xf7\x8b')  # 0x96d4f78b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x00\x1e\r')  # 0x15001e0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\xa61\x00')  # 0xe3a63100
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rolling_sound2))

        data.write(b';\x01l\xfa')  # 0x3b016cfa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xc9ZU')  # 0xc95a55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\xfd\xfcs')  # 0x74fdfc73
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xe6`\xaf')  # 0xebe660af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jump_sound))

        data.write(b'\x0e+\x82\xec')  # 0xe2b82ec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.land_sound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MineCartMaterialSoundsJson", data)
        return cls(
            material=MaterialType.from_json(json_data['material']),
            rolling_sound=json_data['rolling_sound'],
            rolling_sound_low_pass_filter=Spline.from_json(json_data['rolling_sound_low_pass_filter']),
            rolling_sound_pitch=Spline.from_json(json_data['rolling_sound_pitch']),
            rolling_sound_volume=Spline.from_json(json_data['rolling_sound_volume']),
            rolling_sound2=json_data['rolling_sound2'],
            rolling_sound2_low_pass_filter=Spline.from_json(json_data['rolling_sound2_low_pass_filter']),
            rolling_sound2_pitch=Spline.from_json(json_data['rolling_sound2_pitch']),
            rolling_sound2_volume=Spline.from_json(json_data['rolling_sound2_volume']),
            jump_sound=json_data['jump_sound'],
            land_sound=json_data['land_sound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'material': self.material.to_json(),
            'rolling_sound': self.rolling_sound,
            'rolling_sound_low_pass_filter': self.rolling_sound_low_pass_filter.to_json(),
            'rolling_sound_pitch': self.rolling_sound_pitch.to_json(),
            'rolling_sound_volume': self.rolling_sound_volume.to_json(),
            'rolling_sound2': self.rolling_sound2,
            'rolling_sound2_low_pass_filter': self.rolling_sound2_low_pass_filter.to_json(),
            'rolling_sound2_pitch': self.rolling_sound2_pitch.to_json(),
            'rolling_sound2_volume': self.rolling_sound2_volume.to_json(),
            'jump_sound': self.jump_sound,
            'land_sound': self.land_sound,
        }


def _decode_rolling_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rolling_sound2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_jump_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_land_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd72e09e1: ('material', MaterialType.from_stream),
    0x36b1add6: ('rolling_sound', _decode_rolling_sound),
    0xefe4798f: ('rolling_sound_low_pass_filter', Spline.from_stream),
    0x96d4f78b: ('rolling_sound_pitch', Spline.from_stream),
    0x15001e0d: ('rolling_sound_volume', Spline.from_stream),
    0xe3a63100: ('rolling_sound2', _decode_rolling_sound2),
    0x3b016cfa: ('rolling_sound2_low_pass_filter', Spline.from_stream),
    0xc95a55: ('rolling_sound2_pitch', Spline.from_stream),
    0x74fdfc73: ('rolling_sound2_volume', Spline.from_stream),
    0xebe660af: ('jump_sound', _decode_jump_sound),
    0xe2b82ec: ('land_sound', _decode_land_sound),
}

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
    class UnknownStruct268Json(typing_extensions.TypedDict):
        spinner_sound: int
        spline_input: int
        sound_ratio_change_factor: float
        sound_low_pass_filter: json_util.JsonObject
        sound_pitch: json_util.JsonObject
        sound_volume: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct268(BaseProperty):
    spinner_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd8738fc8, original_name='SpinnerSound'
        ),
    })
    spline_input: enums.SplineInput = dataclasses.field(default=enums.SplineInput.Unknown1, metadata={
        'reflection': FieldReflection[enums.SplineInput](
            enums.SplineInput, id=0x6a06faee, original_name='SplineInput', from_json=enums.SplineInput.from_json, to_json=enums.SplineInput.to_json
        ),
    })
    sound_ratio_change_factor: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0ac56fc9, original_name='SoundRatioChangeFactor'
        ),
    })
    sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xf27c01ee, original_name='SoundLowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    sound_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xcfe42324, original_name='SoundPitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    sound_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x533090a0, original_name='SoundVolume', from_json=Spline.from_json, to_json=Spline.to_json
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
        if property_count != 6:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd8738fc8
        spinner_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a06faee
        spline_input = enums.SplineInput.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0ac56fc9
        sound_ratio_change_factor = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf27c01ee
        sound_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcfe42324
        sound_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x533090a0
        sound_volume = Spline.from_stream(data, property_size)
    
        return cls(spinner_sound, spline_input, sound_ratio_change_factor, sound_low_pass_filter, sound_pitch, sound_volume)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xd8s\x8f\xc8')  # 0xd8738fc8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.spinner_sound))

        data.write(b'j\x06\xfa\xee')  # 0x6a06faee
        data.write(b'\x00\x04')  # size
        self.spline_input.to_stream(data)

        data.write(b'\n\xc5o\xc9')  # 0xac56fc9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sound_ratio_change_factor))

        data.write(b'\xf2|\x01\xee')  # 0xf27c01ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\xe4#$')  # 0xcfe42324
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S0\x90\xa0')  # 0x533090a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct268Json", data)
        return cls(
            spinner_sound=json_data['spinner_sound'],
            spline_input=enums.SplineInput.from_json(json_data['spline_input']),
            sound_ratio_change_factor=json_data['sound_ratio_change_factor'],
            sound_low_pass_filter=Spline.from_json(json_data['sound_low_pass_filter']),
            sound_pitch=Spline.from_json(json_data['sound_pitch']),
            sound_volume=Spline.from_json(json_data['sound_volume']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'spinner_sound': self.spinner_sound,
            'spline_input': self.spline_input.to_json(),
            'sound_ratio_change_factor': self.sound_ratio_change_factor,
            'sound_low_pass_filter': self.sound_low_pass_filter.to_json(),
            'sound_pitch': self.sound_pitch.to_json(),
            'sound_volume': self.sound_volume.to_json(),
        }


def _decode_spinner_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_spline_input(data: typing.BinaryIO, property_size: int):
    return enums.SplineInput.from_stream(data)


def _decode_sound_ratio_change_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd8738fc8: ('spinner_sound', _decode_spinner_sound),
    0x6a06faee: ('spline_input', _decode_spline_input),
    0xac56fc9: ('sound_ratio_change_factor', _decode_sound_ratio_change_factor),
    0xf27c01ee: ('sound_low_pass_filter', Spline.from_stream),
    0xcfe42324: ('sound_pitch', Spline.from_stream),
    0x533090a0: ('sound_volume', Spline.from_stream),
}

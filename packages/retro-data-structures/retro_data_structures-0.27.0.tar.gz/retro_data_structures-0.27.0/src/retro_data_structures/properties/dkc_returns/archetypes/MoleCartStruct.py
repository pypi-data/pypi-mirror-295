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
    class MoleCartStructJson(typing_extensions.TypedDict):
        spline_input: int
        max_angle: float
        unknown_0x61dd3eb6: float
        fade_in_time: float
        sound: int
        unknown_0x8a939379: json_util.JsonObject
        pitch: json_util.JsonObject
        volume: json_util.JsonObject
    

@dataclasses.dataclass()
class MoleCartStruct(BaseProperty):
    spline_input: int = dataclasses.field(default=1306613276, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6a06faee, original_name='SplineInput'
        ),
    })  # Choice
    max_angle: float = dataclasses.field(default=45.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd9635583, original_name='MaxAngle'
        ),
    })
    unknown_0x61dd3eb6: float = dataclasses.field(default=45.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x61dd3eb6, original_name='Unknown'
        ),
    })
    fade_in_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x90aa341f, original_name='FadeInTime'
        ),
    })
    sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa55dacf6, original_name='Sound'
        ),
    })
    unknown_0x8a939379: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x8a939379, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x0e727fc4, original_name='Pitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xf3fbe484, original_name='Volume', from_json=Spline.from_json, to_json=Spline.to_json
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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a06faee
        spline_input = struct.unpack(">L", data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9635583
        max_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x61dd3eb6
        unknown_0x61dd3eb6 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x90aa341f
        fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa55dacf6
        sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8a939379
        unknown_0x8a939379 = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0e727fc4
        pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf3fbe484
        volume = Spline.from_stream(data, property_size)
    
        return cls(spline_input, max_angle, unknown_0x61dd3eb6, fade_in_time, sound, unknown_0x8a939379, pitch, volume)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'j\x06\xfa\xee')  # 0x6a06faee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.spline_input))

        data.write(b'\xd9cU\x83')  # 0xd9635583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_angle))

        data.write(b'a\xdd>\xb6')  # 0x61dd3eb6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61dd3eb6))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'\xa5]\xac\xf6')  # 0xa55dacf6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound))

        data.write(b'\x8a\x93\x93y')  # 0x8a939379
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x8a939379.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0er\x7f\xc4')  # 0xe727fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xfb\xe4\x84')  # 0xf3fbe484
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MoleCartStructJson", data)
        return cls(
            spline_input=json_data['spline_input'],
            max_angle=json_data['max_angle'],
            unknown_0x61dd3eb6=json_data['unknown_0x61dd3eb6'],
            fade_in_time=json_data['fade_in_time'],
            sound=json_data['sound'],
            unknown_0x8a939379=Spline.from_json(json_data['unknown_0x8a939379']),
            pitch=Spline.from_json(json_data['pitch']),
            volume=Spline.from_json(json_data['volume']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'spline_input': self.spline_input,
            'max_angle': self.max_angle,
            'unknown_0x61dd3eb6': self.unknown_0x61dd3eb6,
            'fade_in_time': self.fade_in_time,
            'sound': self.sound,
            'unknown_0x8a939379': self.unknown_0x8a939379.to_json(),
            'pitch': self.pitch.to_json(),
            'volume': self.volume.to_json(),
        }


def _decode_spline_input(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61dd3eb6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6a06faee: ('spline_input', _decode_spline_input),
    0xd9635583: ('max_angle', _decode_max_angle),
    0x61dd3eb6: ('unknown_0x61dd3eb6', _decode_unknown_0x61dd3eb6),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0xa55dacf6: ('sound', _decode_sound),
    0x8a939379: ('unknown_0x8a939379', Spline.from_stream),
    0xe727fc4: ('pitch', Spline.from_stream),
    0xf3fbe484: ('volume', Spline.from_stream),
}

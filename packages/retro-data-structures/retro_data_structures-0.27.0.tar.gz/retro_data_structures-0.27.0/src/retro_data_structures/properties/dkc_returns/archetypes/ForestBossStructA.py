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
    class ForestBossStructAJson(typing_extensions.TypedDict):
        sound: int
        unknown: json_util.JsonObject
        pitch: json_util.JsonObject
        volume: json_util.JsonObject
        maximum_input_value: float
        minimum_input_value: float
    

@dataclasses.dataclass()
class ForestBossStructA(BaseProperty):
    sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa55dacf6, original_name='Sound'
        ),
    })
    unknown: Spline = dataclasses.field(default_factory=Spline, metadata={
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
    maximum_input_value: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe2973405, original_name='MaximumInputValue'
        ),
    })
    minimum_input_value: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa3800b83, original_name='MinimumInputValue'
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
        assert property_id == 0xa55dacf6
        sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8a939379
        unknown = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0e727fc4
        pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf3fbe484
        volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2973405
        maximum_input_value = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa3800b83
        minimum_input_value = struct.unpack('>f', data.read(4))[0]
    
        return cls(sound, unknown, pitch, volume, maximum_input_value, minimum_input_value)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xa5]\xac\xf6')  # 0xa55dacf6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound))

        data.write(b'\x8a\x93\x93y')  # 0x8a939379
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
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

        data.write(b'\xe2\x974\x05')  # 0xe2973405
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_input_value))

        data.write(b'\xa3\x80\x0b\x83')  # 0xa3800b83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_input_value))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ForestBossStructAJson", data)
        return cls(
            sound=json_data['sound'],
            unknown=Spline.from_json(json_data['unknown']),
            pitch=Spline.from_json(json_data['pitch']),
            volume=Spline.from_json(json_data['volume']),
            maximum_input_value=json_data['maximum_input_value'],
            minimum_input_value=json_data['minimum_input_value'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'sound': self.sound,
            'unknown': self.unknown.to_json(),
            'pitch': self.pitch.to_json(),
            'volume': self.volume.to_json(),
            'maximum_input_value': self.maximum_input_value,
            'minimum_input_value': self.minimum_input_value,
        }


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_maximum_input_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_input_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa55dacf6: ('sound', _decode_sound),
    0x8a939379: ('unknown', Spline.from_stream),
    0xe727fc4: ('pitch', Spline.from_stream),
    0xf3fbe484: ('volume', Spline.from_stream),
    0xe2973405: ('maximum_input_value', _decode_maximum_input_value),
    0xa3800b83: ('minimum_input_value', _decode_minimum_input_value),
}

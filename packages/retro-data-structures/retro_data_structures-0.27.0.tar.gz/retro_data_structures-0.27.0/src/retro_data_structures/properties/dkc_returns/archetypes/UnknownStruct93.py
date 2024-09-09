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
    class UnknownStruct93Json(typing_extensions.TypedDict):
        auto_loop_effect: bool
        auto_start_effect: bool
        effect_weight: json_util.JsonObject
        screen_warp_texture: int
        unknown_0xb883ac66: float
        offset_v: float
        unknown_0xa02bb525: float
        unknown_0x26bfc78b: float
        unknown_0x83f8f585: float
        scale_factor: int
    

@dataclasses.dataclass()
class UnknownStruct93(BaseProperty):
    auto_loop_effect: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc8fc49d0, original_name='AutoLoopEffect'
        ),
    })
    auto_start_effect: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x65470f5b, original_name='AutoStartEffect'
        ),
    })
    effect_weight: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x6057938a, original_name='EffectWeight', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    screen_warp_texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5e96989a, original_name='ScreenWarpTexture'
        ),
    })
    unknown_0xb883ac66: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb883ac66, original_name='Unknown'
        ),
    })
    offset_v: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3e17dec8, original_name='OffsetV'
        ),
    })
    unknown_0xa02bb525: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa02bb525, original_name='Unknown'
        ),
    })
    unknown_0x26bfc78b: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x26bfc78b, original_name='Unknown'
        ),
    })
    unknown_0x83f8f585: float = dataclasses.field(default=30.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x83f8f585, original_name='Unknown'
        ),
    })
    scale_factor: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb2807d6d, original_name='ScaleFactor'
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
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc8fc49d0
        auto_loop_effect = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x65470f5b
        auto_start_effect = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6057938a
        effect_weight = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e96989a
        screen_warp_texture = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb883ac66
        unknown_0xb883ac66 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3e17dec8
        offset_v = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa02bb525
        unknown_0xa02bb525 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26bfc78b
        unknown_0x26bfc78b = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x83f8f585
        unknown_0x83f8f585 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb2807d6d
        scale_factor = struct.unpack('>l', data.read(4))[0]
    
        return cls(auto_loop_effect, auto_start_effect, effect_weight, screen_warp_texture, unknown_0xb883ac66, offset_v, unknown_0xa02bb525, unknown_0x26bfc78b, unknown_0x83f8f585, scale_factor)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xc8\xfcI\xd0')  # 0xc8fc49d0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_loop_effect))

        data.write(b'eG\x0f[')  # 0x65470f5b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start_effect))

        data.write(b'`W\x93\x8a')  # 0x6057938a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.effect_weight.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\x96\x98\x9a')  # 0x5e96989a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.screen_warp_texture))

        data.write(b'\xb8\x83\xacf')  # 0xb883ac66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb883ac66))

        data.write(b'>\x17\xde\xc8')  # 0x3e17dec8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.offset_v))

        data.write(b'\xa0+\xb5%')  # 0xa02bb525
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa02bb525))

        data.write(b'&\xbf\xc7\x8b')  # 0x26bfc78b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x26bfc78b))

        data.write(b'\x83\xf8\xf5\x85')  # 0x83f8f585
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x83f8f585))

        data.write(b'\xb2\x80}m')  # 0xb2807d6d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.scale_factor))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct93Json", data)
        return cls(
            auto_loop_effect=json_data['auto_loop_effect'],
            auto_start_effect=json_data['auto_start_effect'],
            effect_weight=Spline.from_json(json_data['effect_weight']),
            screen_warp_texture=json_data['screen_warp_texture'],
            unknown_0xb883ac66=json_data['unknown_0xb883ac66'],
            offset_v=json_data['offset_v'],
            unknown_0xa02bb525=json_data['unknown_0xa02bb525'],
            unknown_0x26bfc78b=json_data['unknown_0x26bfc78b'],
            unknown_0x83f8f585=json_data['unknown_0x83f8f585'],
            scale_factor=json_data['scale_factor'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'auto_loop_effect': self.auto_loop_effect,
            'auto_start_effect': self.auto_start_effect,
            'effect_weight': self.effect_weight.to_json(),
            'screen_warp_texture': self.screen_warp_texture,
            'unknown_0xb883ac66': self.unknown_0xb883ac66,
            'offset_v': self.offset_v,
            'unknown_0xa02bb525': self.unknown_0xa02bb525,
            'unknown_0x26bfc78b': self.unknown_0x26bfc78b,
            'unknown_0x83f8f585': self.unknown_0x83f8f585,
            'scale_factor': self.scale_factor,
        }


def _decode_auto_loop_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_screen_warp_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xb883ac66(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_offset_v(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa02bb525(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x26bfc78b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x83f8f585(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scale_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc8fc49d0: ('auto_loop_effect', _decode_auto_loop_effect),
    0x65470f5b: ('auto_start_effect', _decode_auto_start_effect),
    0x6057938a: ('effect_weight', Spline.from_stream),
    0x5e96989a: ('screen_warp_texture', _decode_screen_warp_texture),
    0xb883ac66: ('unknown_0xb883ac66', _decode_unknown_0xb883ac66),
    0x3e17dec8: ('offset_v', _decode_offset_v),
    0xa02bb525: ('unknown_0xa02bb525', _decode_unknown_0xa02bb525),
    0x26bfc78b: ('unknown_0x26bfc78b', _decode_unknown_0x26bfc78b),
    0x83f8f585: ('unknown_0x83f8f585', _decode_unknown_0x83f8f585),
    0xb2807d6d: ('scale_factor', _decode_scale_factor),
}

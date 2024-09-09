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
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct147Json(typing_extensions.TypedDict):
        hud_frame: int
        board_transition_time: float
        board_rotation: json_util.JsonObject
        visible_time: float
        unknown_0x5aedf7c9: float
        transition_out_time: float
        fade_alpha: float
        banana_increment_sound: int
        banana_reset_sound: int
        increment_delay: float
        strg_0x569bd8a7: int
        strg_0x7affc159: int
        unknown_0xf7d838f6: float
        strg_0x09f666e5: int
        text_gradient_start_color: json_util.JsonValue
        text_gradient_end_color: json_util.JsonValue
        text_outline_color: json_util.JsonValue
        unknown_0xa5f210ba: bool
        unknown_0x4038140e: bool
    

@dataclasses.dataclass()
class UnknownStruct147(BaseProperty):
    hud_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf2299ed6, original_name='HUDFrame'
        ),
    })
    board_transition_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x172addb3, original_name='BoardTransitionTime'
        ),
    })
    board_rotation: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x69dc0a16, original_name='BoardRotation', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    visible_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5704897c, original_name='VisibleTime'
        ),
    })
    unknown_0x5aedf7c9: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5aedf7c9, original_name='Unknown'
        ),
    })
    transition_out_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5e4a1076, original_name='TransitionOutTime'
        ),
    })
    fade_alpha: float = dataclasses.field(default=0.30000001192092896, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5d84ace2, original_name='FadeAlpha'
        ),
    })
    banana_increment_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5b928a5d, original_name='BananaIncrementSound'
        ),
    })
    banana_reset_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd840598d, original_name='BananaResetSound'
        ),
    })
    increment_delay: float = dataclasses.field(default=0.0625, metadata={
        'reflection': FieldReflection[float](
            float, id=0xeeb39069, original_name='IncrementDelay'
        ),
    })
    strg_0x569bd8a7: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x569bd8a7, original_name='STRG'
        ),
    })
    strg_0x7affc159: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7affc159, original_name='STRG'
        ),
    })
    unknown_0xf7d838f6: float = dataclasses.field(default=0.30000001192092896, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf7d838f6, original_name='Unknown'
        ),
    })
    strg_0x09f666e5: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x09f666e5, original_name='STRG'
        ),
    })
    text_gradient_start_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xf9e0d0fb, original_name='TextGradientStartColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    text_gradient_end_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xe0417e89, original_name='TextGradientEndColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xf2e13506, original_name='TextOutlineColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    unknown_0xa5f210ba: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa5f210ba, original_name='Unknown'
        ),
    })
    unknown_0x4038140e: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4038140e, original_name='Unknown'
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
        if property_count != 19:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf2299ed6
        hud_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x172addb3
        board_transition_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x69dc0a16
        board_rotation = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5704897c
        visible_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5aedf7c9
        unknown_0x5aedf7c9 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e4a1076
        transition_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5d84ace2
        fade_alpha = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5b928a5d
        banana_increment_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd840598d
        banana_reset_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeeb39069
        increment_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x569bd8a7
        strg_0x569bd8a7 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7affc159
        strg_0x7affc159 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf7d838f6
        unknown_0xf7d838f6 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x09f666e5
        strg_0x09f666e5 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf9e0d0fb
        text_gradient_start_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe0417e89
        text_gradient_end_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf2e13506
        text_outline_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa5f210ba
        unknown_0xa5f210ba = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4038140e
        unknown_0x4038140e = struct.unpack('>?', data.read(1))[0]
    
        return cls(hud_frame, board_transition_time, board_rotation, visible_time, unknown_0x5aedf7c9, transition_out_time, fade_alpha, banana_increment_sound, banana_reset_sound, increment_delay, strg_0x569bd8a7, strg_0x7affc159, unknown_0xf7d838f6, strg_0x09f666e5, text_gradient_start_color, text_gradient_end_color, text_outline_color, unknown_0xa5f210ba, unknown_0x4038140e)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\x17*\xdd\xb3')  # 0x172addb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.board_transition_time))

        data.write(b'i\xdc\n\x16')  # 0x69dc0a16
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.board_rotation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'W\x04\x89|')  # 0x5704897c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_time))

        data.write(b'Z\xed\xf7\xc9')  # 0x5aedf7c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5aedf7c9))

        data.write(b'^J\x10v')  # 0x5e4a1076
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.transition_out_time))

        data.write(b']\x84\xac\xe2')  # 0x5d84ace2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_alpha))

        data.write(b'[\x92\x8a]')  # 0x5b928a5d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.banana_increment_sound))

        data.write(b'\xd8@Y\x8d')  # 0xd840598d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.banana_reset_sound))

        data.write(b'\xee\xb3\x90i')  # 0xeeb39069
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.increment_delay))

        data.write(b'V\x9b\xd8\xa7')  # 0x569bd8a7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x569bd8a7))

        data.write(b'z\xff\xc1Y')  # 0x7affc159
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x7affc159))

        data.write(b'\xf7\xd88\xf6')  # 0xf7d838f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf7d838f6))

        data.write(b'\t\xf6f\xe5')  # 0x9f666e5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x09f666e5))

        data.write(b'\xf9\xe0\xd0\xfb')  # 0xf9e0d0fb
        data.write(b'\x00\x10')  # size
        self.text_gradient_start_color.to_stream(data)

        data.write(b'\xe0A~\x89')  # 0xe0417e89
        data.write(b'\x00\x10')  # size
        self.text_gradient_end_color.to_stream(data)

        data.write(b'\xf2\xe15\x06')  # 0xf2e13506
        data.write(b'\x00\x10')  # size
        self.text_outline_color.to_stream(data)

        data.write(b'\xa5\xf2\x10\xba')  # 0xa5f210ba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa5f210ba))

        data.write(b'@8\x14\x0e')  # 0x4038140e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4038140e))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct147Json", data)
        return cls(
            hud_frame=json_data['hud_frame'],
            board_transition_time=json_data['board_transition_time'],
            board_rotation=Spline.from_json(json_data['board_rotation']),
            visible_time=json_data['visible_time'],
            unknown_0x5aedf7c9=json_data['unknown_0x5aedf7c9'],
            transition_out_time=json_data['transition_out_time'],
            fade_alpha=json_data['fade_alpha'],
            banana_increment_sound=json_data['banana_increment_sound'],
            banana_reset_sound=json_data['banana_reset_sound'],
            increment_delay=json_data['increment_delay'],
            strg_0x569bd8a7=json_data['strg_0x569bd8a7'],
            strg_0x7affc159=json_data['strg_0x7affc159'],
            unknown_0xf7d838f6=json_data['unknown_0xf7d838f6'],
            strg_0x09f666e5=json_data['strg_0x09f666e5'],
            text_gradient_start_color=Color.from_json(json_data['text_gradient_start_color']),
            text_gradient_end_color=Color.from_json(json_data['text_gradient_end_color']),
            text_outline_color=Color.from_json(json_data['text_outline_color']),
            unknown_0xa5f210ba=json_data['unknown_0xa5f210ba'],
            unknown_0x4038140e=json_data['unknown_0x4038140e'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'hud_frame': self.hud_frame,
            'board_transition_time': self.board_transition_time,
            'board_rotation': self.board_rotation.to_json(),
            'visible_time': self.visible_time,
            'unknown_0x5aedf7c9': self.unknown_0x5aedf7c9,
            'transition_out_time': self.transition_out_time,
            'fade_alpha': self.fade_alpha,
            'banana_increment_sound': self.banana_increment_sound,
            'banana_reset_sound': self.banana_reset_sound,
            'increment_delay': self.increment_delay,
            'strg_0x569bd8a7': self.strg_0x569bd8a7,
            'strg_0x7affc159': self.strg_0x7affc159,
            'unknown_0xf7d838f6': self.unknown_0xf7d838f6,
            'strg_0x09f666e5': self.strg_0x09f666e5,
            'text_gradient_start_color': self.text_gradient_start_color.to_json(),
            'text_gradient_end_color': self.text_gradient_end_color.to_json(),
            'text_outline_color': self.text_outline_color.to_json(),
            'unknown_0xa5f210ba': self.unknown_0xa5f210ba,
            'unknown_0x4038140e': self.unknown_0x4038140e,
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_board_transition_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5aedf7c9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_transition_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_banana_increment_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_banana_reset_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_increment_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_strg_0x569bd8a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x7affc159(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf7d838f6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_strg_0x09f666e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_gradient_start_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_gradient_end_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa5f210ba(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4038140e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0x172addb3: ('board_transition_time', _decode_board_transition_time),
    0x69dc0a16: ('board_rotation', Spline.from_stream),
    0x5704897c: ('visible_time', _decode_visible_time),
    0x5aedf7c9: ('unknown_0x5aedf7c9', _decode_unknown_0x5aedf7c9),
    0x5e4a1076: ('transition_out_time', _decode_transition_out_time),
    0x5d84ace2: ('fade_alpha', _decode_fade_alpha),
    0x5b928a5d: ('banana_increment_sound', _decode_banana_increment_sound),
    0xd840598d: ('banana_reset_sound', _decode_banana_reset_sound),
    0xeeb39069: ('increment_delay', _decode_increment_delay),
    0x569bd8a7: ('strg_0x569bd8a7', _decode_strg_0x569bd8a7),
    0x7affc159: ('strg_0x7affc159', _decode_strg_0x7affc159),
    0xf7d838f6: ('unknown_0xf7d838f6', _decode_unknown_0xf7d838f6),
    0x9f666e5: ('strg_0x09f666e5', _decode_strg_0x09f666e5),
    0xf9e0d0fb: ('text_gradient_start_color', _decode_text_gradient_start_color),
    0xe0417e89: ('text_gradient_end_color', _decode_text_gradient_end_color),
    0xf2e13506: ('text_outline_color', _decode_text_outline_color),
    0xa5f210ba: ('unknown_0xa5f210ba', _decode_unknown_0xa5f210ba),
    0x4038140e: ('unknown_0x4038140e', _decode_unknown_0x4038140e),
}

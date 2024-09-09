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
from retro_data_structures.properties.dkc_returns.core.Color import Color

if typing.TYPE_CHECKING:
    class TextPropertiesJson(typing_extensions.TypedDict):
        text_render_mode: int
        text_bounding_width: int
        text_bounding_height: int
        line_spacing: float
        line_extra_space: int
        character_extra_space: int
        foreground_color: json_util.JsonValue
        outline_color: json_util.JsonValue
        geometry_color: json_util.JsonValue
        gradient_start: json_util.JsonValue
        gradient_end: json_util.JsonValue
        default_font: int
        unknown_0x18dd95cd: int
        unknown_0x42091548: int
        wrap_text: bool
        draw_shadow: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x9f1bd46d, 0xee521dc6, 0xf2d36abb, 0x1a996292, 0x5eff913, 0x45830901, 0x3f39e635, 0x60d78569, 0x5908ef39, 0xfbb7be45, 0xfbce3fb, 0xdb9f8b6, 0x18dd95cd, 0x42091548, 0x330573e9, 0xd8a2eef0)


@dataclasses.dataclass()
class TextProperties(BaseProperty):
    text_render_mode: enums.UnknownEnum3 = dataclasses.field(default=enums.UnknownEnum3.Unknown1, metadata={
        'reflection': FieldReflection[enums.UnknownEnum3](
            enums.UnknownEnum3, id=0x9f1bd46d, original_name='TextRenderMode', from_json=enums.UnknownEnum3.from_json, to_json=enums.UnknownEnum3.to_json
        ),
    })
    text_bounding_width: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xee521dc6, original_name='TextBoundingWidth'
        ),
    })
    text_bounding_height: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf2d36abb, original_name='TextBoundingHeight'
        ),
    })
    line_spacing: float = dataclasses.field(default=100.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1a996292, original_name='LineSpacing'
        ),
    })
    line_extra_space: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x05eff913, original_name='LineExtraSpace'
        ),
    })
    character_extra_space: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x45830901, original_name='CharacterExtraSpace'
        ),
    })
    foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x3f39e635, original_name='ForegroundColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x60d78569, original_name='OutlineColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    geometry_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x5908ef39, original_name='GeometryColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    gradient_start: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xfbb7be45, original_name='GradientStart', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    gradient_end: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x0fbce3fb, original_name='GradientEnd', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    default_font: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FONT'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0db9f8b6, original_name='DefaultFont'
        ),
    })
    unknown_0x18dd95cd: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x18dd95cd, original_name='Unknown'
        ),
    })
    unknown_0x42091548: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x42091548, original_name='Unknown'
        ),
    })
    wrap_text: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x330573e9, original_name='WrapText'
        ),
    })
    draw_shadow: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd8a2eef0, original_name='DrawShadow'
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
        if property_count != 16:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHLLHlLHlLHfLHlLHlLHffffLHffffLHffffLHffffLHffffLHQLHlLHlLH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(218))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[24], dec[30], dec[36], dec[42], dec[48], dec[51], dec[54], dec[57], dec[60]) == _FAST_IDS
        return cls(
            enums.UnknownEnum3(dec[2]),
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            Color(*dec[20:24]),
            Color(*dec[26:30]),
            Color(*dec[32:36]),
            Color(*dec[38:42]),
            Color(*dec[44:48]),
            dec[50],
            dec[53],
            dec[56],
            dec[59],
            dec[62],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'\x9f\x1b\xd4m')  # 0x9f1bd46d
        data.write(b'\x00\x04')  # size
        self.text_render_mode.to_stream(data)

        data.write(b'\xeeR\x1d\xc6')  # 0xee521dc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_bounding_width))

        data.write(b'\xf2\xd3j\xbb')  # 0xf2d36abb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_bounding_height))

        data.write(b'\x1a\x99b\x92')  # 0x1a996292
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.line_spacing))

        data.write(b'\x05\xef\xf9\x13')  # 0x5eff913
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.line_extra_space))

        data.write(b'E\x83\t\x01')  # 0x45830901
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.character_extra_space))

        data.write(b'?9\xe65')  # 0x3f39e635
        data.write(b'\x00\x10')  # size
        self.foreground_color.to_stream(data)

        data.write(b'`\xd7\x85i')  # 0x60d78569
        data.write(b'\x00\x10')  # size
        self.outline_color.to_stream(data)

        data.write(b'Y\x08\xef9')  # 0x5908ef39
        data.write(b'\x00\x10')  # size
        self.geometry_color.to_stream(data)

        data.write(b'\xfb\xb7\xbeE')  # 0xfbb7be45
        data.write(b'\x00\x10')  # size
        self.gradient_start.to_stream(data)

        data.write(b'\x0f\xbc\xe3\xfb')  # 0xfbce3fb
        data.write(b'\x00\x10')  # size
        self.gradient_end.to_stream(data)

        data.write(b'\r\xb9\xf8\xb6')  # 0xdb9f8b6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.default_font))

        data.write(b'\x18\xdd\x95\xcd')  # 0x18dd95cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x18dd95cd))

        data.write(b'B\t\x15H')  # 0x42091548
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x42091548))

        data.write(b'3\x05s\xe9')  # 0x330573e9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.wrap_text))

        data.write(b'\xd8\xa2\xee\xf0')  # 0xd8a2eef0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.draw_shadow))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TextPropertiesJson", data)
        return cls(
            text_render_mode=enums.UnknownEnum3.from_json(json_data['text_render_mode']),
            text_bounding_width=json_data['text_bounding_width'],
            text_bounding_height=json_data['text_bounding_height'],
            line_spacing=json_data['line_spacing'],
            line_extra_space=json_data['line_extra_space'],
            character_extra_space=json_data['character_extra_space'],
            foreground_color=Color.from_json(json_data['foreground_color']),
            outline_color=Color.from_json(json_data['outline_color']),
            geometry_color=Color.from_json(json_data['geometry_color']),
            gradient_start=Color.from_json(json_data['gradient_start']),
            gradient_end=Color.from_json(json_data['gradient_end']),
            default_font=json_data['default_font'],
            unknown_0x18dd95cd=json_data['unknown_0x18dd95cd'],
            unknown_0x42091548=json_data['unknown_0x42091548'],
            wrap_text=json_data['wrap_text'],
            draw_shadow=json_data['draw_shadow'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'text_render_mode': self.text_render_mode.to_json(),
            'text_bounding_width': self.text_bounding_width,
            'text_bounding_height': self.text_bounding_height,
            'line_spacing': self.line_spacing,
            'line_extra_space': self.line_extra_space,
            'character_extra_space': self.character_extra_space,
            'foreground_color': self.foreground_color.to_json(),
            'outline_color': self.outline_color.to_json(),
            'geometry_color': self.geometry_color.to_json(),
            'gradient_start': self.gradient_start.to_json(),
            'gradient_end': self.gradient_end.to_json(),
            'default_font': self.default_font,
            'unknown_0x18dd95cd': self.unknown_0x18dd95cd,
            'unknown_0x42091548': self.unknown_0x42091548,
            'wrap_text': self.wrap_text,
            'draw_shadow': self.draw_shadow,
        }


def _decode_text_render_mode(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum3.from_stream(data)


def _decode_text_bounding_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_text_bounding_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_line_spacing(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_line_extra_space(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_character_extra_space(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_geometry_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_gradient_start(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_gradient_end(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_default_font(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x18dd95cd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x42091548(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_wrap_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_draw_shadow(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9f1bd46d: ('text_render_mode', _decode_text_render_mode),
    0xee521dc6: ('text_bounding_width', _decode_text_bounding_width),
    0xf2d36abb: ('text_bounding_height', _decode_text_bounding_height),
    0x1a996292: ('line_spacing', _decode_line_spacing),
    0x5eff913: ('line_extra_space', _decode_line_extra_space),
    0x45830901: ('character_extra_space', _decode_character_extra_space),
    0x3f39e635: ('foreground_color', _decode_foreground_color),
    0x60d78569: ('outline_color', _decode_outline_color),
    0x5908ef39: ('geometry_color', _decode_geometry_color),
    0xfbb7be45: ('gradient_start', _decode_gradient_start),
    0xfbce3fb: ('gradient_end', _decode_gradient_end),
    0xdb9f8b6: ('default_font', _decode_default_font),
    0x18dd95cd: ('unknown_0x18dd95cd', _decode_unknown_0x18dd95cd),
    0x42091548: ('unknown_0x42091548', _decode_unknown_0x42091548),
    0x330573e9: ('wrap_text', _decode_wrap_text),
    0xd8a2eef0: ('draw_shadow', _decode_draw_shadow),
}

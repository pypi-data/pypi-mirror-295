# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.field_reflection import FieldReflection
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.Color import Color

if typing.TYPE_CHECKING:
    class LevelDarkenerJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        darken_time: float
        darken_color: json_util.JsonValue
        hide_world_when_fully_drawn: bool
    

@dataclasses.dataclass()
class LevelDarkener(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    darken_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x49793287, original_name='DarkenTime'
        ),
    })
    darken_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x691463fb, original_name='DarkenColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    hide_world_when_fully_drawn: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x897d3616, original_name='HideWorldWhenFullyDrawn'
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> str | None:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'LVLD'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x49793287
        darken_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x691463fb
        darken_color = Color.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x897d3616
        hide_world_when_fully_drawn = struct.unpack('>?', data.read(1))[0]
    
        return cls(editor_properties, darken_time, darken_color, hide_world_when_fully_drawn)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Iy2\x87')  # 0x49793287
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.darken_time))

        data.write(b'i\x14c\xfb')  # 0x691463fb
        data.write(b'\x00\x10')  # size
        self.darken_color.to_stream(data)

        data.write(b'\x89}6\x16')  # 0x897d3616
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.hide_world_when_fully_drawn))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("LevelDarkenerJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            darken_time=json_data['darken_time'],
            darken_color=Color.from_json(json_data['darken_color']),
            hide_world_when_fully_drawn=json_data['hide_world_when_fully_drawn'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'darken_time': self.darken_time,
            'darken_color': self.darken_color.to_json(),
            'hide_world_when_fully_drawn': self.hide_world_when_fully_drawn,
        }


def _decode_darken_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_darken_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hide_world_when_fully_drawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x49793287: ('darken_time', _decode_darken_time),
    0x691463fb: ('darken_color', _decode_darken_color),
    0x897d3616: ('hide_world_when_fully_drawn', _decode_hide_world_when_fully_drawn),
}

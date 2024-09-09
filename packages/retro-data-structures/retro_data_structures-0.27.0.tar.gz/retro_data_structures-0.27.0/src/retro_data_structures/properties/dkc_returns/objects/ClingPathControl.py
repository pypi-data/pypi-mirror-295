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
from retro_data_structures.properties.dkc_returns.archetypes.ClingPathControlData import ClingPathControlData
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.SplineType import SplineType
from retro_data_structures.properties.dkc_returns.core.Color import Color

if typing.TYPE_CHECKING:
    class ClingPathControlJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        path_flags: int
        spline_type: json_util.JsonObject
        cling_path_control_data: json_util.JsonObject
        editor_color: json_util.JsonValue
    

@dataclasses.dataclass()
class ClingPathControl(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    path_flags: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb0b97f9f, original_name='PathFlags'
        ),
    })
    spline_type: SplineType = dataclasses.field(default_factory=SplineType, metadata={
        'reflection': FieldReflection[SplineType](
            SplineType, id=0x20091b54, original_name='SplineType', from_json=SplineType.from_json, to_json=SplineType.to_json
        ),
    })
    cling_path_control_data: ClingPathControlData = dataclasses.field(default_factory=ClingPathControlData, metadata={
        'reflection': FieldReflection[ClingPathControlData](
            ClingPathControlData, id=0x4985a099, original_name='ClingPathControlData', from_json=ClingPathControlData.from_json, to_json=ClingPathControlData.to_json
        ),
    })
    editor_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0x00dd86e2, original_name='EditorColor', from_json=Color.from_json, to_json=Color.to_json
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
        return 'CLPC'

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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0b97f9f
        path_flags = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x20091b54
        spline_type = SplineType.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4985a099
        cling_path_control_data = ClingPathControlData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00dd86e2
        editor_color = Color.from_stream(data)
    
        return cls(editor_properties, path_flags, spline_type, cling_path_control_data, editor_color)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xb9\x7f\x9f')  # 0xb0b97f9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.path_flags))

        data.write(b' \t\x1bT')  # 0x20091b54
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'I\x85\xa0\x99')  # 0x4985a099
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cling_path_control_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xdd\x86\xe2')  # 0xdd86e2
        data.write(b'\x00\x10')  # size
        self.editor_color.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ClingPathControlJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            path_flags=json_data['path_flags'],
            spline_type=SplineType.from_json(json_data['spline_type']),
            cling_path_control_data=ClingPathControlData.from_json(json_data['cling_path_control_data']),
            editor_color=Color.from_json(json_data['editor_color']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'path_flags': self.path_flags,
            'spline_type': self.spline_type.to_json(),
            'cling_path_control_data': self.cling_path_control_data.to_json(),
            'editor_color': self.editor_color.to_json(),
        }


def _decode_path_flags(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_editor_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xb0b97f9f: ('path_flags', _decode_path_flags),
    0x20091b54: ('spline_type', SplineType.from_stream),
    0x4985a099: ('cling_path_control_data', ClingPathControlData.from_stream),
    0xdd86e2: ('editor_color', _decode_editor_color),
}

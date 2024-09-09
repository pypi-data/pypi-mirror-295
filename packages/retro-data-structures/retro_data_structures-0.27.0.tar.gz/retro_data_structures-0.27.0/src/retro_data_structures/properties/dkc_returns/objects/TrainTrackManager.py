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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct273 import UnknownStruct273
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct274 import UnknownStruct274
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct275 import UnknownStruct275

if typing.TYPE_CHECKING:
    class TrainTrackManagerJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        unknown_struct273: json_util.JsonObject
        unknown_struct274: json_util.JsonObject
        unknown_struct275: json_util.JsonObject
    

@dataclasses.dataclass()
class TrainTrackManager(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    unknown_struct273: UnknownStruct273 = dataclasses.field(default_factory=UnknownStruct273, metadata={
        'reflection': FieldReflection[UnknownStruct273](
            UnknownStruct273, id=0x3edf57b4, original_name='UnknownStruct273', from_json=UnknownStruct273.from_json, to_json=UnknownStruct273.to_json
        ),
    })
    unknown_struct274: UnknownStruct274 = dataclasses.field(default_factory=UnknownStruct274, metadata={
        'reflection': FieldReflection[UnknownStruct274](
            UnknownStruct274, id=0x019c9392, original_name='UnknownStruct274', from_json=UnknownStruct274.from_json, to_json=UnknownStruct274.to_json
        ),
    })
    unknown_struct275: UnknownStruct275 = dataclasses.field(default_factory=UnknownStruct275, metadata={
        'reflection': FieldReflection[UnknownStruct275](
            UnknownStruct275, id=0x1871ba9b, original_name='UnknownStruct275', from_json=UnknownStruct275.from_json, to_json=UnknownStruct275.to_json
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
        return 'TMGR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_MoleTrain.rso']

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
        assert property_id == 0x3edf57b4
        unknown_struct273 = UnknownStruct273.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x019c9392
        unknown_struct274 = UnknownStruct274.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1871ba9b
        unknown_struct275 = UnknownStruct275.from_stream(data, property_size)
    
        return cls(editor_properties, unknown_struct273, unknown_struct274, unknown_struct275)

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

        data.write(b'>\xdfW\xb4')  # 0x3edf57b4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct273.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\x9c\x93\x92')  # 0x19c9392
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct274.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18q\xba\x9b')  # 0x1871ba9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct275.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TrainTrackManagerJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            unknown_struct273=UnknownStruct273.from_json(json_data['unknown_struct273']),
            unknown_struct274=UnknownStruct274.from_json(json_data['unknown_struct274']),
            unknown_struct275=UnknownStruct275.from_json(json_data['unknown_struct275']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct273': self.unknown_struct273.to_json(),
            'unknown_struct274': self.unknown_struct274.to_json(),
            'unknown_struct275': self.unknown_struct275.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x3edf57b4: ('unknown_struct273', UnknownStruct273.from_stream),
    0x19c9392: ('unknown_struct274', UnknownStruct274.from_stream),
    0x1871ba9b: ('unknown_struct275', UnknownStruct275.from_stream),
}

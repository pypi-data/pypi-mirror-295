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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties

if typing.TYPE_CHECKING:
    class TransitionScreenJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        transition_type: int
        unknown_0x5106feb9: bool
        unknown_0x49469271: bool
    

@dataclasses.dataclass()
class TransitionScreen(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    transition_type: enums.TransitionType = dataclasses.field(default=enums.TransitionType.Unknown1, metadata={
        'reflection': FieldReflection[enums.TransitionType](
            enums.TransitionType, id=0xf5e86958, original_name='TransitionType', from_json=enums.TransitionType.from_json, to_json=enums.TransitionType.to_json
        ),
    })
    unknown_0x5106feb9: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5106feb9, original_name='Unknown'
        ),
    })
    unknown_0x49469271: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x49469271, original_name='Unknown'
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
        return 'TRSC'

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
        assert property_id == 0xf5e86958
        transition_type = enums.TransitionType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5106feb9
        unknown_0x5106feb9 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x49469271
        unknown_0x49469271 = struct.unpack('>?', data.read(1))[0]
    
        return cls(editor_properties, transition_type, unknown_0x5106feb9, unknown_0x49469271)

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

        data.write(b'\xf5\xe8iX')  # 0xf5e86958
        data.write(b'\x00\x04')  # size
        self.transition_type.to_stream(data)

        data.write(b'Q\x06\xfe\xb9')  # 0x5106feb9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5106feb9))

        data.write(b'IF\x92q')  # 0x49469271
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x49469271))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TransitionScreenJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            transition_type=enums.TransitionType.from_json(json_data['transition_type']),
            unknown_0x5106feb9=json_data['unknown_0x5106feb9'],
            unknown_0x49469271=json_data['unknown_0x49469271'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'transition_type': self.transition_type.to_json(),
            'unknown_0x5106feb9': self.unknown_0x5106feb9,
            'unknown_0x49469271': self.unknown_0x49469271,
        }


def _decode_transition_type(data: typing.BinaryIO, property_size: int):
    return enums.TransitionType.from_stream(data)


def _decode_unknown_0x5106feb9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x49469271(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xf5e86958: ('transition_type', _decode_transition_type),
    0x5106feb9: ('unknown_0x5106feb9', _decode_unknown_0x5106feb9),
    0x49469271: ('unknown_0x49469271', _decode_unknown_0x49469271),
}

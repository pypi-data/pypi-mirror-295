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
    class EOLDisplayJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        give_item_award: bool
        item_award: int
    

@dataclasses.dataclass()
class EOLDisplay(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    give_item_award: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x87c8b399, original_name='GiveItemAward'
        ),
    })
    item_award: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana, metadata={
        'reflection': FieldReflection[enums.PlayerItem](
            enums.PlayerItem, id=0xe7338932, original_name='ItemAward', from_json=enums.PlayerItem.from_json, to_json=enums.PlayerItem.to_json
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
        return 'EOLD'

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
        if property_count != 3:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x87c8b399
        give_item_award = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe7338932
        item_award = enums.PlayerItem.from_stream(data)
    
        return cls(editor_properties, give_item_award, item_award)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x87\xc8\xb3\x99')  # 0x87c8b399
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.give_item_award))

        data.write(b'\xe73\x892')  # 0xe7338932
        data.write(b'\x00\x04')  # size
        self.item_award.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("EOLDisplayJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            give_item_award=json_data['give_item_award'],
            item_award=enums.PlayerItem.from_json(json_data['item_award']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'give_item_award': self.give_item_award,
            'item_award': self.item_award.to_json(),
        }


def _decode_give_item_award(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_item_award(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x87c8b399: ('give_item_award', _decode_give_item_award),
    0xe7338932: ('item_award', _decode_item_award),
}

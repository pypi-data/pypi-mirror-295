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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct146Json(typing_extensions.TypedDict):
        unknown_struct28: json_util.JsonObject
        horizontal_instructions: int
        strg: int
        title_string_table: int
    

@dataclasses.dataclass()
class UnknownStruct146(BaseProperty):
    unknown_struct28: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0xc68bc9ec, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    horizontal_instructions: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf2009132, original_name='HorizontalInstructions'
        ),
    })
    strg: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x00ce7374, original_name='STRG'
        ),
    })
    title_string_table: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc7b183b7, original_name='TitleStringTable'
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
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc68bc9ec
        unknown_struct28 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf2009132
        horizontal_instructions = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00ce7374
        strg = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc7b183b7
        title_string_table = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_struct28, horizontal_instructions, strg, title_string_table)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xc6\x8b\xc9\xec')  # 0xc68bc9ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2\x00\x912')  # 0xf2009132
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.horizontal_instructions))

        data.write(b'\x00\xcest')  # 0xce7374
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xc7\xb1\x83\xb7')  # 0xc7b183b7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title_string_table))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct146Json", data)
        return cls(
            unknown_struct28=UnknownStruct28.from_json(json_data['unknown_struct28']),
            horizontal_instructions=json_data['horizontal_instructions'],
            strg=json_data['strg'],
            title_string_table=json_data['title_string_table'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct28': self.unknown_struct28.to_json(),
            'horizontal_instructions': self.horizontal_instructions,
            'strg': self.strg,
            'title_string_table': self.title_string_table,
        }


def _decode_horizontal_instructions(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc68bc9ec: ('unknown_struct28', UnknownStruct28.from_stream),
    0xf2009132: ('horizontal_instructions', _decode_horizontal_instructions),
    0xce7374: ('strg', _decode_strg),
    0xc7b183b7: ('title_string_table', _decode_title_string_table),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct170Json(typing_extensions.TypedDict):
        unknown_struct29: json_util.JsonObject
        title_strings: int
        instruction: int
        instruction_core: int
        back: int
        back_core: int
        unknown_0x3dc0f2be: int
        unknown_0x6fdabad6: int
        strg: int
        text_background: int
    

@dataclasses.dataclass()
class UnknownStruct170(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29, metadata={
        'reflection': FieldReflection[UnknownStruct29](
            UnknownStruct29, id=0x305b3232, original_name='UnknownStruct29', from_json=UnknownStruct29.from_json, to_json=UnknownStruct29.to_json
        ),
    })
    title_strings: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x17c847c0, original_name='TitleStrings'
        ),
    })
    instruction: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x37fd1913, original_name='Instruction'
        ),
    })
    instruction_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa14f34ca, original_name='InstructionCore'
        ),
    })
    back: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe9336455, original_name='Back'
        ),
    })
    back_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x770bcd3b, original_name='BackCore'
        ),
    })
    unknown_0x3dc0f2be: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3dc0f2be, original_name='Unknown'
        ),
    })
    unknown_0x6fdabad6: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6fdabad6, original_name='Unknown'
        ),
    })
    strg: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9c24f6c5, original_name='STRG'
        ),
    })
    text_background: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe119319b, original_name='TextBackground'
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
        assert property_id == 0x305b3232
        unknown_struct29 = UnknownStruct29.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x17c847c0
        title_strings = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x37fd1913
        instruction = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa14f34ca
        instruction_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9336455
        back = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x770bcd3b
        back_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3dc0f2be
        unknown_0x3dc0f2be = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6fdabad6
        unknown_0x6fdabad6 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9c24f6c5
        strg = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe119319b
        text_background = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_struct29, title_strings, instruction, instruction_core, back, back_core, unknown_0x3dc0f2be, unknown_0x6fdabad6, strg, text_background)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'0[22')  # 0x305b3232
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xc8G\xc0')  # 0x17c847c0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title_strings))

        data.write(b'7\xfd\x19\x13')  # 0x37fd1913
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.instruction))

        data.write(b'\xa1O4\xca')  # 0xa14f34ca
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.instruction_core))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'=\xc0\xf2\xbe')  # 0x3dc0f2be
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x3dc0f2be))

        data.write(b'o\xda\xba\xd6')  # 0x6fdabad6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x6fdabad6))

        data.write(b'\x9c$\xf6\xc5')  # 0x9c24f6c5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct170Json", data)
        return cls(
            unknown_struct29=UnknownStruct29.from_json(json_data['unknown_struct29']),
            title_strings=json_data['title_strings'],
            instruction=json_data['instruction'],
            instruction_core=json_data['instruction_core'],
            back=json_data['back'],
            back_core=json_data['back_core'],
            unknown_0x3dc0f2be=json_data['unknown_0x3dc0f2be'],
            unknown_0x6fdabad6=json_data['unknown_0x6fdabad6'],
            strg=json_data['strg'],
            text_background=json_data['text_background'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title_strings': self.title_strings,
            'instruction': self.instruction,
            'instruction_core': self.instruction_core,
            'back': self.back,
            'back_core': self.back_core,
            'unknown_0x3dc0f2be': self.unknown_0x3dc0f2be,
            'unknown_0x6fdabad6': self.unknown_0x6fdabad6,
            'strg': self.strg,
            'text_background': self.text_background,
        }


def _decode_title_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_instruction(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_instruction_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x3dc0f2be(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x6fdabad6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', UnknownStruct29.from_stream),
    0x17c847c0: ('title_strings', _decode_title_strings),
    0x37fd1913: ('instruction', _decode_instruction),
    0xa14f34ca: ('instruction_core', _decode_instruction_core),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0x3dc0f2be: ('unknown_0x3dc0f2be', _decode_unknown_0x3dc0f2be),
    0x6fdabad6: ('unknown_0x6fdabad6', _decode_unknown_0x6fdabad6),
    0x9c24f6c5: ('strg', _decode_strg),
    0xe119319b: ('text_background', _decode_text_background),
}

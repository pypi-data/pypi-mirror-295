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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct160 import UnknownStruct160
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct163 import UnknownStruct163
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct164Json(typing_extensions.TypedDict):
        gui_frame: int
        title_text: int
        continue_text: int
        core_continue_text: int
        quit_text: int
        strg: int
        quit_confirm_text: int
        unknown: json_util.JsonObject
        unknown_struct163: json_util.JsonObject
        unknown_struct26_0x860139ad: json_util.JsonObject
        unknown_struct26_0x6a598a9b: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct164(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    title_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xefc5a137, original_name='TitleText'
        ),
    })
    continue_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1f5b271d, original_name='ContinueText'
        ),
    })
    core_continue_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x449f5275, original_name='CoreContinueText'
        ),
    })
    quit_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7049ee4d, original_name='QuitText'
        ),
    })
    strg: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa90107c6, original_name='STRG'
        ),
    })
    quit_confirm_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xfdb3aac2, original_name='QuitConfirmText'
        ),
    })
    unknown: UnknownStruct160 = dataclasses.field(default_factory=UnknownStruct160, metadata={
        'reflection': FieldReflection[UnknownStruct160](
            UnknownStruct160, id=0x2a83fbbb, original_name='Unknown', from_json=UnknownStruct160.from_json, to_json=UnknownStruct160.to_json
        ),
    })
    unknown_struct163: UnknownStruct163 = dataclasses.field(default_factory=UnknownStruct163, metadata={
        'reflection': FieldReflection[UnknownStruct163](
            UnknownStruct163, id=0x78673ab6, original_name='UnknownStruct163', from_json=UnknownStruct163.from_json, to_json=UnknownStruct163.to_json
        ),
    })
    unknown_struct26_0x860139ad: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x860139ad, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x6a598a9b: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x6a598a9b, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xefc5a137
        title_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1f5b271d
        continue_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x449f5275
        core_continue_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7049ee4d
        quit_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa90107c6
        strg = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfdb3aac2
        quit_confirm_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2a83fbbb
        unknown = UnknownStruct160.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x78673ab6
        unknown_struct163 = UnknownStruct163.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x860139ad
        unknown_struct26_0x860139ad = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a598a9b
        unknown_struct26_0x6a598a9b = UnknownStruct26.from_stream(data, property_size)
    
        return cls(gui_frame, title_text, continue_text, core_continue_text, quit_text, strg, quit_confirm_text, unknown, unknown_struct163, unknown_struct26_0x860139ad, unknown_struct26_0x6a598a9b)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xef\xc5\xa17')  # 0xefc5a137
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title_text))

        data.write(b"\x1f['\x1d")  # 0x1f5b271d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.continue_text))

        data.write(b'D\x9fRu')  # 0x449f5275
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.core_continue_text))

        data.write(b'pI\xeeM')  # 0x7049ee4d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.quit_text))

        data.write(b'\xa9\x01\x07\xc6')  # 0xa90107c6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xfd\xb3\xaa\xc2')  # 0xfdb3aac2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.quit_confirm_text))

        data.write(b'*\x83\xfb\xbb')  # 0x2a83fbbb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'xg:\xb6')  # 0x78673ab6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct163.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\x019\xad')  # 0x860139ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x860139ad.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jY\x8a\x9b')  # 0x6a598a9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x6a598a9b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct164Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            title_text=json_data['title_text'],
            continue_text=json_data['continue_text'],
            core_continue_text=json_data['core_continue_text'],
            quit_text=json_data['quit_text'],
            strg=json_data['strg'],
            quit_confirm_text=json_data['quit_confirm_text'],
            unknown=UnknownStruct160.from_json(json_data['unknown']),
            unknown_struct163=UnknownStruct163.from_json(json_data['unknown_struct163']),
            unknown_struct26_0x860139ad=UnknownStruct26.from_json(json_data['unknown_struct26_0x860139ad']),
            unknown_struct26_0x6a598a9b=UnknownStruct26.from_json(json_data['unknown_struct26_0x6a598a9b']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'title_text': self.title_text,
            'continue_text': self.continue_text,
            'core_continue_text': self.core_continue_text,
            'quit_text': self.quit_text,
            'strg': self.strg,
            'quit_confirm_text': self.quit_confirm_text,
            'unknown': self.unknown.to_json(),
            'unknown_struct163': self.unknown_struct163.to_json(),
            'unknown_struct26_0x860139ad': self.unknown_struct26_0x860139ad.to_json(),
            'unknown_struct26_0x6a598a9b': self.unknown_struct26_0x6a598a9b.to_json(),
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_continue_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_core_continue_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_quit_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_quit_confirm_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xefc5a137: ('title_text', _decode_title_text),
    0x1f5b271d: ('continue_text', _decode_continue_text),
    0x449f5275: ('core_continue_text', _decode_core_continue_text),
    0x7049ee4d: ('quit_text', _decode_quit_text),
    0xa90107c6: ('strg', _decode_strg),
    0xfdb3aac2: ('quit_confirm_text', _decode_quit_confirm_text),
    0x2a83fbbb: ('unknown', UnknownStruct160.from_stream),
    0x78673ab6: ('unknown_struct163', UnknownStruct163.from_stream),
    0x860139ad: ('unknown_struct26_0x860139ad', UnknownStruct26.from_stream),
    0x6a598a9b: ('unknown_struct26_0x6a598a9b', UnknownStruct26.from_stream),
}

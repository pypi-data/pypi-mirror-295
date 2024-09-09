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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct177Json(typing_extensions.TypedDict):
        gui_frame: int
        unknown_struct27: json_util.JsonObject
        add_drop: int
        summary: int
        options: int
        quit: int
        quit_confirm: int
        select: int
        select_core: int
        return_: int
        return_core: int
    

@dataclasses.dataclass()
class UnknownStruct177(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
        ),
    })
    add_drop: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc8b7dbd5, original_name='AddDrop'
        ),
    })
    summary: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x46993681, original_name='Summary'
        ),
    })
    options: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xace4067e, original_name='Options'
        ),
    })
    quit: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd27fca30, original_name='Quit'
        ),
    })
    quit_confirm: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb85aef47, original_name='QuitConfirm'
        ),
    })
    select: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD', 'STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x8ed65283, original_name='Select'
        ),
    })
    select_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa40d410e, original_name='SelectCore'
        ),
    })
    return_: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x471fea86, original_name='Return'
        ),
    })
    return_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa01e0887, original_name='ReturnCore'
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
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc8b7dbd5
        add_drop = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46993681
        summary = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xace4067e
        options = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd27fca30
        quit = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb85aef47
        quit_confirm = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ed65283
        select = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa40d410e
        select_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x471fea86
        return_ = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa01e0887
        return_core = struct.unpack(">Q", data.read(8))[0]
    
        return cls(gui_frame, unknown_struct27, add_drop, summary, options, quit, quit_confirm, select, select_core, return_, return_core)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8\xb7\xdb\xd5')  # 0xc8b7dbd5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.add_drop))

        data.write(b'F\x996\x81')  # 0x46993681
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.summary))

        data.write(b'\xac\xe4\x06~')  # 0xace4067e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.options))

        data.write(b'\xd2\x7f\xca0')  # 0xd27fca30
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.quit))

        data.write(b'\xb8Z\xefG')  # 0xb85aef47
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.quit_confirm))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xa4\rA\x0e')  # 0xa40d410e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_core))

        data.write(b'G\x1f\xea\x86')  # 0x471fea86
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_))

        data.write(b'\xa0\x1e\x08\x87')  # 0xa01e0887
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_core))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct177Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            add_drop=json_data['add_drop'],
            summary=json_data['summary'],
            options=json_data['options'],
            quit=json_data['quit'],
            quit_confirm=json_data['quit_confirm'],
            select=json_data['select'],
            select_core=json_data['select_core'],
            return_=json_data['return_'],
            return_core=json_data['return_core'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'add_drop': self.add_drop,
            'summary': self.summary,
            'options': self.options,
            'quit': self.quit,
            'quit_confirm': self.quit_confirm,
            'select': self.select,
            'select_core': self.select_core,
            'return_': self.return_,
            'return_core': self.return_core,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_add_drop(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_summary(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_options(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_quit(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_quit_confirm(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0xc8b7dbd5: ('add_drop', _decode_add_drop),
    0x46993681: ('summary', _decode_summary),
    0xace4067e: ('options', _decode_options),
    0xd27fca30: ('quit', _decode_quit),
    0xb85aef47: ('quit_confirm', _decode_quit_confirm),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0x471fea86: ('return_', _decode_return_),
    0xa01e0887: ('return_core', _decode_return_core),
}

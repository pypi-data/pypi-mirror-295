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
    class UnknownStruct166Json(typing_extensions.TypedDict):
        gui_frame: int
        freelook_text: int
        freelook_prompt_text: int
        strg_0xe8ac748d: int
        strg_0xfebbc04e: int
        strg_0x5eeb7f9d: int
        strg_0xcbc01154: int
        strg_0x777cf37f: int
        strg_0x66b1160b: int
        strg_0x7f1e6dec: int
        cancel_prompt_text: int
        strg_0x6b016db2: int
        select: int
        select_core: int
        menu: int
        menu_core: int
        unknown_struct27: json_util.JsonObject
        text_background: int
    

@dataclasses.dataclass()
class UnknownStruct166(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    freelook_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf5cb9f32, original_name='FreelookText'
        ),
    })
    freelook_prompt_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x21cb2d81, original_name='FreelookPromptText'
        ),
    })
    strg_0xe8ac748d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe8ac748d, original_name='STRG'
        ),
    })
    strg_0xfebbc04e: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xfebbc04e, original_name='STRG'
        ),
    })
    strg_0x5eeb7f9d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5eeb7f9d, original_name='STRG'
        ),
    })
    strg_0xcbc01154: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcbc01154, original_name='STRG'
        ),
    })
    strg_0x777cf37f: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x777cf37f, original_name='STRG'
        ),
    })
    strg_0x66b1160b: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x66b1160b, original_name='STRG'
        ),
    })
    strg_0x7f1e6dec: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7f1e6dec, original_name='STRG'
        ),
    })
    cancel_prompt_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb7990651, original_name='CancelPromptText'
        ),
    })
    strg_0x6b016db2: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6b016db2, original_name='STRG'
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
    menu: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xeacba755, original_name='Menu'
        ),
    })
    menu_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa18edf2d, original_name='MenuCore'
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
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
        if property_count != 18:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5cb9f32
        freelook_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x21cb2d81
        freelook_prompt_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe8ac748d
        strg_0xe8ac748d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfebbc04e
        strg_0xfebbc04e = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5eeb7f9d
        strg_0x5eeb7f9d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcbc01154
        strg_0xcbc01154 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x777cf37f
        strg_0x777cf37f = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x66b1160b
        strg_0x66b1160b = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f1e6dec
        strg_0x7f1e6dec = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb7990651
        cancel_prompt_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b016db2
        strg_0x6b016db2 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ed65283
        select = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa40d410e
        select_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeacba755
        menu = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa18edf2d
        menu_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe119319b
        text_background = struct.unpack(">Q", data.read(8))[0]
    
        return cls(gui_frame, freelook_text, freelook_prompt_text, strg_0xe8ac748d, strg_0xfebbc04e, strg_0x5eeb7f9d, strg_0xcbc01154, strg_0x777cf37f, strg_0x66b1160b, strg_0x7f1e6dec, cancel_prompt_text, strg_0x6b016db2, select, select_core, menu, menu_core, unknown_struct27, text_background)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xf5\xcb\x9f2')  # 0xf5cb9f32
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.freelook_text))

        data.write(b'!\xcb-\x81')  # 0x21cb2d81
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.freelook_prompt_text))

        data.write(b'\xe8\xact\x8d')  # 0xe8ac748d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xe8ac748d))

        data.write(b'\xfe\xbb\xc0N')  # 0xfebbc04e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xfebbc04e))

        data.write(b'^\xeb\x7f\x9d')  # 0x5eeb7f9d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x5eeb7f9d))

        data.write(b'\xcb\xc0\x11T')  # 0xcbc01154
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xcbc01154))

        data.write(b'w|\xf3\x7f')  # 0x777cf37f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x777cf37f))

        data.write(b'f\xb1\x16\x0b')  # 0x66b1160b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x66b1160b))

        data.write(b'\x7f\x1em\xec')  # 0x7f1e6dec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x7f1e6dec))

        data.write(b'\xb7\x99\x06Q')  # 0xb7990651
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel_prompt_text))

        data.write(b'k\x01m\xb2')  # 0x6b016db2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x6b016db2))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xa4\rA\x0e')  # 0xa40d410e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_core))

        data.write(b'\xea\xcb\xa7U')  # 0xeacba755
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.menu))

        data.write(b'\xa1\x8e\xdf-')  # 0xa18edf2d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.menu_core))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct166Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            freelook_text=json_data['freelook_text'],
            freelook_prompt_text=json_data['freelook_prompt_text'],
            strg_0xe8ac748d=json_data['strg_0xe8ac748d'],
            strg_0xfebbc04e=json_data['strg_0xfebbc04e'],
            strg_0x5eeb7f9d=json_data['strg_0x5eeb7f9d'],
            strg_0xcbc01154=json_data['strg_0xcbc01154'],
            strg_0x777cf37f=json_data['strg_0x777cf37f'],
            strg_0x66b1160b=json_data['strg_0x66b1160b'],
            strg_0x7f1e6dec=json_data['strg_0x7f1e6dec'],
            cancel_prompt_text=json_data['cancel_prompt_text'],
            strg_0x6b016db2=json_data['strg_0x6b016db2'],
            select=json_data['select'],
            select_core=json_data['select_core'],
            menu=json_data['menu'],
            menu_core=json_data['menu_core'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            text_background=json_data['text_background'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'freelook_text': self.freelook_text,
            'freelook_prompt_text': self.freelook_prompt_text,
            'strg_0xe8ac748d': self.strg_0xe8ac748d,
            'strg_0xfebbc04e': self.strg_0xfebbc04e,
            'strg_0x5eeb7f9d': self.strg_0x5eeb7f9d,
            'strg_0xcbc01154': self.strg_0xcbc01154,
            'strg_0x777cf37f': self.strg_0x777cf37f,
            'strg_0x66b1160b': self.strg_0x66b1160b,
            'strg_0x7f1e6dec': self.strg_0x7f1e6dec,
            'cancel_prompt_text': self.cancel_prompt_text,
            'strg_0x6b016db2': self.strg_0x6b016db2,
            'select': self.select,
            'select_core': self.select_core,
            'menu': self.menu,
            'menu_core': self.menu_core,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'text_background': self.text_background,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_freelook_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_freelook_prompt_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xe8ac748d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xfebbc04e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x5eeb7f9d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xcbc01154(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x777cf37f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x66b1160b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x7f1e6dec(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel_prompt_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x6b016db2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_menu(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_menu_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xf5cb9f32: ('freelook_text', _decode_freelook_text),
    0x21cb2d81: ('freelook_prompt_text', _decode_freelook_prompt_text),
    0xe8ac748d: ('strg_0xe8ac748d', _decode_strg_0xe8ac748d),
    0xfebbc04e: ('strg_0xfebbc04e', _decode_strg_0xfebbc04e),
    0x5eeb7f9d: ('strg_0x5eeb7f9d', _decode_strg_0x5eeb7f9d),
    0xcbc01154: ('strg_0xcbc01154', _decode_strg_0xcbc01154),
    0x777cf37f: ('strg_0x777cf37f', _decode_strg_0x777cf37f),
    0x66b1160b: ('strg_0x66b1160b', _decode_strg_0x66b1160b),
    0x7f1e6dec: ('strg_0x7f1e6dec', _decode_strg_0x7f1e6dec),
    0xb7990651: ('cancel_prompt_text', _decode_cancel_prompt_text),
    0x6b016db2: ('strg_0x6b016db2', _decode_strg_0x6b016db2),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0xeacba755: ('menu', _decode_menu),
    0xa18edf2d: ('menu_core', _decode_menu_core),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0xe119319b: ('text_background', _decode_text_background),
}

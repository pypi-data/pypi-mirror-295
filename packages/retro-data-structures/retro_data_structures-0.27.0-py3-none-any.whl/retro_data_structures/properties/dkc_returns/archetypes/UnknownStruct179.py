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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct179Json(typing_extensions.TypedDict):
        unknown_struct28_0xc68bc9ec: json_util.JsonObject
        unknown_struct28_0x569d9045: json_util.JsonObject
        unknown_struct28_0x67a7c770: json_util.JsonObject
        unknown_struct28_0x8c9c574c: json_util.JsonObject
        gui_frame: int
        unknown_struct27: json_util.JsonObject
        caud_0x9bf39933: int
        caud_0x7f33c52c: int
        caud_0xd239b11f: int
        caud_0xf5427fd9: int
        strg_0x970e5f4f: int
        strg_0xa0efb8dc: int
        button: int
        select: int
        select_core: int
        back: int
        back_core: int
        strg_0x43054f47: int
        yes_string: int
        strg_0xbe564845: int
        no_string: int
        no_string_core: int
        ok_string: int
        strg_0xf5340e52: int
        add_button_string: int
        strg_0x56245afc: int
        add_prompt_string: int
        strg_0xbab119d6: int
        drop_button_string: int
        drop_prompt_string: int
        strg_0x23ef5c35: int
        strg_0xd590f85d: int
        dest_true_text: int
        strg_0xcc2e857d: int
        strg_0x8abad426: int
        strg_0xc92542e8: int
        strg_0x9cbfa0bc: int
        strg_0xaf9a52cc: int
    

@dataclasses.dataclass()
class UnknownStruct179(BaseProperty):
    unknown_struct28_0xc68bc9ec: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0xc68bc9ec, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0x569d9045: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x569d9045, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0x67a7c770: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x67a7c770, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0x8c9c574c: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x8c9c574c, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
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
    caud_0x9bf39933: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9bf39933, original_name='CAUD'
        ),
    })
    caud_0x7f33c52c: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7f33c52c, original_name='CAUD'
        ),
    })
    caud_0xd239b11f: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd239b11f, original_name='CAUD'
        ),
    })
    caud_0xf5427fd9: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf5427fd9, original_name='CAUD'
        ),
    })
    strg_0x970e5f4f: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x970e5f4f, original_name='STRG'
        ),
    })
    strg_0xa0efb8dc: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa0efb8dc, original_name='STRG'
        ),
    })
    button: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x04e45235, original_name='Button'
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
    strg_0x43054f47: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x43054f47, original_name='STRG'
        ),
    })
    yes_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe2ebe3b3, original_name='YesString'
        ),
    })
    strg_0xbe564845: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbe564845, original_name='STRG'
        ),
    })
    no_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe8dcbc00, original_name='NoString'
        ),
    })
    no_string_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa6a38996, original_name='NoStringCore'
        ),
    })
    ok_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x364c5efa, original_name='OkString'
        ),
    })
    strg_0xf5340e52: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf5340e52, original_name='STRG'
        ),
    })
    add_button_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x708eb465, original_name='AddButtonString'
        ),
    })
    strg_0x56245afc: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x56245afc, original_name='STRG'
        ),
    })
    add_prompt_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6930c945, original_name='AddPromptString'
        ),
    })
    strg_0xbab119d6: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbab119d6, original_name='STRG'
        ),
    })
    drop_button_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x022805ff, original_name='DropButtonString'
        ),
    })
    drop_prompt_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1b9678df, original_name='DropPromptString'
        ),
    })
    strg_0x23ef5c35: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x23ef5c35, original_name='STRG'
        ),
    })
    strg_0xd590f85d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd590f85d, original_name='STRG'
        ),
    })
    dest_true_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3a512115, original_name='DestTrueText'
        ),
    })
    strg_0xcc2e857d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcc2e857d, original_name='STRG'
        ),
    })
    strg_0x8abad426: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x8abad426, original_name='STRG'
        ),
    })
    strg_0xc92542e8: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc92542e8, original_name='STRG'
        ),
    })
    strg_0x9cbfa0bc: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9cbfa0bc, original_name='STRG'
        ),
    })
    strg_0xaf9a52cc: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xaf9a52cc, original_name='STRG'
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
        if property_count != 38:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc68bc9ec
        unknown_struct28_0xc68bc9ec = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x569d9045
        unknown_struct28_0x569d9045 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67a7c770
        unknown_struct28_0x67a7c770 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8c9c574c
        unknown_struct28_0x8c9c574c = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9bf39933
        caud_0x9bf39933 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f33c52c
        caud_0x7f33c52c = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd239b11f
        caud_0xd239b11f = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5427fd9
        caud_0xf5427fd9 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x970e5f4f
        strg_0x970e5f4f = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa0efb8dc
        strg_0xa0efb8dc = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x04e45235
        button = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ed65283
        select = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa40d410e
        select_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9336455
        back = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x770bcd3b
        back_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43054f47
        strg_0x43054f47 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2ebe3b3
        yes_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbe564845
        strg_0xbe564845 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe8dcbc00
        no_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa6a38996
        no_string_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x364c5efa
        ok_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5340e52
        strg_0xf5340e52 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x708eb465
        add_button_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x56245afc
        strg_0x56245afc = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6930c945
        add_prompt_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbab119d6
        strg_0xbab119d6 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x022805ff
        drop_button_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b9678df
        drop_prompt_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x23ef5c35
        strg_0x23ef5c35 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd590f85d
        strg_0xd590f85d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a512115
        dest_true_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcc2e857d
        strg_0xcc2e857d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8abad426
        strg_0x8abad426 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc92542e8
        strg_0xc92542e8 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9cbfa0bc
        strg_0x9cbfa0bc = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaf9a52cc
        strg_0xaf9a52cc = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_struct28_0xc68bc9ec, unknown_struct28_0x569d9045, unknown_struct28_0x67a7c770, unknown_struct28_0x8c9c574c, gui_frame, unknown_struct27, caud_0x9bf39933, caud_0x7f33c52c, caud_0xd239b11f, caud_0xf5427fd9, strg_0x970e5f4f, strg_0xa0efb8dc, button, select, select_core, back, back_core, strg_0x43054f47, yes_string, strg_0xbe564845, no_string, no_string_core, ok_string, strg_0xf5340e52, add_button_string, strg_0x56245afc, add_prompt_string, strg_0xbab119d6, drop_button_string, drop_prompt_string, strg_0x23ef5c35, strg_0xd590f85d, dest_true_text, strg_0xcc2e857d, strg_0x8abad426, strg_0xc92542e8, strg_0x9cbfa0bc, strg_0xaf9a52cc)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00&')  # 38 properties

        data.write(b'\xc6\x8b\xc9\xec')  # 0xc68bc9ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xc68bc9ec.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x9d\x90E')  # 0x569d9045
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x569d9045.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xa7\xc7p')  # 0x67a7c770
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x67a7c770.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c\x9cWL')  # 0x8c9c574c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x8c9c574c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

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

        data.write(b'\x9b\xf3\x993')  # 0x9bf39933
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x9bf39933))

        data.write(b'\x7f3\xc5,')  # 0x7f33c52c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x7f33c52c))

        data.write(b'\xd29\xb1\x1f')  # 0xd239b11f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xd239b11f))

        data.write(b'\xf5B\x7f\xd9')  # 0xf5427fd9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xf5427fd9))

        data.write(b'\x97\x0e_O')  # 0x970e5f4f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x970e5f4f))

        data.write(b'\xa0\xef\xb8\xdc')  # 0xa0efb8dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xa0efb8dc))

        data.write(b'\x04\xe4R5')  # 0x4e45235
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.button))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xa4\rA\x0e')  # 0xa40d410e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_core))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'C\x05OG')  # 0x43054f47
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x43054f47))

        data.write(b'\xe2\xeb\xe3\xb3')  # 0xe2ebe3b3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes_string))

        data.write(b'\xbeVHE')  # 0xbe564845
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xbe564845))

        data.write(b'\xe8\xdc\xbc\x00')  # 0xe8dcbc00
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_string))

        data.write(b'\xa6\xa3\x89\x96')  # 0xa6a38996
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_string_core))

        data.write(b'6L^\xfa')  # 0x364c5efa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ok_string))

        data.write(b'\xf54\x0eR')  # 0xf5340e52
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xf5340e52))

        data.write(b'p\x8e\xb4e')  # 0x708eb465
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.add_button_string))

        data.write(b'V$Z\xfc')  # 0x56245afc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x56245afc))

        data.write(b'i0\xc9E')  # 0x6930c945
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.add_prompt_string))

        data.write(b'\xba\xb1\x19\xd6')  # 0xbab119d6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xbab119d6))

        data.write(b'\x02(\x05\xff')  # 0x22805ff
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.drop_button_string))

        data.write(b'\x1b\x96x\xdf')  # 0x1b9678df
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.drop_prompt_string))

        data.write(b'#\xef\\5')  # 0x23ef5c35
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x23ef5c35))

        data.write(b'\xd5\x90\xf8]')  # 0xd590f85d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xd590f85d))

        data.write(b':Q!\x15')  # 0x3a512115
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dest_true_text))

        data.write(b'\xcc.\x85}')  # 0xcc2e857d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xcc2e857d))

        data.write(b'\x8a\xba\xd4&')  # 0x8abad426
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x8abad426))

        data.write(b'\xc9%B\xe8')  # 0xc92542e8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xc92542e8))

        data.write(b'\x9c\xbf\xa0\xbc')  # 0x9cbfa0bc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x9cbfa0bc))

        data.write(b'\xaf\x9aR\xcc')  # 0xaf9a52cc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xaf9a52cc))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct179Json", data)
        return cls(
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(json_data['unknown_struct28_0xc68bc9ec']),
            unknown_struct28_0x569d9045=UnknownStruct28.from_json(json_data['unknown_struct28_0x569d9045']),
            unknown_struct28_0x67a7c770=UnknownStruct28.from_json(json_data['unknown_struct28_0x67a7c770']),
            unknown_struct28_0x8c9c574c=UnknownStruct28.from_json(json_data['unknown_struct28_0x8c9c574c']),
            gui_frame=json_data['gui_frame'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            caud_0x9bf39933=json_data['caud_0x9bf39933'],
            caud_0x7f33c52c=json_data['caud_0x7f33c52c'],
            caud_0xd239b11f=json_data['caud_0xd239b11f'],
            caud_0xf5427fd9=json_data['caud_0xf5427fd9'],
            strg_0x970e5f4f=json_data['strg_0x970e5f4f'],
            strg_0xa0efb8dc=json_data['strg_0xa0efb8dc'],
            button=json_data['button'],
            select=json_data['select'],
            select_core=json_data['select_core'],
            back=json_data['back'],
            back_core=json_data['back_core'],
            strg_0x43054f47=json_data['strg_0x43054f47'],
            yes_string=json_data['yes_string'],
            strg_0xbe564845=json_data['strg_0xbe564845'],
            no_string=json_data['no_string'],
            no_string_core=json_data['no_string_core'],
            ok_string=json_data['ok_string'],
            strg_0xf5340e52=json_data['strg_0xf5340e52'],
            add_button_string=json_data['add_button_string'],
            strg_0x56245afc=json_data['strg_0x56245afc'],
            add_prompt_string=json_data['add_prompt_string'],
            strg_0xbab119d6=json_data['strg_0xbab119d6'],
            drop_button_string=json_data['drop_button_string'],
            drop_prompt_string=json_data['drop_prompt_string'],
            strg_0x23ef5c35=json_data['strg_0x23ef5c35'],
            strg_0xd590f85d=json_data['strg_0xd590f85d'],
            dest_true_text=json_data['dest_true_text'],
            strg_0xcc2e857d=json_data['strg_0xcc2e857d'],
            strg_0x8abad426=json_data['strg_0x8abad426'],
            strg_0xc92542e8=json_data['strg_0xc92542e8'],
            strg_0x9cbfa0bc=json_data['strg_0x9cbfa0bc'],
            strg_0xaf9a52cc=json_data['strg_0xaf9a52cc'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_struct28_0x569d9045': self.unknown_struct28_0x569d9045.to_json(),
            'unknown_struct28_0x67a7c770': self.unknown_struct28_0x67a7c770.to_json(),
            'unknown_struct28_0x8c9c574c': self.unknown_struct28_0x8c9c574c.to_json(),
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'caud_0x9bf39933': self.caud_0x9bf39933,
            'caud_0x7f33c52c': self.caud_0x7f33c52c,
            'caud_0xd239b11f': self.caud_0xd239b11f,
            'caud_0xf5427fd9': self.caud_0xf5427fd9,
            'strg_0x970e5f4f': self.strg_0x970e5f4f,
            'strg_0xa0efb8dc': self.strg_0xa0efb8dc,
            'button': self.button,
            'select': self.select,
            'select_core': self.select_core,
            'back': self.back,
            'back_core': self.back_core,
            'strg_0x43054f47': self.strg_0x43054f47,
            'yes_string': self.yes_string,
            'strg_0xbe564845': self.strg_0xbe564845,
            'no_string': self.no_string,
            'no_string_core': self.no_string_core,
            'ok_string': self.ok_string,
            'strg_0xf5340e52': self.strg_0xf5340e52,
            'add_button_string': self.add_button_string,
            'strg_0x56245afc': self.strg_0x56245afc,
            'add_prompt_string': self.add_prompt_string,
            'strg_0xbab119d6': self.strg_0xbab119d6,
            'drop_button_string': self.drop_button_string,
            'drop_prompt_string': self.drop_prompt_string,
            'strg_0x23ef5c35': self.strg_0x23ef5c35,
            'strg_0xd590f85d': self.strg_0xd590f85d,
            'dest_true_text': self.dest_true_text,
            'strg_0xcc2e857d': self.strg_0xcc2e857d,
            'strg_0x8abad426': self.strg_0x8abad426,
            'strg_0xc92542e8': self.strg_0xc92542e8,
            'strg_0x9cbfa0bc': self.strg_0x9cbfa0bc,
            'strg_0xaf9a52cc': self.strg_0xaf9a52cc,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x9bf39933(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x7f33c52c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xd239b11f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xf5427fd9(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x970e5f4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xa0efb8dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_button(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x43054f47(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xbe564845(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no_string_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ok_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xf5340e52(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_add_button_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x56245afc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_add_prompt_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xbab119d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_drop_button_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_drop_prompt_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x23ef5c35(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xd590f85d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dest_true_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xcc2e857d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x8abad426(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xc92542e8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x9cbfa0bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xaf9a52cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', UnknownStruct28.from_stream),
    0x569d9045: ('unknown_struct28_0x569d9045', UnknownStruct28.from_stream),
    0x67a7c770: ('unknown_struct28_0x67a7c770', UnknownStruct28.from_stream),
    0x8c9c574c: ('unknown_struct28_0x8c9c574c', UnknownStruct28.from_stream),
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0x9bf39933: ('caud_0x9bf39933', _decode_caud_0x9bf39933),
    0x7f33c52c: ('caud_0x7f33c52c', _decode_caud_0x7f33c52c),
    0xd239b11f: ('caud_0xd239b11f', _decode_caud_0xd239b11f),
    0xf5427fd9: ('caud_0xf5427fd9', _decode_caud_0xf5427fd9),
    0x970e5f4f: ('strg_0x970e5f4f', _decode_strg_0x970e5f4f),
    0xa0efb8dc: ('strg_0xa0efb8dc', _decode_strg_0xa0efb8dc),
    0x4e45235: ('button', _decode_button),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0x43054f47: ('strg_0x43054f47', _decode_strg_0x43054f47),
    0xe2ebe3b3: ('yes_string', _decode_yes_string),
    0xbe564845: ('strg_0xbe564845', _decode_strg_0xbe564845),
    0xe8dcbc00: ('no_string', _decode_no_string),
    0xa6a38996: ('no_string_core', _decode_no_string_core),
    0x364c5efa: ('ok_string', _decode_ok_string),
    0xf5340e52: ('strg_0xf5340e52', _decode_strg_0xf5340e52),
    0x708eb465: ('add_button_string', _decode_add_button_string),
    0x56245afc: ('strg_0x56245afc', _decode_strg_0x56245afc),
    0x6930c945: ('add_prompt_string', _decode_add_prompt_string),
    0xbab119d6: ('strg_0xbab119d6', _decode_strg_0xbab119d6),
    0x22805ff: ('drop_button_string', _decode_drop_button_string),
    0x1b9678df: ('drop_prompt_string', _decode_drop_prompt_string),
    0x23ef5c35: ('strg_0x23ef5c35', _decode_strg_0x23ef5c35),
    0xd590f85d: ('strg_0xd590f85d', _decode_strg_0xd590f85d),
    0x3a512115: ('dest_true_text', _decode_dest_true_text),
    0xcc2e857d: ('strg_0xcc2e857d', _decode_strg_0xcc2e857d),
    0x8abad426: ('strg_0x8abad426', _decode_strg_0x8abad426),
    0xc92542e8: ('strg_0xc92542e8', _decode_strg_0xc92542e8),
    0x9cbfa0bc: ('strg_0x9cbfa0bc', _decode_strg_0x9cbfa0bc),
    0xaf9a52cc: ('strg_0xaf9a52cc', _decode_strg_0xaf9a52cc),
}

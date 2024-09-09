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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct167 import UnknownStruct167
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct168Json(typing_extensions.TypedDict):
        gui_frame: int
        unknown_struct29: json_util.JsonObject
        unknown_struct28: json_util.JsonObject
        unknown_struct167: json_util.JsonObject
        unknown_struct27: json_util.JsonObject
        caud_0x4d4749a8: int
        caud_0xdebfbd6e: int
        caud_0xc9e1c63a: int
        mirror_mode_sound: int
        time_attack_sound: int
        play_text: int
        time_attack_text: int
        mirror_mode_text: int
        strg: int
        inventory_text: int
        select: int
        select_core: int
        return_: int
        return_core: int
        inventory1_text: int
        inventory2_text: int
        inventory3_text: int
        inventory4_text: int
        inventory5_text: int
    

@dataclasses.dataclass()
class UnknownStruct168(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29, metadata={
        'reflection': FieldReflection[UnknownStruct29](
            UnknownStruct29, id=0x1145ae1b, original_name='UnknownStruct29', from_json=UnknownStruct29.from_json, to_json=UnknownStruct29.to_json
        ),
    })
    unknown_struct28: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x67a7c770, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct167: UnknownStruct167 = dataclasses.field(default_factory=UnknownStruct167, metadata={
        'reflection': FieldReflection[UnknownStruct167](
            UnknownStruct167, id=0x308b92dd, original_name='UnknownStruct167', from_json=UnknownStruct167.from_json, to_json=UnknownStruct167.to_json
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
        ),
    })
    caud_0x4d4749a8: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4d4749a8, original_name='CAUD'
        ),
    })
    caud_0xdebfbd6e: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xdebfbd6e, original_name='CAUD'
        ),
    })
    caud_0xc9e1c63a: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc9e1c63a, original_name='CAUD'
        ),
    })
    mirror_mode_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcf363b64, original_name='MirrorModeSound'
        ),
    })
    time_attack_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf49c4c1a, original_name='TimeAttackSound'
        ),
    })
    play_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x73538a50, original_name='PlayText'
        ),
    })
    time_attack_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3a1aff1f, original_name='TimeAttackText'
        ),
    })
    mirror_mode_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xfe4d493f, original_name='MirrorModeText'
        ),
    })
    strg: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x00b4ffdb, original_name='STRG'
        ),
    })
    inventory_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe2366eef, original_name='InventoryText'
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
    inventory1_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4bec8291, original_name='Inventory1Text'
        ),
    })
    inventory2_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa0db3992, original_name='Inventory2Text'
        ),
    })
    inventory3_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4f1952ac, original_name='Inventory3Text'
        ),
    })
    inventory4_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xadc549d5, original_name='Inventory4Text'
        ),
    })
    inventory5_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x420722eb, original_name='Inventory5Text'
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
        if property_count != 24:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1145ae1b
        unknown_struct29 = UnknownStruct29.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67a7c770
        unknown_struct28 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x308b92dd
        unknown_struct167 = UnknownStruct167.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4d4749a8
        caud_0x4d4749a8 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdebfbd6e
        caud_0xdebfbd6e = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc9e1c63a
        caud_0xc9e1c63a = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcf363b64
        mirror_mode_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf49c4c1a
        time_attack_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73538a50
        play_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a1aff1f
        time_attack_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe4d493f
        mirror_mode_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00b4ffdb
        strg = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2366eef
        inventory_text = struct.unpack(">Q", data.read(8))[0]
    
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4bec8291
        inventory1_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa0db3992
        inventory2_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4f1952ac
        inventory3_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xadc549d5
        inventory4_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x420722eb
        inventory5_text = struct.unpack(">Q", data.read(8))[0]
    
        return cls(gui_frame, unknown_struct29, unknown_struct28, unknown_struct167, unknown_struct27, caud_0x4d4749a8, caud_0xdebfbd6e, caud_0xc9e1c63a, mirror_mode_sound, time_attack_sound, play_text, time_attack_text, mirror_mode_text, strg, inventory_text, select, select_core, return_, return_core, inventory1_text, inventory2_text, inventory3_text, inventory4_text, inventory5_text)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\x11E\xae\x1b')  # 0x1145ae1b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xa7\xc7p')  # 0x67a7c770
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\x8b\x92\xdd')  # 0x308b92dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct167.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'MGI\xa8')  # 0x4d4749a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x4d4749a8))

        data.write(b'\xde\xbf\xbdn')  # 0xdebfbd6e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xdebfbd6e))

        data.write(b'\xc9\xe1\xc6:')  # 0xc9e1c63a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xc9e1c63a))

        data.write(b'\xcf6;d')  # 0xcf363b64
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.mirror_mode_sound))

        data.write(b'\xf4\x9cL\x1a')  # 0xf49c4c1a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.time_attack_sound))

        data.write(b'sS\x8aP')  # 0x73538a50
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.play_text))

        data.write(b':\x1a\xff\x1f')  # 0x3a1aff1f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.time_attack_text))

        data.write(b'\xfeMI?')  # 0xfe4d493f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.mirror_mode_text))

        data.write(b'\x00\xb4\xff\xdb')  # 0xb4ffdb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xe26n\xef')  # 0xe2366eef
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inventory_text))

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

        data.write(b'K\xec\x82\x91')  # 0x4bec8291
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inventory1_text))

        data.write(b'\xa0\xdb9\x92')  # 0xa0db3992
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inventory2_text))

        data.write(b'O\x19R\xac')  # 0x4f1952ac
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inventory3_text))

        data.write(b'\xad\xc5I\xd5')  # 0xadc549d5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inventory4_text))

        data.write(b'B\x07"\xeb')  # 0x420722eb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inventory5_text))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct168Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            unknown_struct29=UnknownStruct29.from_json(json_data['unknown_struct29']),
            unknown_struct28=UnknownStruct28.from_json(json_data['unknown_struct28']),
            unknown_struct167=UnknownStruct167.from_json(json_data['unknown_struct167']),
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            caud_0x4d4749a8=json_data['caud_0x4d4749a8'],
            caud_0xdebfbd6e=json_data['caud_0xdebfbd6e'],
            caud_0xc9e1c63a=json_data['caud_0xc9e1c63a'],
            mirror_mode_sound=json_data['mirror_mode_sound'],
            time_attack_sound=json_data['time_attack_sound'],
            play_text=json_data['play_text'],
            time_attack_text=json_data['time_attack_text'],
            mirror_mode_text=json_data['mirror_mode_text'],
            strg=json_data['strg'],
            inventory_text=json_data['inventory_text'],
            select=json_data['select'],
            select_core=json_data['select_core'],
            return_=json_data['return_'],
            return_core=json_data['return_core'],
            inventory1_text=json_data['inventory1_text'],
            inventory2_text=json_data['inventory2_text'],
            inventory3_text=json_data['inventory3_text'],
            inventory4_text=json_data['inventory4_text'],
            inventory5_text=json_data['inventory5_text'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct29': self.unknown_struct29.to_json(),
            'unknown_struct28': self.unknown_struct28.to_json(),
            'unknown_struct167': self.unknown_struct167.to_json(),
            'unknown_struct27': self.unknown_struct27.to_json(),
            'caud_0x4d4749a8': self.caud_0x4d4749a8,
            'caud_0xdebfbd6e': self.caud_0xdebfbd6e,
            'caud_0xc9e1c63a': self.caud_0xc9e1c63a,
            'mirror_mode_sound': self.mirror_mode_sound,
            'time_attack_sound': self.time_attack_sound,
            'play_text': self.play_text,
            'time_attack_text': self.time_attack_text,
            'mirror_mode_text': self.mirror_mode_text,
            'strg': self.strg,
            'inventory_text': self.inventory_text,
            'select': self.select,
            'select_core': self.select_core,
            'return_': self.return_,
            'return_core': self.return_core,
            'inventory1_text': self.inventory1_text,
            'inventory2_text': self.inventory2_text,
            'inventory3_text': self.inventory3_text,
            'inventory4_text': self.inventory4_text,
            'inventory5_text': self.inventory5_text,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x4d4749a8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xdebfbd6e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xc9e1c63a(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_mirror_mode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_time_attack_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_play_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_time_attack_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_mirror_mode_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inventory_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inventory1_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inventory2_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inventory3_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inventory4_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inventory5_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x1145ae1b: ('unknown_struct29', UnknownStruct29.from_stream),
    0x67a7c770: ('unknown_struct28', UnknownStruct28.from_stream),
    0x308b92dd: ('unknown_struct167', UnknownStruct167.from_stream),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0x4d4749a8: ('caud_0x4d4749a8', _decode_caud_0x4d4749a8),
    0xdebfbd6e: ('caud_0xdebfbd6e', _decode_caud_0xdebfbd6e),
    0xc9e1c63a: ('caud_0xc9e1c63a', _decode_caud_0xc9e1c63a),
    0xcf363b64: ('mirror_mode_sound', _decode_mirror_mode_sound),
    0xf49c4c1a: ('time_attack_sound', _decode_time_attack_sound),
    0x73538a50: ('play_text', _decode_play_text),
    0x3a1aff1f: ('time_attack_text', _decode_time_attack_text),
    0xfe4d493f: ('mirror_mode_text', _decode_mirror_mode_text),
    0xb4ffdb: ('strg', _decode_strg),
    0xe2366eef: ('inventory_text', _decode_inventory_text),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0x471fea86: ('return_', _decode_return_),
    0xa01e0887: ('return_core', _decode_return_core),
    0x4bec8291: ('inventory1_text', _decode_inventory1_text),
    0xa0db3992: ('inventory2_text', _decode_inventory2_text),
    0x4f1952ac: ('inventory3_text', _decode_inventory3_text),
    0xadc549d5: ('inventory4_text', _decode_inventory4_text),
    0x420722eb: ('inventory5_text', _decode_inventory5_text),
}

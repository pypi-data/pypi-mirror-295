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
    class UnknownStruct181Json(typing_extensions.TypedDict):
        hud_frame: int
        unknown_struct27: json_util.JsonObject
        unknown_struct28_0x67a7c770: json_util.JsonObject
        unknown_struct28_0xc68bc9ec: json_util.JsonObject
        unknown_0x9be6a5d6: float
        comment_delay: float
        comment_duration: float
        unknown_0xf34d7c81: int
        input_string: int
        strg_0xabc01c18: int
        first_entry_string: int
        first_exit_string: int
        generic_entry_strings: int
        generic_exit_strings: int
        strg_0x7f2a409c: int
        failed_key_string: int
        failed_capacity_string: int
        coin_icon_string: int
        exit_confirm: int
        select: int
        select_core: int
        return_text: int
        strg_0x9c31d707: int
    

@dataclasses.dataclass()
class UnknownStruct181(BaseProperty):
    hud_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf2299ed6, original_name='HUDFrame'
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
        ),
    })
    unknown_struct28_0x67a7c770: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x67a7c770, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0xc68bc9ec: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0xc68bc9ec, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_0x9be6a5d6: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9be6a5d6, original_name='Unknown'
        ),
    })
    comment_delay: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9ebe812d, original_name='CommentDelay'
        ),
    })
    comment_duration: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x531f1ce0, original_name='CommentDuration'
        ),
    })
    unknown_0xf34d7c81: int = dataclasses.field(default=3, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf34d7c81, original_name='Unknown'
        ),
    })
    input_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x200ebc5e, original_name='InputString'
        ),
    })
    strg_0xabc01c18: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xabc01c18, original_name='STRG'
        ),
    })
    first_entry_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3daf3b6a, original_name='FirstEntryString'
        ),
    })
    first_exit_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x8f61a255, original_name='FirstExitString'
        ),
    })
    generic_entry_strings: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc25f2e19, original_name='GenericEntryStrings'
        ),
    })
    generic_exit_strings: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x70cca12d, original_name='GenericExitStrings'
        ),
    })
    strg_0x7f2a409c: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7f2a409c, original_name='STRG'
        ),
    })
    failed_key_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2eb4a90d, original_name='FailedKeyString'
        ),
    })
    failed_capacity_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x891a741f, original_name='FailedCapacityString'
        ),
    })
    coin_icon_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x70a28554, original_name='CoinIconString'
        ),
    })
    exit_confirm: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7642ef52, original_name='ExitConfirm'
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
    return_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9585b587, original_name='ReturnText'
        ),
    })
    strg_0x9c31d707: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9c31d707, original_name='STRG'
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
        if property_count != 23:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf2299ed6
        hud_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67a7c770
        unknown_struct28_0x67a7c770 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc68bc9ec
        unknown_struct28_0xc68bc9ec = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9be6a5d6
        unknown_0x9be6a5d6 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ebe812d
        comment_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x531f1ce0
        comment_duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf34d7c81
        unknown_0xf34d7c81 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x200ebc5e
        input_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xabc01c18
        strg_0xabc01c18 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3daf3b6a
        first_entry_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f61a255
        first_exit_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc25f2e19
        generic_entry_strings = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x70cca12d
        generic_exit_strings = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f2a409c
        strg_0x7f2a409c = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2eb4a90d
        failed_key_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x891a741f
        failed_capacity_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x70a28554
        coin_icon_string = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7642ef52
        exit_confirm = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ed65283
        select = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa40d410e
        select_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9585b587
        return_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9c31d707
        strg_0x9c31d707 = struct.unpack(">Q", data.read(8))[0]
    
        return cls(hud_frame, unknown_struct27, unknown_struct28_0x67a7c770, unknown_struct28_0xc68bc9ec, unknown_0x9be6a5d6, comment_delay, comment_duration, unknown_0xf34d7c81, input_string, strg_0xabc01c18, first_entry_string, first_exit_string, generic_entry_strings, generic_exit_strings, strg_0x7f2a409c, failed_key_string, failed_capacity_string, coin_icon_string, exit_confirm, select, select_core, return_text, strg_0x9c31d707)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
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

        data.write(b'\xc6\x8b\xc9\xec')  # 0xc68bc9ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xc68bc9ec.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\xe6\xa5\xd6')  # 0x9be6a5d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9be6a5d6))

        data.write(b'\x9e\xbe\x81-')  # 0x9ebe812d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.comment_delay))

        data.write(b'S\x1f\x1c\xe0')  # 0x531f1ce0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.comment_duration))

        data.write(b'\xf3M|\x81')  # 0xf34d7c81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf34d7c81))

        data.write(b' \x0e\xbc^')  # 0x200ebc5e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.input_string))

        data.write(b'\xab\xc0\x1c\x18')  # 0xabc01c18
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xabc01c18))

        data.write(b'=\xaf;j')  # 0x3daf3b6a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.first_entry_string))

        data.write(b'\x8fa\xa2U')  # 0x8f61a255
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.first_exit_string))

        data.write(b'\xc2_.\x19')  # 0xc25f2e19
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.generic_entry_strings))

        data.write(b'p\xcc\xa1-')  # 0x70cca12d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.generic_exit_strings))

        data.write(b'\x7f*@\x9c')  # 0x7f2a409c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x7f2a409c))

        data.write(b'.\xb4\xa9\r')  # 0x2eb4a90d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.failed_key_string))

        data.write(b'\x89\x1at\x1f')  # 0x891a741f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.failed_capacity_string))

        data.write(b'p\xa2\x85T')  # 0x70a28554
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.coin_icon_string))

        data.write(b'vB\xefR')  # 0x7642ef52
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.exit_confirm))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xa4\rA\x0e')  # 0xa40d410e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_core))

        data.write(b'\x95\x85\xb5\x87')  # 0x9585b587
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_text))

        data.write(b'\x9c1\xd7\x07')  # 0x9c31d707
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x9c31d707))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct181Json", data)
        return cls(
            hud_frame=json_data['hud_frame'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            unknown_struct28_0x67a7c770=UnknownStruct28.from_json(json_data['unknown_struct28_0x67a7c770']),
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(json_data['unknown_struct28_0xc68bc9ec']),
            unknown_0x9be6a5d6=json_data['unknown_0x9be6a5d6'],
            comment_delay=json_data['comment_delay'],
            comment_duration=json_data['comment_duration'],
            unknown_0xf34d7c81=json_data['unknown_0xf34d7c81'],
            input_string=json_data['input_string'],
            strg_0xabc01c18=json_data['strg_0xabc01c18'],
            first_entry_string=json_data['first_entry_string'],
            first_exit_string=json_data['first_exit_string'],
            generic_entry_strings=json_data['generic_entry_strings'],
            generic_exit_strings=json_data['generic_exit_strings'],
            strg_0x7f2a409c=json_data['strg_0x7f2a409c'],
            failed_key_string=json_data['failed_key_string'],
            failed_capacity_string=json_data['failed_capacity_string'],
            coin_icon_string=json_data['coin_icon_string'],
            exit_confirm=json_data['exit_confirm'],
            select=json_data['select'],
            select_core=json_data['select_core'],
            return_text=json_data['return_text'],
            strg_0x9c31d707=json_data['strg_0x9c31d707'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'hud_frame': self.hud_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'unknown_struct28_0x67a7c770': self.unknown_struct28_0x67a7c770.to_json(),
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_0x9be6a5d6': self.unknown_0x9be6a5d6,
            'comment_delay': self.comment_delay,
            'comment_duration': self.comment_duration,
            'unknown_0xf34d7c81': self.unknown_0xf34d7c81,
            'input_string': self.input_string,
            'strg_0xabc01c18': self.strg_0xabc01c18,
            'first_entry_string': self.first_entry_string,
            'first_exit_string': self.first_exit_string,
            'generic_entry_strings': self.generic_entry_strings,
            'generic_exit_strings': self.generic_exit_strings,
            'strg_0x7f2a409c': self.strg_0x7f2a409c,
            'failed_key_string': self.failed_key_string,
            'failed_capacity_string': self.failed_capacity_string,
            'coin_icon_string': self.coin_icon_string,
            'exit_confirm': self.exit_confirm,
            'select': self.select,
            'select_core': self.select_core,
            'return_text': self.return_text,
            'strg_0x9c31d707': self.strg_0x9c31d707,
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x9be6a5d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_comment_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_comment_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf34d7c81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_input_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xabc01c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_first_entry_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_first_exit_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_generic_entry_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_generic_exit_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x7f2a409c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_failed_key_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_failed_capacity_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_coin_icon_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_exit_confirm(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x9c31d707(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0x67a7c770: ('unknown_struct28_0x67a7c770', UnknownStruct28.from_stream),
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', UnknownStruct28.from_stream),
    0x9be6a5d6: ('unknown_0x9be6a5d6', _decode_unknown_0x9be6a5d6),
    0x9ebe812d: ('comment_delay', _decode_comment_delay),
    0x531f1ce0: ('comment_duration', _decode_comment_duration),
    0xf34d7c81: ('unknown_0xf34d7c81', _decode_unknown_0xf34d7c81),
    0x200ebc5e: ('input_string', _decode_input_string),
    0xabc01c18: ('strg_0xabc01c18', _decode_strg_0xabc01c18),
    0x3daf3b6a: ('first_entry_string', _decode_first_entry_string),
    0x8f61a255: ('first_exit_string', _decode_first_exit_string),
    0xc25f2e19: ('generic_entry_strings', _decode_generic_entry_strings),
    0x70cca12d: ('generic_exit_strings', _decode_generic_exit_strings),
    0x7f2a409c: ('strg_0x7f2a409c', _decode_strg_0x7f2a409c),
    0x2eb4a90d: ('failed_key_string', _decode_failed_key_string),
    0x891a741f: ('failed_capacity_string', _decode_failed_capacity_string),
    0x70a28554: ('coin_icon_string', _decode_coin_icon_string),
    0x7642ef52: ('exit_confirm', _decode_exit_confirm),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0x9585b587: ('return_text', _decode_return_text),
    0x9c31d707: ('strg_0x9c31d707', _decode_strg_0x9c31d707),
}

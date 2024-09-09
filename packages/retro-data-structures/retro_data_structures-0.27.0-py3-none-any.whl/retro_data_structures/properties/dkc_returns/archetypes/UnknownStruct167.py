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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct167Json(typing_extensions.TypedDict):
        unknown_struct29: json_util.JsonObject
        unknown_struct27: json_util.JsonObject
        strg: int
        title: int
        back: int
        select: int
        caud_0x7b084ab6: int
        select_diddy_sound: int
        select_shield_sound: int
        select_heart_sound: int
        caud_0xa0c913a9: int
    

@dataclasses.dataclass()
class UnknownStruct167(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29, metadata={
        'reflection': FieldReflection[UnknownStruct29](
            UnknownStruct29, id=0x44f57507, original_name='UnknownStruct29', from_json=UnknownStruct29.from_json, to_json=UnknownStruct29.to_json
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
        ),
    })
    strg: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x013180f0, original_name='STRG'
        ),
    })
    title: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa4f20c17, original_name='Title'
        ),
    })
    back: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe9336455, original_name='Back'
        ),
    })
    select: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD', 'STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x8ed65283, original_name='Select'
        ),
    })
    caud_0x7b084ab6: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7b084ab6, original_name='CAUD'
        ),
    })
    select_diddy_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6667c9b1, original_name='SelectDiddySound'
        ),
    })
    select_shield_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x79d450b1, original_name='SelectShieldSound'
        ),
    })
    select_heart_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3cf94770, original_name='SelectHeartSound'
        ),
    })
    caud_0xa0c913a9: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa0c913a9, original_name='CAUD'
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
        assert property_id == 0x44f57507
        unknown_struct29 = UnknownStruct29.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x013180f0
        strg = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa4f20c17
        title = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9336455
        back = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ed65283
        select = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b084ab6
        caud_0x7b084ab6 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6667c9b1
        select_diddy_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x79d450b1
        select_shield_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3cf94770
        select_heart_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa0c913a9
        caud_0xa0c913a9 = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_struct29, unknown_struct27, strg, title, back, select, caud_0x7b084ab6, select_diddy_sound, select_shield_sound, select_heart_sound, caud_0xa0c913a9)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'D\xf5u\x07')  # 0x44f57507
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
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

        data.write(b'\x011\x80\xf0')  # 0x13180f0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'{\x08J\xb6')  # 0x7b084ab6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x7b084ab6))

        data.write(b'fg\xc9\xb1')  # 0x6667c9b1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_diddy_sound))

        data.write(b'y\xd4P\xb1')  # 0x79d450b1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_shield_sound))

        data.write(b'<\xf9Gp')  # 0x3cf94770
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_heart_sound))

        data.write(b'\xa0\xc9\x13\xa9')  # 0xa0c913a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xa0c913a9))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct167Json", data)
        return cls(
            unknown_struct29=UnknownStruct29.from_json(json_data['unknown_struct29']),
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            strg=json_data['strg'],
            title=json_data['title'],
            back=json_data['back'],
            select=json_data['select'],
            caud_0x7b084ab6=json_data['caud_0x7b084ab6'],
            select_diddy_sound=json_data['select_diddy_sound'],
            select_shield_sound=json_data['select_shield_sound'],
            select_heart_sound=json_data['select_heart_sound'],
            caud_0xa0c913a9=json_data['caud_0xa0c913a9'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'unknown_struct27': self.unknown_struct27.to_json(),
            'strg': self.strg,
            'title': self.title,
            'back': self.back,
            'select': self.select,
            'caud_0x7b084ab6': self.caud_0x7b084ab6,
            'select_diddy_sound': self.select_diddy_sound,
            'select_shield_sound': self.select_shield_sound,
            'select_heart_sound': self.select_heart_sound,
            'caud_0xa0c913a9': self.caud_0xa0c913a9,
        }


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x7b084ab6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_diddy_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_shield_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_heart_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xa0c913a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x44f57507: ('unknown_struct29', UnknownStruct29.from_stream),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0x13180f0: ('strg', _decode_strg),
    0xa4f20c17: ('title', _decode_title),
    0xe9336455: ('back', _decode_back),
    0x8ed65283: ('select', _decode_select),
    0x7b084ab6: ('caud_0x7b084ab6', _decode_caud_0x7b084ab6),
    0x6667c9b1: ('select_diddy_sound', _decode_select_diddy_sound),
    0x79d450b1: ('select_shield_sound', _decode_select_shield_sound),
    0x3cf94770: ('select_heart_sound', _decode_select_heart_sound),
    0xa0c913a9: ('caud_0xa0c913a9', _decode_caud_0xa0c913a9),
}

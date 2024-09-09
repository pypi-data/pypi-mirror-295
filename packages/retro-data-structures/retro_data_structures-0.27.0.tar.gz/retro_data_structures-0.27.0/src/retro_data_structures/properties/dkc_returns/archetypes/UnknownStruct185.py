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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct185Json(typing_extensions.TypedDict):
        caud_0xa28b199d: int
        caud_0x003e7991: int
        walking_sound: int
        arrival_sound: int
        enter_area_sound: int
        exit_area_sound: int
        highlight_area_sound: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xa28b199d, 0x3e7991, 0x87501d31, 0x72679165, 0xcc70e91c, 0xb2b02a99, 0x4392d0c4)


@dataclasses.dataclass()
class UnknownStruct185(BaseProperty):
    caud_0xa28b199d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa28b199d, original_name='CAUD'
        ),
    })
    caud_0x003e7991: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x003e7991, original_name='CAUD'
        ),
    })
    walking_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x87501d31, original_name='WalkingSound'
        ),
    })
    arrival_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x72679165, original_name='ArrivalSound'
        ),
    })
    enter_area_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcc70e91c, original_name='EnterAreaSound'
        ),
    })
    exit_area_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb2b02a99, original_name='ExitAreaSound'
        ),
    })
    highlight_area_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4392d0c4, original_name='HighlightAreaSound'
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
        if property_count != 7:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(98))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xa2\x8b\x19\x9d')  # 0xa28b199d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xa28b199d))

        data.write(b'\x00>y\x91')  # 0x3e7991
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x003e7991))

        data.write(b'\x87P\x1d1')  # 0x87501d31
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.walking_sound))

        data.write(b'rg\x91e')  # 0x72679165
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.arrival_sound))

        data.write(b'\xccp\xe9\x1c')  # 0xcc70e91c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.enter_area_sound))

        data.write(b'\xb2\xb0*\x99')  # 0xb2b02a99
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.exit_area_sound))

        data.write(b'C\x92\xd0\xc4')  # 0x4392d0c4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.highlight_area_sound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct185Json", data)
        return cls(
            caud_0xa28b199d=json_data['caud_0xa28b199d'],
            caud_0x003e7991=json_data['caud_0x003e7991'],
            walking_sound=json_data['walking_sound'],
            arrival_sound=json_data['arrival_sound'],
            enter_area_sound=json_data['enter_area_sound'],
            exit_area_sound=json_data['exit_area_sound'],
            highlight_area_sound=json_data['highlight_area_sound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'caud_0xa28b199d': self.caud_0xa28b199d,
            'caud_0x003e7991': self.caud_0x003e7991,
            'walking_sound': self.walking_sound,
            'arrival_sound': self.arrival_sound,
            'enter_area_sound': self.enter_area_sound,
            'exit_area_sound': self.exit_area_sound,
            'highlight_area_sound': self.highlight_area_sound,
        }


def _decode_caud_0xa28b199d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x003e7991(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_walking_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_arrival_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_enter_area_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_exit_area_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_highlight_area_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa28b199d: ('caud_0xa28b199d', _decode_caud_0xa28b199d),
    0x3e7991: ('caud_0x003e7991', _decode_caud_0x003e7991),
    0x87501d31: ('walking_sound', _decode_walking_sound),
    0x72679165: ('arrival_sound', _decode_arrival_sound),
    0xcc70e91c: ('enter_area_sound', _decode_enter_area_sound),
    0xb2b02a99: ('exit_area_sound', _decode_exit_area_sound),
    0x4392d0c4: ('highlight_area_sound', _decode_highlight_area_sound),
}

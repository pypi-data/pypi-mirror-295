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
    class UnknownStruct183Json(typing_extensions.TypedDict):
        status_empty: int
        strg_0x4cb7e35d: int
        status_puzzle: int
        strg_0x71280e23: int
        status_mirror: int
        status_invisible: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x472bf35f, 0x4cb7e35d, 0x38a22ac5, 0x71280e23, 0x2754537c, 0xe2e62ee5)


@dataclasses.dataclass()
class UnknownStruct183(BaseProperty):
    status_empty: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x472bf35f, original_name='StatusEmpty'
        ),
    })
    strg_0x4cb7e35d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4cb7e35d, original_name='STRG'
        ),
    })
    status_puzzle: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x38a22ac5, original_name='StatusPuzzle'
        ),
    })
    strg_0x71280e23: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x71280e23, original_name='STRG'
        ),
    })
    status_mirror: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2754537c, original_name='StatusMirror'
        ),
    })
    status_invisible: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe2e62ee5, original_name='StatusInvisible'
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
        if property_count != 6:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(84))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'G+\xf3_')  # 0x472bf35f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.status_empty))

        data.write(b'L\xb7\xe3]')  # 0x4cb7e35d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x4cb7e35d))

        data.write(b'8\xa2*\xc5')  # 0x38a22ac5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.status_puzzle))

        data.write(b'q(\x0e#')  # 0x71280e23
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x71280e23))

        data.write(b"'TS|")  # 0x2754537c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.status_mirror))

        data.write(b'\xe2\xe6.\xe5')  # 0xe2e62ee5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.status_invisible))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct183Json", data)
        return cls(
            status_empty=json_data['status_empty'],
            strg_0x4cb7e35d=json_data['strg_0x4cb7e35d'],
            status_puzzle=json_data['status_puzzle'],
            strg_0x71280e23=json_data['strg_0x71280e23'],
            status_mirror=json_data['status_mirror'],
            status_invisible=json_data['status_invisible'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'status_empty': self.status_empty,
            'strg_0x4cb7e35d': self.strg_0x4cb7e35d,
            'status_puzzle': self.status_puzzle,
            'strg_0x71280e23': self.strg_0x71280e23,
            'status_mirror': self.status_mirror,
            'status_invisible': self.status_invisible,
        }


def _decode_status_empty(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x4cb7e35d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_status_puzzle(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x71280e23(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_status_mirror(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_status_invisible(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x472bf35f: ('status_empty', _decode_status_empty),
    0x4cb7e35d: ('strg_0x4cb7e35d', _decode_strg_0x4cb7e35d),
    0x38a22ac5: ('status_puzzle', _decode_status_puzzle),
    0x71280e23: ('strg_0x71280e23', _decode_strg_0x71280e23),
    0x2754537c: ('status_mirror', _decode_status_mirror),
    0xe2e62ee5: ('status_invisible', _decode_status_invisible),
}

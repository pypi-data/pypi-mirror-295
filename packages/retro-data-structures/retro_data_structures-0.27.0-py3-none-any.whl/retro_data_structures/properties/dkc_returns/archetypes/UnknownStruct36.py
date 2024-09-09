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
    class UnknownStruct36Json(typing_extensions.TypedDict):
        unknown: int
        cine_lever: int
        caud: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xe0c67593, 0xd9bed8d3, 0xd01eae75)


@dataclasses.dataclass()
class UnknownStruct36(BaseProperty):
    unknown: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe0c67593, original_name='Unknown'
        ),
    })
    cine_lever: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd9bed8d3, original_name='CineLever'
        ),
    })
    caud: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd01eae75, original_name='CAUD'
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
        if property_count != 3:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHQLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(42))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xe0\xc6u\x93')  # 0xe0c67593
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown))

        data.write(b'\xd9\xbe\xd8\xd3')  # 0xd9bed8d3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cine_lever))

        data.write(b'\xd0\x1e\xaeu')  # 0xd01eae75
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct36Json", data)
        return cls(
            unknown=json_data['unknown'],
            cine_lever=json_data['cine_lever'],
            caud=json_data['caud'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'cine_lever': self.cine_lever,
            'caud': self.caud,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cine_lever(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe0c67593: ('unknown', _decode_unknown),
    0xd9bed8d3: ('cine_lever', _decode_cine_lever),
    0xd01eae75: ('caud', _decode_caud),
}

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
    class IslandAreaStructJson(typing_extensions.TypedDict):
        cost: int
        purchase_text: int
        comment_text: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x5fed5c9d, 0xc5b4de6, 0x1417435)


@dataclasses.dataclass()
class IslandAreaStruct(BaseProperty):
    cost: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x5fed5c9d, original_name='Cost'
        ),
    })
    purchase_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0c5b4de6, original_name='PurchaseText'
        ),
    })
    comment_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x01417435, original_name='CommentText'
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
            _FAST_FORMAT = struct.Struct('>LHlLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(38))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'_\xed\\\x9d')  # 0x5fed5c9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cost))

        data.write(b'\x0c[M\xe6')  # 0xc5b4de6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.purchase_text))

        data.write(b'\x01At5')  # 0x1417435
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.comment_text))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("IslandAreaStructJson", data)
        return cls(
            cost=json_data['cost'],
            purchase_text=json_data['purchase_text'],
            comment_text=json_data['comment_text'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'cost': self.cost,
            'purchase_text': self.purchase_text,
            'comment_text': self.comment_text,
        }


def _decode_cost(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_purchase_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_comment_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5fed5c9d: ('cost', _decode_cost),
    0xc5b4de6: ('purchase_text', _decode_purchase_text),
    0x1417435: ('comment_text', _decode_comment_text),
}

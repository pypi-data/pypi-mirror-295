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
    class UnknownStruct151Json(typing_extensions.TypedDict):
        hud_frame: int
        text_string: int
        confirm_string: int
        cancel_string: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xf2299ed6, 0xe6f6e270, 0x4fabac09, 0xcb6af89b)


@dataclasses.dataclass()
class UnknownStruct151(BaseProperty):
    hud_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf2299ed6, original_name='HUDFrame'
        ),
    })
    text_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe6f6e270, original_name='TextString'
        ),
    })
    confirm_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4fabac09, original_name='ConfirmString'
        ),
    })
    cancel_string: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcb6af89b, original_name='CancelString'
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
        if property_count != 4:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(56))
        assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\xe6\xf6\xe2p')  # 0xe6f6e270
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_string))

        data.write(b'O\xab\xac\t')  # 0x4fabac09
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.confirm_string))

        data.write(b'\xcbj\xf8\x9b')  # 0xcb6af89b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel_string))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct151Json", data)
        return cls(
            hud_frame=json_data['hud_frame'],
            text_string=json_data['text_string'],
            confirm_string=json_data['confirm_string'],
            cancel_string=json_data['cancel_string'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'hud_frame': self.hud_frame,
            'text_string': self.text_string,
            'confirm_string': self.confirm_string,
            'cancel_string': self.cancel_string,
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_confirm_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0xe6f6e270: ('text_string', _decode_text_string),
    0x4fabac09: ('confirm_string', _decode_confirm_string),
    0xcb6af89b: ('cancel_string', _decode_cancel_string),
}

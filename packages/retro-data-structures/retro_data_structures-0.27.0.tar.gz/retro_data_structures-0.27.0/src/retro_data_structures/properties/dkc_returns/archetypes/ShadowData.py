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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class ShadowDataJson(typing_extensions.TypedDict):
        unknown_0xcecb77dd: bool
        shadow_texture: int
        edge_adjust: int
        minimum_opacity: float
        maximum_opacity: float
        unknown_0x1524c118: float
        unknown_0xc7c4c8a9: float
        unknown_0x565c73a2: float
        floor_offset: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xcecb77dd, 0x64c0c54f, 0x79cfa775, 0x1cf3f468, 0xbbc77411, 0x1524c118, 0xc7c4c8a9, 0x565c73a2, 0x808e9e32)


@dataclasses.dataclass()
class ShadowData(BaseProperty):
    unknown_0xcecb77dd: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcecb77dd, original_name='Unknown'
        ),
    })
    shadow_texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x64c0c54f, original_name='ShadowTexture'
        ),
    })
    edge_adjust: enums.EdgeAdjust = dataclasses.field(default=enums.EdgeAdjust.Unknown1, metadata={
        'reflection': FieldReflection[enums.EdgeAdjust](
            enums.EdgeAdjust, id=0x79cfa775, original_name='EdgeAdjust', from_json=enums.EdgeAdjust.from_json, to_json=enums.EdgeAdjust.to_json
        ),
    })
    minimum_opacity: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1cf3f468, original_name='MinimumOpacity'
        ),
    })
    maximum_opacity: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbbc77411, original_name='MaximumOpacity'
        ),
    })
    unknown_0x1524c118: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1524c118, original_name='Unknown'
        ),
    })
    unknown_0xc7c4c8a9: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc7c4c8a9, original_name='Unknown'
        ),
    })
    unknown_0x565c73a2: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x565c73a2, original_name='Unknown'
        ),
    })
    floor_offset: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0x808e9e32, original_name='FloorOffset'
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
        if property_count != 9:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LHQLHLLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(91))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            enums.EdgeAdjust(dec[8]),
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xce\xcbw\xdd')  # 0xcecb77dd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcecb77dd))

        data.write(b'd\xc0\xc5O')  # 0x64c0c54f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shadow_texture))

        data.write(b'y\xcf\xa7u')  # 0x79cfa775
        data.write(b'\x00\x04')  # size
        self.edge_adjust.to_stream(data)

        data.write(b'\x1c\xf3\xf4h')  # 0x1cf3f468
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_opacity))

        data.write(b'\xbb\xc7t\x11')  # 0xbbc77411
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_opacity))

        data.write(b'\x15$\xc1\x18')  # 0x1524c118
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1524c118))

        data.write(b'\xc7\xc4\xc8\xa9')  # 0xc7c4c8a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc7c4c8a9))

        data.write(b'V\\s\xa2')  # 0x565c73a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x565c73a2))

        data.write(b'\x80\x8e\x9e2')  # 0x808e9e32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_offset))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ShadowDataJson", data)
        return cls(
            unknown_0xcecb77dd=json_data['unknown_0xcecb77dd'],
            shadow_texture=json_data['shadow_texture'],
            edge_adjust=enums.EdgeAdjust.from_json(json_data['edge_adjust']),
            minimum_opacity=json_data['minimum_opacity'],
            maximum_opacity=json_data['maximum_opacity'],
            unknown_0x1524c118=json_data['unknown_0x1524c118'],
            unknown_0xc7c4c8a9=json_data['unknown_0xc7c4c8a9'],
            unknown_0x565c73a2=json_data['unknown_0x565c73a2'],
            floor_offset=json_data['floor_offset'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xcecb77dd': self.unknown_0xcecb77dd,
            'shadow_texture': self.shadow_texture,
            'edge_adjust': self.edge_adjust.to_json(),
            'minimum_opacity': self.minimum_opacity,
            'maximum_opacity': self.maximum_opacity,
            'unknown_0x1524c118': self.unknown_0x1524c118,
            'unknown_0xc7c4c8a9': self.unknown_0xc7c4c8a9,
            'unknown_0x565c73a2': self.unknown_0x565c73a2,
            'floor_offset': self.floor_offset,
        }


def _decode_unknown_0xcecb77dd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shadow_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_edge_adjust(data: typing.BinaryIO, property_size: int):
    return enums.EdgeAdjust.from_stream(data)


def _decode_minimum_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1524c118(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc7c4c8a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x565c73a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcecb77dd: ('unknown_0xcecb77dd', _decode_unknown_0xcecb77dd),
    0x64c0c54f: ('shadow_texture', _decode_shadow_texture),
    0x79cfa775: ('edge_adjust', _decode_edge_adjust),
    0x1cf3f468: ('minimum_opacity', _decode_minimum_opacity),
    0xbbc77411: ('maximum_opacity', _decode_maximum_opacity),
    0x1524c118: ('unknown_0x1524c118', _decode_unknown_0x1524c118),
    0xc7c4c8a9: ('unknown_0xc7c4c8a9', _decode_unknown_0xc7c4c8a9),
    0x565c73a2: ('unknown_0x565c73a2', _decode_unknown_0x565c73a2),
    0x808e9e32: ('floor_offset', _decode_floor_offset),
}

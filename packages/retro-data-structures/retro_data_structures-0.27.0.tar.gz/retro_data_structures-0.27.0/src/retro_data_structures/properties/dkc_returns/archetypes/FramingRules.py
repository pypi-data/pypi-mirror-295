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

if typing.TYPE_CHECKING:
    class FramingRulesJson(typing_extensions.TypedDict):
        limit_view_to_bounds: bool
        ignore_upper_lower_bounds: bool
        bounds_buffer: float
        allow_zooming: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x1d2830c3, 0x685952e3, 0xd098956e, 0x4a2e425f)


@dataclasses.dataclass()
class FramingRules(BaseProperty):
    limit_view_to_bounds: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1d2830c3, original_name='LimitViewToBounds'
        ),
    })
    ignore_upper_lower_bounds: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x685952e3, original_name='IgnoreUpperLowerBounds'
        ),
    })
    bounds_buffer: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd098956e, original_name='BoundsBuffer'
        ),
    })
    allow_zooming: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4a2e425f, original_name='AllowZooming'
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
            _FAST_FORMAT = struct.Struct('>LH?LH?LHfLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(31))
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

        data.write(b'\x1d(0\xc3')  # 0x1d2830c3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.limit_view_to_bounds))

        data.write(b'hYR\xe3')  # 0x685952e3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_upper_lower_bounds))

        data.write(b'\xd0\x98\x95n')  # 0xd098956e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounds_buffer))

        data.write(b'J.B_')  # 0x4a2e425f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_zooming))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("FramingRulesJson", data)
        return cls(
            limit_view_to_bounds=json_data['limit_view_to_bounds'],
            ignore_upper_lower_bounds=json_data['ignore_upper_lower_bounds'],
            bounds_buffer=json_data['bounds_buffer'],
            allow_zooming=json_data['allow_zooming'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'limit_view_to_bounds': self.limit_view_to_bounds,
            'ignore_upper_lower_bounds': self.ignore_upper_lower_bounds,
            'bounds_buffer': self.bounds_buffer,
            'allow_zooming': self.allow_zooming,
        }


def _decode_limit_view_to_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_upper_lower_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bounds_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allow_zooming(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1d2830c3: ('limit_view_to_bounds', _decode_limit_view_to_bounds),
    0x685952e3: ('ignore_upper_lower_bounds', _decode_ignore_upper_lower_bounds),
    0xd098956e: ('bounds_buffer', _decode_bounds_buffer),
    0x4a2e425f: ('allow_zooming', _decode_allow_zooming),
}

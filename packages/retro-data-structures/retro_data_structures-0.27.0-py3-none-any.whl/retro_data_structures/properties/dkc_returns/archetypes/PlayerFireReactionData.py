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

if typing.TYPE_CHECKING:
    class PlayerFireReactionDataJson(typing_extensions.TypedDict):
        gravity_multiplier: float
        hurl_height: float
        hurl_direction: int
        hurl_degree_range: float
        bounce_count: int
        bounce_value: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x42ac42ea, 0xe2a43392, 0xda44986f, 0x3707468e, 0x9d331279, 0xd90270f8)


@dataclasses.dataclass()
class PlayerFireReactionData(BaseProperty):
    gravity_multiplier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42ac42ea, original_name='GravityMultiplier'
        ),
    })
    hurl_height: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe2a43392, original_name='HurlHeight'
        ),
    })
    hurl_direction: enums.HurlDirection = dataclasses.field(default=enums.HurlDirection.Unknown2, metadata={
        'reflection': FieldReflection[enums.HurlDirection](
            enums.HurlDirection, id=0xda44986f, original_name='HurlDirection', from_json=enums.HurlDirection.from_json, to_json=enums.HurlDirection.to_json
        ),
    })
    hurl_degree_range: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3707468e, original_name='HurlDegreeRange'
        ),
    })
    bounce_count: int = dataclasses.field(default=2, metadata={
        'reflection': FieldReflection[int](
            int, id=0x9d331279, original_name='BounceCount'
        ),
    })
    bounce_value: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd90270f8, original_name='BounceValue'
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
            _FAST_FORMAT = struct.Struct('>LHfLHfLHLLHfLHlLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(60))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            enums.HurlDirection(dec[8]),
            dec[11],
            dec[14],
            dec[17],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'B\xacB\xea')  # 0x42ac42ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_multiplier))

        data.write(b'\xe2\xa43\x92')  # 0xe2a43392
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height))

        data.write(b'\xdaD\x98o')  # 0xda44986f
        data.write(b'\x00\x04')  # size
        self.hurl_direction.to_stream(data)

        data.write(b'7\x07F\x8e')  # 0x3707468e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_degree_range))

        data.write(b'\x9d3\x12y')  # 0x9d331279
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.bounce_count))

        data.write(b'\xd9\x02p\xf8')  # 0xd90270f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_value))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerFireReactionDataJson", data)
        return cls(
            gravity_multiplier=json_data['gravity_multiplier'],
            hurl_height=json_data['hurl_height'],
            hurl_direction=enums.HurlDirection.from_json(json_data['hurl_direction']),
            hurl_degree_range=json_data['hurl_degree_range'],
            bounce_count=json_data['bounce_count'],
            bounce_value=json_data['bounce_value'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gravity_multiplier': self.gravity_multiplier,
            'hurl_height': self.hurl_height,
            'hurl_direction': self.hurl_direction.to_json(),
            'hurl_degree_range': self.hurl_degree_range,
            'bounce_count': self.bounce_count,
            'bounce_value': self.bounce_value,
        }


def _decode_gravity_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_direction(data: typing.BinaryIO, property_size: int):
    return enums.HurlDirection.from_stream(data)


def _decode_hurl_degree_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bounce_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x42ac42ea: ('gravity_multiplier', _decode_gravity_multiplier),
    0xe2a43392: ('hurl_height', _decode_hurl_height),
    0xda44986f: ('hurl_direction', _decode_hurl_direction),
    0x3707468e: ('hurl_degree_range', _decode_hurl_degree_range),
    0x9d331279: ('bounce_count', _decode_bounce_count),
    0xd90270f8: ('bounce_value', _decode_bounce_value),
}

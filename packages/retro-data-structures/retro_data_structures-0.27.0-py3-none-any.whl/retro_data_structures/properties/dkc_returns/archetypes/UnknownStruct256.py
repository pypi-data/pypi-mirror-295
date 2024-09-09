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
    class UnknownStruct256Json(typing_extensions.TypedDict):
        enable_head: bool
        enable_spikes: bool
        enable_above_spikes: bool
        enable_left_leg: bool
        enable_left_foot: bool
        enable_right_leg: bool
        enable_right_foot: bool
        unknown_0x2d88c50f: bool
        unknown_0x0703bf8f: bool
        unknown_0x2e0e6790: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x8102b827, 0xed936800, 0xa18ed7de, 0x5c4fb14b, 0x4a52d20d, 0xbf311d46, 0x3400d01c, 0x2d88c50f, 0x703bf8f, 0x2e0e6790)


@dataclasses.dataclass()
class UnknownStruct256(BaseProperty):
    enable_head: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8102b827, original_name='EnableHead'
        ),
    })
    enable_spikes: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xed936800, original_name='EnableSpikes'
        ),
    })
    enable_above_spikes: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa18ed7de, original_name='EnableAboveSpikes'
        ),
    })
    enable_left_leg: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5c4fb14b, original_name='EnableLeftLeg'
        ),
    })
    enable_left_foot: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4a52d20d, original_name='EnableLeftFoot'
        ),
    })
    enable_right_leg: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbf311d46, original_name='EnableRightLeg'
        ),
    })
    enable_right_foot: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3400d01c, original_name='EnableRightFoot'
        ),
    })
    unknown_0x2d88c50f: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2d88c50f, original_name='Unknown'
        ),
    })
    unknown_0x0703bf8f: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0703bf8f, original_name='Unknown'
        ),
    })
    unknown_0x2e0e6790: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2e0e6790, original_name='Unknown'
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
        if property_count != 10:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(70))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
            dec[29],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b"\x81\x02\xb8'")  # 0x8102b827
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_head))

        data.write(b'\xed\x93h\x00')  # 0xed936800
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_spikes))

        data.write(b'\xa1\x8e\xd7\xde')  # 0xa18ed7de
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_above_spikes))

        data.write(b'\\O\xb1K')  # 0x5c4fb14b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_left_leg))

        data.write(b'JR\xd2\r')  # 0x4a52d20d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_left_foot))

        data.write(b'\xbf1\x1dF')  # 0xbf311d46
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_right_leg))

        data.write(b'4\x00\xd0\x1c')  # 0x3400d01c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_right_foot))

        data.write(b'-\x88\xc5\x0f')  # 0x2d88c50f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2d88c50f))

        data.write(b'\x07\x03\xbf\x8f')  # 0x703bf8f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0703bf8f))

        data.write(b'.\x0eg\x90')  # 0x2e0e6790
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2e0e6790))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct256Json", data)
        return cls(
            enable_head=json_data['enable_head'],
            enable_spikes=json_data['enable_spikes'],
            enable_above_spikes=json_data['enable_above_spikes'],
            enable_left_leg=json_data['enable_left_leg'],
            enable_left_foot=json_data['enable_left_foot'],
            enable_right_leg=json_data['enable_right_leg'],
            enable_right_foot=json_data['enable_right_foot'],
            unknown_0x2d88c50f=json_data['unknown_0x2d88c50f'],
            unknown_0x0703bf8f=json_data['unknown_0x0703bf8f'],
            unknown_0x2e0e6790=json_data['unknown_0x2e0e6790'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'enable_head': self.enable_head,
            'enable_spikes': self.enable_spikes,
            'enable_above_spikes': self.enable_above_spikes,
            'enable_left_leg': self.enable_left_leg,
            'enable_left_foot': self.enable_left_foot,
            'enable_right_leg': self.enable_right_leg,
            'enable_right_foot': self.enable_right_foot,
            'unknown_0x2d88c50f': self.unknown_0x2d88c50f,
            'unknown_0x0703bf8f': self.unknown_0x0703bf8f,
            'unknown_0x2e0e6790': self.unknown_0x2e0e6790,
        }


def _decode_enable_head(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_spikes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_above_spikes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_left_leg(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_left_foot(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_right_leg(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_right_foot(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2d88c50f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0703bf8f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2e0e6790(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8102b827: ('enable_head', _decode_enable_head),
    0xed936800: ('enable_spikes', _decode_enable_spikes),
    0xa18ed7de: ('enable_above_spikes', _decode_enable_above_spikes),
    0x5c4fb14b: ('enable_left_leg', _decode_enable_left_leg),
    0x4a52d20d: ('enable_left_foot', _decode_enable_left_foot),
    0xbf311d46: ('enable_right_leg', _decode_enable_right_leg),
    0x3400d01c: ('enable_right_foot', _decode_enable_right_foot),
    0x2d88c50f: ('unknown_0x2d88c50f', _decode_unknown_0x2d88c50f),
    0x703bf8f: ('unknown_0x0703bf8f', _decode_unknown_0x0703bf8f),
    0x2e0e6790: ('unknown_0x2e0e6790', _decode_unknown_0x2e0e6790),
}

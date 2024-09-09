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
    class UnknownStruct264Json(typing_extensions.TypedDict):
        unknown: bool
        is_percentage: bool
        percentage_chance: int
        minimum_count: int
        maximum_count: int
        minimum_percentage: int
        maximum_percentage: int
        choose_inactive: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x19a91b3b, 0x54a2d2b1, 0xabbdd047, 0xf3fc6e53, 0xd4470962, 0xf50b11eb, 0xdc75ecf3, 0x432e9d73)


@dataclasses.dataclass()
class UnknownStruct264(BaseProperty):
    unknown: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x19a91b3b, original_name='Unknown'
        ),
    })
    is_percentage: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x54a2d2b1, original_name='IsPercentage'
        ),
    })
    percentage_chance: int = dataclasses.field(default=50, metadata={
        'reflection': FieldReflection[int](
            int, id=0xabbdd047, original_name='PercentageChance'
        ),
    })
    minimum_count: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf3fc6e53, original_name='MinimumCount'
        ),
    })
    maximum_count: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xd4470962, original_name='MaximumCount'
        ),
    })
    minimum_percentage: int = dataclasses.field(default=50, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf50b11eb, original_name='MinimumPercentage'
        ),
    })
    maximum_percentage: int = dataclasses.field(default=50, metadata={
        'reflection': FieldReflection[int](
            int, id=0xdc75ecf3, original_name='MaximumPercentage'
        ),
    })
    choose_inactive: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x432e9d73, original_name='ChooseInactive'
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
        if property_count != 8:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LHlLHlLHlLHlLHlLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(71))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x19\xa9\x1b;')  # 0x19a91b3b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'T\xa2\xd2\xb1')  # 0x54a2d2b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_percentage))

        data.write(b'\xab\xbd\xd0G')  # 0xabbdd047
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.percentage_chance))

        data.write(b'\xf3\xfcnS')  # 0xf3fc6e53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.minimum_count))

        data.write(b'\xd4G\tb')  # 0xd4470962
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.maximum_count))

        data.write(b'\xf5\x0b\x11\xeb')  # 0xf50b11eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.minimum_percentage))

        data.write(b'\xdcu\xec\xf3')  # 0xdc75ecf3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.maximum_percentage))

        data.write(b'C.\x9ds')  # 0x432e9d73
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.choose_inactive))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct264Json", data)
        return cls(
            unknown=json_data['unknown'],
            is_percentage=json_data['is_percentage'],
            percentage_chance=json_data['percentage_chance'],
            minimum_count=json_data['minimum_count'],
            maximum_count=json_data['maximum_count'],
            minimum_percentage=json_data['minimum_percentage'],
            maximum_percentage=json_data['maximum_percentage'],
            choose_inactive=json_data['choose_inactive'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'is_percentage': self.is_percentage,
            'percentage_chance': self.percentage_chance,
            'minimum_count': self.minimum_count,
            'maximum_count': self.maximum_count,
            'minimum_percentage': self.minimum_percentage,
            'maximum_percentage': self.maximum_percentage,
            'choose_inactive': self.choose_inactive,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_percentage_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_minimum_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_maximum_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_minimum_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_maximum_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_choose_inactive(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x19a91b3b: ('unknown', _decode_unknown),
    0x54a2d2b1: ('is_percentage', _decode_is_percentage),
    0xabbdd047: ('percentage_chance', _decode_percentage_chance),
    0xf3fc6e53: ('minimum_count', _decode_minimum_count),
    0xd4470962: ('maximum_count', _decode_maximum_count),
    0xf50b11eb: ('minimum_percentage', _decode_minimum_percentage),
    0xdc75ecf3: ('maximum_percentage', _decode_maximum_percentage),
    0x432e9d73: ('choose_inactive', _decode_choose_inactive),
}

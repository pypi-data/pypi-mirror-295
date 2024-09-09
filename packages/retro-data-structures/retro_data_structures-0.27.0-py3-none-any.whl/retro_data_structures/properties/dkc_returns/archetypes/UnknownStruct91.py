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
    class UnknownStruct91Json(typing_extensions.TypedDict):
        world: bool
        primary: bool
        secondary: bool
        third: bool
        fourth: bool
        fifth: bool
        sixth: bool
        seventh: bool
        eighth: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x1ab843d9, 0x4e78c4ac, 0x36cc22c2, 0x75f5ddda, 0xde786a38, 0xde88c946, 0xf3e29eb, 0xcfe583ef, 0xbb655d67)


@dataclasses.dataclass()
class UnknownStruct91(BaseProperty):
    world: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1ab843d9, original_name='World'
        ),
    })
    primary: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4e78c4ac, original_name='Primary'
        ),
    })
    secondary: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x36cc22c2, original_name='Secondary'
        ),
    })
    third: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x75f5ddda, original_name='Third'
        ),
    })
    fourth: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xde786a38, original_name='Fourth'
        ),
    })
    fifth: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xde88c946, original_name='Fifth'
        ),
    })
    sixth: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0f3e29eb, original_name='Sixth'
        ),
    })
    seventh: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcfe583ef, original_name='Seventh'
        ),
    })
    eighth: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbb655d67, original_name='Eighth'
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
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(63))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) == _FAST_IDS
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
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x1a\xb8C\xd9')  # 0x1ab843d9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.world))

        data.write(b'Nx\xc4\xac')  # 0x4e78c4ac
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.primary))

        data.write(b'6\xcc"\xc2')  # 0x36cc22c2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.secondary))

        data.write(b'u\xf5\xdd\xda')  # 0x75f5ddda
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.third))

        data.write(b'\xdexj8')  # 0xde786a38
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.fourth))

        data.write(b'\xde\x88\xc9F')  # 0xde88c946
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.fifth))

        data.write(b'\x0f>)\xeb')  # 0xf3e29eb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sixth))

        data.write(b'\xcf\xe5\x83\xef')  # 0xcfe583ef
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.seventh))

        data.write(b'\xbbe]g')  # 0xbb655d67
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.eighth))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct91Json", data)
        return cls(
            world=json_data['world'],
            primary=json_data['primary'],
            secondary=json_data['secondary'],
            third=json_data['third'],
            fourth=json_data['fourth'],
            fifth=json_data['fifth'],
            sixth=json_data['sixth'],
            seventh=json_data['seventh'],
            eighth=json_data['eighth'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'world': self.world,
            'primary': self.primary,
            'secondary': self.secondary,
            'third': self.third,
            'fourth': self.fourth,
            'fifth': self.fifth,
            'sixth': self.sixth,
            'seventh': self.seventh,
            'eighth': self.eighth,
        }


def _decode_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_primary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_secondary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_third(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fourth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fifth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sixth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seventh(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_eighth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1ab843d9: ('world', _decode_world),
    0x4e78c4ac: ('primary', _decode_primary),
    0x36cc22c2: ('secondary', _decode_secondary),
    0x75f5ddda: ('third', _decode_third),
    0xde786a38: ('fourth', _decode_fourth),
    0xde88c946: ('fifth', _decode_fifth),
    0xf3e29eb: ('sixth', _decode_sixth),
    0xcfe583ef: ('seventh', _decode_seventh),
    0xbb655d67: ('eighth', _decode_eighth),
}

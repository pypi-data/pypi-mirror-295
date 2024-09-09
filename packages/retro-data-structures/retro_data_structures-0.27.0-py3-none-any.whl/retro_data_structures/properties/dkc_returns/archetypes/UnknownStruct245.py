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
    class UnknownStruct245Json(typing_extensions.TypedDict):
        can_crush_player: bool
        unknown_0x5409b2be: bool
        unknown_0xd8a25f18: bool
        enable_pinch: bool
        enable_crush: bool
        instant_kill: bool
        unknown_0xc75386a1: bool
        unknown_0x1e456737: bool
        unknown_0x5a60111f: bool
        unknown_0xcf2f0bf9: bool
        unknown_0x5783e404: bool
        can_crush_push_player: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x22ecf23e, 0x5409b2be, 0xd8a25f18, 0xd982bc68, 0xb11250e, 0x3d4264ee, 0xc75386a1, 0x1e456737, 0x5a60111f, 0xcf2f0bf9, 0x5783e404, 0x57018cf1)


@dataclasses.dataclass()
class UnknownStruct245(BaseProperty):
    can_crush_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x22ecf23e, original_name='CanCrushPlayer'
        ),
    })
    unknown_0x5409b2be: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5409b2be, original_name='Unknown'
        ),
    })
    unknown_0xd8a25f18: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd8a25f18, original_name='Unknown'
        ),
    })
    enable_pinch: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd982bc68, original_name='EnablePinch'
        ),
    })
    enable_crush: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0b11250e, original_name='EnableCrush'
        ),
    })
    instant_kill: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3d4264ee, original_name='InstantKill'
        ),
    })
    unknown_0xc75386a1: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc75386a1, original_name='Unknown'
        ),
    })
    unknown_0x1e456737: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1e456737, original_name='Unknown'
        ),
    })
    unknown_0x5a60111f: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5a60111f, original_name='Unknown'
        ),
    })
    unknown_0xcf2f0bf9: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcf2f0bf9, original_name='Unknown'
        ),
    })
    unknown_0x5783e404: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5783e404, original_name='Unknown'
        ),
    })
    can_crush_push_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x57018cf1, original_name='CanCrushPushPlayer'
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
        if property_count != 12:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(84))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) == _FAST_IDS
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
            dec[32],
            dec[35],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'"\xec\xf2>')  # 0x22ecf23e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_crush_player))

        data.write(b'T\t\xb2\xbe')  # 0x5409b2be
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5409b2be))

        data.write(b'\xd8\xa2_\x18')  # 0xd8a25f18
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd8a25f18))

        data.write(b'\xd9\x82\xbch')  # 0xd982bc68
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_pinch))

        data.write(b'\x0b\x11%\x0e')  # 0xb11250e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_crush))

        data.write(b'=Bd\xee')  # 0x3d4264ee
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.instant_kill))

        data.write(b'\xc7S\x86\xa1')  # 0xc75386a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc75386a1))

        data.write(b'\x1eEg7')  # 0x1e456737
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1e456737))

        data.write(b'Z`\x11\x1f')  # 0x5a60111f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5a60111f))

        data.write(b'\xcf/\x0b\xf9')  # 0xcf2f0bf9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcf2f0bf9))

        data.write(b'W\x83\xe4\x04')  # 0x5783e404
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5783e404))

        data.write(b'W\x01\x8c\xf1')  # 0x57018cf1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_crush_push_player))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct245Json", data)
        return cls(
            can_crush_player=json_data['can_crush_player'],
            unknown_0x5409b2be=json_data['unknown_0x5409b2be'],
            unknown_0xd8a25f18=json_data['unknown_0xd8a25f18'],
            enable_pinch=json_data['enable_pinch'],
            enable_crush=json_data['enable_crush'],
            instant_kill=json_data['instant_kill'],
            unknown_0xc75386a1=json_data['unknown_0xc75386a1'],
            unknown_0x1e456737=json_data['unknown_0x1e456737'],
            unknown_0x5a60111f=json_data['unknown_0x5a60111f'],
            unknown_0xcf2f0bf9=json_data['unknown_0xcf2f0bf9'],
            unknown_0x5783e404=json_data['unknown_0x5783e404'],
            can_crush_push_player=json_data['can_crush_push_player'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'can_crush_player': self.can_crush_player,
            'unknown_0x5409b2be': self.unknown_0x5409b2be,
            'unknown_0xd8a25f18': self.unknown_0xd8a25f18,
            'enable_pinch': self.enable_pinch,
            'enable_crush': self.enable_crush,
            'instant_kill': self.instant_kill,
            'unknown_0xc75386a1': self.unknown_0xc75386a1,
            'unknown_0x1e456737': self.unknown_0x1e456737,
            'unknown_0x5a60111f': self.unknown_0x5a60111f,
            'unknown_0xcf2f0bf9': self.unknown_0xcf2f0bf9,
            'unknown_0x5783e404': self.unknown_0x5783e404,
            'can_crush_push_player': self.can_crush_push_player,
        }


def _decode_can_crush_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5409b2be(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xd8a25f18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_pinch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_crush(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_instant_kill(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xc75386a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x1e456737(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5a60111f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xcf2f0bf9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5783e404(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_crush_push_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x22ecf23e: ('can_crush_player', _decode_can_crush_player),
    0x5409b2be: ('unknown_0x5409b2be', _decode_unknown_0x5409b2be),
    0xd8a25f18: ('unknown_0xd8a25f18', _decode_unknown_0xd8a25f18),
    0xd982bc68: ('enable_pinch', _decode_enable_pinch),
    0xb11250e: ('enable_crush', _decode_enable_crush),
    0x3d4264ee: ('instant_kill', _decode_instant_kill),
    0xc75386a1: ('unknown_0xc75386a1', _decode_unknown_0xc75386a1),
    0x1e456737: ('unknown_0x1e456737', _decode_unknown_0x1e456737),
    0x5a60111f: ('unknown_0x5a60111f', _decode_unknown_0x5a60111f),
    0xcf2f0bf9: ('unknown_0xcf2f0bf9', _decode_unknown_0xcf2f0bf9),
    0x5783e404: ('unknown_0x5783e404', _decode_unknown_0x5783e404),
    0x57018cf1: ('can_crush_push_player', _decode_can_crush_push_player),
}

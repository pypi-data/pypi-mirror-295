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
    class SpawnPointDataJson(typing_extensions.TypedDict):
        unknown_0x1b92d687: bool
        can_spawn_dk: bool
        can_spawn_diddy: bool
        delete_rambi: bool
        hide_rambi: bool
        unknown_0xebe3bf3f: bool
        unknown_0x0ca54843: bool
        unknown_0xb95c4953: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x1b92d687, 0xefa42418, 0x6ab717b5, 0x320723a9, 0x7a6231bf, 0xebe3bf3f, 0xca54843, 0xb95c4953)


@dataclasses.dataclass()
class SpawnPointData(BaseProperty):
    unknown_0x1b92d687: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1b92d687, original_name='Unknown'
        ),
    })
    can_spawn_dk: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xefa42418, original_name='CanSpawnDK'
        ),
    })
    can_spawn_diddy: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6ab717b5, original_name='CanSpawnDiddy'
        ),
    })
    delete_rambi: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x320723a9, original_name='DeleteRambi'
        ),
    })
    hide_rambi: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7a6231bf, original_name='HideRambi'
        ),
    })
    unknown_0xebe3bf3f: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xebe3bf3f, original_name='Unknown'
        ),
    })
    unknown_0x0ca54843: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0ca54843, original_name='Unknown'
        ),
    })
    unknown_0xb95c4953: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xb95c4953, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(56))
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

        data.write(b'\x1b\x92\xd6\x87')  # 0x1b92d687
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x1b92d687))

        data.write(b'\xef\xa4$\x18')  # 0xefa42418
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_spawn_dk))

        data.write(b'j\xb7\x17\xb5')  # 0x6ab717b5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_spawn_diddy))

        data.write(b'2\x07#\xa9')  # 0x320723a9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.delete_rambi))

        data.write(b'zb1\xbf')  # 0x7a6231bf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.hide_rambi))

        data.write(b'\xeb\xe3\xbf?')  # 0xebe3bf3f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xebe3bf3f))

        data.write(b'\x0c\xa5HC')  # 0xca54843
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0ca54843))

        data.write(b'\xb9\\IS')  # 0xb95c4953
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb95c4953))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SpawnPointDataJson", data)
        return cls(
            unknown_0x1b92d687=json_data['unknown_0x1b92d687'],
            can_spawn_dk=json_data['can_spawn_dk'],
            can_spawn_diddy=json_data['can_spawn_diddy'],
            delete_rambi=json_data['delete_rambi'],
            hide_rambi=json_data['hide_rambi'],
            unknown_0xebe3bf3f=json_data['unknown_0xebe3bf3f'],
            unknown_0x0ca54843=json_data['unknown_0x0ca54843'],
            unknown_0xb95c4953=json_data['unknown_0xb95c4953'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x1b92d687': self.unknown_0x1b92d687,
            'can_spawn_dk': self.can_spawn_dk,
            'can_spawn_diddy': self.can_spawn_diddy,
            'delete_rambi': self.delete_rambi,
            'hide_rambi': self.hide_rambi,
            'unknown_0xebe3bf3f': self.unknown_0xebe3bf3f,
            'unknown_0x0ca54843': self.unknown_0x0ca54843,
            'unknown_0xb95c4953': self.unknown_0xb95c4953,
        }


def _decode_unknown_0x1b92d687(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_spawn_dk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_spawn_diddy(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_delete_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_hide_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xebe3bf3f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x0ca54843(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb95c4953(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1b92d687: ('unknown_0x1b92d687', _decode_unknown_0x1b92d687),
    0xefa42418: ('can_spawn_dk', _decode_can_spawn_dk),
    0x6ab717b5: ('can_spawn_diddy', _decode_can_spawn_diddy),
    0x320723a9: ('delete_rambi', _decode_delete_rambi),
    0x7a6231bf: ('hide_rambi', _decode_hide_rambi),
    0xebe3bf3f: ('unknown_0xebe3bf3f', _decode_unknown_0xebe3bf3f),
    0xca54843: ('unknown_0x0ca54843', _decode_unknown_0x0ca54843),
    0xb95c4953: ('unknown_0xb95c4953', _decode_unknown_0xb95c4953),
}

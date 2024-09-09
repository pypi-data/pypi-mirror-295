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
    class GenericCreatureStructEJson(typing_extensions.TypedDict):
        animation: int
        group: int
        loop: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xaacdb11c, 0x8acd5b6f, 0xeda47ff6)


@dataclasses.dataclass()
class GenericCreatureStructE(BaseProperty):
    animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xaacdb11c, original_name='Animation'
        ),
    })
    group: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8acd5b6f, original_name='Group'
        ),
    })
    loop: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xeda47ff6, original_name='Loop'
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
            _FAST_FORMAT = struct.Struct('>LHlLHlLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(27))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        data.write(b'\x8a\xcd[o')  # 0x8acd5b6f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.group))

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GenericCreatureStructEJson", data)
        return cls(
            animation=json_data['animation'],
            group=json_data['group'],
            loop=json_data['loop'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'animation': self.animation,
            'group': self.group,
            'loop': self.loop,
        }


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_group(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaacdb11c: ('animation', _decode_animation),
    0x8acd5b6f: ('group', _decode_group),
    0xeda47ff6: ('loop', _decode_loop),
}

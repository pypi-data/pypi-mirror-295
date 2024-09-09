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
    class ActorMultiKeyframeStructJson(typing_extensions.TypedDict):
        unknown: int
        loop: bool
        force_secondary: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xc215a24f, 0xeda47ff6, 0x5cce5b97)


@dataclasses.dataclass()
class ActorMultiKeyframeStruct(BaseProperty):
    unknown: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xc215a24f, original_name='Unknown'
        ),
    })
    loop: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xeda47ff6, original_name='Loop'
        ),
    })
    force_secondary: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5cce5b97, original_name='ForceSecondary'
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
            _FAST_FORMAT = struct.Struct('>LHlLH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(24))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xc2\x15\xa2O')  # 0xc215a24f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'\\\xce[\x97')  # 0x5cce5b97
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_secondary))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ActorMultiKeyframeStructJson", data)
        return cls(
            unknown=json_data['unknown'],
            loop=json_data['loop'],
            force_secondary=json_data['force_secondary'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'loop': self.loop,
            'force_secondary': self.force_secondary,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_force_secondary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc215a24f: ('unknown', _decode_unknown),
    0xeda47ff6: ('loop', _decode_loop),
    0x5cce5b97: ('force_secondary', _decode_force_secondary),
}

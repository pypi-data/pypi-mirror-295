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
    class UnknownStruct87Json(typing_extensions.TypedDict):
        flip_duration: float
        unknown_0xf5fa970d: float
        unknown_0x14044489: float
        struggle_duration: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xf7f8387a, 0xf5fa970d, 0x14044489, 0x39870d35)


@dataclasses.dataclass()
class UnknownStruct87(BaseProperty):
    flip_duration: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf7f8387a, original_name='FlipDuration'
        ),
    })
    unknown_0xf5fa970d: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf5fa970d, original_name='Unknown'
        ),
    })
    unknown_0x14044489: float = dataclasses.field(default=0.33000001311302185, metadata={
        'reflection': FieldReflection[float](
            float, id=0x14044489, original_name='Unknown'
        ),
    })
    struggle_duration: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39870d35, original_name='StruggleDuration'
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
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(40))
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

        data.write(b'\xf7\xf88z')  # 0xf7f8387a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flip_duration))

        data.write(b'\xf5\xfa\x97\r')  # 0xf5fa970d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf5fa970d))

        data.write(b'\x14\x04D\x89')  # 0x14044489
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x14044489))

        data.write(b'9\x87\r5')  # 0x39870d35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.struggle_duration))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct87Json", data)
        return cls(
            flip_duration=json_data['flip_duration'],
            unknown_0xf5fa970d=json_data['unknown_0xf5fa970d'],
            unknown_0x14044489=json_data['unknown_0x14044489'],
            struggle_duration=json_data['struggle_duration'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'flip_duration': self.flip_duration,
            'unknown_0xf5fa970d': self.unknown_0xf5fa970d,
            'unknown_0x14044489': self.unknown_0x14044489,
            'struggle_duration': self.struggle_duration,
        }


def _decode_flip_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf5fa970d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x14044489(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_struggle_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf7f8387a: ('flip_duration', _decode_flip_duration),
    0xf5fa970d: ('unknown_0xf5fa970d', _decode_unknown_0xf5fa970d),
    0x14044489: ('unknown_0x14044489', _decode_unknown_0x14044489),
    0x39870d35: ('struggle_duration', _decode_struggle_duration),
}

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
    class UnknownStruct16Json(typing_extensions.TypedDict):
        max_delay: float
        delay: float
        feedback: float
        unknown: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xf5b6bf6c, 0x14fff39c, 0x1da37b0d, 0x11bc5e7a)


@dataclasses.dataclass()
class UnknownStruct16(BaseProperty):
    max_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf5b6bf6c, original_name='MaxDelay'
        ),
    })
    delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x14fff39c, original_name='Delay'
        ),
    })
    feedback: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1da37b0d, original_name='Feedback'
        ),
    })
    unknown: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x11bc5e7a, original_name='Unknown'
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

        data.write(b'\xf5\xb6\xbfl')  # 0xf5b6bf6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_delay))

        data.write(b'\x14\xff\xf3\x9c')  # 0x14fff39c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay))

        data.write(b'\x1d\xa3{\r')  # 0x1da37b0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.feedback))

        data.write(b'\x11\xbc^z')  # 0x11bc5e7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct16Json", data)
        return cls(
            max_delay=json_data['max_delay'],
            delay=json_data['delay'],
            feedback=json_data['feedback'],
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'max_delay': self.max_delay,
            'delay': self.delay,
            'feedback': self.feedback,
            'unknown': self.unknown,
        }


def _decode_max_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_feedback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf5b6bf6c: ('max_delay', _decode_max_delay),
    0x14fff39c: ('delay', _decode_delay),
    0x1da37b0d: ('feedback', _decode_feedback),
    0x11bc5e7a: ('unknown', _decode_unknown),
}

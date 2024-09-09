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
    class MoleTrainManagerStructAJson(typing_extensions.TypedDict):
        unknown_0xee447d6b: bool
        unknown_0x4d765168: float
        unknown_0x4f01c9e2: float
        chase_offset: float
        chase_speed: float
        unknown_0xd33f6240: float
        chase_delay: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xee447d6b, 0x4d765168, 0x4f01c9e2, 0xed0d6895, 0x92fbc161, 0xd33f6240, 0xe59672b3)


@dataclasses.dataclass()
class MoleTrainManagerStructA(BaseProperty):
    unknown_0xee447d6b: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xee447d6b, original_name='Unknown'
        ),
    })
    unknown_0x4d765168: float = dataclasses.field(default=46.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4d765168, original_name='Unknown'
        ),
    })
    unknown_0x4f01c9e2: float = dataclasses.field(default=36.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4f01c9e2, original_name='Unknown'
        ),
    })
    chase_offset: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xed0d6895, original_name='ChaseOffset'
        ),
    })
    chase_speed: float = dataclasses.field(default=11.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x92fbc161, original_name='ChaseSpeed'
        ),
    })
    unknown_0xd33f6240: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd33f6240, original_name='Unknown'
        ),
    })
    chase_delay: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe59672b3, original_name='ChaseDelay'
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
        if property_count != 7:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(67))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xeeD}k')  # 0xee447d6b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xee447d6b))

        data.write(b'MvQh')  # 0x4d765168
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4d765168))

        data.write(b'O\x01\xc9\xe2')  # 0x4f01c9e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f01c9e2))

        data.write(b'\xed\rh\x95')  # 0xed0d6895
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_offset))

        data.write(b'\x92\xfb\xc1a')  # 0x92fbc161
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_speed))

        data.write(b'\xd3?b@')  # 0xd33f6240
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd33f6240))

        data.write(b'\xe5\x96r\xb3')  # 0xe59672b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_delay))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MoleTrainManagerStructAJson", data)
        return cls(
            unknown_0xee447d6b=json_data['unknown_0xee447d6b'],
            unknown_0x4d765168=json_data['unknown_0x4d765168'],
            unknown_0x4f01c9e2=json_data['unknown_0x4f01c9e2'],
            chase_offset=json_data['chase_offset'],
            chase_speed=json_data['chase_speed'],
            unknown_0xd33f6240=json_data['unknown_0xd33f6240'],
            chase_delay=json_data['chase_delay'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xee447d6b': self.unknown_0xee447d6b,
            'unknown_0x4d765168': self.unknown_0x4d765168,
            'unknown_0x4f01c9e2': self.unknown_0x4f01c9e2,
            'chase_offset': self.chase_offset,
            'chase_speed': self.chase_speed,
            'unknown_0xd33f6240': self.unknown_0xd33f6240,
            'chase_delay': self.chase_delay,
        }


def _decode_unknown_0xee447d6b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4d765168(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4f01c9e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd33f6240(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xee447d6b: ('unknown_0xee447d6b', _decode_unknown_0xee447d6b),
    0x4d765168: ('unknown_0x4d765168', _decode_unknown_0x4d765168),
    0x4f01c9e2: ('unknown_0x4f01c9e2', _decode_unknown_0x4f01c9e2),
    0xed0d6895: ('chase_offset', _decode_chase_offset),
    0x92fbc161: ('chase_speed', _decode_chase_speed),
    0xd33f6240: ('unknown_0xd33f6240', _decode_unknown_0xd33f6240),
    0xe59672b3: ('chase_delay', _decode_chase_delay),
}

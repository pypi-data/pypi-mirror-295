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
    class UnknownStruct9Json(typing_extensions.TypedDict):
        unknown_0x5d28cce5: float
        unknown_0x1fe2e0b4: float
        lerp_duration: float
        unknown_0x9adf7732: bool
        unknown_0x7fbfe9fd: bool
        unknown_0x6a54d863: bool
        unknown_0x17d5302a: float
        unknown_0xfa271b70: bool
        unknown_0x5c927fb2: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x5d28cce5, 0x1fe2e0b4, 0x8239d04c, 0x9adf7732, 0x7fbfe9fd, 0x6a54d863, 0x17d5302a, 0xfa271b70, 0x5c927fb2)


@dataclasses.dataclass()
class UnknownStruct9(BaseProperty):
    unknown_0x5d28cce5: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5d28cce5, original_name='Unknown'
        ),
    })
    unknown_0x1fe2e0b4: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1fe2e0b4, original_name='Unknown'
        ),
    })
    lerp_duration: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8239d04c, original_name='LerpDuration'
        ),
    })
    unknown_0x9adf7732: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9adf7732, original_name='Unknown'
        ),
    })
    unknown_0x7fbfe9fd: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7fbfe9fd, original_name='Unknown'
        ),
    })
    unknown_0x6a54d863: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6a54d863, original_name='Unknown'
        ),
    })
    unknown_0x17d5302a: float = dataclasses.field(default=7.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x17d5302a, original_name='Unknown'
        ),
    })
    unknown_0xfa271b70: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xfa271b70, original_name='Unknown'
        ),
    })
    unknown_0x5c927fb2: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5c927fb2, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLH?LH?LH?LHfLH?LHf')
    
        dec = _FAST_FORMAT.unpack(data.read(78))
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

        data.write(b'](\xcc\xe5')  # 0x5d28cce5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d28cce5))

        data.write(b'\x1f\xe2\xe0\xb4')  # 0x1fe2e0b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1fe2e0b4))

        data.write(b'\x829\xd0L')  # 0x8239d04c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lerp_duration))

        data.write(b'\x9a\xdfw2')  # 0x9adf7732
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9adf7732))

        data.write(b'\x7f\xbf\xe9\xfd')  # 0x7fbfe9fd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7fbfe9fd))

        data.write(b'jT\xd8c')  # 0x6a54d863
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6a54d863))

        data.write(b'\x17\xd50*')  # 0x17d5302a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x17d5302a))

        data.write(b"\xfa'\x1bp")  # 0xfa271b70
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xfa271b70))

        data.write(b'\\\x92\x7f\xb2')  # 0x5c927fb2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5c927fb2))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct9Json", data)
        return cls(
            unknown_0x5d28cce5=json_data['unknown_0x5d28cce5'],
            unknown_0x1fe2e0b4=json_data['unknown_0x1fe2e0b4'],
            lerp_duration=json_data['lerp_duration'],
            unknown_0x9adf7732=json_data['unknown_0x9adf7732'],
            unknown_0x7fbfe9fd=json_data['unknown_0x7fbfe9fd'],
            unknown_0x6a54d863=json_data['unknown_0x6a54d863'],
            unknown_0x17d5302a=json_data['unknown_0x17d5302a'],
            unknown_0xfa271b70=json_data['unknown_0xfa271b70'],
            unknown_0x5c927fb2=json_data['unknown_0x5c927fb2'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x5d28cce5': self.unknown_0x5d28cce5,
            'unknown_0x1fe2e0b4': self.unknown_0x1fe2e0b4,
            'lerp_duration': self.lerp_duration,
            'unknown_0x9adf7732': self.unknown_0x9adf7732,
            'unknown_0x7fbfe9fd': self.unknown_0x7fbfe9fd,
            'unknown_0x6a54d863': self.unknown_0x6a54d863,
            'unknown_0x17d5302a': self.unknown_0x17d5302a,
            'unknown_0xfa271b70': self.unknown_0xfa271b70,
            'unknown_0x5c927fb2': self.unknown_0x5c927fb2,
        }


def _decode_unknown_0x5d28cce5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1fe2e0b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lerp_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9adf7732(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7fbfe9fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6a54d863(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x17d5302a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfa271b70(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5c927fb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d28cce5: ('unknown_0x5d28cce5', _decode_unknown_0x5d28cce5),
    0x1fe2e0b4: ('unknown_0x1fe2e0b4', _decode_unknown_0x1fe2e0b4),
    0x8239d04c: ('lerp_duration', _decode_lerp_duration),
    0x9adf7732: ('unknown_0x9adf7732', _decode_unknown_0x9adf7732),
    0x7fbfe9fd: ('unknown_0x7fbfe9fd', _decode_unknown_0x7fbfe9fd),
    0x6a54d863: ('unknown_0x6a54d863', _decode_unknown_0x6a54d863),
    0x17d5302a: ('unknown_0x17d5302a', _decode_unknown_0x17d5302a),
    0xfa271b70: ('unknown_0xfa271b70', _decode_unknown_0xfa271b70),
    0x5c927fb2: ('unknown_0x5c927fb2', _decode_unknown_0x5c927fb2),
}

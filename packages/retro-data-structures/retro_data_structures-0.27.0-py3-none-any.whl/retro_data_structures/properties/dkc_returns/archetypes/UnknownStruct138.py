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
    class UnknownStruct138Json(typing_extensions.TypedDict):
        unknown_0xd4b4ad93: float
        unknown_0x035f1fd2: float
        unknown_0x354d1781: float
        unknown_0xe2a6a5c0: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xd4b4ad93, 0x35f1fd2, 0x354d1781, 0xe2a6a5c0)


@dataclasses.dataclass()
class UnknownStruct138(BaseProperty):
    unknown_0xd4b4ad93: float = dataclasses.field(default=-1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd4b4ad93, original_name='Unknown'
        ),
    })
    unknown_0x035f1fd2: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x035f1fd2, original_name='Unknown'
        ),
    })
    unknown_0x354d1781: float = dataclasses.field(default=-1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x354d1781, original_name='Unknown'
        ),
    })
    unknown_0xe2a6a5c0: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe2a6a5c0, original_name='Unknown'
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

        data.write(b'\xd4\xb4\xad\x93')  # 0xd4b4ad93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd4b4ad93))

        data.write(b'\x03_\x1f\xd2')  # 0x35f1fd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x035f1fd2))

        data.write(b'5M\x17\x81')  # 0x354d1781
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x354d1781))

        data.write(b'\xe2\xa6\xa5\xc0')  # 0xe2a6a5c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe2a6a5c0))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct138Json", data)
        return cls(
            unknown_0xd4b4ad93=json_data['unknown_0xd4b4ad93'],
            unknown_0x035f1fd2=json_data['unknown_0x035f1fd2'],
            unknown_0x354d1781=json_data['unknown_0x354d1781'],
            unknown_0xe2a6a5c0=json_data['unknown_0xe2a6a5c0'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xd4b4ad93': self.unknown_0xd4b4ad93,
            'unknown_0x035f1fd2': self.unknown_0x035f1fd2,
            'unknown_0x354d1781': self.unknown_0x354d1781,
            'unknown_0xe2a6a5c0': self.unknown_0xe2a6a5c0,
        }


def _decode_unknown_0xd4b4ad93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x035f1fd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x354d1781(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe2a6a5c0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd4b4ad93: ('unknown_0xd4b4ad93', _decode_unknown_0xd4b4ad93),
    0x35f1fd2: ('unknown_0x035f1fd2', _decode_unknown_0x035f1fd2),
    0x354d1781: ('unknown_0x354d1781', _decode_unknown_0x354d1781),
    0xe2a6a5c0: ('unknown_0xe2a6a5c0', _decode_unknown_0xe2a6a5c0),
}

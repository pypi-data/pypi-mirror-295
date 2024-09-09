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
    class UnknownStruct118Json(typing_extensions.TypedDict):
        acceleration: float
        deceleration: float
        max_speed: float
        unknown_0x7e1338f8: float
        unknown_0x3cd77ebc: float
        unknown_0xe79a390f: float
        unknown_0x8f922c1c: float
        unknown_0xd4c6cc95: float
        unknown_0xadb1d371: float
        unknown_0x89732f60: float
        unknown_0x3b774d55: float
        max_additive_change: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x39fb7978, 0x9ec4fc10, 0x82db0cbe, 0x7e1338f8, 0x3cd77ebc, 0xe79a390f, 0x8f922c1c, 0xd4c6cc95, 0xadb1d371, 0x89732f60, 0x3b774d55, 0x4de17472)


@dataclasses.dataclass()
class UnknownStruct118(BaseProperty):
    acceleration: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39fb7978, original_name='Acceleration'
        ),
    })
    deceleration: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9ec4fc10, original_name='Deceleration'
        ),
    })
    max_speed: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x82db0cbe, original_name='MaxSpeed'
        ),
    })
    unknown_0x7e1338f8: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7e1338f8, original_name='Unknown'
        ),
    })
    unknown_0x3cd77ebc: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3cd77ebc, original_name='Unknown'
        ),
    })
    unknown_0xe79a390f: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe79a390f, original_name='Unknown'
        ),
    })
    unknown_0x8f922c1c: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8f922c1c, original_name='Unknown'
        ),
    })
    unknown_0xd4c6cc95: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd4c6cc95, original_name='Unknown'
        ),
    })
    unknown_0xadb1d371: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xadb1d371, original_name='Unknown'
        ),
    })
    unknown_0x89732f60: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x89732f60, original_name='Unknown'
        ),
    })
    unknown_0x3b774d55: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3b774d55, original_name='Unknown'
        ),
    })
    max_additive_change: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4de17472, original_name='MaxAdditiveChange'
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
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(120))
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

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\x82\xdb\x0c\xbe')  # 0x82db0cbe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_speed))

        data.write(b'~\x138\xf8')  # 0x7e1338f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7e1338f8))

        data.write(b'<\xd7~\xbc')  # 0x3cd77ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3cd77ebc))

        data.write(b'\xe7\x9a9\x0f')  # 0xe79a390f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe79a390f))

        data.write(b'\x8f\x92,\x1c')  # 0x8f922c1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f922c1c))

        data.write(b'\xd4\xc6\xcc\x95')  # 0xd4c6cc95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd4c6cc95))

        data.write(b'\xad\xb1\xd3q')  # 0xadb1d371
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xadb1d371))

        data.write(b'\x89s/`')  # 0x89732f60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x89732f60))

        data.write(b';wMU')  # 0x3b774d55
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b774d55))

        data.write(b'M\xe1tr')  # 0x4de17472
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_additive_change))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct118Json", data)
        return cls(
            acceleration=json_data['acceleration'],
            deceleration=json_data['deceleration'],
            max_speed=json_data['max_speed'],
            unknown_0x7e1338f8=json_data['unknown_0x7e1338f8'],
            unknown_0x3cd77ebc=json_data['unknown_0x3cd77ebc'],
            unknown_0xe79a390f=json_data['unknown_0xe79a390f'],
            unknown_0x8f922c1c=json_data['unknown_0x8f922c1c'],
            unknown_0xd4c6cc95=json_data['unknown_0xd4c6cc95'],
            unknown_0xadb1d371=json_data['unknown_0xadb1d371'],
            unknown_0x89732f60=json_data['unknown_0x89732f60'],
            unknown_0x3b774d55=json_data['unknown_0x3b774d55'],
            max_additive_change=json_data['max_additive_change'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'max_speed': self.max_speed,
            'unknown_0x7e1338f8': self.unknown_0x7e1338f8,
            'unknown_0x3cd77ebc': self.unknown_0x3cd77ebc,
            'unknown_0xe79a390f': self.unknown_0xe79a390f,
            'unknown_0x8f922c1c': self.unknown_0x8f922c1c,
            'unknown_0xd4c6cc95': self.unknown_0xd4c6cc95,
            'unknown_0xadb1d371': self.unknown_0xadb1d371,
            'unknown_0x89732f60': self.unknown_0x89732f60,
            'unknown_0x3b774d55': self.unknown_0x3b774d55,
            'max_additive_change': self.max_additive_change,
        }


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7e1338f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3cd77ebc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe79a390f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f922c1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd4c6cc95(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xadb1d371(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x89732f60(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3b774d55(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_additive_change(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x82db0cbe: ('max_speed', _decode_max_speed),
    0x7e1338f8: ('unknown_0x7e1338f8', _decode_unknown_0x7e1338f8),
    0x3cd77ebc: ('unknown_0x3cd77ebc', _decode_unknown_0x3cd77ebc),
    0xe79a390f: ('unknown_0xe79a390f', _decode_unknown_0xe79a390f),
    0x8f922c1c: ('unknown_0x8f922c1c', _decode_unknown_0x8f922c1c),
    0xd4c6cc95: ('unknown_0xd4c6cc95', _decode_unknown_0xd4c6cc95),
    0xadb1d371: ('unknown_0xadb1d371', _decode_unknown_0xadb1d371),
    0x89732f60: ('unknown_0x89732f60', _decode_unknown_0x89732f60),
    0x3b774d55: ('unknown_0x3b774d55', _decode_unknown_0x3b774d55),
    0x4de17472: ('max_additive_change', _decode_max_additive_change),
}

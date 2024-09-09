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
    class UnknownStruct122Json(typing_extensions.TypedDict):
        unknown_0x9aebebc8: int
        unknown_0x9af3fd16: bool
        unknown_0x314c7ce4: float
        unknown_0x74367d95: int
        mechanoid_delta_rate: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x9aebebc8, 0x9af3fd16, 0x314c7ce4, 0x74367d95, 0x72173369)


@dataclasses.dataclass()
class UnknownStruct122(BaseProperty):
    unknown_0x9aebebc8: int = dataclasses.field(default=2036438260, metadata={
        'reflection': FieldReflection[int](
            int, id=0x9aebebc8, original_name='Unknown'
        ),
    })  # Choice
    unknown_0x9af3fd16: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9af3fd16, original_name='Unknown'
        ),
    })
    unknown_0x314c7ce4: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x314c7ce4, original_name='Unknown'
        ),
    })
    unknown_0x74367d95: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x74367d95, original_name='Unknown'
        ),
    })
    mechanoid_delta_rate: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x72173369, original_name='MechanoidDeltaRate'
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
        if property_count != 5:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHLLH?LHfLHlLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(47))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\x9a\xeb\xeb\xc8')  # 0x9aebebc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x9aebebc8))

        data.write(b'\x9a\xf3\xfd\x16')  # 0x9af3fd16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9af3fd16))

        data.write(b'1L|\xe4')  # 0x314c7ce4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x314c7ce4))

        data.write(b't6}\x95')  # 0x74367d95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x74367d95))

        data.write(b'r\x173i')  # 0x72173369
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mechanoid_delta_rate))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct122Json", data)
        return cls(
            unknown_0x9aebebc8=json_data['unknown_0x9aebebc8'],
            unknown_0x9af3fd16=json_data['unknown_0x9af3fd16'],
            unknown_0x314c7ce4=json_data['unknown_0x314c7ce4'],
            unknown_0x74367d95=json_data['unknown_0x74367d95'],
            mechanoid_delta_rate=json_data['mechanoid_delta_rate'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x9aebebc8': self.unknown_0x9aebebc8,
            'unknown_0x9af3fd16': self.unknown_0x9af3fd16,
            'unknown_0x314c7ce4': self.unknown_0x314c7ce4,
            'unknown_0x74367d95': self.unknown_0x74367d95,
            'mechanoid_delta_rate': self.mechanoid_delta_rate,
        }


def _decode_unknown_0x9aebebc8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x9af3fd16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x314c7ce4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x74367d95(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mechanoid_delta_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9aebebc8: ('unknown_0x9aebebc8', _decode_unknown_0x9aebebc8),
    0x9af3fd16: ('unknown_0x9af3fd16', _decode_unknown_0x9af3fd16),
    0x314c7ce4: ('unknown_0x314c7ce4', _decode_unknown_0x314c7ce4),
    0x74367d95: ('unknown_0x74367d95', _decode_unknown_0x74367d95),
    0x72173369: ('mechanoid_delta_rate', _decode_mechanoid_delta_rate),
}

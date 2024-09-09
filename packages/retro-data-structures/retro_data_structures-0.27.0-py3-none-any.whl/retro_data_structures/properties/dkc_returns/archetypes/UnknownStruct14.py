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
    class UnknownStruct14Json(typing_extensions.TypedDict):
        view_point: float
        unknown_0x81dc0c16: bool
        unknown_0x2257ae80: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xaed42887, 0x81dc0c16, 0x2257ae80)


@dataclasses.dataclass()
class UnknownStruct14(BaseProperty):
    view_point: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xaed42887, original_name='ViewPoint'
        ),
    })
    unknown_0x81dc0c16: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x81dc0c16, original_name='Unknown'
        ),
    })
    unknown_0x2257ae80: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2257ae80, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHfLH?LHf')
    
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

        data.write(b'\xae\xd4(\x87')  # 0xaed42887
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.view_point))

        data.write(b'\x81\xdc\x0c\x16')  # 0x81dc0c16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x81dc0c16))

        data.write(b'"W\xae\x80')  # 0x2257ae80
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2257ae80))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct14Json", data)
        return cls(
            view_point=json_data['view_point'],
            unknown_0x81dc0c16=json_data['unknown_0x81dc0c16'],
            unknown_0x2257ae80=json_data['unknown_0x2257ae80'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'view_point': self.view_point,
            'unknown_0x81dc0c16': self.unknown_0x81dc0c16,
            'unknown_0x2257ae80': self.unknown_0x2257ae80,
        }


def _decode_view_point(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81dc0c16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2257ae80(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaed42887: ('view_point', _decode_view_point),
    0x81dc0c16: ('unknown_0x81dc0c16', _decode_unknown_0x81dc0c16),
    0x2257ae80: ('unknown_0x2257ae80', _decode_unknown_0x2257ae80),
}

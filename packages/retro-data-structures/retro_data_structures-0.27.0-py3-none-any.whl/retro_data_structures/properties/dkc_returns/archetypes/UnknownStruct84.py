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
import retro_data_structures.enums.dkc_returns as enums

if typing.TYPE_CHECKING:
    class UnknownStruct84Json(typing_extensions.TypedDict):
        limits: int
        unknown: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x3cc85f81, 0xc6d0d3a4)


@dataclasses.dataclass()
class UnknownStruct84(BaseProperty):
    limits: enums.Limits = dataclasses.field(default=enums.Limits.Unknown1, metadata={
        'reflection': FieldReflection[enums.Limits](
            enums.Limits, id=0x3cc85f81, original_name='Limits', from_json=enums.Limits.from_json, to_json=enums.Limits.to_json
        ),
    })
    unknown: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc6d0d3a4, original_name='Unknown'
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
        if property_count != 2:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHLLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(17))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            enums.Limits(dec[2]),
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'<\xc8_\x81')  # 0x3cc85f81
        data.write(b'\x00\x04')  # size
        self.limits.to_stream(data)

        data.write(b'\xc6\xd0\xd3\xa4')  # 0xc6d0d3a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct84Json", data)
        return cls(
            limits=enums.Limits.from_json(json_data['limits']),
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'limits': self.limits.to_json(),
            'unknown': self.unknown,
        }


def _decode_limits(data: typing.BinaryIO, property_size: int):
    return enums.Limits.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3cc85f81: ('limits', _decode_limits),
    0xc6d0d3a4: ('unknown', _decode_unknown),
}

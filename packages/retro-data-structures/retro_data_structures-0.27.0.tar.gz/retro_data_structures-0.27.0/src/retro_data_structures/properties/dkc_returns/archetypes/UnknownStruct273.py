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
    class UnknownStruct273Json(typing_extensions.TypedDict):
        unknown_0x0eafc768: int
        unknown_0x03223140: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xeafc768, 0x3223140)


@dataclasses.dataclass()
class UnknownStruct273(BaseProperty):
    unknown_0x0eafc768: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x0eafc768, original_name='Unknown'
        ),
    })
    unknown_0x03223140: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x03223140, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHlLHl')
    
        dec = _FAST_FORMAT.unpack(data.read(20))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x0e\xaf\xc7h')  # 0xeafc768
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x0eafc768))

        data.write(b'\x03"1@')  # 0x3223140
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x03223140))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct273Json", data)
        return cls(
            unknown_0x0eafc768=json_data['unknown_0x0eafc768'],
            unknown_0x03223140=json_data['unknown_0x03223140'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x0eafc768': self.unknown_0x0eafc768,
            'unknown_0x03223140': self.unknown_0x03223140,
        }


def _decode_unknown_0x0eafc768(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x03223140(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xeafc768: ('unknown_0x0eafc768', _decode_unknown_0x0eafc768),
    0x3223140: ('unknown_0x03223140', _decode_unknown_0x03223140),
}

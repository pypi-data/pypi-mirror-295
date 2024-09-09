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
    class UnknownStruct60Json(typing_extensions.TypedDict):
        swoop_direction: int
        type: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x13d70b67, 0x474bcce3)


@dataclasses.dataclass()
class UnknownStruct60(BaseProperty):
    swoop_direction: enums.SwoopDirection = dataclasses.field(default=enums.SwoopDirection.Unknown1, metadata={
        'reflection': FieldReflection[enums.SwoopDirection](
            enums.SwoopDirection, id=0x13d70b67, original_name='SwoopDirection', from_json=enums.SwoopDirection.from_json, to_json=enums.SwoopDirection.to_json
        ),
    })
    type: enums.UnknownEnum4 = dataclasses.field(default=enums.UnknownEnum4.Unknown1, metadata={
        'reflection': FieldReflection[enums.UnknownEnum4](
            enums.UnknownEnum4, id=0x474bcce3, original_name='Type', from_json=enums.UnknownEnum4.from_json, to_json=enums.UnknownEnum4.to_json
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
            _FAST_FORMAT = struct.Struct('>LHLLHL')
    
        dec = _FAST_FORMAT.unpack(data.read(20))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            enums.SwoopDirection(dec[2]),
            enums.UnknownEnum4(dec[5]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x13\xd7\x0bg')  # 0x13d70b67
        data.write(b'\x00\x04')  # size
        self.swoop_direction.to_stream(data)

        data.write(b'GK\xcc\xe3')  # 0x474bcce3
        data.write(b'\x00\x04')  # size
        self.type.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct60Json", data)
        return cls(
            swoop_direction=enums.SwoopDirection.from_json(json_data['swoop_direction']),
            type=enums.UnknownEnum4.from_json(json_data['type']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'swoop_direction': self.swoop_direction.to_json(),
            'type': self.type.to_json(),
        }


def _decode_swoop_direction(data: typing.BinaryIO, property_size: int):
    return enums.SwoopDirection.from_stream(data)


def _decode_type(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum4.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13d70b67: ('swoop_direction', _decode_swoop_direction),
    0x474bcce3: ('type', _decode_type),
}

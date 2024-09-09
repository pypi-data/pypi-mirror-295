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
    class UnknownStruct92Json(typing_extensions.TypedDict):
        unknown: bool
        auto_start_light: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x5d289613, 0xaedfa091)


@dataclasses.dataclass()
class UnknownStruct92(BaseProperty):
    unknown: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5d289613, original_name='Unknown'
        ),
    })
    auto_start_light: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xaedfa091, original_name='AutoStartLight'
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
            _FAST_FORMAT = struct.Struct('>LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(14))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'](\x96\x13')  # 0x5d289613
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\xae\xdf\xa0\x91')  # 0xaedfa091
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start_light))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct92Json", data)
        return cls(
            unknown=json_data['unknown'],
            auto_start_light=json_data['auto_start_light'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'auto_start_light': self.auto_start_light,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start_light(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d289613: ('unknown', _decode_unknown),
    0xaedfa091: ('auto_start_light', _decode_auto_start_light),
}

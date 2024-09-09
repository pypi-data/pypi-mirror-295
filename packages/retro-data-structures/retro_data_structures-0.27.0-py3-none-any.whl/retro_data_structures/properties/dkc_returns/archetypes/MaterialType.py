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
    class MaterialTypeJson(typing_extensions.TypedDict):
        material_type: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x95a68d4c)


@dataclasses.dataclass()
class MaterialType(BaseProperty):
    material_type: enums.UnknownEnum1 = dataclasses.field(default=enums.UnknownEnum1.Unknown1, metadata={
        'reflection': FieldReflection[enums.UnknownEnum1](
            enums.UnknownEnum1, id=0x95a68d4c, original_name='MaterialType', from_json=enums.UnknownEnum1.from_json, to_json=enums.UnknownEnum1.to_json
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
        if property_count != 1:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHL')
    
        dec = _FAST_FORMAT.unpack(data.read(10))
        assert (dec[0]) == _FAST_IDS
        return cls(
            enums.UnknownEnum1(dec[2]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\x95\xa6\x8dL')  # 0x95a68d4c
        data.write(b'\x00\x04')  # size
        self.material_type.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MaterialTypeJson", data)
        return cls(
            material_type=enums.UnknownEnum1.from_json(json_data['material_type']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'material_type': self.material_type.to_json(),
        }


def _decode_material_type(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum1.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x95a68d4c: ('material_type', _decode_material_type),
}

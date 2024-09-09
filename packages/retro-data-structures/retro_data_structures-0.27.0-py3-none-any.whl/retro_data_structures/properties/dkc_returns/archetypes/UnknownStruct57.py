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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct278 import UnknownStruct278

if typing.TYPE_CHECKING:
    class UnknownStruct57Json(typing_extensions.TypedDict):
        unknown_struct278: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct57(BaseProperty):
    unknown_struct278: UnknownStruct278 = dataclasses.field(default_factory=UnknownStruct278, metadata={
        'reflection': FieldReflection[UnknownStruct278](
            UnknownStruct278, id=0x1858cbdb, original_name='UnknownStruct278', from_json=UnknownStruct278.from_json, to_json=UnknownStruct278.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1858cbdb
        unknown_struct278 = UnknownStruct278.from_stream(data, property_size)
    
        return cls(unknown_struct278)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\x18X\xcb\xdb')  # 0x1858cbdb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct278.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct57Json", data)
        return cls(
            unknown_struct278=UnknownStruct278.from_json(json_data['unknown_struct278']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct278': self.unknown_struct278.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1858cbdb: ('unknown_struct278', UnknownStruct278.from_stream),
}

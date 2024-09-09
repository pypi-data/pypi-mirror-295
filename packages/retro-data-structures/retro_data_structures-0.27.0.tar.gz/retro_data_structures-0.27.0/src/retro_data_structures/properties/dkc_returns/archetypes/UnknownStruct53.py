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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct54 import UnknownStruct54

if typing.TYPE_CHECKING:
    class UnknownStruct53Json(typing_extensions.TypedDict):
        unknown_struct54: json_util.JsonObject
        insert_chance: float
    

@dataclasses.dataclass()
class UnknownStruct53(BaseProperty):
    unknown_struct54: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54, metadata={
        'reflection': FieldReflection[UnknownStruct54](
            UnknownStruct54, id=0x45d39080, original_name='UnknownStruct54', from_json=UnknownStruct54.from_json, to_json=UnknownStruct54.to_json
        ),
    })
    insert_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1f9bcb8f, original_name='InsertChance'
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x45d39080
        unknown_struct54 = UnknownStruct54.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1f9bcb8f
        insert_chance = struct.unpack('>f', data.read(4))[0]
    
        return cls(unknown_struct54, insert_chance)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'E\xd3\x90\x80')  # 0x45d39080
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\x9b\xcb\x8f')  # 0x1f9bcb8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.insert_chance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct53Json", data)
        return cls(
            unknown_struct54=UnknownStruct54.from_json(json_data['unknown_struct54']),
            insert_chance=json_data['insert_chance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct54': self.unknown_struct54.to_json(),
            'insert_chance': self.insert_chance,
        }


def _decode_insert_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45d39080: ('unknown_struct54', UnknownStruct54.from_stream),
    0x1f9bcb8f: ('insert_chance', _decode_insert_chance),
}

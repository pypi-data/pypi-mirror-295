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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct285 import UnknownStruct285
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct286 import UnknownStruct286

if typing.TYPE_CHECKING:
    class VolcanoBossBodyPartStructBJson(typing_extensions.TypedDict):
        unknown_struct285: json_util.JsonObject
        unknown_struct286: json_util.JsonObject
    

@dataclasses.dataclass()
class VolcanoBossBodyPartStructB(BaseProperty):
    unknown_struct285: UnknownStruct285 = dataclasses.field(default_factory=UnknownStruct285, metadata={
        'reflection': FieldReflection[UnknownStruct285](
            UnknownStruct285, id=0xcd85b29d, original_name='UnknownStruct285', from_json=UnknownStruct285.from_json, to_json=UnknownStruct285.to_json
        ),
    })
    unknown_struct286: UnknownStruct286 = dataclasses.field(default_factory=UnknownStruct286, metadata={
        'reflection': FieldReflection[UnknownStruct286](
            UnknownStruct286, id=0x50186b6a, original_name='UnknownStruct286', from_json=UnknownStruct286.from_json, to_json=UnknownStruct286.to_json
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
        assert property_id == 0xcd85b29d
        unknown_struct285 = UnknownStruct285.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50186b6a
        unknown_struct286 = UnknownStruct286.from_stream(data, property_size)
    
        return cls(unknown_struct285, unknown_struct286)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xcd\x85\xb2\x9d')  # 0xcd85b29d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct285.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\x18kj')  # 0x50186b6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct286.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("VolcanoBossBodyPartStructBJson", data)
        return cls(
            unknown_struct285=UnknownStruct285.from_json(json_data['unknown_struct285']),
            unknown_struct286=UnknownStruct286.from_json(json_data['unknown_struct286']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct285': self.unknown_struct285.to_json(),
            'unknown_struct286': self.unknown_struct286.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcd85b29d: ('unknown_struct285', UnknownStruct285.from_stream),
    0x50186b6a: ('unknown_struct286', UnknownStruct286.from_stream),
}

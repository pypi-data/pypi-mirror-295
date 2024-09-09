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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct47 import UnknownStruct47

if typing.TYPE_CHECKING:
    class UnknownStruct193Json(typing_extensions.TypedDict):
        unknown_struct47_0xd6554c1a: json_util.JsonObject
        unknown_struct47_0xe59c4016: json_util.JsonObject
        unknown_struct47_0x2416759c: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct193(BaseProperty):
    unknown_struct47_0xd6554c1a: UnknownStruct47 = dataclasses.field(default_factory=UnknownStruct47, metadata={
        'reflection': FieldReflection[UnknownStruct47](
            UnknownStruct47, id=0xd6554c1a, original_name='UnknownStruct47', from_json=UnknownStruct47.from_json, to_json=UnknownStruct47.to_json
        ),
    })
    unknown_struct47_0xe59c4016: UnknownStruct47 = dataclasses.field(default_factory=UnknownStruct47, metadata={
        'reflection': FieldReflection[UnknownStruct47](
            UnknownStruct47, id=0xe59c4016, original_name='UnknownStruct47', from_json=UnknownStruct47.from_json, to_json=UnknownStruct47.to_json
        ),
    })
    unknown_struct47_0x2416759c: UnknownStruct47 = dataclasses.field(default_factory=UnknownStruct47, metadata={
        'reflection': FieldReflection[UnknownStruct47](
            UnknownStruct47, id=0x2416759c, original_name='UnknownStruct47', from_json=UnknownStruct47.from_json, to_json=UnknownStruct47.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd6554c1a
        unknown_struct47_0xd6554c1a = UnknownStruct47.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe59c4016
        unknown_struct47_0xe59c4016 = UnknownStruct47.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2416759c
        unknown_struct47_0x2416759c = UnknownStruct47.from_stream(data, property_size)
    
        return cls(unknown_struct47_0xd6554c1a, unknown_struct47_0xe59c4016, unknown_struct47_0x2416759c)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xd6UL\x1a')  # 0xd6554c1a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct47_0xd6554c1a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x9c@\x16')  # 0xe59c4016
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct47_0xe59c4016.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\x16u\x9c')  # 0x2416759c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct47_0x2416759c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct193Json", data)
        return cls(
            unknown_struct47_0xd6554c1a=UnknownStruct47.from_json(json_data['unknown_struct47_0xd6554c1a']),
            unknown_struct47_0xe59c4016=UnknownStruct47.from_json(json_data['unknown_struct47_0xe59c4016']),
            unknown_struct47_0x2416759c=UnknownStruct47.from_json(json_data['unknown_struct47_0x2416759c']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct47_0xd6554c1a': self.unknown_struct47_0xd6554c1a.to_json(),
            'unknown_struct47_0xe59c4016': self.unknown_struct47_0xe59c4016.to_json(),
            'unknown_struct47_0x2416759c': self.unknown_struct47_0x2416759c.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd6554c1a: ('unknown_struct47_0xd6554c1a', UnknownStruct47.from_stream),
    0xe59c4016: ('unknown_struct47_0xe59c4016', UnknownStruct47.from_stream),
    0x2416759c: ('unknown_struct47_0x2416759c', UnknownStruct47.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct149 import UnknownStruct149
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct150 import UnknownStruct150
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct151 import UnknownStruct151
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct34 import UnknownStruct34

if typing.TYPE_CHECKING:
    class PauseHUDJson(typing_extensions.TypedDict):
        unknown_struct149: json_util.JsonObject
        unknown_struct150: json_util.JsonObject
        unknown_struct151: json_util.JsonObject
        unknown_struct34: json_util.JsonObject
    

@dataclasses.dataclass()
class PauseHUD(BaseProperty):
    unknown_struct149: UnknownStruct149 = dataclasses.field(default_factory=UnknownStruct149, metadata={
        'reflection': FieldReflection[UnknownStruct149](
            UnknownStruct149, id=0xeb03168d, original_name='UnknownStruct149', from_json=UnknownStruct149.from_json, to_json=UnknownStruct149.to_json
        ),
    })
    unknown_struct150: UnknownStruct150 = dataclasses.field(default_factory=UnknownStruct150, metadata={
        'reflection': FieldReflection[UnknownStruct150](
            UnknownStruct150, id=0xccd85456, original_name='UnknownStruct150', from_json=UnknownStruct150.from_json, to_json=UnknownStruct150.to_json
        ),
    })
    unknown_struct151: UnknownStruct151 = dataclasses.field(default_factory=UnknownStruct151, metadata={
        'reflection': FieldReflection[UnknownStruct151](
            UnknownStruct151, id=0xb48315cc, original_name='UnknownStruct151', from_json=UnknownStruct151.from_json, to_json=UnknownStruct151.to_json
        ),
    })
    unknown_struct34: UnknownStruct34 = dataclasses.field(default_factory=UnknownStruct34, metadata={
        'reflection': FieldReflection[UnknownStruct34](
            UnknownStruct34, id=0xb54dd084, original_name='UnknownStruct34', from_json=UnknownStruct34.from_json, to_json=UnknownStruct34.to_json
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
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb03168d
        unknown_struct149 = UnknownStruct149.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xccd85456
        unknown_struct150 = UnknownStruct150.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb48315cc
        unknown_struct151 = UnknownStruct151.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb54dd084
        unknown_struct34 = UnknownStruct34.from_stream(data, property_size)
    
        return cls(unknown_struct149, unknown_struct150, unknown_struct151, unknown_struct34)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xeb\x03\x16\x8d')  # 0xeb03168d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct149.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc\xd8TV')  # 0xccd85456
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct150.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4\x83\x15\xcc')  # 0xb48315cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct151.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb5M\xd0\x84')  # 0xb54dd084
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct34.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PauseHUDJson", data)
        return cls(
            unknown_struct149=UnknownStruct149.from_json(json_data['unknown_struct149']),
            unknown_struct150=UnknownStruct150.from_json(json_data['unknown_struct150']),
            unknown_struct151=UnknownStruct151.from_json(json_data['unknown_struct151']),
            unknown_struct34=UnknownStruct34.from_json(json_data['unknown_struct34']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct149': self.unknown_struct149.to_json(),
            'unknown_struct150': self.unknown_struct150.to_json(),
            'unknown_struct151': self.unknown_struct151.to_json(),
            'unknown_struct34': self.unknown_struct34.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xeb03168d: ('unknown_struct149', UnknownStruct149.from_stream),
    0xccd85456: ('unknown_struct150', UnknownStruct150.from_stream),
    0xb48315cc: ('unknown_struct151', UnknownStruct151.from_stream),
    0xb54dd084: ('unknown_struct34', UnknownStruct34.from_stream),
}

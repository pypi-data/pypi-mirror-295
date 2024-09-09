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
from retro_data_structures.properties.dkc_returns.archetypes.JungleBossStructA import JungleBossStructA

if typing.TYPE_CHECKING:
    class UnknownStruct203Json(typing_extensions.TypedDict):
        jungle_boss_struct_a_0xd9bba58a: json_util.JsonObject
        jungle_boss_struct_a_0x2bec4872: json_util.JsonObject
        jungle_boss_struct_a_0xccf1eee5: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct203(BaseProperty):
    jungle_boss_struct_a_0xd9bba58a: JungleBossStructA = dataclasses.field(default_factory=JungleBossStructA, metadata={
        'reflection': FieldReflection[JungleBossStructA](
            JungleBossStructA, id=0xd9bba58a, original_name='JungleBossStructA', from_json=JungleBossStructA.from_json, to_json=JungleBossStructA.to_json
        ),
    })
    jungle_boss_struct_a_0x2bec4872: JungleBossStructA = dataclasses.field(default_factory=JungleBossStructA, metadata={
        'reflection': FieldReflection[JungleBossStructA](
            JungleBossStructA, id=0x2bec4872, original_name='JungleBossStructA', from_json=JungleBossStructA.from_json, to_json=JungleBossStructA.to_json
        ),
    })
    jungle_boss_struct_a_0xccf1eee5: JungleBossStructA = dataclasses.field(default_factory=JungleBossStructA, metadata={
        'reflection': FieldReflection[JungleBossStructA](
            JungleBossStructA, id=0xccf1eee5, original_name='JungleBossStructA', from_json=JungleBossStructA.from_json, to_json=JungleBossStructA.to_json
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
        assert property_id == 0xd9bba58a
        jungle_boss_struct_a_0xd9bba58a = JungleBossStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2bec4872
        jungle_boss_struct_a_0x2bec4872 = JungleBossStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xccf1eee5
        jungle_boss_struct_a_0xccf1eee5 = JungleBossStructA.from_stream(data, property_size)
    
        return cls(jungle_boss_struct_a_0xd9bba58a, jungle_boss_struct_a_0x2bec4872, jungle_boss_struct_a_0xccf1eee5)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xd9\xbb\xa5\x8a')  # 0xd9bba58a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_a_0xd9bba58a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+\xecHr')  # 0x2bec4872
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_a_0x2bec4872.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc\xf1\xee\xe5')  # 0xccf1eee5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_a_0xccf1eee5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct203Json", data)
        return cls(
            jungle_boss_struct_a_0xd9bba58a=JungleBossStructA.from_json(json_data['jungle_boss_struct_a_0xd9bba58a']),
            jungle_boss_struct_a_0x2bec4872=JungleBossStructA.from_json(json_data['jungle_boss_struct_a_0x2bec4872']),
            jungle_boss_struct_a_0xccf1eee5=JungleBossStructA.from_json(json_data['jungle_boss_struct_a_0xccf1eee5']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'jungle_boss_struct_a_0xd9bba58a': self.jungle_boss_struct_a_0xd9bba58a.to_json(),
            'jungle_boss_struct_a_0x2bec4872': self.jungle_boss_struct_a_0x2bec4872.to_json(),
            'jungle_boss_struct_a_0xccf1eee5': self.jungle_boss_struct_a_0xccf1eee5.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd9bba58a: ('jungle_boss_struct_a_0xd9bba58a', JungleBossStructA.from_stream),
    0x2bec4872: ('jungle_boss_struct_a_0x2bec4872', JungleBossStructA.from_stream),
    0xccf1eee5: ('jungle_boss_struct_a_0xccf1eee5', JungleBossStructA.from_stream),
}

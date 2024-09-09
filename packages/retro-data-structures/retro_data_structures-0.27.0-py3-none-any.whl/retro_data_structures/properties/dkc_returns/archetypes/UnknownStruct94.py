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
from retro_data_structures.properties.dkc_returns.archetypes.ForestBossStructC import ForestBossStructC

if typing.TYPE_CHECKING:
    class UnknownStruct94Json(typing_extensions.TypedDict):
        forest_boss_struct_c_0x63f77b98: json_util.JsonObject
        forest_boss_struct_c_0x8561e02d: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct94(BaseProperty):
    forest_boss_struct_c_0x63f77b98: ForestBossStructC = dataclasses.field(default_factory=ForestBossStructC, metadata={
        'reflection': FieldReflection[ForestBossStructC](
            ForestBossStructC, id=0x63f77b98, original_name='ForestBossStructC', from_json=ForestBossStructC.from_json, to_json=ForestBossStructC.to_json
        ),
    })
    forest_boss_struct_c_0x8561e02d: ForestBossStructC = dataclasses.field(default_factory=ForestBossStructC, metadata={
        'reflection': FieldReflection[ForestBossStructC](
            ForestBossStructC, id=0x8561e02d, original_name='ForestBossStructC', from_json=ForestBossStructC.from_json, to_json=ForestBossStructC.to_json
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
        assert property_id == 0x63f77b98
        forest_boss_struct_c_0x63f77b98 = ForestBossStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8561e02d
        forest_boss_struct_c_0x8561e02d = ForestBossStructC.from_stream(data, property_size)
    
        return cls(forest_boss_struct_c_0x63f77b98, forest_boss_struct_c_0x8561e02d)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'c\xf7{\x98')  # 0x63f77b98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_c_0x63f77b98.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85a\xe0-')  # 0x8561e02d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_c_0x8561e02d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct94Json", data)
        return cls(
            forest_boss_struct_c_0x63f77b98=ForestBossStructC.from_json(json_data['forest_boss_struct_c_0x63f77b98']),
            forest_boss_struct_c_0x8561e02d=ForestBossStructC.from_json(json_data['forest_boss_struct_c_0x8561e02d']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'forest_boss_struct_c_0x63f77b98': self.forest_boss_struct_c_0x63f77b98.to_json(),
            'forest_boss_struct_c_0x8561e02d': self.forest_boss_struct_c_0x8561e02d.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x63f77b98: ('forest_boss_struct_c_0x63f77b98', ForestBossStructC.from_stream),
    0x8561e02d: ('forest_boss_struct_c_0x8561e02d', ForestBossStructC.from_stream),
}

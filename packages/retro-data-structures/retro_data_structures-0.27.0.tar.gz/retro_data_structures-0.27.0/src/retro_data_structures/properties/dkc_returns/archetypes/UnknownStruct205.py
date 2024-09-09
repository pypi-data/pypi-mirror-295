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
from retro_data_structures.properties.dkc_returns.archetypes.JungleBossStructC import JungleBossStructC

if typing.TYPE_CHECKING:
    class UnknownStruct205Json(typing_extensions.TypedDict):
        number_of_sets: int
        jungle_boss_struct_c_0x6e3800d3: json_util.JsonObject
        jungle_boss_struct_c_0xbda31c28: json_util.JsonObject
        jungle_boss_struct_c_0xf32a1781: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct205(BaseProperty):
    number_of_sets: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xfc8227a7, original_name='NumberOfSets'
        ),
    })
    jungle_boss_struct_c_0x6e3800d3: JungleBossStructC = dataclasses.field(default_factory=JungleBossStructC, metadata={
        'reflection': FieldReflection[JungleBossStructC](
            JungleBossStructC, id=0x6e3800d3, original_name='JungleBossStructC', from_json=JungleBossStructC.from_json, to_json=JungleBossStructC.to_json
        ),
    })
    jungle_boss_struct_c_0xbda31c28: JungleBossStructC = dataclasses.field(default_factory=JungleBossStructC, metadata={
        'reflection': FieldReflection[JungleBossStructC](
            JungleBossStructC, id=0xbda31c28, original_name='JungleBossStructC', from_json=JungleBossStructC.from_json, to_json=JungleBossStructC.to_json
        ),
    })
    jungle_boss_struct_c_0xf32a1781: JungleBossStructC = dataclasses.field(default_factory=JungleBossStructC, metadata={
        'reflection': FieldReflection[JungleBossStructC](
            JungleBossStructC, id=0xf32a1781, original_name='JungleBossStructC', from_json=JungleBossStructC.from_json, to_json=JungleBossStructC.to_json
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
        assert property_id == 0xfc8227a7
        number_of_sets = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6e3800d3
        jungle_boss_struct_c_0x6e3800d3 = JungleBossStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbda31c28
        jungle_boss_struct_c_0xbda31c28 = JungleBossStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf32a1781
        jungle_boss_struct_c_0xf32a1781 = JungleBossStructC.from_stream(data, property_size)
    
        return cls(number_of_sets, jungle_boss_struct_c_0x6e3800d3, jungle_boss_struct_c_0xbda31c28, jungle_boss_struct_c_0xf32a1781)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b"\xfc\x82'\xa7")  # 0xfc8227a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_sets))

        data.write(b'n8\x00\xd3')  # 0x6e3800d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_c_0x6e3800d3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\xa3\x1c(')  # 0xbda31c28
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_c_0xbda31c28.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3*\x17\x81')  # 0xf32a1781
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_c_0xf32a1781.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct205Json", data)
        return cls(
            number_of_sets=json_data['number_of_sets'],
            jungle_boss_struct_c_0x6e3800d3=JungleBossStructC.from_json(json_data['jungle_boss_struct_c_0x6e3800d3']),
            jungle_boss_struct_c_0xbda31c28=JungleBossStructC.from_json(json_data['jungle_boss_struct_c_0xbda31c28']),
            jungle_boss_struct_c_0xf32a1781=JungleBossStructC.from_json(json_data['jungle_boss_struct_c_0xf32a1781']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_sets': self.number_of_sets,
            'jungle_boss_struct_c_0x6e3800d3': self.jungle_boss_struct_c_0x6e3800d3.to_json(),
            'jungle_boss_struct_c_0xbda31c28': self.jungle_boss_struct_c_0xbda31c28.to_json(),
            'jungle_boss_struct_c_0xf32a1781': self.jungle_boss_struct_c_0xf32a1781.to_json(),
        }


def _decode_number_of_sets(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfc8227a7: ('number_of_sets', _decode_number_of_sets),
    0x6e3800d3: ('jungle_boss_struct_c_0x6e3800d3', JungleBossStructC.from_stream),
    0xbda31c28: ('jungle_boss_struct_c_0xbda31c28', JungleBossStructC.from_stream),
    0xf32a1781: ('jungle_boss_struct_c_0xf32a1781', JungleBossStructC.from_stream),
}

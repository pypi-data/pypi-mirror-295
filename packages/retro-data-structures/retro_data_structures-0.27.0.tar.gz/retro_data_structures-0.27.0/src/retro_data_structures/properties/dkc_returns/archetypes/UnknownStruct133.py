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
from retro_data_structures.properties.dkc_returns.archetypes.AreaDamageData import AreaDamageData

if typing.TYPE_CHECKING:
    class UnknownStruct133Json(typing_extensions.TypedDict):
        number_of_area_damages: int
        area_damage1: json_util.JsonObject
        area_damage2: json_util.JsonObject
        area_damage3: json_util.JsonObject
        area_damage4: json_util.JsonObject
        area_damage5: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct133(BaseProperty):
    number_of_area_damages: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x4d2af7b7, original_name='NumberOfAreaDamages'
        ),
    })
    area_damage1: AreaDamageData = dataclasses.field(default_factory=AreaDamageData, metadata={
        'reflection': FieldReflection[AreaDamageData](
            AreaDamageData, id=0xd736382f, original_name='AreaDamage1', from_json=AreaDamageData.from_json, to_json=AreaDamageData.to_json
        ),
    })
    area_damage2: AreaDamageData = dataclasses.field(default_factory=AreaDamageData, metadata={
        'reflection': FieldReflection[AreaDamageData](
            AreaDamageData, id=0xc64b5256, original_name='AreaDamage2', from_json=AreaDamageData.from_json, to_json=AreaDamageData.to_json
        ),
    })
    area_damage3: AreaDamageData = dataclasses.field(default_factory=AreaDamageData, metadata={
        'reflection': FieldReflection[AreaDamageData](
            AreaDamageData, id=0x7fb089be, original_name='AreaDamage3', from_json=AreaDamageData.from_json, to_json=AreaDamageData.to_json
        ),
    })
    area_damage4: AreaDamageData = dataclasses.field(default_factory=AreaDamageData, metadata={
        'reflection': FieldReflection[AreaDamageData](
            AreaDamageData, id=0xe4b186a4, original_name='AreaDamage4', from_json=AreaDamageData.from_json, to_json=AreaDamageData.to_json
        ),
    })
    area_damage5: AreaDamageData = dataclasses.field(default_factory=AreaDamageData, metadata={
        'reflection': FieldReflection[AreaDamageData](
            AreaDamageData, id=0x5d4a5d4c, original_name='AreaDamage5', from_json=AreaDamageData.from_json, to_json=AreaDamageData.to_json
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
        if property_count != 6:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4d2af7b7
        number_of_area_damages = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd736382f
        area_damage1 = AreaDamageData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc64b5256
        area_damage2 = AreaDamageData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7fb089be
        area_damage3 = AreaDamageData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe4b186a4
        area_damage4 = AreaDamageData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5d4a5d4c
        area_damage5 = AreaDamageData.from_stream(data, property_size)
    
        return cls(number_of_area_damages, area_damage1, area_damage2, area_damage3, area_damage4, area_damage5)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'M*\xf7\xb7')  # 0x4d2af7b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_area_damages))

        data.write(b'\xd768/')  # 0xd736382f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6KRV')  # 0xc64b5256
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xb0\x89\xbe')  # 0x7fb089be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4\xb1\x86\xa4')  # 0xe4b186a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']J]L')  # 0x5d4a5d4c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.area_damage5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct133Json", data)
        return cls(
            number_of_area_damages=json_data['number_of_area_damages'],
            area_damage1=AreaDamageData.from_json(json_data['area_damage1']),
            area_damage2=AreaDamageData.from_json(json_data['area_damage2']),
            area_damage3=AreaDamageData.from_json(json_data['area_damage3']),
            area_damage4=AreaDamageData.from_json(json_data['area_damage4']),
            area_damage5=AreaDamageData.from_json(json_data['area_damage5']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_area_damages': self.number_of_area_damages,
            'area_damage1': self.area_damage1.to_json(),
            'area_damage2': self.area_damage2.to_json(),
            'area_damage3': self.area_damage3.to_json(),
            'area_damage4': self.area_damage4.to_json(),
            'area_damage5': self.area_damage5.to_json(),
        }


def _decode_number_of_area_damages(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4d2af7b7: ('number_of_area_damages', _decode_number_of_area_damages),
    0xd736382f: ('area_damage1', AreaDamageData.from_stream),
    0xc64b5256: ('area_damage2', AreaDamageData.from_stream),
    0x7fb089be: ('area_damage3', AreaDamageData.from_stream),
    0xe4b186a4: ('area_damage4', AreaDamageData.from_stream),
    0x5d4a5d4c: ('area_damage5', AreaDamageData.from_stream),
}

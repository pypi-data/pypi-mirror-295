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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct23 import UnknownStruct23
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct59 import UnknownStruct59
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct60 import UnknownStruct60
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct61 import UnknownStruct61
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct62 import UnknownStruct62

if typing.TYPE_CHECKING:
    class UnknownStruct48Json(typing_extensions.TypedDict):
        attack_type: int
        unknown: int
        unknown_struct23: json_util.JsonObject
        unknown_struct59: json_util.JsonObject
        unknown_struct60: json_util.JsonObject
        unknown_struct61: json_util.JsonObject
        unknown_struct62: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct48(BaseProperty):
    attack_type: enums.AttackType = dataclasses.field(default=enums.AttackType.Unknown1, metadata={
        'reflection': FieldReflection[enums.AttackType](
            enums.AttackType, id=0x07d939a1, original_name='AttackType', from_json=enums.AttackType.from_json, to_json=enums.AttackType.to_json
        ),
    })
    unknown: int = dataclasses.field(default=3, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8a58a7f8, original_name='Unknown'
        ),
    })
    unknown_struct23: UnknownStruct23 = dataclasses.field(default_factory=UnknownStruct23, metadata={
        'reflection': FieldReflection[UnknownStruct23](
            UnknownStruct23, id=0x93fa48a4, original_name='UnknownStruct23', from_json=UnknownStruct23.from_json, to_json=UnknownStruct23.to_json
        ),
    })
    unknown_struct59: UnknownStruct59 = dataclasses.field(default_factory=UnknownStruct59, metadata={
        'reflection': FieldReflection[UnknownStruct59](
            UnknownStruct59, id=0xc32bdd77, original_name='UnknownStruct59', from_json=UnknownStruct59.from_json, to_json=UnknownStruct59.to_json
        ),
    })
    unknown_struct60: UnknownStruct60 = dataclasses.field(default_factory=UnknownStruct60, metadata={
        'reflection': FieldReflection[UnknownStruct60](
            UnknownStruct60, id=0x5902a3ab, original_name='UnknownStruct60', from_json=UnknownStruct60.from_json, to_json=UnknownStruct60.to_json
        ),
    })
    unknown_struct61: UnknownStruct61 = dataclasses.field(default_factory=UnknownStruct61, metadata={
        'reflection': FieldReflection[UnknownStruct61](
            UnknownStruct61, id=0xc77a8bf8, original_name='UnknownStruct61', from_json=UnknownStruct61.from_json, to_json=UnknownStruct61.to_json
        ),
    })
    unknown_struct62: UnknownStruct62 = dataclasses.field(default_factory=UnknownStruct62, metadata={
        'reflection': FieldReflection[UnknownStruct62](
            UnknownStruct62, id=0x21313785, original_name='UnknownStruct62', from_json=UnknownStruct62.from_json, to_json=UnknownStruct62.to_json
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
        if property_count != 7:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x07d939a1
        attack_type = enums.AttackType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8a58a7f8
        unknown = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x93fa48a4
        unknown_struct23 = UnknownStruct23.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc32bdd77
        unknown_struct59 = UnknownStruct59.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5902a3ab
        unknown_struct60 = UnknownStruct60.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc77a8bf8
        unknown_struct61 = UnknownStruct61.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x21313785
        unknown_struct62 = UnknownStruct62.from_stream(data, property_size)
    
        return cls(attack_type, unknown, unknown_struct23, unknown_struct59, unknown_struct60, unknown_struct61, unknown_struct62)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x07\xd99\xa1')  # 0x7d939a1
        data.write(b'\x00\x04')  # size
        self.attack_type.to_stream(data)

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\x93\xfaH\xa4')  # 0x93fa48a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct23.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3+\xddw')  # 0xc32bdd77
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct59.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x02\xa3\xab')  # 0x5902a3ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct60.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7z\x8b\xf8')  # 0xc77a8bf8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct61.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!17\x85')  # 0x21313785
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct62.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct48Json", data)
        return cls(
            attack_type=enums.AttackType.from_json(json_data['attack_type']),
            unknown=json_data['unknown'],
            unknown_struct23=UnknownStruct23.from_json(json_data['unknown_struct23']),
            unknown_struct59=UnknownStruct59.from_json(json_data['unknown_struct59']),
            unknown_struct60=UnknownStruct60.from_json(json_data['unknown_struct60']),
            unknown_struct61=UnknownStruct61.from_json(json_data['unknown_struct61']),
            unknown_struct62=UnknownStruct62.from_json(json_data['unknown_struct62']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attack_type': self.attack_type.to_json(),
            'unknown': self.unknown,
            'unknown_struct23': self.unknown_struct23.to_json(),
            'unknown_struct59': self.unknown_struct59.to_json(),
            'unknown_struct60': self.unknown_struct60.to_json(),
            'unknown_struct61': self.unknown_struct61.to_json(),
            'unknown_struct62': self.unknown_struct62.to_json(),
        }


def _decode_attack_type(data: typing.BinaryIO, property_size: int):
    return enums.AttackType.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7d939a1: ('attack_type', _decode_attack_type),
    0x8a58a7f8: ('unknown', _decode_unknown),
    0x93fa48a4: ('unknown_struct23', UnknownStruct23.from_stream),
    0xc32bdd77: ('unknown_struct59', UnknownStruct59.from_stream),
    0x5902a3ab: ('unknown_struct60', UnknownStruct60.from_stream),
    0xc77a8bf8: ('unknown_struct61', UnknownStruct61.from_stream),
    0x21313785: ('unknown_struct62', UnknownStruct62.from_stream),
}

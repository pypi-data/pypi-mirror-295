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
from retro_data_structures.properties.dkc_returns.archetypes.GenericCreatureStructD import GenericCreatureStructD

if typing.TYPE_CHECKING:
    class GroupsJson(typing_extensions.TypedDict):
        number_of_groups: int
        group01: json_util.JsonObject
        group02: json_util.JsonObject
        group03: json_util.JsonObject
        group04: json_util.JsonObject
        group05: json_util.JsonObject
        group06: json_util.JsonObject
        group07: json_util.JsonObject
        group08: json_util.JsonObject
    

@dataclasses.dataclass()
class Groups(BaseProperty):
    number_of_groups: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x07f5da3f, original_name='NumberOfGroups'
        ),
    })
    group01: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0x6954c4a6, original_name='Group01', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group02: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0x9b03295e, original_name='Group02', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group03: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0x7c1e8fc9, original_name='Group03', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group04: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0xa4ddf4ef, original_name='Group04', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group05: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0x43c05278, original_name='Group05', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group06: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0xb197bf80, original_name='Group06', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group07: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0x568a1917, original_name='Group07', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
        ),
    })
    group08: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD, metadata={
        'reflection': FieldReflection[GenericCreatureStructD](
            GenericCreatureStructD, id=0xdb604f8d, original_name='Group08', from_json=GenericCreatureStructD.from_json, to_json=GenericCreatureStructD.to_json
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
        if property_count != 9:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x07f5da3f
        number_of_groups = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6954c4a6
        group01 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9b03295e
        group02 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c1e8fc9
        group03 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa4ddf4ef
        group04 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43c05278
        group05 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb197bf80
        group06 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x568a1917
        group07 = GenericCreatureStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb604f8d
        group08 = GenericCreatureStructD.from_stream(data, property_size)
    
        return cls(number_of_groups, group01, group02, group03, group04, group05, group06, group07, group08)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x07\xf5\xda?')  # 0x7f5da3f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_groups))

        data.write(b'iT\xc4\xa6')  # 0x6954c4a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group01.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x03)^')  # 0x9b03295e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\x1e\x8f\xc9')  # 0x7c1e8fc9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group03.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xdd\xf4\xef')  # 0xa4ddf4ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group04.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xc0Rx')  # 0x43c05278
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group05.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb1\x97\xbf\x80')  # 0xb197bf80
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group06.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x8a\x19\x17')  # 0x568a1917
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group07.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdb`O\x8d')  # 0xdb604f8d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group08.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GroupsJson", data)
        return cls(
            number_of_groups=json_data['number_of_groups'],
            group01=GenericCreatureStructD.from_json(json_data['group01']),
            group02=GenericCreatureStructD.from_json(json_data['group02']),
            group03=GenericCreatureStructD.from_json(json_data['group03']),
            group04=GenericCreatureStructD.from_json(json_data['group04']),
            group05=GenericCreatureStructD.from_json(json_data['group05']),
            group06=GenericCreatureStructD.from_json(json_data['group06']),
            group07=GenericCreatureStructD.from_json(json_data['group07']),
            group08=GenericCreatureStructD.from_json(json_data['group08']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_groups': self.number_of_groups,
            'group01': self.group01.to_json(),
            'group02': self.group02.to_json(),
            'group03': self.group03.to_json(),
            'group04': self.group04.to_json(),
            'group05': self.group05.to_json(),
            'group06': self.group06.to_json(),
            'group07': self.group07.to_json(),
            'group08': self.group08.to_json(),
        }


def _decode_number_of_groups(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7f5da3f: ('number_of_groups', _decode_number_of_groups),
    0x6954c4a6: ('group01', GenericCreatureStructD.from_stream),
    0x9b03295e: ('group02', GenericCreatureStructD.from_stream),
    0x7c1e8fc9: ('group03', GenericCreatureStructD.from_stream),
    0xa4ddf4ef: ('group04', GenericCreatureStructD.from_stream),
    0x43c05278: ('group05', GenericCreatureStructD.from_stream),
    0xb197bf80: ('group06', GenericCreatureStructD.from_stream),
    0x568a1917: ('group07', GenericCreatureStructD.from_stream),
    0xdb604f8d: ('group08', GenericCreatureStructD.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.Animations import Animations
from retro_data_structures.properties.dkc_returns.archetypes.Groups import Groups
from retro_data_structures.properties.dkc_returns.archetypes.Sets import Sets

if typing.TYPE_CHECKING:
    class RetronomeMessageJson(typing_extensions.TypedDict):
        time_offset: float
        sets: json_util.JsonObject
        groups: json_util.JsonObject
        animations: json_util.JsonObject
    

@dataclasses.dataclass()
class RetronomeMessage(BaseProperty):
    time_offset: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2539de46, original_name='TimeOffset'
        ),
    })
    sets: Sets = dataclasses.field(default_factory=Sets, metadata={
        'reflection': FieldReflection[Sets](
            Sets, id=0x4ab7d5b8, original_name='Sets', from_json=Sets.from_json, to_json=Sets.to_json
        ),
    })
    groups: Groups = dataclasses.field(default_factory=Groups, metadata={
        'reflection': FieldReflection[Groups](
            Groups, id=0xfe257ce1, original_name='Groups', from_json=Groups.from_json, to_json=Groups.to_json
        ),
    })
    animations: Animations = dataclasses.field(default_factory=Animations, metadata={
        'reflection': FieldReflection[Animations](
            Animations, id=0xd78a4b1f, original_name='Animations', from_json=Animations.from_json, to_json=Animations.to_json
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
        assert property_id == 0x2539de46
        time_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4ab7d5b8
        sets = Sets.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe257ce1
        groups = Groups.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd78a4b1f
        animations = Animations.from_stream(data, property_size)
    
        return cls(time_offset, sets, groups, animations)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'%9\xdeF')  # 0x2539de46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_offset))

        data.write(b'J\xb7\xd5\xb8')  # 0x4ab7d5b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sets.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfe%|\xe1')  # 0xfe257ce1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.groups.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7\x8aK\x1f')  # 0xd78a4b1f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animations.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("RetronomeMessageJson", data)
        return cls(
            time_offset=json_data['time_offset'],
            sets=Sets.from_json(json_data['sets']),
            groups=Groups.from_json(json_data['groups']),
            animations=Animations.from_json(json_data['animations']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'time_offset': self.time_offset,
            'sets': self.sets.to_json(),
            'groups': self.groups.to_json(),
            'animations': self.animations.to_json(),
        }


def _decode_time_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2539de46: ('time_offset', _decode_time_offset),
    0x4ab7d5b8: ('sets', Sets.from_stream),
    0xfe257ce1: ('groups', Groups.from_stream),
    0xd78a4b1f: ('animations', Animations.from_stream),
}

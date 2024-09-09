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
from retro_data_structures.properties.dkc_returns.archetypes.GenericCreatureStructC import GenericCreatureStructC

if typing.TYPE_CHECKING:
    class CollisionActorModifierDataJson(typing_extensions.TypedDict):
        number_of_collision_actor_sets: int
        actor_rule1: json_util.JsonObject
        actor_rule2: json_util.JsonObject
        actor_rule3: json_util.JsonObject
        actor_rule4: json_util.JsonObject
        actor_rule5: json_util.JsonObject
    

@dataclasses.dataclass()
class CollisionActorModifierData(BaseProperty):
    number_of_collision_actor_sets: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6950b5da, original_name='NumberOfCollisionActorSets'
        ),
    })
    actor_rule1: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC, metadata={
        'reflection': FieldReflection[GenericCreatureStructC](
            GenericCreatureStructC, id=0xd54d6fad, original_name='ActorRule1', from_json=GenericCreatureStructC.from_json, to_json=GenericCreatureStructC.to_json
        ),
    })
    actor_rule2: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC, metadata={
        'reflection': FieldReflection[GenericCreatureStructC](
            GenericCreatureStructC, id=0xae53ed4e, original_name='ActorRule2', from_json=GenericCreatureStructC.from_json, to_json=GenericCreatureStructC.to_json
        ),
    })
    actor_rule3: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC, metadata={
        'reflection': FieldReflection[GenericCreatureStructC](
            GenericCreatureStructC, id=0x31896ed0, original_name='ActorRule3', from_json=GenericCreatureStructC.from_json, to_json=GenericCreatureStructC.to_json
        ),
    })
    actor_rule4: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC, metadata={
        'reflection': FieldReflection[GenericCreatureStructC](
            GenericCreatureStructC, id=0x586ee888, original_name='ActorRule4', from_json=GenericCreatureStructC.from_json, to_json=GenericCreatureStructC.to_json
        ),
    })
    actor_rule5: GenericCreatureStructC = dataclasses.field(default_factory=GenericCreatureStructC, metadata={
        'reflection': FieldReflection[GenericCreatureStructC](
            GenericCreatureStructC, id=0xc7b46b16, original_name='ActorRule5', from_json=GenericCreatureStructC.from_json, to_json=GenericCreatureStructC.to_json
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
        assert property_id == 0x6950b5da
        number_of_collision_actor_sets = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd54d6fad
        actor_rule1 = GenericCreatureStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xae53ed4e
        actor_rule2 = GenericCreatureStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x31896ed0
        actor_rule3 = GenericCreatureStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x586ee888
        actor_rule4 = GenericCreatureStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc7b46b16
        actor_rule5 = GenericCreatureStructC.from_stream(data, property_size)
    
        return cls(number_of_collision_actor_sets, actor_rule1, actor_rule2, actor_rule3, actor_rule4, actor_rule5)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'iP\xb5\xda')  # 0x6950b5da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_collision_actor_sets))

        data.write(b'\xd5Mo\xad')  # 0xd54d6fad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaeS\xedN')  # 0xae53ed4e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\x89n\xd0')  # 0x31896ed0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Xn\xe8\x88')  # 0x586ee888
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7\xb4k\x16')  # 0xc7b46b16
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_rule5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CollisionActorModifierDataJson", data)
        return cls(
            number_of_collision_actor_sets=json_data['number_of_collision_actor_sets'],
            actor_rule1=GenericCreatureStructC.from_json(json_data['actor_rule1']),
            actor_rule2=GenericCreatureStructC.from_json(json_data['actor_rule2']),
            actor_rule3=GenericCreatureStructC.from_json(json_data['actor_rule3']),
            actor_rule4=GenericCreatureStructC.from_json(json_data['actor_rule4']),
            actor_rule5=GenericCreatureStructC.from_json(json_data['actor_rule5']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_collision_actor_sets': self.number_of_collision_actor_sets,
            'actor_rule1': self.actor_rule1.to_json(),
            'actor_rule2': self.actor_rule2.to_json(),
            'actor_rule3': self.actor_rule3.to_json(),
            'actor_rule4': self.actor_rule4.to_json(),
            'actor_rule5': self.actor_rule5.to_json(),
        }


def _decode_number_of_collision_actor_sets(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6950b5da: ('number_of_collision_actor_sets', _decode_number_of_collision_actor_sets),
    0xd54d6fad: ('actor_rule1', GenericCreatureStructC.from_stream),
    0xae53ed4e: ('actor_rule2', GenericCreatureStructC.from_stream),
    0x31896ed0: ('actor_rule3', GenericCreatureStructC.from_stream),
    0x586ee888: ('actor_rule4', GenericCreatureStructC.from_stream),
    0xc7b46b16: ('actor_rule5', GenericCreatureStructC.from_stream),
}

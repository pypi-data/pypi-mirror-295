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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class GenericCreatureStructCJson(typing_extensions.TypedDict):
        collision_actor_name: str
        contact_rule: int
        send_state_message: bool
        min_time_between_messages: float
        non_solid: bool
        use_for_creature_touch_bounds: bool
        potential_shadow_receiver: bool
        use_creature_damage_vulnerability: bool
    

@dataclasses.dataclass()
class GenericCreatureStructC(BaseProperty):
    collision_actor_name: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x6c805f56, original_name='CollisionActorName'
        ),
    })
    contact_rule: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd29aaae6, original_name='ContactRule'
        ),
    })
    send_state_message: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4baba4a6, original_name='SendStateMessage'
        ),
    })
    min_time_between_messages: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6e92d661, original_name='MinTimeBetweenMessages'
        ),
    })
    non_solid: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x68f484e7, original_name='NonSolid'
        ),
    })
    use_for_creature_touch_bounds: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe13de823, original_name='UseForCreatureTouchBounds'
        ),
    })
    potential_shadow_receiver: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x99260f54, original_name='PotentialShadowReceiver'
        ),
    })
    use_creature_damage_vulnerability: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8fbdc112, original_name='UseCreatureDamageVulnerability'
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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6c805f56
        collision_actor_name = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd29aaae6
        contact_rule = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4baba4a6
        send_state_message = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6e92d661
        min_time_between_messages = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68f484e7
        non_solid = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe13de823
        use_for_creature_touch_bounds = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x99260f54
        potential_shadow_receiver = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8fbdc112
        use_creature_damage_vulnerability = struct.unpack('>?', data.read(1))[0]
    
        return cls(collision_actor_name, contact_rule, send_state_message, min_time_between_messages, non_solid, use_for_creature_touch_bounds, potential_shadow_receiver, use_creature_damage_vulnerability)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'l\x80_V')  # 0x6c805f56
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.collision_actor_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x9a\xaa\xe6')  # 0xd29aaae6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rule))

        data.write(b'K\xab\xa4\xa6')  # 0x4baba4a6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.send_state_message))

        data.write(b'n\x92\xd6a')  # 0x6e92d661
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_time_between_messages))

        data.write(b'h\xf4\x84\xe7')  # 0x68f484e7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.non_solid))

        data.write(b'\xe1=\xe8#')  # 0xe13de823
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_for_creature_touch_bounds))

        data.write(b'\x99&\x0fT')  # 0x99260f54
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.potential_shadow_receiver))

        data.write(b'\x8f\xbd\xc1\x12')  # 0x8fbdc112
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_creature_damage_vulnerability))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GenericCreatureStructCJson", data)
        return cls(
            collision_actor_name=json_data['collision_actor_name'],
            contact_rule=json_data['contact_rule'],
            send_state_message=json_data['send_state_message'],
            min_time_between_messages=json_data['min_time_between_messages'],
            non_solid=json_data['non_solid'],
            use_for_creature_touch_bounds=json_data['use_for_creature_touch_bounds'],
            potential_shadow_receiver=json_data['potential_shadow_receiver'],
            use_creature_damage_vulnerability=json_data['use_creature_damage_vulnerability'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'collision_actor_name': self.collision_actor_name,
            'contact_rule': self.contact_rule,
            'send_state_message': self.send_state_message,
            'min_time_between_messages': self.min_time_between_messages,
            'non_solid': self.non_solid,
            'use_for_creature_touch_bounds': self.use_for_creature_touch_bounds,
            'potential_shadow_receiver': self.potential_shadow_receiver,
            'use_creature_damage_vulnerability': self.use_creature_damage_vulnerability,
        }


def _decode_collision_actor_name(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_contact_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_send_state_message(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_min_time_between_messages(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_non_solid(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_for_creature_touch_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_potential_shadow_receiver(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_creature_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6c805f56: ('collision_actor_name', _decode_collision_actor_name),
    0xd29aaae6: ('contact_rule', _decode_contact_rule),
    0x4baba4a6: ('send_state_message', _decode_send_state_message),
    0x6e92d661: ('min_time_between_messages', _decode_min_time_between_messages),
    0x68f484e7: ('non_solid', _decode_non_solid),
    0xe13de823: ('use_for_creature_touch_bounds', _decode_use_for_creature_touch_bounds),
    0x99260f54: ('potential_shadow_receiver', _decode_potential_shadow_receiver),
    0x8fbdc112: ('use_creature_damage_vulnerability', _decode_use_creature_damage_vulnerability),
}

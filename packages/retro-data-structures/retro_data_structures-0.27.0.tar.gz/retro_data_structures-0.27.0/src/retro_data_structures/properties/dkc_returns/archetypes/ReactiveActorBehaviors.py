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
from retro_data_structures.properties.dkc_returns.archetypes.ReactiveActorBehavior import ReactiveActorBehavior

if typing.TYPE_CHECKING:
    class ReactiveActorBehaviorsJson(typing_extensions.TypedDict):
        num_behaviors: int
        behavior1: json_util.JsonObject
        behavior2: json_util.JsonObject
        behavior3: json_util.JsonObject
        behavior4: json_util.JsonObject
        behavior5: json_util.JsonObject
        behavior6: json_util.JsonObject
    

@dataclasses.dataclass()
class ReactiveActorBehaviors(BaseProperty):
    num_behaviors: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xc07fa9be, original_name='NumBehaviors'
        ),
    })
    behavior1: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior, metadata={
        'reflection': FieldReflection[ReactiveActorBehavior](
            ReactiveActorBehavior, id=0x8ea67c4f, original_name='Behavior1', from_json=ReactiveActorBehavior.from_json, to_json=ReactiveActorBehavior.to_json
        ),
    })
    behavior2: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior, metadata={
        'reflection': FieldReflection[ReactiveActorBehavior](
            ReactiveActorBehavior, id=0xb7ded10f, original_name='Behavior2', from_json=ReactiveActorBehavior.from_json, to_json=ReactiveActorBehavior.to_json
        ),
    })
    behavior3: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior, metadata={
        'reflection': FieldReflection[ReactiveActorBehavior](
            ReactiveActorBehavior, id=0xa0f6b5cf, original_name='Behavior3', from_json=ReactiveActorBehavior.from_json, to_json=ReactiveActorBehavior.to_json
        ),
    })
    behavior4: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior, metadata={
        'reflection': FieldReflection[ReactiveActorBehavior](
            ReactiveActorBehavior, id=0xc52f8b8f, original_name='Behavior4', from_json=ReactiveActorBehavior.from_json, to_json=ReactiveActorBehavior.to_json
        ),
    })
    behavior5: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior, metadata={
        'reflection': FieldReflection[ReactiveActorBehavior](
            ReactiveActorBehavior, id=0xd207ef4f, original_name='Behavior5', from_json=ReactiveActorBehavior.from_json, to_json=ReactiveActorBehavior.to_json
        ),
    })
    behavior6: ReactiveActorBehavior = dataclasses.field(default_factory=ReactiveActorBehavior, metadata={
        'reflection': FieldReflection[ReactiveActorBehavior](
            ReactiveActorBehavior, id=0xeb7f420f, original_name='Behavior6', from_json=ReactiveActorBehavior.from_json, to_json=ReactiveActorBehavior.to_json
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
        assert property_id == 0xc07fa9be
        num_behaviors = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8ea67c4f
        behavior1 = ReactiveActorBehavior.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb7ded10f
        behavior2 = ReactiveActorBehavior.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa0f6b5cf
        behavior3 = ReactiveActorBehavior.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc52f8b8f
        behavior4 = ReactiveActorBehavior.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd207ef4f
        behavior5 = ReactiveActorBehavior.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb7f420f
        behavior6 = ReactiveActorBehavior.from_stream(data, property_size)
    
        return cls(num_behaviors, behavior1, behavior2, behavior3, behavior4, behavior5, behavior6)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xc0\x7f\xa9\xbe')  # 0xc07fa9be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_behaviors))

        data.write(b'\x8e\xa6|O')  # 0x8ea67c4f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\xde\xd1\x0f')  # 0xb7ded10f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0\xf6\xb5\xcf')  # 0xa0f6b5cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5/\x8b\x8f')  # 0xc52f8b8f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x07\xefO')  # 0xd207ef4f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\x7fB\x0f')  # 0xeb7f420f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behavior6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ReactiveActorBehaviorsJson", data)
        return cls(
            num_behaviors=json_data['num_behaviors'],
            behavior1=ReactiveActorBehavior.from_json(json_data['behavior1']),
            behavior2=ReactiveActorBehavior.from_json(json_data['behavior2']),
            behavior3=ReactiveActorBehavior.from_json(json_data['behavior3']),
            behavior4=ReactiveActorBehavior.from_json(json_data['behavior4']),
            behavior5=ReactiveActorBehavior.from_json(json_data['behavior5']),
            behavior6=ReactiveActorBehavior.from_json(json_data['behavior6']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'num_behaviors': self.num_behaviors,
            'behavior1': self.behavior1.to_json(),
            'behavior2': self.behavior2.to_json(),
            'behavior3': self.behavior3.to_json(),
            'behavior4': self.behavior4.to_json(),
            'behavior5': self.behavior5.to_json(),
            'behavior6': self.behavior6.to_json(),
        }


def _decode_num_behaviors(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc07fa9be: ('num_behaviors', _decode_num_behaviors),
    0x8ea67c4f: ('behavior1', ReactiveActorBehavior.from_stream),
    0xb7ded10f: ('behavior2', ReactiveActorBehavior.from_stream),
    0xa0f6b5cf: ('behavior3', ReactiveActorBehavior.from_stream),
    0xc52f8b8f: ('behavior4', ReactiveActorBehavior.from_stream),
    0xd207ef4f: ('behavior5', ReactiveActorBehavior.from_stream),
    0xeb7f420f: ('behavior6', ReactiveActorBehavior.from_stream),
}

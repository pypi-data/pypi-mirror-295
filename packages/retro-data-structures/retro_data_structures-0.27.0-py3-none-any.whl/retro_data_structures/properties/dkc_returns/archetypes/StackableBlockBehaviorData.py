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

if typing.TYPE_CHECKING:
    class StackableBlockBehaviorDataJson(typing_extensions.TypedDict):
        solid_for_roll: bool
        push_impulse: float
        disable_physics: bool
        replace_collision_when_deactivated: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x1df1c4d1, 0x5bb59a3b, 0xe15a93d0, 0x7dbacf7a)


@dataclasses.dataclass()
class StackableBlockBehaviorData(BaseProperty):
    solid_for_roll: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1df1c4d1, original_name='SolidForRoll'
        ),
    })
    push_impulse: float = dataclasses.field(default=1000.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5bb59a3b, original_name='PushImpulse'
        ),
    })
    disable_physics: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe15a93d0, original_name='DisablePhysics'
        ),
    })
    replace_collision_when_deactivated: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7dbacf7a, original_name='ReplaceCollisionWhenDeactivated'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LHfLH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(31))
        assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x1d\xf1\xc4\xd1')  # 0x1df1c4d1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.solid_for_roll))

        data.write(b'[\xb5\x9a;')  # 0x5bb59a3b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.push_impulse))

        data.write(b'\xe1Z\x93\xd0')  # 0xe15a93d0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_physics))

        data.write(b'}\xba\xcfz')  # 0x7dbacf7a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.replace_collision_when_deactivated))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("StackableBlockBehaviorDataJson", data)
        return cls(
            solid_for_roll=json_data['solid_for_roll'],
            push_impulse=json_data['push_impulse'],
            disable_physics=json_data['disable_physics'],
            replace_collision_when_deactivated=json_data['replace_collision_when_deactivated'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'solid_for_roll': self.solid_for_roll,
            'push_impulse': self.push_impulse,
            'disable_physics': self.disable_physics,
            'replace_collision_when_deactivated': self.replace_collision_when_deactivated,
        }


def _decode_solid_for_roll(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_push_impulse(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_physics(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_replace_collision_when_deactivated(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1df1c4d1: ('solid_for_roll', _decode_solid_for_roll),
    0x5bb59a3b: ('push_impulse', _decode_push_impulse),
    0xe15a93d0: ('disable_physics', _decode_disable_physics),
    0x7dbacf7a: ('replace_collision_when_deactivated', _decode_replace_collision_when_deactivated),
}

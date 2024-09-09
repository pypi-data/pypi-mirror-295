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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class ReactiveActorBehaviorJson(typing_extensions.TypedDict):
        triggering_behavior: int
        player: bool
        rambi: bool
        generic_creature: bool
        actor: bool
        unknown_0xbb0ee668: int
        repeat_delay: float
        detection_radius: float
        unknown_0x8ffefc1e: json_util.JsonValue
    

_FAST_FORMAT = None
_FAST_IDS = (0xde87546a, 0xd5699264, 0x16a95d42, 0x793a3f7, 0x982948db, 0xbb0ee668, 0x21311dce, 0x21cdcf21, 0x8ffefc1e)


@dataclasses.dataclass()
class ReactiveActorBehavior(BaseProperty):
    triggering_behavior: enums.TriggeringBehavior = dataclasses.field(default=enums.TriggeringBehavior.Unknown1, metadata={
        'reflection': FieldReflection[enums.TriggeringBehavior](
            enums.TriggeringBehavior, id=0xde87546a, original_name='TriggeringBehavior', from_json=enums.TriggeringBehavior.from_json, to_json=enums.TriggeringBehavior.to_json
        ),
    })
    player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd5699264, original_name='Player'
        ),
    })
    rambi: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x16a95d42, original_name='Rambi'
        ),
    })
    generic_creature: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0793a3f7, original_name='GenericCreature'
        ),
    })
    actor: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x982948db, original_name='Actor'
        ),
    })
    unknown_0xbb0ee668: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xbb0ee668, original_name='Unknown'
        ),
    })
    repeat_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x21311dce, original_name='RepeatDelay'
        ),
    })
    detection_radius: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x21cdcf21, original_name='DetectionRadius'
        ),
    })
    unknown_0x8ffefc1e: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x8ffefc1e, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHLLH?LH?LH?LH?LHlLHfLHfLHfff')
    
        dec = _FAST_FORMAT.unpack(data.read(86))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) == _FAST_IDS
        return cls(
            enums.TriggeringBehavior(dec[2]),
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            Vector(*dec[26:29]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xde\x87Tj')  # 0xde87546a
        data.write(b'\x00\x04')  # size
        self.triggering_behavior.to_stream(data)

        data.write(b'\xd5i\x92d')  # 0xd5699264
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player))

        data.write(b'\x16\xa9]B')  # 0x16a95d42
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rambi))

        data.write(b'\x07\x93\xa3\xf7')  # 0x793a3f7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.generic_creature))

        data.write(b'\x98)H\xdb')  # 0x982948db
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.actor))

        data.write(b'\xbb\x0e\xe6h')  # 0xbb0ee668
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbb0ee668))

        data.write(b'!1\x1d\xce')  # 0x21311dce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.repeat_delay))

        data.write(b'!\xcd\xcf!')  # 0x21cdcf21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_radius))

        data.write(b'\x8f\xfe\xfc\x1e')  # 0x8ffefc1e
        data.write(b'\x00\x0c')  # size
        self.unknown_0x8ffefc1e.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ReactiveActorBehaviorJson", data)
        return cls(
            triggering_behavior=enums.TriggeringBehavior.from_json(json_data['triggering_behavior']),
            player=json_data['player'],
            rambi=json_data['rambi'],
            generic_creature=json_data['generic_creature'],
            actor=json_data['actor'],
            unknown_0xbb0ee668=json_data['unknown_0xbb0ee668'],
            repeat_delay=json_data['repeat_delay'],
            detection_radius=json_data['detection_radius'],
            unknown_0x8ffefc1e=Vector.from_json(json_data['unknown_0x8ffefc1e']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'triggering_behavior': self.triggering_behavior.to_json(),
            'player': self.player,
            'rambi': self.rambi,
            'generic_creature': self.generic_creature,
            'actor': self.actor,
            'unknown_0xbb0ee668': self.unknown_0xbb0ee668,
            'repeat_delay': self.repeat_delay,
            'detection_radius': self.detection_radius,
            'unknown_0x8ffefc1e': self.unknown_0x8ffefc1e.to_json(),
        }


def _decode_triggering_behavior(data: typing.BinaryIO, property_size: int):
    return enums.TriggeringBehavior.from_stream(data)


def _decode_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_generic_creature(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_actor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbb0ee668(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_repeat_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8ffefc1e(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde87546a: ('triggering_behavior', _decode_triggering_behavior),
    0xd5699264: ('player', _decode_player),
    0x16a95d42: ('rambi', _decode_rambi),
    0x793a3f7: ('generic_creature', _decode_generic_creature),
    0x982948db: ('actor', _decode_actor),
    0xbb0ee668: ('unknown_0xbb0ee668', _decode_unknown_0xbb0ee668),
    0x21311dce: ('repeat_delay', _decode_repeat_delay),
    0x21cdcf21: ('detection_radius', _decode_detection_radius),
    0x8ffefc1e: ('unknown_0x8ffefc1e', _decode_unknown_0x8ffefc1e),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo

if typing.TYPE_CHECKING:
    class UnknownStruct244Json(typing_extensions.TypedDict):
        can_be_blown_out: bool
        contact_damage: json_util.JsonObject
        damage_duration: float
        unknown_0xd258286d: str
        unknown_0xe22dd9bb: str
    

@dataclasses.dataclass()
class UnknownStruct244(BaseProperty):
    can_be_blown_out: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd5417338, original_name='CanBeBlownOut'
        ),
    })
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0xd756416e, original_name='ContactDamage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    damage_duration: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd5e7b11e, original_name='DamageDuration'
        ),
    })
    unknown_0xd258286d: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xd258286d, original_name='Unknown'
        ),
    })
    unknown_0xe22dd9bb: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xe22dd9bb, original_name='Unknown'
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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd5417338
        can_be_blown_out = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd756416e
        contact_damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd5e7b11e
        damage_duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd258286d
        unknown_0xd258286d = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe22dd9bb
        unknown_0xe22dd9bb = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(can_be_blown_out, contact_damage, damage_duration, unknown_0xd258286d, unknown_0xe22dd9bb)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xd5As8')  # 0xd5417338
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_be_blown_out))

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd5\xe7\xb1\x1e')  # 0xd5e7b11e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_duration))

        data.write(b'\xd2X(m')  # 0xd258286d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xd258286d.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2-\xd9\xbb')  # 0xe22dd9bb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xe22dd9bb.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct244Json", data)
        return cls(
            can_be_blown_out=json_data['can_be_blown_out'],
            contact_damage=DamageInfo.from_json(json_data['contact_damage']),
            damage_duration=json_data['damage_duration'],
            unknown_0xd258286d=json_data['unknown_0xd258286d'],
            unknown_0xe22dd9bb=json_data['unknown_0xe22dd9bb'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'can_be_blown_out': self.can_be_blown_out,
            'contact_damage': self.contact_damage.to_json(),
            'damage_duration': self.damage_duration,
            'unknown_0xd258286d': self.unknown_0xd258286d,
            'unknown_0xe22dd9bb': self.unknown_0xe22dd9bb,
        }


def _decode_can_be_blown_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damage_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd258286d(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown_0xe22dd9bb(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd5417338: ('can_be_blown_out', _decode_can_be_blown_out),
    0xd756416e: ('contact_damage', DamageInfo.from_stream),
    0xd5e7b11e: ('damage_duration', _decode_damage_duration),
    0xd258286d: ('unknown_0xd258286d', _decode_unknown_0xd258286d),
    0xe22dd9bb: ('unknown_0xe22dd9bb', _decode_unknown_0xe22dd9bb),
}

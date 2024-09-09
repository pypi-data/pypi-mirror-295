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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAttackBounceData import PlayerAttackBounceData
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class PlayerBarrelCannonDataJson(typing_extensions.TypedDict):
        part: int
        barrel_cannon_effect_locator: str
        wall_bounce_constant: float
        max_land_carry_over_speed: float
        attack_damage_sound: int
        attack_bounce_data: json_util.JsonObject
        unknown_0xe06d7b15: int
        unknown_0x4364525d: int
        unknown_0x2abd7e71: int
    

@dataclasses.dataclass()
class PlayerBarrelCannonData(BaseProperty):
    part: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x381882d7, original_name='PART'
        ),
    })
    barrel_cannon_effect_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xbd8e1d39, original_name='BarrelCannonEffectLocator'
        ),
    })
    wall_bounce_constant: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x48b5def1, original_name='WallBounceConstant'
        ),
    })
    max_land_carry_over_speed: float = dataclasses.field(default=4.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4c97be6e, original_name='MaxLandCarryOverSpeed'
        ),
    })
    attack_damage_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6b4ed718, original_name='AttackDamageSound'
        ),
    })
    attack_bounce_data: PlayerAttackBounceData = dataclasses.field(default_factory=PlayerAttackBounceData, metadata={
        'reflection': FieldReflection[PlayerAttackBounceData](
            PlayerAttackBounceData, id=0x9583ee9a, original_name='AttackBounceData', from_json=PlayerAttackBounceData.from_json, to_json=PlayerAttackBounceData.to_json
        ),
    })
    unknown_0xe06d7b15: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe06d7b15, original_name='Unknown'
        ),
    })
    unknown_0x4364525d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4364525d, original_name='Unknown'
        ),
    })
    unknown_0x2abd7e71: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2abd7e71, original_name='Unknown'
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
        assert property_id == 0x381882d7
        part = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbd8e1d39
        barrel_cannon_effect_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x48b5def1
        wall_bounce_constant = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4c97be6e
        max_land_carry_over_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b4ed718
        attack_damage_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9583ee9a
        attack_bounce_data = PlayerAttackBounceData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe06d7b15
        unknown_0xe06d7b15 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4364525d
        unknown_0x4364525d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2abd7e71
        unknown_0x2abd7e71 = struct.unpack(">Q", data.read(8))[0]
    
        return cls(part, barrel_cannon_effect_locator, wall_bounce_constant, max_land_carry_over_speed, attack_damage_sound, attack_bounce_data, unknown_0xe06d7b15, unknown_0x4364525d, unknown_0x2abd7e71)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'8\x18\x82\xd7')  # 0x381882d7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'\xbd\x8e\x1d9')  # 0xbd8e1d39
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.barrel_cannon_effect_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'H\xb5\xde\xf1')  # 0x48b5def1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_bounce_constant))

        data.write(b'L\x97\xben')  # 0x4c97be6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_land_carry_over_speed))

        data.write(b'kN\xd7\x18')  # 0x6b4ed718
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.attack_damage_sound))

        data.write(b'\x95\x83\xee\x9a')  # 0x9583ee9a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_bounce_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0m{\x15')  # 0xe06d7b15
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xe06d7b15))

        data.write(b'CdR]')  # 0x4364525d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x4364525d))

        data.write(b'*\xbd~q')  # 0x2abd7e71
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x2abd7e71))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerBarrelCannonDataJson", data)
        return cls(
            part=json_data['part'],
            barrel_cannon_effect_locator=json_data['barrel_cannon_effect_locator'],
            wall_bounce_constant=json_data['wall_bounce_constant'],
            max_land_carry_over_speed=json_data['max_land_carry_over_speed'],
            attack_damage_sound=json_data['attack_damage_sound'],
            attack_bounce_data=PlayerAttackBounceData.from_json(json_data['attack_bounce_data']),
            unknown_0xe06d7b15=json_data['unknown_0xe06d7b15'],
            unknown_0x4364525d=json_data['unknown_0x4364525d'],
            unknown_0x2abd7e71=json_data['unknown_0x2abd7e71'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'part': self.part,
            'barrel_cannon_effect_locator': self.barrel_cannon_effect_locator,
            'wall_bounce_constant': self.wall_bounce_constant,
            'max_land_carry_over_speed': self.max_land_carry_over_speed,
            'attack_damage_sound': self.attack_damage_sound,
            'attack_bounce_data': self.attack_bounce_data.to_json(),
            'unknown_0xe06d7b15': self.unknown_0xe06d7b15,
            'unknown_0x4364525d': self.unknown_0x4364525d,
            'unknown_0x2abd7e71': self.unknown_0x2abd7e71,
        }


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_barrel_cannon_effect_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_wall_bounce_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_land_carry_over_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_damage_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xe06d7b15(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x4364525d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x2abd7e71(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x381882d7: ('part', _decode_part),
    0xbd8e1d39: ('barrel_cannon_effect_locator', _decode_barrel_cannon_effect_locator),
    0x48b5def1: ('wall_bounce_constant', _decode_wall_bounce_constant),
    0x4c97be6e: ('max_land_carry_over_speed', _decode_max_land_carry_over_speed),
    0x6b4ed718: ('attack_damage_sound', _decode_attack_damage_sound),
    0x9583ee9a: ('attack_bounce_data', PlayerAttackBounceData.from_stream),
    0xe06d7b15: ('unknown_0xe06d7b15', _decode_unknown_0xe06d7b15),
    0x4364525d: ('unknown_0x4364525d', _decode_unknown_0x4364525d),
    0x2abd7e71: ('unknown_0x2abd7e71', _decode_unknown_0x2abd7e71),
}

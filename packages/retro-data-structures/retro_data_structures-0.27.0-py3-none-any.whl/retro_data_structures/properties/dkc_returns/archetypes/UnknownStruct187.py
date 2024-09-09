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
from retro_data_structures.properties.dkc_returns.archetypes.DamageEffectData import DamageEffectData
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct187Json(typing_extensions.TypedDict):
        unknown: int
        impact_stun_radius: float
        impact_stun_velocity: float
        impact_stun_duration: float
        shock_wave_ring_effect: int
        damage_effect_data: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct187(BaseProperty):
    unknown: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8a58a7f8, original_name='Unknown'
        ),
    })
    impact_stun_radius: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd43aac22, original_name='ImpactStunRadius'
        ),
    })
    impact_stun_velocity: float = dataclasses.field(default=8.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x59ccac1b, original_name='ImpactStunVelocity'
        ),
    })
    impact_stun_duration: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd06d58a7, original_name='ImpactStunDuration'
        ),
    })
    shock_wave_ring_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd3c1390e, original_name='ShockWaveRingEffect'
        ),
    })
    damage_effect_data: DamageEffectData = dataclasses.field(default_factory=DamageEffectData, metadata={
        'reflection': FieldReflection[DamageEffectData](
            DamageEffectData, id=0xae342f0f, original_name='DamageEffectData', from_json=DamageEffectData.from_json, to_json=DamageEffectData.to_json
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
        assert property_id == 0x8a58a7f8
        unknown = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd43aac22
        impact_stun_radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59ccac1b
        impact_stun_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd06d58a7
        impact_stun_duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd3c1390e
        shock_wave_ring_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xae342f0f
        damage_effect_data = DamageEffectData.from_stream(data, property_size)
    
        return cls(unknown, impact_stun_radius, impact_stun_velocity, impact_stun_duration, shock_wave_ring_effect, damage_effect_data)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xd4:\xac"')  # 0xd43aac22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impact_stun_radius))

        data.write(b'Y\xcc\xac\x1b')  # 0x59ccac1b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impact_stun_velocity))

        data.write(b'\xd0mX\xa7')  # 0xd06d58a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impact_stun_duration))

        data.write(b'\xd3\xc19\x0e')  # 0xd3c1390e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shock_wave_ring_effect))

        data.write(b'\xae4/\x0f')  # 0xae342f0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct187Json", data)
        return cls(
            unknown=json_data['unknown'],
            impact_stun_radius=json_data['impact_stun_radius'],
            impact_stun_velocity=json_data['impact_stun_velocity'],
            impact_stun_duration=json_data['impact_stun_duration'],
            shock_wave_ring_effect=json_data['shock_wave_ring_effect'],
            damage_effect_data=DamageEffectData.from_json(json_data['damage_effect_data']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'impact_stun_radius': self.impact_stun_radius,
            'impact_stun_velocity': self.impact_stun_velocity,
            'impact_stun_duration': self.impact_stun_duration,
            'shock_wave_ring_effect': self.shock_wave_ring_effect,
            'damage_effect_data': self.damage_effect_data.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_impact_stun_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impact_stun_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impact_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shock_wave_ring_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown', _decode_unknown),
    0xd43aac22: ('impact_stun_radius', _decode_impact_stun_radius),
    0x59ccac1b: ('impact_stun_velocity', _decode_impact_stun_velocity),
    0xd06d58a7: ('impact_stun_duration', _decode_impact_stun_duration),
    0xd3c1390e: ('shock_wave_ring_effect', _decode_shock_wave_ring_effect),
    0xae342f0f: ('damage_effect_data', DamageEffectData.from_stream),
}

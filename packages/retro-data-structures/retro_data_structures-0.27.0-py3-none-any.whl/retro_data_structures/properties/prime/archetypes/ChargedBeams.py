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
import retro_data_structures.enums.prime as enums

if typing.TYPE_CHECKING:
    class ChargedBeamsJson(typing_extensions.TypedDict):
        power: int
        ice: int
        wave: int
        plasma: int
        phazon: int
    

@dataclasses.dataclass()
class ChargedBeams(BaseProperty):
    power: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage, metadata={
        'reflection': FieldReflection[enums.VulnerabilityType](
            enums.VulnerabilityType, id=0x00000000, original_name='Power', from_json=enums.VulnerabilityType.from_json, to_json=enums.VulnerabilityType.to_json
        ),
    })
    ice: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage, metadata={
        'reflection': FieldReflection[enums.VulnerabilityType](
            enums.VulnerabilityType, id=0x00000001, original_name='Ice', from_json=enums.VulnerabilityType.from_json, to_json=enums.VulnerabilityType.to_json
        ),
    })
    wave: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage, metadata={
        'reflection': FieldReflection[enums.VulnerabilityType](
            enums.VulnerabilityType, id=0x00000002, original_name='Wave', from_json=enums.VulnerabilityType.from_json, to_json=enums.VulnerabilityType.to_json
        ),
    })
    plasma: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage, metadata={
        'reflection': FieldReflection[enums.VulnerabilityType](
            enums.VulnerabilityType, id=0x00000003, original_name='Plasma', from_json=enums.VulnerabilityType.from_json, to_json=enums.VulnerabilityType.to_json
        ),
    })
    phazon: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage, metadata={
        'reflection': FieldReflection[enums.VulnerabilityType](
            enums.VulnerabilityType, id=0x00000004, original_name='Phazon', from_json=enums.VulnerabilityType.from_json, to_json=enums.VulnerabilityType.to_json
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        property_size = None  # Atomic
        power = enums.VulnerabilityType.from_stream(data)
        ice = enums.VulnerabilityType.from_stream(data)
        wave = enums.VulnerabilityType.from_stream(data)
        plasma = enums.VulnerabilityType.from_stream(data)
        phazon = enums.VulnerabilityType.from_stream(data)
        return cls(power, ice, wave, plasma, phazon)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        self.power.to_stream(data)
        self.ice.to_stream(data)
        self.wave.to_stream(data)
        self.plasma.to_stream(data)
        self.phazon.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ChargedBeamsJson", data)
        return cls(
            power=enums.VulnerabilityType.from_json(json_data['power']),
            ice=enums.VulnerabilityType.from_json(json_data['ice']),
            wave=enums.VulnerabilityType.from_json(json_data['wave']),
            plasma=enums.VulnerabilityType.from_json(json_data['plasma']),
            phazon=enums.VulnerabilityType.from_json(json_data['phazon']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'power': self.power.to_json(),
            'ice': self.ice.to_json(),
            'wave': self.wave.to_json(),
            'plasma': self.plasma.to_json(),
            'phazon': self.phazon.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []

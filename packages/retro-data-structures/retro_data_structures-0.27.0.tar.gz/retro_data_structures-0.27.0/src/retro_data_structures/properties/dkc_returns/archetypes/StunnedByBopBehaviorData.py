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
    class StunnedByBopBehaviorDataJson(typing_extensions.TypedDict):
        stun_duration: float
        fall_to_ground_rule: int
        can_be_stunned_in_air: bool
        override_terrain_alignment: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x2d8db31d, 0x750eb3eb, 0xfe0086a4, 0xff8b7ba4)


@dataclasses.dataclass()
class StunnedByBopBehaviorData(BaseProperty):
    stun_duration: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d8db31d, original_name='StunDuration'
        ),
    })
    fall_to_ground_rule: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x750eb3eb, original_name='FallToGroundRule'
        ),
    })
    can_be_stunned_in_air: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xfe0086a4, original_name='CanBeStunnedInAir'
        ),
    })
    override_terrain_alignment: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xff8b7ba4, original_name='OverrideTerrainAlignment'
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
            _FAST_FORMAT = struct.Struct('>LHfLHQLH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(38))
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

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

        data.write(b'u\x0e\xb3\xeb')  # 0x750eb3eb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fall_to_ground_rule))

        data.write(b'\xfe\x00\x86\xa4')  # 0xfe0086a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_be_stunned_in_air))

        data.write(b'\xff\x8b{\xa4')  # 0xff8b7ba4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override_terrain_alignment))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("StunnedByBopBehaviorDataJson", data)
        return cls(
            stun_duration=json_data['stun_duration'],
            fall_to_ground_rule=json_data['fall_to_ground_rule'],
            can_be_stunned_in_air=json_data['can_be_stunned_in_air'],
            override_terrain_alignment=json_data['override_terrain_alignment'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'stun_duration': self.stun_duration,
            'fall_to_ground_rule': self.fall_to_ground_rule,
            'can_be_stunned_in_air': self.can_be_stunned_in_air,
            'override_terrain_alignment': self.override_terrain_alignment,
        }


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fall_to_ground_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_can_be_stunned_in_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_override_terrain_alignment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
    0x750eb3eb: ('fall_to_ground_rule', _decode_fall_to_ground_rule),
    0xfe0086a4: ('can_be_stunned_in_air', _decode_can_be_stunned_in_air),
    0xff8b7ba4: ('override_terrain_alignment', _decode_override_terrain_alignment),
}

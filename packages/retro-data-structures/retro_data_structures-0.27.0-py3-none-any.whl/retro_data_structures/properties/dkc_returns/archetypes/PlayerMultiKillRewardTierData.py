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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class PlayerMultiKillRewardTierDataJson(typing_extensions.TypedDict):
        item_to_give: int
        bop_threshold: int
        throw_kill_threshold: int
        barrel_cannon_kill_threshold: int
        reward_speed: float
        reward_target_scale: json_util.JsonValue
        reward_model: int
        reward_reveal_effect: int
        reward_effect: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xa02ef0c4, 0x7b7c262a, 0xdb289b55, 0xa77efc04, 0x2658958d, 0x384baf36, 0x87b52f4c, 0xab5b8caf, 0xb4a43449)


@dataclasses.dataclass()
class PlayerMultiKillRewardTierData(BaseProperty):
    item_to_give: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana, metadata={
        'reflection': FieldReflection[enums.PlayerItem](
            enums.PlayerItem, id=0xa02ef0c4, original_name='ItemToGive', from_json=enums.PlayerItem.from_json, to_json=enums.PlayerItem.to_json
        ),
    })
    bop_threshold: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x7b7c262a, original_name='BopThreshold'
        ),
    })
    throw_kill_threshold: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xdb289b55, original_name='ThrowKillThreshold'
        ),
    })
    barrel_cannon_kill_threshold: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xa77efc04, original_name='BarrelCannonKillThreshold'
        ),
    })
    reward_speed: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2658958d, original_name='RewardSpeed'
        ),
    })
    reward_target_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x384baf36, original_name='RewardTargetScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    reward_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x87b52f4c, original_name='RewardModel'
        ),
    })
    reward_reveal_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xab5b8caf, original_name='RewardRevealEffect'
        ),
    })
    reward_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb4a43449, original_name='RewardEffect'
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
            _FAST_FORMAT = struct.Struct('>LHLLHlLHlLHlLHfLHfffLHQLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(110))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[20], dec[23], dec[26]) == _FAST_IDS
        return cls(
            enums.PlayerItem(dec[2]),
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            Vector(*dec[17:20]),
            dec[22],
            dec[25],
            dec[28],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xa0.\xf0\xc4')  # 0xa02ef0c4
        data.write(b'\x00\x04')  # size
        self.item_to_give.to_stream(data)

        data.write(b'{|&*')  # 0x7b7c262a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.bop_threshold))

        data.write(b'\xdb(\x9bU')  # 0xdb289b55
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.throw_kill_threshold))

        data.write(b'\xa7~\xfc\x04')  # 0xa77efc04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.barrel_cannon_kill_threshold))

        data.write(b'&X\x95\x8d')  # 0x2658958d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reward_speed))

        data.write(b'8K\xaf6')  # 0x384baf36
        data.write(b'\x00\x0c')  # size
        self.reward_target_scale.to_stream(data)

        data.write(b'\x87\xb5/L')  # 0x87b52f4c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reward_model))

        data.write(b'\xab[\x8c\xaf')  # 0xab5b8caf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reward_reveal_effect))

        data.write(b'\xb4\xa44I')  # 0xb4a43449
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reward_effect))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerMultiKillRewardTierDataJson", data)
        return cls(
            item_to_give=enums.PlayerItem.from_json(json_data['item_to_give']),
            bop_threshold=json_data['bop_threshold'],
            throw_kill_threshold=json_data['throw_kill_threshold'],
            barrel_cannon_kill_threshold=json_data['barrel_cannon_kill_threshold'],
            reward_speed=json_data['reward_speed'],
            reward_target_scale=Vector.from_json(json_data['reward_target_scale']),
            reward_model=json_data['reward_model'],
            reward_reveal_effect=json_data['reward_reveal_effect'],
            reward_effect=json_data['reward_effect'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'item_to_give': self.item_to_give.to_json(),
            'bop_threshold': self.bop_threshold,
            'throw_kill_threshold': self.throw_kill_threshold,
            'barrel_cannon_kill_threshold': self.barrel_cannon_kill_threshold,
            'reward_speed': self.reward_speed,
            'reward_target_scale': self.reward_target_scale.to_json(),
            'reward_model': self.reward_model,
            'reward_reveal_effect': self.reward_reveal_effect,
            'reward_effect': self.reward_effect,
        }


def _decode_item_to_give(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_bop_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_throw_kill_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_barrel_cannon_kill_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_reward_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reward_target_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_reward_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reward_reveal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reward_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa02ef0c4: ('item_to_give', _decode_item_to_give),
    0x7b7c262a: ('bop_threshold', _decode_bop_threshold),
    0xdb289b55: ('throw_kill_threshold', _decode_throw_kill_threshold),
    0xa77efc04: ('barrel_cannon_kill_threshold', _decode_barrel_cannon_kill_threshold),
    0x2658958d: ('reward_speed', _decode_reward_speed),
    0x384baf36: ('reward_target_scale', _decode_reward_target_scale),
    0x87b52f4c: ('reward_model', _decode_reward_model),
    0xab5b8caf: ('reward_reveal_effect', _decode_reward_reveal_effect),
    0xb4a43449: ('reward_effect', _decode_reward_effect),
}

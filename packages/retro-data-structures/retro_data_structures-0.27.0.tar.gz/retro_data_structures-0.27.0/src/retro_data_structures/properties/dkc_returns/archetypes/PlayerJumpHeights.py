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

if typing.TYPE_CHECKING:
    class PlayerJumpHeightsJson(typing_extensions.TypedDict):
        minimum_jump_height: float
        maximum_jump_height: float
        attack_bounce_data: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerJumpHeights(BaseProperty):
    minimum_jump_height: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x797aa551, original_name='MinimumJumpHeight'
        ),
    })
    maximum_jump_height: float = dataclasses.field(default=4.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x386d9ad7, original_name='MaximumJumpHeight'
        ),
    })
    attack_bounce_data: PlayerAttackBounceData = dataclasses.field(default_factory=PlayerAttackBounceData, metadata={
        'reflection': FieldReflection[PlayerAttackBounceData](
            PlayerAttackBounceData, id=0x9583ee9a, original_name='AttackBounceData', from_json=PlayerAttackBounceData.from_json, to_json=PlayerAttackBounceData.to_json
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
        if property_count != 3:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x797aa551
        minimum_jump_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x386d9ad7
        maximum_jump_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9583ee9a
        attack_bounce_data = PlayerAttackBounceData.from_stream(data, property_size)
    
        return cls(minimum_jump_height, maximum_jump_height, attack_bounce_data)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'yz\xa5Q')  # 0x797aa551
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_jump_height))

        data.write(b'8m\x9a\xd7')  # 0x386d9ad7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_jump_height))

        data.write(b'\x95\x83\xee\x9a')  # 0x9583ee9a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_bounce_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerJumpHeightsJson", data)
        return cls(
            minimum_jump_height=json_data['minimum_jump_height'],
            maximum_jump_height=json_data['maximum_jump_height'],
            attack_bounce_data=PlayerAttackBounceData.from_json(json_data['attack_bounce_data']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'minimum_jump_height': self.minimum_jump_height,
            'maximum_jump_height': self.maximum_jump_height,
            'attack_bounce_data': self.attack_bounce_data.to_json(),
        }


def _decode_minimum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x797aa551: ('minimum_jump_height', _decode_minimum_jump_height),
    0x386d9ad7: ('maximum_jump_height', _decode_maximum_jump_height),
    0x9583ee9a: ('attack_bounce_data', PlayerAttackBounceData.from_stream),
}

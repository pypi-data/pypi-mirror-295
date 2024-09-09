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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardSoundData import PlayerMultiKillRewardSoundData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardTierData import PlayerMultiKillRewardTierData
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class PlayerMultiKillRewardDataJson(typing_extensions.TypedDict):
        reveal_height_spline: json_util.JsonObject
        tier1: json_util.JsonObject
        tier2: json_util.JsonObject
        sound: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerMultiKillRewardData(BaseProperty):
    reveal_height_spline: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x32152ab2, original_name='RevealHeightSpline', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    tier1: PlayerMultiKillRewardTierData = dataclasses.field(default_factory=PlayerMultiKillRewardTierData, metadata={
        'reflection': FieldReflection[PlayerMultiKillRewardTierData](
            PlayerMultiKillRewardTierData, id=0x005e3be9, original_name='Tier1', from_json=PlayerMultiKillRewardTierData.from_json, to_json=PlayerMultiKillRewardTierData.to_json
        ),
    })
    tier2: PlayerMultiKillRewardTierData = dataclasses.field(default_factory=PlayerMultiKillRewardTierData, metadata={
        'reflection': FieldReflection[PlayerMultiKillRewardTierData](
            PlayerMultiKillRewardTierData, id=0x44ff1ef1, original_name='Tier2', from_json=PlayerMultiKillRewardTierData.from_json, to_json=PlayerMultiKillRewardTierData.to_json
        ),
    })
    sound: PlayerMultiKillRewardSoundData = dataclasses.field(default_factory=PlayerMultiKillRewardSoundData, metadata={
        'reflection': FieldReflection[PlayerMultiKillRewardSoundData](
            PlayerMultiKillRewardSoundData, id=0x7384aea3, original_name='Sound', from_json=PlayerMultiKillRewardSoundData.from_json, to_json=PlayerMultiKillRewardSoundData.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x32152ab2
        reveal_height_spline = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x005e3be9
        tier1 = PlayerMultiKillRewardTierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x44ff1ef1
        tier2 = PlayerMultiKillRewardTierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7384aea3
        sound = PlayerMultiKillRewardSoundData.from_stream(data, property_size)
    
        return cls(reveal_height_spline, tier1, tier2, sound)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'2\x15*\xb2')  # 0x32152ab2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.reveal_height_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00^;\xe9')  # 0x5e3be9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tier1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D\xff\x1e\xf1')  # 0x44ff1ef1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tier2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\x84\xae\xa3')  # 0x7384aea3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerMultiKillRewardDataJson", data)
        return cls(
            reveal_height_spline=Spline.from_json(json_data['reveal_height_spline']),
            tier1=PlayerMultiKillRewardTierData.from_json(json_data['tier1']),
            tier2=PlayerMultiKillRewardTierData.from_json(json_data['tier2']),
            sound=PlayerMultiKillRewardSoundData.from_json(json_data['sound']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'reveal_height_spline': self.reveal_height_spline.to_json(),
            'tier1': self.tier1.to_json(),
            'tier2': self.tier2.to_json(),
            'sound': self.sound.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x32152ab2: ('reveal_height_spline', Spline.from_stream),
    0x5e3be9: ('tier1', PlayerMultiKillRewardTierData.from_stream),
    0x44ff1ef1: ('tier2', PlayerMultiKillRewardTierData.from_stream),
    0x7384aea3: ('sound', PlayerMultiKillRewardSoundData.from_stream),
}

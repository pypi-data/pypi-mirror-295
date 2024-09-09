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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountRiderData import PlayerMountRiderData

if typing.TYPE_CHECKING:
    class PlayerMountRiderListJson(typing_extensions.TypedDict):
        max_riders: int
        rider1: json_util.JsonObject
        rider2: json_util.JsonObject
        rider3: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerMountRiderList(BaseProperty):
    max_riders: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xfb6a981b, original_name='MaxRiders'
        ),
    })
    rider1: PlayerMountRiderData = dataclasses.field(default_factory=PlayerMountRiderData, metadata={
        'reflection': FieldReflection[PlayerMountRiderData](
            PlayerMountRiderData, id=0x3982dec6, original_name='Rider1', from_json=PlayerMountRiderData.from_json, to_json=PlayerMountRiderData.to_json
        ),
    })
    rider2: PlayerMountRiderData = dataclasses.field(default_factory=PlayerMountRiderData, metadata={
        'reflection': FieldReflection[PlayerMountRiderData](
            PlayerMountRiderData, id=0x429c5c25, original_name='Rider2', from_json=PlayerMountRiderData.from_json, to_json=PlayerMountRiderData.to_json
        ),
    })
    rider3: PlayerMountRiderData = dataclasses.field(default_factory=PlayerMountRiderData, metadata={
        'reflection': FieldReflection[PlayerMountRiderData](
            PlayerMountRiderData, id=0xdd46dfbb, original_name='Rider3', from_json=PlayerMountRiderData.from_json, to_json=PlayerMountRiderData.to_json
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
        assert property_id == 0xfb6a981b
        max_riders = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3982dec6
        rider1 = PlayerMountRiderData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x429c5c25
        rider2 = PlayerMountRiderData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdd46dfbb
        rider3 = PlayerMountRiderData.from_stream(data, property_size)
    
        return cls(max_riders, rider1, rider2, rider3)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xfbj\x98\x1b')  # 0xfb6a981b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_riders))

        data.write(b'9\x82\xde\xc6')  # 0x3982dec6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x9c\\%')  # 0x429c5c25
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xddF\xdf\xbb')  # 0xdd46dfbb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerMountRiderListJson", data)
        return cls(
            max_riders=json_data['max_riders'],
            rider1=PlayerMountRiderData.from_json(json_data['rider1']),
            rider2=PlayerMountRiderData.from_json(json_data['rider2']),
            rider3=PlayerMountRiderData.from_json(json_data['rider3']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'max_riders': self.max_riders,
            'rider1': self.rider1.to_json(),
            'rider2': self.rider2.to_json(),
            'rider3': self.rider3.to_json(),
        }


def _decode_max_riders(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfb6a981b: ('max_riders', _decode_max_riders),
    0x3982dec6: ('rider1', PlayerMountRiderData.from_stream),
    0x429c5c25: ('rider2', PlayerMountRiderData.from_stream),
    0xdd46dfbb: ('rider3', PlayerMountRiderData.from_stream),
}

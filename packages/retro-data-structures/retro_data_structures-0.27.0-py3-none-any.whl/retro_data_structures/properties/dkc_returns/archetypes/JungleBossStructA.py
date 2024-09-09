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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct192 import UnknownStruct192
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct56 import UnknownStruct56
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class JungleBossStructAJson(typing_extensions.TypedDict):
        texture: int
        health: float
        unknown_struct56_0x02eb59dc: json_util.JsonObject
        unknown_struct56_0xf0bcb424: json_util.JsonObject
        unknown_struct56_0x17a112b3: json_util.JsonObject
        unknown_struct56_0xcf626995: json_util.JsonObject
        unknown_struct56_0x287fcf02: json_util.JsonObject
        unknown_struct192: json_util.JsonObject
    

@dataclasses.dataclass()
class JungleBossStructA(BaseProperty):
    texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd1f65872, original_name='Texture'
        ),
    })
    health: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf0668919, original_name='Health'
        ),
    })
    unknown_struct56_0x02eb59dc: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56, metadata={
        'reflection': FieldReflection[UnknownStruct56](
            UnknownStruct56, id=0x02eb59dc, original_name='UnknownStruct56', from_json=UnknownStruct56.from_json, to_json=UnknownStruct56.to_json
        ),
    })
    unknown_struct56_0xf0bcb424: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56, metadata={
        'reflection': FieldReflection[UnknownStruct56](
            UnknownStruct56, id=0xf0bcb424, original_name='UnknownStruct56', from_json=UnknownStruct56.from_json, to_json=UnknownStruct56.to_json
        ),
    })
    unknown_struct56_0x17a112b3: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56, metadata={
        'reflection': FieldReflection[UnknownStruct56](
            UnknownStruct56, id=0x17a112b3, original_name='UnknownStruct56', from_json=UnknownStruct56.from_json, to_json=UnknownStruct56.to_json
        ),
    })
    unknown_struct56_0xcf626995: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56, metadata={
        'reflection': FieldReflection[UnknownStruct56](
            UnknownStruct56, id=0xcf626995, original_name='UnknownStruct56', from_json=UnknownStruct56.from_json, to_json=UnknownStruct56.to_json
        ),
    })
    unknown_struct56_0x287fcf02: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56, metadata={
        'reflection': FieldReflection[UnknownStruct56](
            UnknownStruct56, id=0x287fcf02, original_name='UnknownStruct56', from_json=UnknownStruct56.from_json, to_json=UnknownStruct56.to_json
        ),
    })
    unknown_struct192: UnknownStruct192 = dataclasses.field(default_factory=UnknownStruct192, metadata={
        'reflection': FieldReflection[UnknownStruct192](
            UnknownStruct192, id=0x72544afd, original_name='UnknownStruct192', from_json=UnknownStruct192.from_json, to_json=UnknownStruct192.to_json
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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1f65872
        texture = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0668919
        health = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x02eb59dc
        unknown_struct56_0x02eb59dc = UnknownStruct56.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0bcb424
        unknown_struct56_0xf0bcb424 = UnknownStruct56.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x17a112b3
        unknown_struct56_0x17a112b3 = UnknownStruct56.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcf626995
        unknown_struct56_0xcf626995 = UnknownStruct56.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x287fcf02
        unknown_struct56_0x287fcf02 = UnknownStruct56.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x72544afd
        unknown_struct192 = UnknownStruct192.from_stream(data, property_size)
    
        return cls(texture, health, unknown_struct56_0x02eb59dc, unknown_struct56_0xf0bcb424, unknown_struct56_0x17a112b3, unknown_struct56_0xcf626995, unknown_struct56_0x287fcf02, unknown_struct192)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xd1\xf6Xr')  # 0xd1f65872
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.texture))

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'\x02\xebY\xdc')  # 0x2eb59dc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0x02eb59dc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0\xbc\xb4$')  # 0xf0bcb424
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0xf0bcb424.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xa1\x12\xb3')  # 0x17a112b3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0x17a112b3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcfbi\x95')  # 0xcf626995
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0xcf626995.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x7f\xcf\x02')  # 0x287fcf02
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0x287fcf02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'rTJ\xfd')  # 0x72544afd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct192.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("JungleBossStructAJson", data)
        return cls(
            texture=json_data['texture'],
            health=json_data['health'],
            unknown_struct56_0x02eb59dc=UnknownStruct56.from_json(json_data['unknown_struct56_0x02eb59dc']),
            unknown_struct56_0xf0bcb424=UnknownStruct56.from_json(json_data['unknown_struct56_0xf0bcb424']),
            unknown_struct56_0x17a112b3=UnknownStruct56.from_json(json_data['unknown_struct56_0x17a112b3']),
            unknown_struct56_0xcf626995=UnknownStruct56.from_json(json_data['unknown_struct56_0xcf626995']),
            unknown_struct56_0x287fcf02=UnknownStruct56.from_json(json_data['unknown_struct56_0x287fcf02']),
            unknown_struct192=UnknownStruct192.from_json(json_data['unknown_struct192']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'texture': self.texture,
            'health': self.health,
            'unknown_struct56_0x02eb59dc': self.unknown_struct56_0x02eb59dc.to_json(),
            'unknown_struct56_0xf0bcb424': self.unknown_struct56_0xf0bcb424.to_json(),
            'unknown_struct56_0x17a112b3': self.unknown_struct56_0x17a112b3.to_json(),
            'unknown_struct56_0xcf626995': self.unknown_struct56_0xcf626995.to_json(),
            'unknown_struct56_0x287fcf02': self.unknown_struct56_0x287fcf02.to_json(),
            'unknown_struct192': self.unknown_struct192.to_json(),
        }


def _decode_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd1f65872: ('texture', _decode_texture),
    0xf0668919: ('health', _decode_health),
    0x2eb59dc: ('unknown_struct56_0x02eb59dc', UnknownStruct56.from_stream),
    0xf0bcb424: ('unknown_struct56_0xf0bcb424', UnknownStruct56.from_stream),
    0x17a112b3: ('unknown_struct56_0x17a112b3', UnknownStruct56.from_stream),
    0xcf626995: ('unknown_struct56_0xcf626995', UnknownStruct56.from_stream),
    0x287fcf02: ('unknown_struct56_0x287fcf02', UnknownStruct56.from_stream),
    0x72544afd: ('unknown_struct192', UnknownStruct192.from_stream),
}

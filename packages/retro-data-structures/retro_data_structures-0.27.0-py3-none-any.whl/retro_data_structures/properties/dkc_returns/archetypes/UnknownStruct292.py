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
    class UnknownStruct292Json(typing_extensions.TypedDict):
        gem_model: int
        unknown_0xa826bd98: str
        unknown_0x46cc2fd0: float
        unknown_0x82b6dc81: float
        ground_pound_relapse_multiplier: float
        ground_pound_window: float
        part: int
        unknown_0xebf3b81d: int
    

@dataclasses.dataclass()
class UnknownStruct292(BaseProperty):
    gem_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc5ce83af, original_name='GemModel'
        ),
    })
    unknown_0xa826bd98: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xa826bd98, original_name='Unknown'
        ),
    })
    unknown_0x46cc2fd0: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x46cc2fd0, original_name='Unknown'
        ),
    })
    unknown_0x82b6dc81: float = dataclasses.field(default=0.699999988079071, metadata={
        'reflection': FieldReflection[float](
            float, id=0x82b6dc81, original_name='Unknown'
        ),
    })
    ground_pound_relapse_multiplier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x686e030b, original_name='GroundPoundRelapseMultiplier'
        ),
    })
    ground_pound_window: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x68d787b4, original_name='GroundPoundWindow'
        ),
    })
    part: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x68137ea7, original_name='PART'
        ),
    })
    unknown_0xebf3b81d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xebf3b81d, original_name='Unknown'
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
        assert property_id == 0xc5ce83af
        gem_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa826bd98
        unknown_0xa826bd98 = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46cc2fd0
        unknown_0x46cc2fd0 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82b6dc81
        unknown_0x82b6dc81 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x686e030b
        ground_pound_relapse_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68d787b4
        ground_pound_window = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68137ea7
        part = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xebf3b81d
        unknown_0xebf3b81d = struct.unpack(">Q", data.read(8))[0]
    
        return cls(gem_model, unknown_0xa826bd98, unknown_0x46cc2fd0, unknown_0x82b6dc81, ground_pound_relapse_multiplier, ground_pound_window, part, unknown_0xebf3b81d)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xc5\xce\x83\xaf')  # 0xc5ce83af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gem_model))

        data.write(b'\xa8&\xbd\x98')  # 0xa826bd98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xa826bd98.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\xcc/\xd0')  # 0x46cc2fd0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x46cc2fd0))

        data.write(b'\x82\xb6\xdc\x81')  # 0x82b6dc81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x82b6dc81))

        data.write(b'hn\x03\x0b')  # 0x686e030b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_relapse_multiplier))

        data.write(b'h\xd7\x87\xb4')  # 0x68d787b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_window))

        data.write(b'h\x13~\xa7')  # 0x68137ea7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'\xeb\xf3\xb8\x1d')  # 0xebf3b81d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xebf3b81d))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct292Json", data)
        return cls(
            gem_model=json_data['gem_model'],
            unknown_0xa826bd98=json_data['unknown_0xa826bd98'],
            unknown_0x46cc2fd0=json_data['unknown_0x46cc2fd0'],
            unknown_0x82b6dc81=json_data['unknown_0x82b6dc81'],
            ground_pound_relapse_multiplier=json_data['ground_pound_relapse_multiplier'],
            ground_pound_window=json_data['ground_pound_window'],
            part=json_data['part'],
            unknown_0xebf3b81d=json_data['unknown_0xebf3b81d'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gem_model': self.gem_model,
            'unknown_0xa826bd98': self.unknown_0xa826bd98,
            'unknown_0x46cc2fd0': self.unknown_0x46cc2fd0,
            'unknown_0x82b6dc81': self.unknown_0x82b6dc81,
            'ground_pound_relapse_multiplier': self.ground_pound_relapse_multiplier,
            'ground_pound_window': self.ground_pound_window,
            'part': self.part,
            'unknown_0xebf3b81d': self.unknown_0xebf3b81d,
        }


def _decode_gem_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xa826bd98(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown_0x46cc2fd0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x82b6dc81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_relapse_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xebf3b81d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc5ce83af: ('gem_model', _decode_gem_model),
    0xa826bd98: ('unknown_0xa826bd98', _decode_unknown_0xa826bd98),
    0x46cc2fd0: ('unknown_0x46cc2fd0', _decode_unknown_0x46cc2fd0),
    0x82b6dc81: ('unknown_0x82b6dc81', _decode_unknown_0x82b6dc81),
    0x686e030b: ('ground_pound_relapse_multiplier', _decode_ground_pound_relapse_multiplier),
    0x68d787b4: ('ground_pound_window', _decode_ground_pound_window),
    0x68137ea7: ('part', _decode_part),
    0xebf3b81d: ('unknown_0xebf3b81d', _decode_unknown_0xebf3b81d),
}

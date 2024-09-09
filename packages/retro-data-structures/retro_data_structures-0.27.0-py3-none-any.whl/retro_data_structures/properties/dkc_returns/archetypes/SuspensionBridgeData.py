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
from retro_data_structures.properties.dkc_returns.archetypes.SuspensionBridgeStruct import SuspensionBridgeStruct
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct269 import UnknownStruct269

if typing.TYPE_CHECKING:
    class SuspensionBridgeDataJson(typing_extensions.TypedDict):
        unknown_0x0e4c8a24: bool
        unknown_0x7b5d0e29: float
        unknown_0x06df8bd9: float
        unknown_0xda13807d: float
        unknown_struct269: json_util.JsonObject
        suspension_bridge_struct_0xf6555670: json_util.JsonObject
        suspension_bridge_struct_0x7cb2693b: json_util.JsonObject
    

@dataclasses.dataclass()
class SuspensionBridgeData(BaseProperty):
    unknown_0x0e4c8a24: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0e4c8a24, original_name='Unknown'
        ),
    })
    unknown_0x7b5d0e29: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7b5d0e29, original_name='Unknown'
        ),
    })
    unknown_0x06df8bd9: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x06df8bd9, original_name='Unknown'
        ),
    })
    unknown_0xda13807d: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xda13807d, original_name='Unknown'
        ),
    })
    unknown_struct269: UnknownStruct269 = dataclasses.field(default_factory=UnknownStruct269, metadata={
        'reflection': FieldReflection[UnknownStruct269](
            UnknownStruct269, id=0x681f4c76, original_name='UnknownStruct269', from_json=UnknownStruct269.from_json, to_json=UnknownStruct269.to_json
        ),
    })
    suspension_bridge_struct_0xf6555670: SuspensionBridgeStruct = dataclasses.field(default_factory=SuspensionBridgeStruct, metadata={
        'reflection': FieldReflection[SuspensionBridgeStruct](
            SuspensionBridgeStruct, id=0xf6555670, original_name='SuspensionBridgeStruct', from_json=SuspensionBridgeStruct.from_json, to_json=SuspensionBridgeStruct.to_json
        ),
    })
    suspension_bridge_struct_0x7cb2693b: SuspensionBridgeStruct = dataclasses.field(default_factory=SuspensionBridgeStruct, metadata={
        'reflection': FieldReflection[SuspensionBridgeStruct](
            SuspensionBridgeStruct, id=0x7cb2693b, original_name='SuspensionBridgeStruct', from_json=SuspensionBridgeStruct.from_json, to_json=SuspensionBridgeStruct.to_json
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
        if property_count != 7:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0e4c8a24
        unknown_0x0e4c8a24 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b5d0e29
        unknown_0x7b5d0e29 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x06df8bd9
        unknown_0x06df8bd9 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xda13807d
        unknown_0xda13807d = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x681f4c76
        unknown_struct269 = UnknownStruct269.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf6555670
        suspension_bridge_struct_0xf6555670 = SuspensionBridgeStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7cb2693b
        suspension_bridge_struct_0x7cb2693b = SuspensionBridgeStruct.from_stream(data, property_size)
    
        return cls(unknown_0x0e4c8a24, unknown_0x7b5d0e29, unknown_0x06df8bd9, unknown_0xda13807d, unknown_struct269, suspension_bridge_struct_0xf6555670, suspension_bridge_struct_0x7cb2693b)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x0eL\x8a$')  # 0xe4c8a24
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0e4c8a24))

        data.write(b'{]\x0e)')  # 0x7b5d0e29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7b5d0e29))

        data.write(b'\x06\xdf\x8b\xd9')  # 0x6df8bd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x06df8bd9))

        data.write(b'\xda\x13\x80}')  # 0xda13807d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xda13807d))

        data.write(b'h\x1fLv')  # 0x681f4c76
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct269.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6UVp')  # 0xf6555670
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.suspension_bridge_struct_0xf6555670.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xb2i;')  # 0x7cb2693b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.suspension_bridge_struct_0x7cb2693b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SuspensionBridgeDataJson", data)
        return cls(
            unknown_0x0e4c8a24=json_data['unknown_0x0e4c8a24'],
            unknown_0x7b5d0e29=json_data['unknown_0x7b5d0e29'],
            unknown_0x06df8bd9=json_data['unknown_0x06df8bd9'],
            unknown_0xda13807d=json_data['unknown_0xda13807d'],
            unknown_struct269=UnknownStruct269.from_json(json_data['unknown_struct269']),
            suspension_bridge_struct_0xf6555670=SuspensionBridgeStruct.from_json(json_data['suspension_bridge_struct_0xf6555670']),
            suspension_bridge_struct_0x7cb2693b=SuspensionBridgeStruct.from_json(json_data['suspension_bridge_struct_0x7cb2693b']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x0e4c8a24': self.unknown_0x0e4c8a24,
            'unknown_0x7b5d0e29': self.unknown_0x7b5d0e29,
            'unknown_0x06df8bd9': self.unknown_0x06df8bd9,
            'unknown_0xda13807d': self.unknown_0xda13807d,
            'unknown_struct269': self.unknown_struct269.to_json(),
            'suspension_bridge_struct_0xf6555670': self.suspension_bridge_struct_0xf6555670.to_json(),
            'suspension_bridge_struct_0x7cb2693b': self.suspension_bridge_struct_0x7cb2693b.to_json(),
        }


def _decode_unknown_0x0e4c8a24(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7b5d0e29(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x06df8bd9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xda13807d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe4c8a24: ('unknown_0x0e4c8a24', _decode_unknown_0x0e4c8a24),
    0x7b5d0e29: ('unknown_0x7b5d0e29', _decode_unknown_0x7b5d0e29),
    0x6df8bd9: ('unknown_0x06df8bd9', _decode_unknown_0x06df8bd9),
    0xda13807d: ('unknown_0xda13807d', _decode_unknown_0xda13807d),
    0x681f4c76: ('unknown_struct269', UnknownStruct269.from_stream),
    0xf6555670: ('suspension_bridge_struct_0xf6555670', SuspensionBridgeStruct.from_stream),
    0x7cb2693b: ('suspension_bridge_struct_0x7cb2693b', SuspensionBridgeStruct.from_stream),
}

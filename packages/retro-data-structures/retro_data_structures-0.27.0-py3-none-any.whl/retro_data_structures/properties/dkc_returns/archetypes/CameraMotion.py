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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct76 import UnknownStruct76
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct77 import UnknownStruct77

if typing.TYPE_CHECKING:
    class CameraMotionJson(typing_extensions.TypedDict):
        motion_type: int
        unknown_struct76: json_util.JsonObject
        unknown_struct77: json_util.JsonObject
    

@dataclasses.dataclass()
class CameraMotion(BaseProperty):
    motion_type: int = dataclasses.field(default=888911163, metadata={
        'reflection': FieldReflection[int](
            int, id=0x948af571, original_name='MotionType'
        ),
    })  # Choice
    unknown_struct76: UnknownStruct76 = dataclasses.field(default_factory=UnknownStruct76, metadata={
        'reflection': FieldReflection[UnknownStruct76](
            UnknownStruct76, id=0xb40a41b8, original_name='UnknownStruct76', from_json=UnknownStruct76.from_json, to_json=UnknownStruct76.to_json
        ),
    })
    unknown_struct77: UnknownStruct77 = dataclasses.field(default_factory=UnknownStruct77, metadata={
        'reflection': FieldReflection[UnknownStruct77](
            UnknownStruct77, id=0x0c38a009, original_name='UnknownStruct77', from_json=UnknownStruct77.from_json, to_json=UnknownStruct77.to_json
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
        assert property_id == 0x948af571
        motion_type = struct.unpack(">L", data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb40a41b8
        unknown_struct76 = UnknownStruct76.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0c38a009
        unknown_struct77 = UnknownStruct77.from_stream(data, property_size)
    
        return cls(motion_type, unknown_struct76, unknown_struct77)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x94\x8a\xf5q')  # 0x948af571
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.motion_type))

        data.write(b'\xb4\nA\xb8')  # 0xb40a41b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct76.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c8\xa0\t')  # 0xc38a009
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct77.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CameraMotionJson", data)
        return cls(
            motion_type=json_data['motion_type'],
            unknown_struct76=UnknownStruct76.from_json(json_data['unknown_struct76']),
            unknown_struct77=UnknownStruct77.from_json(json_data['unknown_struct77']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'motion_type': self.motion_type,
            'unknown_struct76': self.unknown_struct76.to_json(),
            'unknown_struct77': self.unknown_struct77.to_json(),
        }


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x948af571: ('motion_type', _decode_motion_type),
    0xb40a41b8: ('unknown_struct76', UnknownStruct76.from_stream),
    0xc38a009: ('unknown_struct77', UnknownStruct77.from_stream),
}

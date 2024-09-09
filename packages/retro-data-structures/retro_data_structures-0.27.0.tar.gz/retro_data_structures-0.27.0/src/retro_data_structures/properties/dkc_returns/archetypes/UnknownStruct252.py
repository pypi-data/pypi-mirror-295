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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct251 import UnknownStruct251

if typing.TYPE_CHECKING:
    class UnknownStruct252Json(typing_extensions.TypedDict):
        surface_height: float
        unknown: float
        unknown_struct251: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct252(BaseProperty):
    surface_height: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0a886af5, original_name='SurfaceHeight'
        ),
    })
    unknown: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe61e4448, original_name='Unknown'
        ),
    })
    unknown_struct251: UnknownStruct251 = dataclasses.field(default_factory=UnknownStruct251, metadata={
        'reflection': FieldReflection[UnknownStruct251](
            UnknownStruct251, id=0xfe6f6d0f, original_name='UnknownStruct251', from_json=UnknownStruct251.from_json, to_json=UnknownStruct251.to_json
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
        assert property_id == 0x0a886af5
        surface_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe61e4448
        unknown = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe6f6d0f
        unknown_struct251 = UnknownStruct251.from_stream(data, property_size)
    
        return cls(surface_height, unknown, unknown_struct251)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\n\x88j\xf5')  # 0xa886af5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.surface_height))

        data.write(b'\xe6\x1eDH')  # 0xe61e4448
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xfeom\x0f')  # 0xfe6f6d0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct251.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct252Json", data)
        return cls(
            surface_height=json_data['surface_height'],
            unknown=json_data['unknown'],
            unknown_struct251=UnknownStruct251.from_json(json_data['unknown_struct251']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'surface_height': self.surface_height,
            'unknown': self.unknown,
            'unknown_struct251': self.unknown_struct251.to_json(),
        }


def _decode_surface_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa886af5: ('surface_height', _decode_surface_height),
    0xe61e4448: ('unknown', _decode_unknown),
    0xfe6f6d0f: ('unknown_struct251', UnknownStruct251.from_stream),
}

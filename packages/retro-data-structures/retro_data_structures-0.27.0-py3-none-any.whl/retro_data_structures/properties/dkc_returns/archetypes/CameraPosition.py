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
from retro_data_structures.properties.dkc_returns.archetypes.OffsetPosition import OffsetPosition
from retro_data_structures.properties.dkc_returns.archetypes.PathPosition import PathPosition
from retro_data_structures.properties.dkc_returns.archetypes.SpindlePosition import SpindlePosition
from retro_data_structures.properties.dkc_returns.archetypes.SurfacePosition import SurfacePosition
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct73 import UnknownStruct73

if typing.TYPE_CHECKING:
    class CameraPositionJson(typing_extensions.TypedDict):
        position_type: int
        flags_camera_position: int
        path: json_util.JsonObject
        spindle: json_util.JsonObject
        surface: json_util.JsonObject
        offset: json_util.JsonObject
        unknown_struct73: json_util.JsonObject
    

@dataclasses.dataclass()
class CameraPosition(BaseProperty):
    position_type: enums.PositionType = dataclasses.field(default=enums.PositionType.Unknown2, metadata={
        'reflection': FieldReflection[enums.PositionType](
            enums.PositionType, id=0xb7cd4710, original_name='PositionType', from_json=enums.PositionType.from_json, to_json=enums.PositionType.to_json
        ),
    })
    flags_camera_position: int = dataclasses.field(default=2, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb1b6cf33, original_name='FlagsCameraPosition'
        ),
    })  # Flagset
    path: PathPosition = dataclasses.field(default_factory=PathPosition, metadata={
        'reflection': FieldReflection[PathPosition](
            PathPosition, id=0xe8ab9bc8, original_name='Path', from_json=PathPosition.from_json, to_json=PathPosition.to_json
        ),
    })
    spindle: SpindlePosition = dataclasses.field(default_factory=SpindlePosition, metadata={
        'reflection': FieldReflection[SpindlePosition](
            SpindlePosition, id=0x9ec1df0c, original_name='Spindle', from_json=SpindlePosition.from_json, to_json=SpindlePosition.to_json
        ),
    })
    surface: SurfacePosition = dataclasses.field(default_factory=SurfacePosition, metadata={
        'reflection': FieldReflection[SurfacePosition](
            SurfacePosition, id=0xbbb2d1e6, original_name='Surface', from_json=SurfacePosition.from_json, to_json=SurfacePosition.to_json
        ),
    })
    offset: OffsetPosition = dataclasses.field(default_factory=OffsetPosition, metadata={
        'reflection': FieldReflection[OffsetPosition](
            OffsetPosition, id=0x07d194af, original_name='Offset', from_json=OffsetPosition.from_json, to_json=OffsetPosition.to_json
        ),
    })
    unknown_struct73: UnknownStruct73 = dataclasses.field(default_factory=UnknownStruct73, metadata={
        'reflection': FieldReflection[UnknownStruct73](
            UnknownStruct73, id=0xebbf81d7, original_name='UnknownStruct73', from_json=UnknownStruct73.from_json, to_json=UnknownStruct73.to_json
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
        assert property_id == 0xb7cd4710
        position_type = enums.PositionType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb1b6cf33
        flags_camera_position = struct.unpack(">L", data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe8ab9bc8
        path = PathPosition.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ec1df0c
        spindle = SpindlePosition.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbb2d1e6
        surface = SurfacePosition.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x07d194af
        offset = OffsetPosition.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xebbf81d7
        unknown_struct73 = UnknownStruct73.from_stream(data, property_size)
    
        return cls(position_type, flags_camera_position, path, spindle, surface, offset, unknown_struct73)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xb7\xcdG\x10')  # 0xb7cd4710
        data.write(b'\x00\x04')  # size
        self.position_type.to_stream(data)

        data.write(b'\xb1\xb6\xcf3')  # 0xb1b6cf33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_camera_position))

        data.write(b'\xe8\xab\x9b\xc8')  # 0xe8ab9bc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xc1\xdf\x0c')  # 0x9ec1df0c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xb2\xd1\xe6')  # 0xbbb2d1e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surface.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07\xd1\x94\xaf')  # 0x7d194af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xbf\x81\xd7')  # 0xebbf81d7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct73.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CameraPositionJson", data)
        return cls(
            position_type=enums.PositionType.from_json(json_data['position_type']),
            flags_camera_position=json_data['flags_camera_position'],
            path=PathPosition.from_json(json_data['path']),
            spindle=SpindlePosition.from_json(json_data['spindle']),
            surface=SurfacePosition.from_json(json_data['surface']),
            offset=OffsetPosition.from_json(json_data['offset']),
            unknown_struct73=UnknownStruct73.from_json(json_data['unknown_struct73']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'position_type': self.position_type.to_json(),
            'flags_camera_position': self.flags_camera_position,
            'path': self.path.to_json(),
            'spindle': self.spindle.to_json(),
            'surface': self.surface.to_json(),
            'offset': self.offset.to_json(),
            'unknown_struct73': self.unknown_struct73.to_json(),
        }


def _decode_position_type(data: typing.BinaryIO, property_size: int):
    return enums.PositionType.from_stream(data)


def _decode_flags_camera_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb7cd4710: ('position_type', _decode_position_type),
    0xb1b6cf33: ('flags_camera_position', _decode_flags_camera_position),
    0xe8ab9bc8: ('path', PathPosition.from_stream),
    0x9ec1df0c: ('spindle', SpindlePosition.from_stream),
    0xbbb2d1e6: ('surface', SurfacePosition.from_stream),
    0x7d194af: ('offset', OffsetPosition.from_stream),
    0xebbf81d7: ('unknown_struct73', UnknownStruct73.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct15 import UnknownStruct15
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct68 import UnknownStruct68
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct71 import UnknownStruct71
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct72 import UnknownStruct72
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class UnknownStruct73Json(typing_extensions.TypedDict):
        camera_offset: json_util.JsonValue
        unknown_struct68: json_util.JsonObject
        adjust_vertical_based_on_pullback: bool
        unknown: bool
        unknown_struct71: json_util.JsonObject
        unknown_struct15: json_util.JsonObject
        unknown_struct72: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct73(BaseProperty):
    camera_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=26.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x6717088c, original_name='CameraOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_struct68: UnknownStruct68 = dataclasses.field(default_factory=UnknownStruct68, metadata={
        'reflection': FieldReflection[UnknownStruct68](
            UnknownStruct68, id=0xd52cd4fb, original_name='UnknownStruct68', from_json=UnknownStruct68.from_json, to_json=UnknownStruct68.to_json
        ),
    })
    adjust_vertical_based_on_pullback: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x947aa955, original_name='AdjustVerticalBasedOnPullback'
        ),
    })
    unknown: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8178a60f, original_name='Unknown'
        ),
    })
    unknown_struct71: UnknownStruct71 = dataclasses.field(default_factory=UnknownStruct71, metadata={
        'reflection': FieldReflection[UnknownStruct71](
            UnknownStruct71, id=0x2701771f, original_name='UnknownStruct71', from_json=UnknownStruct71.from_json, to_json=UnknownStruct71.to_json
        ),
    })
    unknown_struct15: UnknownStruct15 = dataclasses.field(default_factory=UnknownStruct15, metadata={
        'reflection': FieldReflection[UnknownStruct15](
            UnknownStruct15, id=0xc0c31785, original_name='UnknownStruct15', from_json=UnknownStruct15.from_json, to_json=UnknownStruct15.to_json
        ),
    })
    unknown_struct72: UnknownStruct72 = dataclasses.field(default_factory=UnknownStruct72, metadata={
        'reflection': FieldReflection[UnknownStruct72](
            UnknownStruct72, id=0x2d63b0f7, original_name='UnknownStruct72', from_json=UnknownStruct72.from_json, to_json=UnknownStruct72.to_json
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
        assert property_id == 0x6717088c
        camera_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd52cd4fb
        unknown_struct68 = UnknownStruct68.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x947aa955
        adjust_vertical_based_on_pullback = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8178a60f
        unknown = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2701771f
        unknown_struct71 = UnknownStruct71.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc0c31785
        unknown_struct15 = UnknownStruct15.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2d63b0f7
        unknown_struct72 = UnknownStruct72.from_stream(data, property_size)
    
        return cls(camera_offset, unknown_struct68, adjust_vertical_based_on_pullback, unknown, unknown_struct71, unknown_struct15, unknown_struct72)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'g\x17\x08\x8c')  # 0x6717088c
        data.write(b'\x00\x0c')  # size
        self.camera_offset.to_stream(data)

        data.write(b'\xd5,\xd4\xfb')  # 0xd52cd4fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct68.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x94z\xa9U')  # 0x947aa955
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_vertical_based_on_pullback))

        data.write(b'\x81x\xa6\x0f')  # 0x8178a60f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b"'\x01w\x1f")  # 0x2701771f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct71.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\xc3\x17\x85')  # 0xc0c31785
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-c\xb0\xf7')  # 0x2d63b0f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct72.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct73Json", data)
        return cls(
            camera_offset=Vector.from_json(json_data['camera_offset']),
            unknown_struct68=UnknownStruct68.from_json(json_data['unknown_struct68']),
            adjust_vertical_based_on_pullback=json_data['adjust_vertical_based_on_pullback'],
            unknown=json_data['unknown'],
            unknown_struct71=UnknownStruct71.from_json(json_data['unknown_struct71']),
            unknown_struct15=UnknownStruct15.from_json(json_data['unknown_struct15']),
            unknown_struct72=UnknownStruct72.from_json(json_data['unknown_struct72']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'camera_offset': self.camera_offset.to_json(),
            'unknown_struct68': self.unknown_struct68.to_json(),
            'adjust_vertical_based_on_pullback': self.adjust_vertical_based_on_pullback,
            'unknown': self.unknown,
            'unknown_struct71': self.unknown_struct71.to_json(),
            'unknown_struct15': self.unknown_struct15.to_json(),
            'unknown_struct72': self.unknown_struct72.to_json(),
        }


def _decode_camera_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_adjust_vertical_based_on_pullback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6717088c: ('camera_offset', _decode_camera_offset),
    0xd52cd4fb: ('unknown_struct68', UnknownStruct68.from_stream),
    0x947aa955: ('adjust_vertical_based_on_pullback', _decode_adjust_vertical_based_on_pullback),
    0x8178a60f: ('unknown', _decode_unknown),
    0x2701771f: ('unknown_struct71', UnknownStruct71.from_stream),
    0xc0c31785: ('unknown_struct15', UnknownStruct15.from_stream),
    0x2d63b0f7: ('unknown_struct72', UnknownStruct72.from_stream),
}

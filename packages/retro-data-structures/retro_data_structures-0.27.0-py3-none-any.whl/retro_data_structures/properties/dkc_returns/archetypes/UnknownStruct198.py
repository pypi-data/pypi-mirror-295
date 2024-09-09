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
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct198Json(typing_extensions.TypedDict):
        x_motion: json_util.JsonObject
        y_motion: json_util.JsonObject
        z_motion: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct198(BaseProperty):
    x_motion: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x97f6ea79, original_name='XMotion', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    y_motion: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x4a6033fc, original_name='YMotion', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    z_motion: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xf7aa5f32, original_name='ZMotion', from_json=Spline.from_json, to_json=Spline.to_json
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
        assert property_id == 0x97f6ea79
        x_motion = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4a6033fc
        y_motion = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf7aa5f32
        z_motion = Spline.from_stream(data, property_size)
    
        return cls(x_motion, y_motion, z_motion)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x97\xf6\xeay')  # 0x97f6ea79
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.x_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J`3\xfc')  # 0x4a6033fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.y_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\xaa_2')  # 0xf7aa5f32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct198Json", data)
        return cls(
            x_motion=Spline.from_json(json_data['x_motion']),
            y_motion=Spline.from_json(json_data['y_motion']),
            z_motion=Spline.from_json(json_data['z_motion']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'x_motion': self.x_motion.to_json(),
            'y_motion': self.y_motion.to_json(),
            'z_motion': self.z_motion.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97f6ea79: ('x_motion', Spline.from_stream),
    0x4a6033fc: ('y_motion', Spline.from_stream),
    0xf7aa5f32: ('z_motion', Spline.from_stream),
}

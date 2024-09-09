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
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct199Json(typing_extensions.TypedDict):
        spline_target_type: int
        unknown_0xef531185: float
        unknown_0x7a0d286c: float
        horizontal_motion: json_util.JsonObject
        vertical_motion: json_util.JsonObject
        only_target_active: bool
    

@dataclasses.dataclass()
class UnknownStruct199(BaseProperty):
    spline_target_type: enums.SplineTargetType = dataclasses.field(default=enums.SplineTargetType.Unknown2, metadata={
        'reflection': FieldReflection[enums.SplineTargetType](
            enums.SplineTargetType, id=0x68230b65, original_name='SplineTargetType', from_json=enums.SplineTargetType.from_json, to_json=enums.SplineTargetType.to_json
        ),
    })
    unknown_0xef531185: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xef531185, original_name='Unknown'
        ),
    })
    unknown_0x7a0d286c: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7a0d286c, original_name='Unknown'
        ),
    })
    horizontal_motion: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xf122cd97, original_name='HorizontalMotion', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    vertical_motion: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x2927e544, original_name='VerticalMotion', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    only_target_active: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0364f0b8, original_name='OnlyTargetActive'
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
        if property_count != 6:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68230b65
        spline_target_type = enums.SplineTargetType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xef531185
        unknown_0xef531185 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7a0d286c
        unknown_0x7a0d286c = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf122cd97
        horizontal_motion = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2927e544
        vertical_motion = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0364f0b8
        only_target_active = struct.unpack('>?', data.read(1))[0]
    
        return cls(spline_target_type, unknown_0xef531185, unknown_0x7a0d286c, horizontal_motion, vertical_motion, only_target_active)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'h#\x0be')  # 0x68230b65
        data.write(b'\x00\x04')  # size
        self.spline_target_type.to_stream(data)

        data.write(b'\xefS\x11\x85')  # 0xef531185
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xef531185))

        data.write(b'z\r(l')  # 0x7a0d286c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7a0d286c))

        data.write(b'\xf1"\xcd\x97')  # 0xf122cd97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.horizontal_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b")'\xe5D")  # 0x2927e544
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vertical_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03d\xf0\xb8')  # 0x364f0b8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.only_target_active))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct199Json", data)
        return cls(
            spline_target_type=enums.SplineTargetType.from_json(json_data['spline_target_type']),
            unknown_0xef531185=json_data['unknown_0xef531185'],
            unknown_0x7a0d286c=json_data['unknown_0x7a0d286c'],
            horizontal_motion=Spline.from_json(json_data['horizontal_motion']),
            vertical_motion=Spline.from_json(json_data['vertical_motion']),
            only_target_active=json_data['only_target_active'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'spline_target_type': self.spline_target_type.to_json(),
            'unknown_0xef531185': self.unknown_0xef531185,
            'unknown_0x7a0d286c': self.unknown_0x7a0d286c,
            'horizontal_motion': self.horizontal_motion.to_json(),
            'vertical_motion': self.vertical_motion.to_json(),
            'only_target_active': self.only_target_active,
        }


def _decode_spline_target_type(data: typing.BinaryIO, property_size: int):
    return enums.SplineTargetType.from_stream(data)


def _decode_unknown_0xef531185(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7a0d286c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_only_target_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x68230b65: ('spline_target_type', _decode_spline_target_type),
    0xef531185: ('unknown_0xef531185', _decode_unknown_0xef531185),
    0x7a0d286c: ('unknown_0x7a0d286c', _decode_unknown_0x7a0d286c),
    0xf122cd97: ('horizontal_motion', Spline.from_stream),
    0x2927e544: ('vertical_motion', Spline.from_stream),
    0x364f0b8: ('only_target_active', _decode_only_target_active),
}

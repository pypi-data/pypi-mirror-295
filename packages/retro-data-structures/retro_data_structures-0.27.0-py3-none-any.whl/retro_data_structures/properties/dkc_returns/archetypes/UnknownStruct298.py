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
    class UnknownStruct298Json(typing_extensions.TypedDict):
        scale_spline: json_util.JsonObject
        auto_start: bool
        duration: float
        unknown_0x396861d0: float
        max_distance: float
        unknown_0x73bef3cb: int
        unknown_0xb7074f38: float
        unknown_0x30a1847b: float
        unknown_0x633bdfff: float
        unknown_0xe49d14bc: float
    

@dataclasses.dataclass()
class UnknownStruct298(BaseProperty):
    scale_spline: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x672255f7, original_name='ScaleSpline', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    auto_start: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3217dff8, original_name='AutoStart'
        ),
    })
    duration: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8b51e23f, original_name='Duration'
        ),
    })
    unknown_0x396861d0: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x396861d0, original_name='Unknown'
        ),
    })
    max_distance: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x25b7c9b2, original_name='MaxDistance'
        ),
    })
    unknown_0x73bef3cb: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0x73bef3cb, original_name='Unknown'
        ),
    })
    unknown_0xb7074f38: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb7074f38, original_name='Unknown'
        ),
    })
    unknown_0x30a1847b: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x30a1847b, original_name='Unknown'
        ),
    })
    unknown_0x633bdfff: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x633bdfff, original_name='Unknown'
        ),
    })
    unknown_0xe49d14bc: float = dataclasses.field(default=9.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe49d14bc, original_name='Unknown'
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
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x672255f7
        scale_spline = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3217dff8
        auto_start = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8b51e23f
        duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x396861d0
        unknown_0x396861d0 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x25b7c9b2
        max_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73bef3cb
        unknown_0x73bef3cb = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb7074f38
        unknown_0xb7074f38 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x30a1847b
        unknown_0x30a1847b = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x633bdfff
        unknown_0x633bdfff = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe49d14bc
        unknown_0xe49d14bc = struct.unpack('>f', data.read(4))[0]
    
        return cls(scale_spline, auto_start, duration, unknown_0x396861d0, max_distance, unknown_0x73bef3cb, unknown_0xb7074f38, unknown_0x30a1847b, unknown_0x633bdfff, unknown_0xe49d14bc)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'g"U\xf7')  # 0x672255f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'9ha\xd0')  # 0x396861d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x396861d0))

        data.write(b'%\xb7\xc9\xb2')  # 0x25b7c9b2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_distance))

        data.write(b's\xbe\xf3\xcb')  # 0x73bef3cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x73bef3cb))

        data.write(b'\xb7\x07O8')  # 0xb7074f38
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb7074f38))

        data.write(b'0\xa1\x84{')  # 0x30a1847b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x30a1847b))

        data.write(b'c;\xdf\xff')  # 0x633bdfff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x633bdfff))

        data.write(b'\xe4\x9d\x14\xbc')  # 0xe49d14bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe49d14bc))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct298Json", data)
        return cls(
            scale_spline=Spline.from_json(json_data['scale_spline']),
            auto_start=json_data['auto_start'],
            duration=json_data['duration'],
            unknown_0x396861d0=json_data['unknown_0x396861d0'],
            max_distance=json_data['max_distance'],
            unknown_0x73bef3cb=json_data['unknown_0x73bef3cb'],
            unknown_0xb7074f38=json_data['unknown_0xb7074f38'],
            unknown_0x30a1847b=json_data['unknown_0x30a1847b'],
            unknown_0x633bdfff=json_data['unknown_0x633bdfff'],
            unknown_0xe49d14bc=json_data['unknown_0xe49d14bc'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'scale_spline': self.scale_spline.to_json(),
            'auto_start': self.auto_start,
            'duration': self.duration,
            'unknown_0x396861d0': self.unknown_0x396861d0,
            'max_distance': self.max_distance,
            'unknown_0x73bef3cb': self.unknown_0x73bef3cb,
            'unknown_0xb7074f38': self.unknown_0xb7074f38,
            'unknown_0x30a1847b': self.unknown_0x30a1847b,
            'unknown_0x633bdfff': self.unknown_0x633bdfff,
            'unknown_0xe49d14bc': self.unknown_0xe49d14bc,
        }


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x396861d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x73bef3cb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb7074f38(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x30a1847b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x633bdfff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe49d14bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x672255f7: ('scale_spline', Spline.from_stream),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x8b51e23f: ('duration', _decode_duration),
    0x396861d0: ('unknown_0x396861d0', _decode_unknown_0x396861d0),
    0x25b7c9b2: ('max_distance', _decode_max_distance),
    0x73bef3cb: ('unknown_0x73bef3cb', _decode_unknown_0x73bef3cb),
    0xb7074f38: ('unknown_0xb7074f38', _decode_unknown_0xb7074f38),
    0x30a1847b: ('unknown_0x30a1847b', _decode_unknown_0x30a1847b),
    0x633bdfff: ('unknown_0x633bdfff', _decode_unknown_0x633bdfff),
    0xe49d14bc: ('unknown_0xe49d14bc', _decode_unknown_0xe49d14bc),
}

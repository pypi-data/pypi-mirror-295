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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct266 import UnknownStruct266

if typing.TYPE_CHECKING:
    class UnknownStruct267Json(typing_extensions.TypedDict):
        unknown_struct266: json_util.JsonObject
        unknown: json_util.JsonObject
        min_anim_rate: float
        max_anim_rate: float
        stick_to_max: bool
        loop_forward: bool
        loop_backwards: bool
    

@dataclasses.dataclass()
class UnknownStruct267(BaseProperty):
    unknown_struct266: UnknownStruct266 = dataclasses.field(default_factory=UnknownStruct266, metadata={
        'reflection': FieldReflection[UnknownStruct266](
            UnknownStruct266, id=0x69b1ede1, original_name='UnknownStruct266', from_json=UnknownStruct266.from_json, to_json=UnknownStruct266.to_json
        ),
    })
    unknown: UnknownStruct266 = dataclasses.field(default_factory=UnknownStruct266, metadata={
        'reflection': FieldReflection[UnknownStruct266](
            UnknownStruct266, id=0x1b23374b, original_name='Unknown', from_json=UnknownStruct266.from_json, to_json=UnknownStruct266.to_json
        ),
    })
    min_anim_rate: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe6fe52e5, original_name='MinAnimRate'
        ),
    })
    max_anim_rate: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb707e9b8, original_name='MaxAnimRate'
        ),
    })
    stick_to_max: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x27cf0fe0, original_name='StickToMax'
        ),
    })
    loop_forward: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x652fb7d2, original_name='LoopForward'
        ),
    })
    loop_backwards: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x918d26be, original_name='LoopBackwards'
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
        assert property_id == 0x69b1ede1
        unknown_struct266 = UnknownStruct266.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b23374b
        unknown = UnknownStruct266.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe6fe52e5
        min_anim_rate = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb707e9b8
        max_anim_rate = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x27cf0fe0
        stick_to_max = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x652fb7d2
        loop_forward = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x918d26be
        loop_backwards = struct.unpack('>?', data.read(1))[0]
    
        return cls(unknown_struct266, unknown, min_anim_rate, max_anim_rate, stick_to_max, loop_forward, loop_backwards)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'i\xb1\xed\xe1')  # 0x69b1ede1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct266.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b#7K')  # 0x1b23374b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\xfeR\xe5')  # 0xe6fe52e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_anim_rate))

        data.write(b'\xb7\x07\xe9\xb8')  # 0xb707e9b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_anim_rate))

        data.write(b"'\xcf\x0f\xe0")  # 0x27cf0fe0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stick_to_max))

        data.write(b'e/\xb7\xd2')  # 0x652fb7d2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop_forward))

        data.write(b'\x91\x8d&\xbe')  # 0x918d26be
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop_backwards))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct267Json", data)
        return cls(
            unknown_struct266=UnknownStruct266.from_json(json_data['unknown_struct266']),
            unknown=UnknownStruct266.from_json(json_data['unknown']),
            min_anim_rate=json_data['min_anim_rate'],
            max_anim_rate=json_data['max_anim_rate'],
            stick_to_max=json_data['stick_to_max'],
            loop_forward=json_data['loop_forward'],
            loop_backwards=json_data['loop_backwards'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct266': self.unknown_struct266.to_json(),
            'unknown': self.unknown.to_json(),
            'min_anim_rate': self.min_anim_rate,
            'max_anim_rate': self.max_anim_rate,
            'stick_to_max': self.stick_to_max,
            'loop_forward': self.loop_forward,
            'loop_backwards': self.loop_backwards,
        }


def _decode_min_anim_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_anim_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stick_to_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_forward(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_backwards(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x69b1ede1: ('unknown_struct266', UnknownStruct266.from_stream),
    0x1b23374b: ('unknown', UnknownStruct266.from_stream),
    0xe6fe52e5: ('min_anim_rate', _decode_min_anim_rate),
    0xb707e9b8: ('max_anim_rate', _decode_max_anim_rate),
    0x27cf0fe0: ('stick_to_max', _decode_stick_to_max),
    0x652fb7d2: ('loop_forward', _decode_loop_forward),
    0x918d26be: ('loop_backwards', _decode_loop_backwards),
}

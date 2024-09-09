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

if typing.TYPE_CHECKING:
    class PlayerPeriodicAdditiveAnimationDataJson(typing_extensions.TypedDict):
        random_delay_minimum: float
        random_delay_maximum: float
        animation: int
        visibility_key: str
    

@dataclasses.dataclass()
class PlayerPeriodicAdditiveAnimationData(BaseProperty):
    random_delay_minimum: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6e323295, original_name='RandomDelayMinimum'
        ),
    })
    random_delay_maximum: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfe41227f, original_name='RandomDelayMaximum'
        ),
    })
    animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xaacdb11c, original_name='Animation'
        ),
    })
    visibility_key: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x15dba741, original_name='VisibilityKey'
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
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6e323295
        random_delay_minimum = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe41227f
        random_delay_maximum = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaacdb11c
        animation = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x15dba741
        visibility_key = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(random_delay_minimum, random_delay_maximum, animation, visibility_key)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'n22\x95')  # 0x6e323295
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_delay_minimum))

        data.write(b'\xfeA"\x7f')  # 0xfe41227f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_delay_maximum))

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        data.write(b'\x15\xdb\xa7A')  # 0x15dba741
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.visibility_key.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerPeriodicAdditiveAnimationDataJson", data)
        return cls(
            random_delay_minimum=json_data['random_delay_minimum'],
            random_delay_maximum=json_data['random_delay_maximum'],
            animation=json_data['animation'],
            visibility_key=json_data['visibility_key'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'random_delay_minimum': self.random_delay_minimum,
            'random_delay_maximum': self.random_delay_maximum,
            'animation': self.animation,
            'visibility_key': self.visibility_key,
        }


def _decode_random_delay_minimum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_delay_maximum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_visibility_key(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6e323295: ('random_delay_minimum', _decode_random_delay_minimum),
    0xfe41227f: ('random_delay_maximum', _decode_random_delay_maximum),
    0xaacdb11c: ('animation', _decode_animation),
    0x15dba741: ('visibility_key', _decode_visibility_key),
}

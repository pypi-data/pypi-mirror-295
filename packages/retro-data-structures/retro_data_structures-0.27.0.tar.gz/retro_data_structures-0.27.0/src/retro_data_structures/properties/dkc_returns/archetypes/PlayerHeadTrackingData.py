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
    class PlayerHeadTrackingDataJson(typing_extensions.TypedDict):
        animation: int
        unknown_0x7f96d93c: int
        unknown_0xd0ed78b3: int
        head_aim_locator: str
        head_locator: str
        upper_lip_locator: str
    

@dataclasses.dataclass()
class PlayerHeadTrackingData(BaseProperty):
    animation: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xaacdb11c, original_name='Animation'
        ),
    })
    unknown_0x7f96d93c: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x7f96d93c, original_name='Unknown'
        ),
    })
    unknown_0xd0ed78b3: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xd0ed78b3, original_name='Unknown'
        ),
    })
    head_aim_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xf0eb772d, original_name='HeadAimLocator'
        ),
    })
    head_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xda075c18, original_name='HeadLocator'
        ),
    })
    upper_lip_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xa5fa9d22, original_name='UpperLipLocator'
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
        assert property_id == 0xaacdb11c
        animation = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f96d93c
        unknown_0x7f96d93c = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd0ed78b3
        unknown_0xd0ed78b3 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0eb772d
        head_aim_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xda075c18
        head_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa5fa9d22
        upper_lip_locator = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(animation, unknown_0x7f96d93c, unknown_0xd0ed78b3, head_aim_locator, head_locator, upper_lip_locator)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        data.write(b'\x7f\x96\xd9<')  # 0x7f96d93c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7f96d93c))

        data.write(b'\xd0\xedx\xb3')  # 0xd0ed78b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd0ed78b3))

        data.write(b'\xf0\xebw-')  # 0xf0eb772d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.head_aim_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda\x07\\\x18')  # 0xda075c18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.head_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\xfa\x9d"')  # 0xa5fa9d22
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.upper_lip_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerHeadTrackingDataJson", data)
        return cls(
            animation=json_data['animation'],
            unknown_0x7f96d93c=json_data['unknown_0x7f96d93c'],
            unknown_0xd0ed78b3=json_data['unknown_0xd0ed78b3'],
            head_aim_locator=json_data['head_aim_locator'],
            head_locator=json_data['head_locator'],
            upper_lip_locator=json_data['upper_lip_locator'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'animation': self.animation,
            'unknown_0x7f96d93c': self.unknown_0x7f96d93c,
            'unknown_0xd0ed78b3': self.unknown_0xd0ed78b3,
            'head_aim_locator': self.head_aim_locator,
            'head_locator': self.head_locator,
            'upper_lip_locator': self.upper_lip_locator,
        }


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7f96d93c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd0ed78b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_head_aim_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_head_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_upper_lip_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaacdb11c: ('animation', _decode_animation),
    0x7f96d93c: ('unknown_0x7f96d93c', _decode_unknown_0x7f96d93c),
    0xd0ed78b3: ('unknown_0xd0ed78b3', _decode_unknown_0xd0ed78b3),
    0xf0eb772d: ('head_aim_locator', _decode_head_aim_locator),
    0xda075c18: ('head_locator', _decode_head_locator),
    0xa5fa9d22: ('upper_lip_locator', _decode_upper_lip_locator),
}

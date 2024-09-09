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
    class UnknownStruct230Json(typing_extensions.TypedDict):
        unknown_0x43bc661c: bool
        allow_swipe: bool
        unknown_0xe10e94ec: float
        unknown_0x84b3080b: str
        unknown_0x69170884: str
    

@dataclasses.dataclass()
class UnknownStruct230(BaseProperty):
    unknown_0x43bc661c: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x43bc661c, original_name='Unknown'
        ),
    })
    allow_swipe: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x410bdef2, original_name='AllowSwipe'
        ),
    })
    unknown_0xe10e94ec: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe10e94ec, original_name='Unknown'
        ),
    })
    unknown_0x84b3080b: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x84b3080b, original_name='Unknown'
        ),
    })
    unknown_0x69170884: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x69170884, original_name='Unknown'
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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43bc661c
        unknown_0x43bc661c = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x410bdef2
        allow_swipe = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe10e94ec
        unknown_0xe10e94ec = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x84b3080b
        unknown_0x84b3080b = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x69170884
        unknown_0x69170884 = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(unknown_0x43bc661c, allow_swipe, unknown_0xe10e94ec, unknown_0x84b3080b, unknown_0x69170884)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'C\xbcf\x1c')  # 0x43bc661c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x43bc661c))

        data.write(b'A\x0b\xde\xf2')  # 0x410bdef2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_swipe))

        data.write(b'\xe1\x0e\x94\xec')  # 0xe10e94ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe10e94ec))

        data.write(b'\x84\xb3\x08\x0b')  # 0x84b3080b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x84b3080b.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i\x17\x08\x84')  # 0x69170884
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x69170884.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct230Json", data)
        return cls(
            unknown_0x43bc661c=json_data['unknown_0x43bc661c'],
            allow_swipe=json_data['allow_swipe'],
            unknown_0xe10e94ec=json_data['unknown_0xe10e94ec'],
            unknown_0x84b3080b=json_data['unknown_0x84b3080b'],
            unknown_0x69170884=json_data['unknown_0x69170884'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x43bc661c': self.unknown_0x43bc661c,
            'allow_swipe': self.allow_swipe,
            'unknown_0xe10e94ec': self.unknown_0xe10e94ec,
            'unknown_0x84b3080b': self.unknown_0x84b3080b,
            'unknown_0x69170884': self.unknown_0x69170884,
        }


def _decode_unknown_0x43bc661c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_swipe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe10e94ec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x84b3080b(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown_0x69170884(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x43bc661c: ('unknown_0x43bc661c', _decode_unknown_0x43bc661c),
    0x410bdef2: ('allow_swipe', _decode_allow_swipe),
    0xe10e94ec: ('unknown_0xe10e94ec', _decode_unknown_0xe10e94ec),
    0x84b3080b: ('unknown_0x84b3080b', _decode_unknown_0x84b3080b),
    0x69170884: ('unknown_0x69170884', _decode_unknown_0x69170884),
}

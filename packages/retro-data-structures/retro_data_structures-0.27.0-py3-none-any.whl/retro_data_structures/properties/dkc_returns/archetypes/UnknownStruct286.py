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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct57 import UnknownStruct57

if typing.TYPE_CHECKING:
    class UnknownStruct286Json(typing_extensions.TypedDict):
        size: int
        unknown_struct57_0xa8233351: json_util.JsonObject
        unknown_struct57_0xf3348244: json_util.JsonObject
        unknown_struct57_0xc5c612b7: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct286(BaseProperty):
    size: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x0bdf71c5, original_name='Size'
        ),
    })
    unknown_struct57_0xa8233351: UnknownStruct57 = dataclasses.field(default_factory=UnknownStruct57, metadata={
        'reflection': FieldReflection[UnknownStruct57](
            UnknownStruct57, id=0xa8233351, original_name='UnknownStruct57', from_json=UnknownStruct57.from_json, to_json=UnknownStruct57.to_json
        ),
    })
    unknown_struct57_0xf3348244: UnknownStruct57 = dataclasses.field(default_factory=UnknownStruct57, metadata={
        'reflection': FieldReflection[UnknownStruct57](
            UnknownStruct57, id=0xf3348244, original_name='UnknownStruct57', from_json=UnknownStruct57.from_json, to_json=UnknownStruct57.to_json
        ),
    })
    unknown_struct57_0xc5c612b7: UnknownStruct57 = dataclasses.field(default_factory=UnknownStruct57, metadata={
        'reflection': FieldReflection[UnknownStruct57](
            UnknownStruct57, id=0xc5c612b7, original_name='UnknownStruct57', from_json=UnknownStruct57.from_json, to_json=UnknownStruct57.to_json
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
        assert property_id == 0x0bdf71c5
        size = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa8233351
        unknown_struct57_0xa8233351 = UnknownStruct57.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf3348244
        unknown_struct57_0xf3348244 = UnknownStruct57.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc5c612b7
        unknown_struct57_0xc5c612b7 = UnknownStruct57.from_stream(data, property_size)
    
        return cls(size, unknown_struct57_0xa8233351, unknown_struct57_0xf3348244, unknown_struct57_0xc5c612b7)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x0b\xdfq\xc5')  # 0xbdf71c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.size))

        data.write(b'\xa8#3Q')  # 0xa8233351
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct57_0xa8233351.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf34\x82D')  # 0xf3348244
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct57_0xf3348244.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\xc6\x12\xb7')  # 0xc5c612b7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct57_0xc5c612b7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct286Json", data)
        return cls(
            size=json_data['size'],
            unknown_struct57_0xa8233351=UnknownStruct57.from_json(json_data['unknown_struct57_0xa8233351']),
            unknown_struct57_0xf3348244=UnknownStruct57.from_json(json_data['unknown_struct57_0xf3348244']),
            unknown_struct57_0xc5c612b7=UnknownStruct57.from_json(json_data['unknown_struct57_0xc5c612b7']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'size': self.size,
            'unknown_struct57_0xa8233351': self.unknown_struct57_0xa8233351.to_json(),
            'unknown_struct57_0xf3348244': self.unknown_struct57_0xf3348244.to_json(),
            'unknown_struct57_0xc5c612b7': self.unknown_struct57_0xc5c612b7.to_json(),
        }


def _decode_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbdf71c5: ('size', _decode_size),
    0xa8233351: ('unknown_struct57_0xa8233351', UnknownStruct57.from_stream),
    0xf3348244: ('unknown_struct57_0xf3348244', UnknownStruct57.from_stream),
    0xc5c612b7: ('unknown_struct57_0xc5c612b7', UnknownStruct57.from_stream),
}

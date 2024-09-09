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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct293 import UnknownStruct293
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct294 import UnknownStruct294

if typing.TYPE_CHECKING:
    class UnknownStruct295Json(typing_extensions.TypedDict):
        gravity: float
        unknown: float
        unknown_struct293: json_util.JsonObject
        unknown_struct294: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct295(BaseProperty):
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    unknown: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xee382651, original_name='Unknown'
        ),
    })
    unknown_struct293: UnknownStruct293 = dataclasses.field(default_factory=UnknownStruct293, metadata={
        'reflection': FieldReflection[UnknownStruct293](
            UnknownStruct293, id=0xa9b9997f, original_name='UnknownStruct293', from_json=UnknownStruct293.from_json, to_json=UnknownStruct293.to_json
        ),
    })
    unknown_struct294: UnknownStruct294 = dataclasses.field(default_factory=UnknownStruct294, metadata={
        'reflection': FieldReflection[UnknownStruct294](
            UnknownStruct294, id=0x7e3b3184, original_name='UnknownStruct294', from_json=UnknownStruct294.from_json, to_json=UnknownStruct294.to_json
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
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xee382651
        unknown = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa9b9997f
        unknown_struct293 = UnknownStruct293.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e3b3184
        unknown_struct294 = UnknownStruct294.from_stream(data, property_size)
    
        return cls(gravity, unknown, unknown_struct293, unknown_struct294)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xee8&Q')  # 0xee382651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xa9\xb9\x99\x7f')  # 0xa9b9997f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct293.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~;1\x84')  # 0x7e3b3184
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct294.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct295Json", data)
        return cls(
            gravity=json_data['gravity'],
            unknown=json_data['unknown'],
            unknown_struct293=UnknownStruct293.from_json(json_data['unknown_struct293']),
            unknown_struct294=UnknownStruct294.from_json(json_data['unknown_struct294']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gravity': self.gravity,
            'unknown': self.unknown,
            'unknown_struct293': self.unknown_struct293.to_json(),
            'unknown_struct294': self.unknown_struct294.to_json(),
        }


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xee382651: ('unknown', _decode_unknown),
    0xa9b9997f: ('unknown_struct293', UnknownStruct293.from_stream),
    0x7e3b3184: ('unknown_struct294', UnknownStruct294.from_stream),
}

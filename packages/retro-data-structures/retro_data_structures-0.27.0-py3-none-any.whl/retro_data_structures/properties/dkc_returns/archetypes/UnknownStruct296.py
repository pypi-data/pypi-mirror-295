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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct287 import UnknownStruct287
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct288 import UnknownStruct288
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct290 import UnknownStruct290
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct291 import UnknownStruct291
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct292 import UnknownStruct292
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct295 import UnknownStruct295

if typing.TYPE_CHECKING:
    class UnknownStruct296Json(typing_extensions.TypedDict):
        unknown_struct287: json_util.JsonObject
        unknown_struct288: json_util.JsonObject
        unknown_struct290: json_util.JsonObject
        unknown_struct291: json_util.JsonObject
        unknown_struct292: json_util.JsonObject
        unknown_struct295: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct296(BaseProperty):
    unknown_struct287: UnknownStruct287 = dataclasses.field(default_factory=UnknownStruct287, metadata={
        'reflection': FieldReflection[UnknownStruct287](
            UnknownStruct287, id=0x4ae8523d, original_name='UnknownStruct287', from_json=UnknownStruct287.from_json, to_json=UnknownStruct287.to_json
        ),
    })
    unknown_struct288: UnknownStruct288 = dataclasses.field(default_factory=UnknownStruct288, metadata={
        'reflection': FieldReflection[UnknownStruct288](
            UnknownStruct288, id=0x2a447166, original_name='UnknownStruct288', from_json=UnknownStruct288.from_json, to_json=UnknownStruct288.to_json
        ),
    })
    unknown_struct290: UnknownStruct290 = dataclasses.field(default_factory=UnknownStruct290, metadata={
        'reflection': FieldReflection[UnknownStruct290](
            UnknownStruct290, id=0xdd5c7083, original_name='UnknownStruct290', from_json=UnknownStruct290.from_json, to_json=UnknownStruct290.to_json
        ),
    })
    unknown_struct291: UnknownStruct291 = dataclasses.field(default_factory=UnknownStruct291, metadata={
        'reflection': FieldReflection[UnknownStruct291](
            UnknownStruct291, id=0xe6857328, original_name='UnknownStruct291', from_json=UnknownStruct291.from_json, to_json=UnknownStruct291.to_json
        ),
    })
    unknown_struct292: UnknownStruct292 = dataclasses.field(default_factory=UnknownStruct292, metadata={
        'reflection': FieldReflection[UnknownStruct292](
            UnknownStruct292, id=0x2b531c2f, original_name='UnknownStruct292', from_json=UnknownStruct292.from_json, to_json=UnknownStruct292.to_json
        ),
    })
    unknown_struct295: UnknownStruct295 = dataclasses.field(default_factory=UnknownStruct295, metadata={
        'reflection': FieldReflection[UnknownStruct295](
            UnknownStruct295, id=0x9127fbc8, original_name='UnknownStruct295', from_json=UnknownStruct295.from_json, to_json=UnknownStruct295.to_json
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
        assert property_id == 0x4ae8523d
        unknown_struct287 = UnknownStruct287.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2a447166
        unknown_struct288 = UnknownStruct288.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdd5c7083
        unknown_struct290 = UnknownStruct290.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe6857328
        unknown_struct291 = UnknownStruct291.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2b531c2f
        unknown_struct292 = UnknownStruct292.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9127fbc8
        unknown_struct295 = UnknownStruct295.from_stream(data, property_size)
    
        return cls(unknown_struct287, unknown_struct288, unknown_struct290, unknown_struct291, unknown_struct292, unknown_struct295)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'J\xe8R=')  # 0x4ae8523d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct287.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*Dqf')  # 0x2a447166
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct288.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd\\p\x83')  # 0xdd5c7083
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct290.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\x85s(')  # 0xe6857328
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct291.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+S\x1c/')  # 0x2b531c2f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct292.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\x91'\xfb\xc8")  # 0x9127fbc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct295.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct296Json", data)
        return cls(
            unknown_struct287=UnknownStruct287.from_json(json_data['unknown_struct287']),
            unknown_struct288=UnknownStruct288.from_json(json_data['unknown_struct288']),
            unknown_struct290=UnknownStruct290.from_json(json_data['unknown_struct290']),
            unknown_struct291=UnknownStruct291.from_json(json_data['unknown_struct291']),
            unknown_struct292=UnknownStruct292.from_json(json_data['unknown_struct292']),
            unknown_struct295=UnknownStruct295.from_json(json_data['unknown_struct295']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct287': self.unknown_struct287.to_json(),
            'unknown_struct288': self.unknown_struct288.to_json(),
            'unknown_struct290': self.unknown_struct290.to_json(),
            'unknown_struct291': self.unknown_struct291.to_json(),
            'unknown_struct292': self.unknown_struct292.to_json(),
            'unknown_struct295': self.unknown_struct295.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4ae8523d: ('unknown_struct287', UnknownStruct287.from_stream),
    0x2a447166: ('unknown_struct288', UnknownStruct288.from_stream),
    0xdd5c7083: ('unknown_struct290', UnknownStruct290.from_stream),
    0xe6857328: ('unknown_struct291', UnknownStruct291.from_stream),
    0x2b531c2f: ('unknown_struct292', UnknownStruct292.from_stream),
    0x9127fbc8: ('unknown_struct295', UnknownStruct295.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct186 import UnknownStruct186
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct187 import UnknownStruct187
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct188 import UnknownStruct188
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct189 import UnknownStruct189
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct190 import UnknownStruct190
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct191 import UnknownStruct191
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct54 import UnknownStruct54

if typing.TYPE_CHECKING:
    class UnknownStruct56Json(typing_extensions.TypedDict):
        unknown_struct54: json_util.JsonObject
        unknown_struct186: json_util.JsonObject
        unknown_struct187: json_util.JsonObject
        unknown_struct188: json_util.JsonObject
        unknown_struct189: json_util.JsonObject
        unknown_struct190: json_util.JsonObject
        unknown_struct191: json_util.JsonObject
        frequency: float
    

@dataclasses.dataclass()
class UnknownStruct56(BaseProperty):
    unknown_struct54: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54, metadata={
        'reflection': FieldReflection[UnknownStruct54](
            UnknownStruct54, id=0x45d39080, original_name='UnknownStruct54', from_json=UnknownStruct54.from_json, to_json=UnknownStruct54.to_json
        ),
    })
    unknown_struct186: UnknownStruct186 = dataclasses.field(default_factory=UnknownStruct186, metadata={
        'reflection': FieldReflection[UnknownStruct186](
            UnknownStruct186, id=0x445ef669, original_name='UnknownStruct186', from_json=UnknownStruct186.from_json, to_json=UnknownStruct186.to_json
        ),
    })
    unknown_struct187: UnknownStruct187 = dataclasses.field(default_factory=UnknownStruct187, metadata={
        'reflection': FieldReflection[UnknownStruct187](
            UnknownStruct187, id=0xec8db600, original_name='UnknownStruct187', from_json=UnknownStruct187.from_json, to_json=UnknownStruct187.to_json
        ),
    })
    unknown_struct188: UnknownStruct188 = dataclasses.field(default_factory=UnknownStruct188, metadata={
        'reflection': FieldReflection[UnknownStruct188](
            UnknownStruct188, id=0xccb08a34, original_name='UnknownStruct188', from_json=UnknownStruct188.from_json, to_json=UnknownStruct188.to_json
        ),
    })
    unknown_struct189: UnknownStruct189 = dataclasses.field(default_factory=UnknownStruct189, metadata={
        'reflection': FieldReflection[UnknownStruct189](
            UnknownStruct189, id=0x01197c47, original_name='UnknownStruct189', from_json=UnknownStruct189.from_json, to_json=UnknownStruct189.to_json
        ),
    })
    unknown_struct190: UnknownStruct190 = dataclasses.field(default_factory=UnknownStruct190, metadata={
        'reflection': FieldReflection[UnknownStruct190](
            UnknownStruct190, id=0xf140225c, original_name='UnknownStruct190', from_json=UnknownStruct190.from_json, to_json=UnknownStruct190.to_json
        ),
    })
    unknown_struct191: UnknownStruct191 = dataclasses.field(default_factory=UnknownStruct191, metadata={
        'reflection': FieldReflection[UnknownStruct191](
            UnknownStruct191, id=0xbf455e0f, original_name='UnknownStruct191', from_json=UnknownStruct191.from_json, to_json=UnknownStruct191.to_json
        ),
    })
    frequency: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x98cbfedc, original_name='Frequency'
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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x45d39080
        unknown_struct54 = UnknownStruct54.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x445ef669
        unknown_struct186 = UnknownStruct186.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xec8db600
        unknown_struct187 = UnknownStruct187.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xccb08a34
        unknown_struct188 = UnknownStruct188.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x01197c47
        unknown_struct189 = UnknownStruct189.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf140225c
        unknown_struct190 = UnknownStruct190.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf455e0f
        unknown_struct191 = UnknownStruct191.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x98cbfedc
        frequency = struct.unpack('>f', data.read(4))[0]
    
        return cls(unknown_struct54, unknown_struct186, unknown_struct187, unknown_struct188, unknown_struct189, unknown_struct190, unknown_struct191, frequency)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'E\xd3\x90\x80')  # 0x45d39080
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D^\xf6i')  # 0x445ef669
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct186.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec\x8d\xb6\x00')  # 0xec8db600
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct187.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc\xb0\x8a4')  # 0xccb08a34
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct188.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\x19|G')  # 0x1197c47
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct189.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1@"\\')  # 0xf140225c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct190.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbfE^\x0f')  # 0xbf455e0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct191.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xcb\xfe\xdc')  # 0x98cbfedc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.frequency))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct56Json", data)
        return cls(
            unknown_struct54=UnknownStruct54.from_json(json_data['unknown_struct54']),
            unknown_struct186=UnknownStruct186.from_json(json_data['unknown_struct186']),
            unknown_struct187=UnknownStruct187.from_json(json_data['unknown_struct187']),
            unknown_struct188=UnknownStruct188.from_json(json_data['unknown_struct188']),
            unknown_struct189=UnknownStruct189.from_json(json_data['unknown_struct189']),
            unknown_struct190=UnknownStruct190.from_json(json_data['unknown_struct190']),
            unknown_struct191=UnknownStruct191.from_json(json_data['unknown_struct191']),
            frequency=json_data['frequency'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct54': self.unknown_struct54.to_json(),
            'unknown_struct186': self.unknown_struct186.to_json(),
            'unknown_struct187': self.unknown_struct187.to_json(),
            'unknown_struct188': self.unknown_struct188.to_json(),
            'unknown_struct189': self.unknown_struct189.to_json(),
            'unknown_struct190': self.unknown_struct190.to_json(),
            'unknown_struct191': self.unknown_struct191.to_json(),
            'frequency': self.frequency,
        }


def _decode_frequency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45d39080: ('unknown_struct54', UnknownStruct54.from_stream),
    0x445ef669: ('unknown_struct186', UnknownStruct186.from_stream),
    0xec8db600: ('unknown_struct187', UnknownStruct187.from_stream),
    0xccb08a34: ('unknown_struct188', UnknownStruct188.from_stream),
    0x1197c47: ('unknown_struct189', UnknownStruct189.from_stream),
    0xf140225c: ('unknown_struct190', UnknownStruct190.from_stream),
    0xbf455e0f: ('unknown_struct191', UnknownStruct191.from_stream),
    0x98cbfedc: ('frequency', _decode_frequency),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.RevolutionControl import RevolutionControl

if typing.TYPE_CHECKING:
    class MiscControlsJson(typing_extensions.TypedDict):
        unknown_0x439f3678: json_util.JsonObject
        unknown_0xbf8653ed: json_util.JsonObject
        unknown_0x9ca552b4: json_util.JsonObject
        unknown_0x88b5fd4d: json_util.JsonObject
        unknown_0xb63c1d0b: json_util.JsonObject
        unknown_0x1d88ee3e: json_util.JsonObject
        skip_cinematic: json_util.JsonObject
        unknown_0xd9cf3e97: json_util.JsonObject
        unknown_0xb7346005: json_util.JsonObject
        unknown_0x76299df7: json_util.JsonObject
        unknown_0x2c2b2b0e: json_util.JsonObject
    

@dataclasses.dataclass()
class MiscControls(BaseProperty):
    unknown_0x439f3678: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x439f3678, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xbf8653ed: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xbf8653ed, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x9ca552b4: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x9ca552b4, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x88b5fd4d: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x88b5fd4d, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xb63c1d0b: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xb63c1d0b, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x1d88ee3e: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x1d88ee3e, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    skip_cinematic: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x19a3e07d, original_name='SkipCinematic', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xd9cf3e97: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xd9cf3e97, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xb7346005: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xb7346005, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x76299df7: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x76299df7, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x2c2b2b0e: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x2c2b2b0e, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x439f3678
        unknown_0x439f3678 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf8653ed
        unknown_0xbf8653ed = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ca552b4
        unknown_0x9ca552b4 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x88b5fd4d
        unknown_0x88b5fd4d = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb63c1d0b
        unknown_0xb63c1d0b = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1d88ee3e
        unknown_0x1d88ee3e = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x19a3e07d
        skip_cinematic = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9cf3e97
        unknown_0xd9cf3e97 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb7346005
        unknown_0xb7346005 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76299df7
        unknown_0x76299df7 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2c2b2b0e
        unknown_0x2c2b2b0e = RevolutionControl.from_stream(data, property_size)
    
        return cls(unknown_0x439f3678, unknown_0xbf8653ed, unknown_0x9ca552b4, unknown_0x88b5fd4d, unknown_0xb63c1d0b, unknown_0x1d88ee3e, skip_cinematic, unknown_0xd9cf3e97, unknown_0xb7346005, unknown_0x76299df7, unknown_0x2c2b2b0e)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'C\x9f6x')  # 0x439f3678
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x439f3678.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x86S\xed')  # 0xbf8653ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbf8653ed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\xa5R\xb4')  # 0x9ca552b4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x9ca552b4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\xb5\xfdM')  # 0x88b5fd4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x88b5fd4d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6<\x1d\x0b')  # 0xb63c1d0b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb63c1d0b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\x88\xee>')  # 0x1d88ee3e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1d88ee3e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xa3\xe0}')  # 0x19a3e07d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.skip_cinematic.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd9\xcf>\x97')  # 0xd9cf3e97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd9cf3e97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb74`\x05')  # 0xb7346005
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb7346005.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v)\x9d\xf7')  # 0x76299df7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x76299df7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',++\x0e')  # 0x2c2b2b0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x2c2b2b0e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MiscControlsJson", data)
        return cls(
            unknown_0x439f3678=RevolutionControl.from_json(json_data['unknown_0x439f3678']),
            unknown_0xbf8653ed=RevolutionControl.from_json(json_data['unknown_0xbf8653ed']),
            unknown_0x9ca552b4=RevolutionControl.from_json(json_data['unknown_0x9ca552b4']),
            unknown_0x88b5fd4d=RevolutionControl.from_json(json_data['unknown_0x88b5fd4d']),
            unknown_0xb63c1d0b=RevolutionControl.from_json(json_data['unknown_0xb63c1d0b']),
            unknown_0x1d88ee3e=RevolutionControl.from_json(json_data['unknown_0x1d88ee3e']),
            skip_cinematic=RevolutionControl.from_json(json_data['skip_cinematic']),
            unknown_0xd9cf3e97=RevolutionControl.from_json(json_data['unknown_0xd9cf3e97']),
            unknown_0xb7346005=RevolutionControl.from_json(json_data['unknown_0xb7346005']),
            unknown_0x76299df7=RevolutionControl.from_json(json_data['unknown_0x76299df7']),
            unknown_0x2c2b2b0e=RevolutionControl.from_json(json_data['unknown_0x2c2b2b0e']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x439f3678': self.unknown_0x439f3678.to_json(),
            'unknown_0xbf8653ed': self.unknown_0xbf8653ed.to_json(),
            'unknown_0x9ca552b4': self.unknown_0x9ca552b4.to_json(),
            'unknown_0x88b5fd4d': self.unknown_0x88b5fd4d.to_json(),
            'unknown_0xb63c1d0b': self.unknown_0xb63c1d0b.to_json(),
            'unknown_0x1d88ee3e': self.unknown_0x1d88ee3e.to_json(),
            'skip_cinematic': self.skip_cinematic.to_json(),
            'unknown_0xd9cf3e97': self.unknown_0xd9cf3e97.to_json(),
            'unknown_0xb7346005': self.unknown_0xb7346005.to_json(),
            'unknown_0x76299df7': self.unknown_0x76299df7.to_json(),
            'unknown_0x2c2b2b0e': self.unknown_0x2c2b2b0e.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x439f3678: ('unknown_0x439f3678', RevolutionControl.from_stream),
    0xbf8653ed: ('unknown_0xbf8653ed', RevolutionControl.from_stream),
    0x9ca552b4: ('unknown_0x9ca552b4', RevolutionControl.from_stream),
    0x88b5fd4d: ('unknown_0x88b5fd4d', RevolutionControl.from_stream),
    0xb63c1d0b: ('unknown_0xb63c1d0b', RevolutionControl.from_stream),
    0x1d88ee3e: ('unknown_0x1d88ee3e', RevolutionControl.from_stream),
    0x19a3e07d: ('skip_cinematic', RevolutionControl.from_stream),
    0xd9cf3e97: ('unknown_0xd9cf3e97', RevolutionControl.from_stream),
    0xb7346005: ('unknown_0xb7346005', RevolutionControl.from_stream),
    0x76299df7: ('unknown_0x76299df7', RevolutionControl.from_stream),
    0x2c2b2b0e: ('unknown_0x2c2b2b0e', RevolutionControl.from_stream),
}

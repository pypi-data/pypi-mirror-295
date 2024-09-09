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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct279 import UnknownStruct279
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct280 import UnknownStruct280
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct281 import UnknownStruct281
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct282 import UnknownStruct282
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct283 import UnknownStruct283
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct284 import UnknownStruct284
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct58 import UnknownStruct58

if typing.TYPE_CHECKING:
    class UnknownStruct285Json(typing_extensions.TypedDict):
        unknown_struct279: json_util.JsonObject
        unknown_struct58_0xc9045a02: json_util.JsonObject
        unknown_struct280: json_util.JsonObject
        unknown_struct58_0xfab2f514: json_util.JsonObject
        unknown_struct281: json_util.JsonObject
        unknown_0x7a5e5e73: json_util.JsonObject
        unknown_struct282: json_util.JsonObject
        unknown_struct283: json_util.JsonObject
        unknown_struct284: json_util.JsonObject
        unknown_0x016768be: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct285(BaseProperty):
    unknown_struct279: UnknownStruct279 = dataclasses.field(default_factory=UnknownStruct279, metadata={
        'reflection': FieldReflection[UnknownStruct279](
            UnknownStruct279, id=0x16d20640, original_name='UnknownStruct279', from_json=UnknownStruct279.from_json, to_json=UnknownStruct279.to_json
        ),
    })
    unknown_struct58_0xc9045a02: UnknownStruct58 = dataclasses.field(default_factory=UnknownStruct58, metadata={
        'reflection': FieldReflection[UnknownStruct58](
            UnknownStruct58, id=0xc9045a02, original_name='UnknownStruct58', from_json=UnknownStruct58.from_json, to_json=UnknownStruct58.to_json
        ),
    })
    unknown_struct280: UnknownStruct280 = dataclasses.field(default_factory=UnknownStruct280, metadata={
        'reflection': FieldReflection[UnknownStruct280](
            UnknownStruct280, id=0xc5a31fc4, original_name='UnknownStruct280', from_json=UnknownStruct280.from_json, to_json=UnknownStruct280.to_json
        ),
    })
    unknown_struct58_0xfab2f514: UnknownStruct58 = dataclasses.field(default_factory=UnknownStruct58, metadata={
        'reflection': FieldReflection[UnknownStruct58](
            UnknownStruct58, id=0xfab2f514, original_name='UnknownStruct58', from_json=UnknownStruct58.from_json, to_json=UnknownStruct58.to_json
        ),
    })
    unknown_struct281: UnknownStruct281 = dataclasses.field(default_factory=UnknownStruct281, metadata={
        'reflection': FieldReflection[UnknownStruct281](
            UnknownStruct281, id=0x6a5549a3, original_name='UnknownStruct281', from_json=UnknownStruct281.from_json, to_json=UnknownStruct281.to_json
        ),
    })
    unknown_0x7a5e5e73: UnknownStruct281 = dataclasses.field(default_factory=UnknownStruct281, metadata={
        'reflection': FieldReflection[UnknownStruct281](
            UnknownStruct281, id=0x7a5e5e73, original_name='Unknown', from_json=UnknownStruct281.from_json, to_json=UnknownStruct281.to_json
        ),
    })
    unknown_struct282: UnknownStruct282 = dataclasses.field(default_factory=UnknownStruct282, metadata={
        'reflection': FieldReflection[UnknownStruct282](
            UnknownStruct282, id=0x63cd839f, original_name='UnknownStruct282', from_json=UnknownStruct282.from_json, to_json=UnknownStruct282.to_json
        ),
    })
    unknown_struct283: UnknownStruct283 = dataclasses.field(default_factory=UnknownStruct283, metadata={
        'reflection': FieldReflection[UnknownStruct283](
            UnknownStruct283, id=0xf17aef10, original_name='UnknownStruct283', from_json=UnknownStruct283.from_json, to_json=UnknownStruct283.to_json
        ),
    })
    unknown_struct284: UnknownStruct284 = dataclasses.field(default_factory=UnknownStruct284, metadata={
        'reflection': FieldReflection[UnknownStruct284](
            UnknownStruct284, id=0xc932f084, original_name='UnknownStruct284', from_json=UnknownStruct284.from_json, to_json=UnknownStruct284.to_json
        ),
    })
    unknown_0x016768be: UnknownStruct284 = dataclasses.field(default_factory=UnknownStruct284, metadata={
        'reflection': FieldReflection[UnknownStruct284](
            UnknownStruct284, id=0x016768be, original_name='Unknown', from_json=UnknownStruct284.from_json, to_json=UnknownStruct284.to_json
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
        assert property_id == 0x16d20640
        unknown_struct279 = UnknownStruct279.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc9045a02
        unknown_struct58_0xc9045a02 = UnknownStruct58.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc5a31fc4
        unknown_struct280 = UnknownStruct280.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfab2f514
        unknown_struct58_0xfab2f514 = UnknownStruct58.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a5549a3
        unknown_struct281 = UnknownStruct281.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7a5e5e73
        unknown_0x7a5e5e73 = UnknownStruct281.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x63cd839f
        unknown_struct282 = UnknownStruct282.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf17aef10
        unknown_struct283 = UnknownStruct283.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc932f084
        unknown_struct284 = UnknownStruct284.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x016768be
        unknown_0x016768be = UnknownStruct284.from_stream(data, property_size)
    
        return cls(unknown_struct279, unknown_struct58_0xc9045a02, unknown_struct280, unknown_struct58_0xfab2f514, unknown_struct281, unknown_0x7a5e5e73, unknown_struct282, unknown_struct283, unknown_struct284, unknown_0x016768be)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x16\xd2\x06@')  # 0x16d20640
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct279.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9\x04Z\x02')  # 0xc9045a02
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct58_0xc9045a02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\xa3\x1f\xc4')  # 0xc5a31fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct280.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xb2\xf5\x14')  # 0xfab2f514
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct58_0xfab2f514.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jUI\xa3')  # 0x6a5549a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct281.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z^^s')  # 0x7a5e5e73
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7a5e5e73.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\xcd\x83\x9f')  # 0x63cd839f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct282.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1z\xef\x10')  # 0xf17aef10
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct283.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc92\xf0\x84')  # 0xc932f084
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct284.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01gh\xbe')  # 0x16768be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x016768be.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct285Json", data)
        return cls(
            unknown_struct279=UnknownStruct279.from_json(json_data['unknown_struct279']),
            unknown_struct58_0xc9045a02=UnknownStruct58.from_json(json_data['unknown_struct58_0xc9045a02']),
            unknown_struct280=UnknownStruct280.from_json(json_data['unknown_struct280']),
            unknown_struct58_0xfab2f514=UnknownStruct58.from_json(json_data['unknown_struct58_0xfab2f514']),
            unknown_struct281=UnknownStruct281.from_json(json_data['unknown_struct281']),
            unknown_0x7a5e5e73=UnknownStruct281.from_json(json_data['unknown_0x7a5e5e73']),
            unknown_struct282=UnknownStruct282.from_json(json_data['unknown_struct282']),
            unknown_struct283=UnknownStruct283.from_json(json_data['unknown_struct283']),
            unknown_struct284=UnknownStruct284.from_json(json_data['unknown_struct284']),
            unknown_0x016768be=UnknownStruct284.from_json(json_data['unknown_0x016768be']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct279': self.unknown_struct279.to_json(),
            'unknown_struct58_0xc9045a02': self.unknown_struct58_0xc9045a02.to_json(),
            'unknown_struct280': self.unknown_struct280.to_json(),
            'unknown_struct58_0xfab2f514': self.unknown_struct58_0xfab2f514.to_json(),
            'unknown_struct281': self.unknown_struct281.to_json(),
            'unknown_0x7a5e5e73': self.unknown_0x7a5e5e73.to_json(),
            'unknown_struct282': self.unknown_struct282.to_json(),
            'unknown_struct283': self.unknown_struct283.to_json(),
            'unknown_struct284': self.unknown_struct284.to_json(),
            'unknown_0x016768be': self.unknown_0x016768be.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x16d20640: ('unknown_struct279', UnknownStruct279.from_stream),
    0xc9045a02: ('unknown_struct58_0xc9045a02', UnknownStruct58.from_stream),
    0xc5a31fc4: ('unknown_struct280', UnknownStruct280.from_stream),
    0xfab2f514: ('unknown_struct58_0xfab2f514', UnknownStruct58.from_stream),
    0x6a5549a3: ('unknown_struct281', UnknownStruct281.from_stream),
    0x7a5e5e73: ('unknown_0x7a5e5e73', UnknownStruct281.from_stream),
    0x63cd839f: ('unknown_struct282', UnknownStruct282.from_stream),
    0xf17aef10: ('unknown_struct283', UnknownStruct283.from_stream),
    0xc932f084: ('unknown_struct284', UnknownStruct284.from_stream),
    0x16768be: ('unknown_0x016768be', UnknownStruct284.from_stream),
}

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
    class MapControlsJson(typing_extensions.TypedDict):
        unknown_0xb5f75bfb: json_util.JsonObject
        unknown_0x2ced2b18: json_util.JsonObject
        unknown_0x640f66c6: json_util.JsonObject
        unknown_0xdfe791c6: json_util.JsonObject
        unknown_0x55861a4b: json_util.JsonObject
        unknown_0xebd3a5f8: json_util.JsonObject
        unknown_0x385cbd2f: json_util.JsonObject
        unknown_0x5f55ccca: json_util.JsonObject
        unknown_0x81e8cf07: json_util.JsonObject
        unknown_0x2ac6123a: json_util.JsonObject
    

@dataclasses.dataclass()
class MapControls(BaseProperty):
    unknown_0xb5f75bfb: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xb5f75bfb, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x2ced2b18: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x2ced2b18, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x640f66c6: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x640f66c6, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xdfe791c6: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xdfe791c6, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x55861a4b: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x55861a4b, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xebd3a5f8: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xebd3a5f8, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x385cbd2f: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x385cbd2f, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x5f55ccca: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x5f55ccca, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x81e8cf07: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x81e8cf07, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x2ac6123a: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x2ac6123a, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
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
        assert property_id == 0xb5f75bfb
        unknown_0xb5f75bfb = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2ced2b18
        unknown_0x2ced2b18 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x640f66c6
        unknown_0x640f66c6 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdfe791c6
        unknown_0xdfe791c6 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x55861a4b
        unknown_0x55861a4b = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xebd3a5f8
        unknown_0xebd3a5f8 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x385cbd2f
        unknown_0x385cbd2f = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5f55ccca
        unknown_0x5f55ccca = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x81e8cf07
        unknown_0x81e8cf07 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2ac6123a
        unknown_0x2ac6123a = RevolutionControl.from_stream(data, property_size)
    
        return cls(unknown_0xb5f75bfb, unknown_0x2ced2b18, unknown_0x640f66c6, unknown_0xdfe791c6, unknown_0x55861a4b, unknown_0xebd3a5f8, unknown_0x385cbd2f, unknown_0x5f55ccca, unknown_0x81e8cf07, unknown_0x2ac6123a)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xb5\xf7[\xfb')  # 0xb5f75bfb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb5f75bfb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',\xed+\x18')  # 0x2ced2b18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x2ced2b18.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd\x0ff\xc6')  # 0x640f66c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x640f66c6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\xe7\x91\xc6')  # 0xdfe791c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xdfe791c6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U\x86\x1aK')  # 0x55861a4b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x55861a4b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xd3\xa5\xf8')  # 0xebd3a5f8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xebd3a5f8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'8\\\xbd/')  # 0x385cbd2f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x385cbd2f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_U\xcc\xca')  # 0x5f55ccca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x5f55ccca.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\xe8\xcf\x07')  # 0x81e8cf07
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x81e8cf07.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*\xc6\x12:')  # 0x2ac6123a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x2ac6123a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MapControlsJson", data)
        return cls(
            unknown_0xb5f75bfb=RevolutionControl.from_json(json_data['unknown_0xb5f75bfb']),
            unknown_0x2ced2b18=RevolutionControl.from_json(json_data['unknown_0x2ced2b18']),
            unknown_0x640f66c6=RevolutionControl.from_json(json_data['unknown_0x640f66c6']),
            unknown_0xdfe791c6=RevolutionControl.from_json(json_data['unknown_0xdfe791c6']),
            unknown_0x55861a4b=RevolutionControl.from_json(json_data['unknown_0x55861a4b']),
            unknown_0xebd3a5f8=RevolutionControl.from_json(json_data['unknown_0xebd3a5f8']),
            unknown_0x385cbd2f=RevolutionControl.from_json(json_data['unknown_0x385cbd2f']),
            unknown_0x5f55ccca=RevolutionControl.from_json(json_data['unknown_0x5f55ccca']),
            unknown_0x81e8cf07=RevolutionControl.from_json(json_data['unknown_0x81e8cf07']),
            unknown_0x2ac6123a=RevolutionControl.from_json(json_data['unknown_0x2ac6123a']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xb5f75bfb': self.unknown_0xb5f75bfb.to_json(),
            'unknown_0x2ced2b18': self.unknown_0x2ced2b18.to_json(),
            'unknown_0x640f66c6': self.unknown_0x640f66c6.to_json(),
            'unknown_0xdfe791c6': self.unknown_0xdfe791c6.to_json(),
            'unknown_0x55861a4b': self.unknown_0x55861a4b.to_json(),
            'unknown_0xebd3a5f8': self.unknown_0xebd3a5f8.to_json(),
            'unknown_0x385cbd2f': self.unknown_0x385cbd2f.to_json(),
            'unknown_0x5f55ccca': self.unknown_0x5f55ccca.to_json(),
            'unknown_0x81e8cf07': self.unknown_0x81e8cf07.to_json(),
            'unknown_0x2ac6123a': self.unknown_0x2ac6123a.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb5f75bfb: ('unknown_0xb5f75bfb', RevolutionControl.from_stream),
    0x2ced2b18: ('unknown_0x2ced2b18', RevolutionControl.from_stream),
    0x640f66c6: ('unknown_0x640f66c6', RevolutionControl.from_stream),
    0xdfe791c6: ('unknown_0xdfe791c6', RevolutionControl.from_stream),
    0x55861a4b: ('unknown_0x55861a4b', RevolutionControl.from_stream),
    0xebd3a5f8: ('unknown_0xebd3a5f8', RevolutionControl.from_stream),
    0x385cbd2f: ('unknown_0x385cbd2f', RevolutionControl.from_stream),
    0x5f55ccca: ('unknown_0x5f55ccca', RevolutionControl.from_stream),
    0x81e8cf07: ('unknown_0x81e8cf07', RevolutionControl.from_stream),
    0x2ac6123a: ('unknown_0x2ac6123a', RevolutionControl.from_stream),
}

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
    class TweakControls_UnknownStruct2Json(typing_extensions.TypedDict):
        unknown_0x1d9b5cc1: json_util.JsonObject
        unknown_0x56aaa727: json_util.JsonObject
        unknown_0xdccb2caa: json_util.JsonObject
        unknown_0x3c573a20: json_util.JsonObject
        jump: json_util.JsonObject
        unknown_0xc66160e6: json_util.JsonObject
        unknown_0xc6bc4b19: json_util.JsonObject
        unknown_0x79810b2b: json_util.JsonObject
        unknown_0xd6787ebe: json_util.JsonObject
        unknown_0x532087d5: json_util.JsonObject
        unknown_0x3ed13a6a: json_util.JsonObject
        unknown_0x7aa0b07c: json_util.JsonObject
        unknown_0x1c204629: json_util.JsonObject
        unknown_0x1996475f: json_util.JsonObject
    

@dataclasses.dataclass()
class TweakControls_UnknownStruct2(BaseProperty):
    unknown_0x1d9b5cc1: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x1d9b5cc1, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x56aaa727: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x56aaa727, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xdccb2caa: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xdccb2caa, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x3c573a20: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x3c573a20, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    jump: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x6b6fce63, original_name='Jump', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xc66160e6: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xc66160e6, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xc6bc4b19: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xc6bc4b19, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x79810b2b: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x79810b2b, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0xd6787ebe: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0xd6787ebe, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x532087d5: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x532087d5, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x3ed13a6a: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x3ed13a6a, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x7aa0b07c: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x7aa0b07c, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x1c204629: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x1c204629, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
        ),
    })
    unknown_0x1996475f: RevolutionControl = dataclasses.field(default_factory=RevolutionControl, metadata={
        'reflection': FieldReflection[RevolutionControl](
            RevolutionControl, id=0x1996475f, original_name='Unknown', from_json=RevolutionControl.from_json, to_json=RevolutionControl.to_json
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
        if property_count != 14:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1d9b5cc1
        unknown_0x1d9b5cc1 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x56aaa727
        unknown_0x56aaa727 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdccb2caa
        unknown_0xdccb2caa = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3c573a20
        unknown_0x3c573a20 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b6fce63
        jump = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc66160e6
        unknown_0xc66160e6 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc6bc4b19
        unknown_0xc6bc4b19 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x79810b2b
        unknown_0x79810b2b = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd6787ebe
        unknown_0xd6787ebe = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x532087d5
        unknown_0x532087d5 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3ed13a6a
        unknown_0x3ed13a6a = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7aa0b07c
        unknown_0x7aa0b07c = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1c204629
        unknown_0x1c204629 = RevolutionControl.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1996475f
        unknown_0x1996475f = RevolutionControl.from_stream(data, property_size)
    
        return cls(unknown_0x1d9b5cc1, unknown_0x56aaa727, unknown_0xdccb2caa, unknown_0x3c573a20, jump, unknown_0xc66160e6, unknown_0xc6bc4b19, unknown_0x79810b2b, unknown_0xd6787ebe, unknown_0x532087d5, unknown_0x3ed13a6a, unknown_0x7aa0b07c, unknown_0x1c204629, unknown_0x1996475f)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\x1d\x9b\\\xc1')  # 0x1d9b5cc1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1d9b5cc1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"V\xaa\xa7'")  # 0x56aaa727
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x56aaa727.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdc\xcb,\xaa')  # 0xdccb2caa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xdccb2caa.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<W: ')  # 0x3c573a20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3c573a20.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ko\xcec')  # 0x6b6fce63
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6a`\xe6')  # 0xc66160e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc66160e6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xbcK\x19')  # 0xc6bc4b19
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc6bc4b19.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x81\x0b+')  # 0x79810b2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x79810b2b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6x~\xbe')  # 0xd6787ebe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd6787ebe.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S \x87\xd5')  # 0x532087d5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x532087d5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\xd1:j')  # 0x3ed13a6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3ed13a6a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z\xa0\xb0|')  # 0x7aa0b07c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7aa0b07c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c F)')  # 0x1c204629
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1c204629.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\x96G_')  # 0x1996475f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1996475f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TweakControls_UnknownStruct2Json", data)
        return cls(
            unknown_0x1d9b5cc1=RevolutionControl.from_json(json_data['unknown_0x1d9b5cc1']),
            unknown_0x56aaa727=RevolutionControl.from_json(json_data['unknown_0x56aaa727']),
            unknown_0xdccb2caa=RevolutionControl.from_json(json_data['unknown_0xdccb2caa']),
            unknown_0x3c573a20=RevolutionControl.from_json(json_data['unknown_0x3c573a20']),
            jump=RevolutionControl.from_json(json_data['jump']),
            unknown_0xc66160e6=RevolutionControl.from_json(json_data['unknown_0xc66160e6']),
            unknown_0xc6bc4b19=RevolutionControl.from_json(json_data['unknown_0xc6bc4b19']),
            unknown_0x79810b2b=RevolutionControl.from_json(json_data['unknown_0x79810b2b']),
            unknown_0xd6787ebe=RevolutionControl.from_json(json_data['unknown_0xd6787ebe']),
            unknown_0x532087d5=RevolutionControl.from_json(json_data['unknown_0x532087d5']),
            unknown_0x3ed13a6a=RevolutionControl.from_json(json_data['unknown_0x3ed13a6a']),
            unknown_0x7aa0b07c=RevolutionControl.from_json(json_data['unknown_0x7aa0b07c']),
            unknown_0x1c204629=RevolutionControl.from_json(json_data['unknown_0x1c204629']),
            unknown_0x1996475f=RevolutionControl.from_json(json_data['unknown_0x1996475f']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x1d9b5cc1': self.unknown_0x1d9b5cc1.to_json(),
            'unknown_0x56aaa727': self.unknown_0x56aaa727.to_json(),
            'unknown_0xdccb2caa': self.unknown_0xdccb2caa.to_json(),
            'unknown_0x3c573a20': self.unknown_0x3c573a20.to_json(),
            'jump': self.jump.to_json(),
            'unknown_0xc66160e6': self.unknown_0xc66160e6.to_json(),
            'unknown_0xc6bc4b19': self.unknown_0xc6bc4b19.to_json(),
            'unknown_0x79810b2b': self.unknown_0x79810b2b.to_json(),
            'unknown_0xd6787ebe': self.unknown_0xd6787ebe.to_json(),
            'unknown_0x532087d5': self.unknown_0x532087d5.to_json(),
            'unknown_0x3ed13a6a': self.unknown_0x3ed13a6a.to_json(),
            'unknown_0x7aa0b07c': self.unknown_0x7aa0b07c.to_json(),
            'unknown_0x1c204629': self.unknown_0x1c204629.to_json(),
            'unknown_0x1996475f': self.unknown_0x1996475f.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1d9b5cc1: ('unknown_0x1d9b5cc1', RevolutionControl.from_stream),
    0x56aaa727: ('unknown_0x56aaa727', RevolutionControl.from_stream),
    0xdccb2caa: ('unknown_0xdccb2caa', RevolutionControl.from_stream),
    0x3c573a20: ('unknown_0x3c573a20', RevolutionControl.from_stream),
    0x6b6fce63: ('jump', RevolutionControl.from_stream),
    0xc66160e6: ('unknown_0xc66160e6', RevolutionControl.from_stream),
    0xc6bc4b19: ('unknown_0xc6bc4b19', RevolutionControl.from_stream),
    0x79810b2b: ('unknown_0x79810b2b', RevolutionControl.from_stream),
    0xd6787ebe: ('unknown_0xd6787ebe', RevolutionControl.from_stream),
    0x532087d5: ('unknown_0x532087d5', RevolutionControl.from_stream),
    0x3ed13a6a: ('unknown_0x3ed13a6a', RevolutionControl.from_stream),
    0x7aa0b07c: ('unknown_0x7aa0b07c', RevolutionControl.from_stream),
    0x1c204629: ('unknown_0x1c204629', RevolutionControl.from_stream),
    0x1996475f: ('unknown_0x1996475f', RevolutionControl.from_stream),
}

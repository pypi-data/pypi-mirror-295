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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct253 import UnknownStruct253
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct50 import UnknownStruct50

if typing.TYPE_CHECKING:
    class RobotChickenStructBJson(typing_extensions.TypedDict):
        attack_type: int
        unknown_0x968337ab: int
        unknown_0x8308e359: int
        unknown_struct253: json_util.JsonObject
        unknown_0x154a2c64: json_util.JsonObject
        unknown_struct50_0x634fddd1: json_util.JsonObject
        unknown_0xd1989e0d: json_util.JsonObject
        unknown_0x7887f42d: json_util.JsonObject
        unknown_0xb29207a6: json_util.JsonObject
        unknown_struct50_0xb4c4fd1c: json_util.JsonObject
        unknown_struct50_0xb61afa3b: json_util.JsonObject
        unknown_struct50_0xb7af0726: json_util.JsonObject
        unknown_struct50_0xb3a6f475: json_util.JsonObject
        unknown_struct50_0xb2130968: json_util.JsonObject
        unknown_struct50_0xb0cd0e4f: json_util.JsonObject
        unknown_struct50_0xb178f352: json_util.JsonObject
        unknown_struct50_0xb8dee8e9: json_util.JsonObject
        unknown_struct50_0xb96b15f4: json_util.JsonObject
        unknown_struct50_0xb7a4789f: json_util.JsonObject
        unknown_struct50_0x4508eb0e: json_util.JsonObject
        unknown_struct50_0x47d6ec29: json_util.JsonObject
        unknown_struct50_0x46631134: json_util.JsonObject
        unknown_struct50_0x426ae267: json_util.JsonObject
        unknown_struct50_0x43df1f7a: json_util.JsonObject
        unknown_struct50_0x4101185d: json_util.JsonObject
        unknown_struct50_0x40b4e540: json_util.JsonObject
        unknown_struct50_0x4912fefb: json_util.JsonObject
        unknown_struct50_0x48a703e6: json_util.JsonObject
        unknown_struct50_0x44ecc5c1: json_util.JsonObject
        unknown_struct50_0x468b1161: json_util.JsonObject
    

@dataclasses.dataclass()
class RobotChickenStructB(BaseProperty):
    attack_type: enums.AttackType = dataclasses.field(default=enums.AttackType.Unknown1, metadata={
        'reflection': FieldReflection[enums.AttackType](
            enums.AttackType, id=0x07d939a1, original_name='AttackType', from_json=enums.AttackType.from_json, to_json=enums.AttackType.to_json
        ),
    })
    unknown_0x968337ab: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x968337ab, original_name='Unknown'
        ),
    })
    unknown_0x8308e359: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8308e359, original_name='Unknown'
        ),
    })
    unknown_struct253: UnknownStruct253 = dataclasses.field(default_factory=UnknownStruct253, metadata={
        'reflection': FieldReflection[UnknownStruct253](
            UnknownStruct253, id=0xc69ccaad, original_name='UnknownStruct253', from_json=UnknownStruct253.from_json, to_json=UnknownStruct253.to_json
        ),
    })
    unknown_0x154a2c64: UnknownStruct253 = dataclasses.field(default_factory=UnknownStruct253, metadata={
        'reflection': FieldReflection[UnknownStruct253](
            UnknownStruct253, id=0x154a2c64, original_name='Unknown', from_json=UnknownStruct253.from_json, to_json=UnknownStruct253.to_json
        ),
    })
    unknown_struct50_0x634fddd1: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x634fddd1, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_0xd1989e0d: UnknownStruct253 = dataclasses.field(default_factory=UnknownStruct253, metadata={
        'reflection': FieldReflection[UnknownStruct253](
            UnknownStruct253, id=0xd1989e0d, original_name='Unknown', from_json=UnknownStruct253.from_json, to_json=UnknownStruct253.to_json
        ),
    })
    unknown_0x7887f42d: UnknownStruct253 = dataclasses.field(default_factory=UnknownStruct253, metadata={
        'reflection': FieldReflection[UnknownStruct253](
            UnknownStruct253, id=0x7887f42d, original_name='Unknown', from_json=UnknownStruct253.from_json, to_json=UnknownStruct253.to_json
        ),
    })
    unknown_0xb29207a6: UnknownStruct253 = dataclasses.field(default_factory=UnknownStruct253, metadata={
        'reflection': FieldReflection[UnknownStruct253](
            UnknownStruct253, id=0xb29207a6, original_name='Unknown', from_json=UnknownStruct253.from_json, to_json=UnknownStruct253.to_json
        ),
    })
    unknown_struct50_0xb4c4fd1c: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb4c4fd1c, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb61afa3b: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb61afa3b, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb7af0726: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb7af0726, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb3a6f475: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb3a6f475, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb2130968: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb2130968, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb0cd0e4f: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb0cd0e4f, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb178f352: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb178f352, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb8dee8e9: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb8dee8e9, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb96b15f4: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb96b15f4, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0xb7a4789f: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0xb7a4789f, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x4508eb0e: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x4508eb0e, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x47d6ec29: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x47d6ec29, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x46631134: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x46631134, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x426ae267: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x426ae267, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x43df1f7a: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x43df1f7a, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x4101185d: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x4101185d, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x40b4e540: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x40b4e540, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x4912fefb: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x4912fefb, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x48a703e6: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x48a703e6, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x44ecc5c1: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x44ecc5c1, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
        ),
    })
    unknown_struct50_0x468b1161: UnknownStruct50 = dataclasses.field(default_factory=UnknownStruct50, metadata={
        'reflection': FieldReflection[UnknownStruct50](
            UnknownStruct50, id=0x468b1161, original_name='UnknownStruct50', from_json=UnknownStruct50.from_json, to_json=UnknownStruct50.to_json
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
        if property_count != 30:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x07d939a1
        attack_type = enums.AttackType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x968337ab
        unknown_0x968337ab = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8308e359
        unknown_0x8308e359 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc69ccaad
        unknown_struct253 = UnknownStruct253.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x154a2c64
        unknown_0x154a2c64 = UnknownStruct253.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x634fddd1
        unknown_struct50_0x634fddd1 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1989e0d
        unknown_0xd1989e0d = UnknownStruct253.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7887f42d
        unknown_0x7887f42d = UnknownStruct253.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb29207a6
        unknown_0xb29207a6 = UnknownStruct253.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb4c4fd1c
        unknown_struct50_0xb4c4fd1c = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb61afa3b
        unknown_struct50_0xb61afa3b = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb7af0726
        unknown_struct50_0xb7af0726 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3a6f475
        unknown_struct50_0xb3a6f475 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb2130968
        unknown_struct50_0xb2130968 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0cd0e4f
        unknown_struct50_0xb0cd0e4f = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb178f352
        unknown_struct50_0xb178f352 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb8dee8e9
        unknown_struct50_0xb8dee8e9 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb96b15f4
        unknown_struct50_0xb96b15f4 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb7a4789f
        unknown_struct50_0xb7a4789f = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4508eb0e
        unknown_struct50_0x4508eb0e = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47d6ec29
        unknown_struct50_0x47d6ec29 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46631134
        unknown_struct50_0x46631134 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x426ae267
        unknown_struct50_0x426ae267 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43df1f7a
        unknown_struct50_0x43df1f7a = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4101185d
        unknown_struct50_0x4101185d = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x40b4e540
        unknown_struct50_0x40b4e540 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4912fefb
        unknown_struct50_0x4912fefb = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x48a703e6
        unknown_struct50_0x48a703e6 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x44ecc5c1
        unknown_struct50_0x44ecc5c1 = UnknownStruct50.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x468b1161
        unknown_struct50_0x468b1161 = UnknownStruct50.from_stream(data, property_size)
    
        return cls(attack_type, unknown_0x968337ab, unknown_0x8308e359, unknown_struct253, unknown_0x154a2c64, unknown_struct50_0x634fddd1, unknown_0xd1989e0d, unknown_0x7887f42d, unknown_0xb29207a6, unknown_struct50_0xb4c4fd1c, unknown_struct50_0xb61afa3b, unknown_struct50_0xb7af0726, unknown_struct50_0xb3a6f475, unknown_struct50_0xb2130968, unknown_struct50_0xb0cd0e4f, unknown_struct50_0xb178f352, unknown_struct50_0xb8dee8e9, unknown_struct50_0xb96b15f4, unknown_struct50_0xb7a4789f, unknown_struct50_0x4508eb0e, unknown_struct50_0x47d6ec29, unknown_struct50_0x46631134, unknown_struct50_0x426ae267, unknown_struct50_0x43df1f7a, unknown_struct50_0x4101185d, unknown_struct50_0x40b4e540, unknown_struct50_0x4912fefb, unknown_struct50_0x48a703e6, unknown_struct50_0x44ecc5c1, unknown_struct50_0x468b1161)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1e')  # 30 properties

        data.write(b'\x07\xd99\xa1')  # 0x7d939a1
        data.write(b'\x00\x04')  # size
        self.attack_type.to_stream(data)

        data.write(b'\x96\x837\xab')  # 0x968337ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x968337ab))

        data.write(b'\x83\x08\xe3Y')  # 0x8308e359
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8308e359))

        data.write(b'\xc6\x9c\xca\xad')  # 0xc69ccaad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct253.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15J,d')  # 0x154a2c64
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x154a2c64.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'cO\xdd\xd1')  # 0x634fddd1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x634fddd1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1\x98\x9e\r')  # 0xd1989e0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd1989e0d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\x87\xf4-')  # 0x7887f42d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7887f42d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\x92\x07\xa6')  # 0xb29207a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb29207a6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4\xc4\xfd\x1c')  # 0xb4c4fd1c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb4c4fd1c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\x1a\xfa;')  # 0xb61afa3b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb61afa3b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\xaf\x07&')  # 0xb7af0726
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb7af0726.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xa6\xf4u')  # 0xb3a6f475
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb3a6f475.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb2\x13\th')  # 0xb2130968
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb2130968.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xcd\x0eO')  # 0xb0cd0e4f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb0cd0e4f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb1x\xf3R')  # 0xb178f352
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb178f352.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8\xde\xe8\xe9')  # 0xb8dee8e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb8dee8e9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9k\x15\xf4')  # 0xb96b15f4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb96b15f4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\xa4x\x9f')  # 0xb7a4789f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0xb7a4789f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'E\x08\xeb\x0e')  # 0x4508eb0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x4508eb0e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\xd6\xec)')  # 0x47d6ec29
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x47d6ec29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Fc\x114')  # 0x46631134
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x46631134.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Bj\xe2g')  # 0x426ae267
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x426ae267.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xdf\x1fz')  # 0x43df1f7a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x43df1f7a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A\x01\x18]')  # 0x4101185d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x4101185d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@\xb4\xe5@')  # 0x40b4e540
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x40b4e540.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'I\x12\xfe\xfb')  # 0x4912fefb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x4912fefb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'H\xa7\x03\xe6')  # 0x48a703e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x48a703e6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D\xec\xc5\xc1')  # 0x44ecc5c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x44ecc5c1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\x8b\x11a')  # 0x468b1161
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct50_0x468b1161.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("RobotChickenStructBJson", data)
        return cls(
            attack_type=enums.AttackType.from_json(json_data['attack_type']),
            unknown_0x968337ab=json_data['unknown_0x968337ab'],
            unknown_0x8308e359=json_data['unknown_0x8308e359'],
            unknown_struct253=UnknownStruct253.from_json(json_data['unknown_struct253']),
            unknown_0x154a2c64=UnknownStruct253.from_json(json_data['unknown_0x154a2c64']),
            unknown_struct50_0x634fddd1=UnknownStruct50.from_json(json_data['unknown_struct50_0x634fddd1']),
            unknown_0xd1989e0d=UnknownStruct253.from_json(json_data['unknown_0xd1989e0d']),
            unknown_0x7887f42d=UnknownStruct253.from_json(json_data['unknown_0x7887f42d']),
            unknown_0xb29207a6=UnknownStruct253.from_json(json_data['unknown_0xb29207a6']),
            unknown_struct50_0xb4c4fd1c=UnknownStruct50.from_json(json_data['unknown_struct50_0xb4c4fd1c']),
            unknown_struct50_0xb61afa3b=UnknownStruct50.from_json(json_data['unknown_struct50_0xb61afa3b']),
            unknown_struct50_0xb7af0726=UnknownStruct50.from_json(json_data['unknown_struct50_0xb7af0726']),
            unknown_struct50_0xb3a6f475=UnknownStruct50.from_json(json_data['unknown_struct50_0xb3a6f475']),
            unknown_struct50_0xb2130968=UnknownStruct50.from_json(json_data['unknown_struct50_0xb2130968']),
            unknown_struct50_0xb0cd0e4f=UnknownStruct50.from_json(json_data['unknown_struct50_0xb0cd0e4f']),
            unknown_struct50_0xb178f352=UnknownStruct50.from_json(json_data['unknown_struct50_0xb178f352']),
            unknown_struct50_0xb8dee8e9=UnknownStruct50.from_json(json_data['unknown_struct50_0xb8dee8e9']),
            unknown_struct50_0xb96b15f4=UnknownStruct50.from_json(json_data['unknown_struct50_0xb96b15f4']),
            unknown_struct50_0xb7a4789f=UnknownStruct50.from_json(json_data['unknown_struct50_0xb7a4789f']),
            unknown_struct50_0x4508eb0e=UnknownStruct50.from_json(json_data['unknown_struct50_0x4508eb0e']),
            unknown_struct50_0x47d6ec29=UnknownStruct50.from_json(json_data['unknown_struct50_0x47d6ec29']),
            unknown_struct50_0x46631134=UnknownStruct50.from_json(json_data['unknown_struct50_0x46631134']),
            unknown_struct50_0x426ae267=UnknownStruct50.from_json(json_data['unknown_struct50_0x426ae267']),
            unknown_struct50_0x43df1f7a=UnknownStruct50.from_json(json_data['unknown_struct50_0x43df1f7a']),
            unknown_struct50_0x4101185d=UnknownStruct50.from_json(json_data['unknown_struct50_0x4101185d']),
            unknown_struct50_0x40b4e540=UnknownStruct50.from_json(json_data['unknown_struct50_0x40b4e540']),
            unknown_struct50_0x4912fefb=UnknownStruct50.from_json(json_data['unknown_struct50_0x4912fefb']),
            unknown_struct50_0x48a703e6=UnknownStruct50.from_json(json_data['unknown_struct50_0x48a703e6']),
            unknown_struct50_0x44ecc5c1=UnknownStruct50.from_json(json_data['unknown_struct50_0x44ecc5c1']),
            unknown_struct50_0x468b1161=UnknownStruct50.from_json(json_data['unknown_struct50_0x468b1161']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attack_type': self.attack_type.to_json(),
            'unknown_0x968337ab': self.unknown_0x968337ab,
            'unknown_0x8308e359': self.unknown_0x8308e359,
            'unknown_struct253': self.unknown_struct253.to_json(),
            'unknown_0x154a2c64': self.unknown_0x154a2c64.to_json(),
            'unknown_struct50_0x634fddd1': self.unknown_struct50_0x634fddd1.to_json(),
            'unknown_0xd1989e0d': self.unknown_0xd1989e0d.to_json(),
            'unknown_0x7887f42d': self.unknown_0x7887f42d.to_json(),
            'unknown_0xb29207a6': self.unknown_0xb29207a6.to_json(),
            'unknown_struct50_0xb4c4fd1c': self.unknown_struct50_0xb4c4fd1c.to_json(),
            'unknown_struct50_0xb61afa3b': self.unknown_struct50_0xb61afa3b.to_json(),
            'unknown_struct50_0xb7af0726': self.unknown_struct50_0xb7af0726.to_json(),
            'unknown_struct50_0xb3a6f475': self.unknown_struct50_0xb3a6f475.to_json(),
            'unknown_struct50_0xb2130968': self.unknown_struct50_0xb2130968.to_json(),
            'unknown_struct50_0xb0cd0e4f': self.unknown_struct50_0xb0cd0e4f.to_json(),
            'unknown_struct50_0xb178f352': self.unknown_struct50_0xb178f352.to_json(),
            'unknown_struct50_0xb8dee8e9': self.unknown_struct50_0xb8dee8e9.to_json(),
            'unknown_struct50_0xb96b15f4': self.unknown_struct50_0xb96b15f4.to_json(),
            'unknown_struct50_0xb7a4789f': self.unknown_struct50_0xb7a4789f.to_json(),
            'unknown_struct50_0x4508eb0e': self.unknown_struct50_0x4508eb0e.to_json(),
            'unknown_struct50_0x47d6ec29': self.unknown_struct50_0x47d6ec29.to_json(),
            'unknown_struct50_0x46631134': self.unknown_struct50_0x46631134.to_json(),
            'unknown_struct50_0x426ae267': self.unknown_struct50_0x426ae267.to_json(),
            'unknown_struct50_0x43df1f7a': self.unknown_struct50_0x43df1f7a.to_json(),
            'unknown_struct50_0x4101185d': self.unknown_struct50_0x4101185d.to_json(),
            'unknown_struct50_0x40b4e540': self.unknown_struct50_0x40b4e540.to_json(),
            'unknown_struct50_0x4912fefb': self.unknown_struct50_0x4912fefb.to_json(),
            'unknown_struct50_0x48a703e6': self.unknown_struct50_0x48a703e6.to_json(),
            'unknown_struct50_0x44ecc5c1': self.unknown_struct50_0x44ecc5c1.to_json(),
            'unknown_struct50_0x468b1161': self.unknown_struct50_0x468b1161.to_json(),
        }


def _decode_attack_type(data: typing.BinaryIO, property_size: int):
    return enums.AttackType.from_stream(data)


def _decode_unknown_0x968337ab(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8308e359(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7d939a1: ('attack_type', _decode_attack_type),
    0x968337ab: ('unknown_0x968337ab', _decode_unknown_0x968337ab),
    0x8308e359: ('unknown_0x8308e359', _decode_unknown_0x8308e359),
    0xc69ccaad: ('unknown_struct253', UnknownStruct253.from_stream),
    0x154a2c64: ('unknown_0x154a2c64', UnknownStruct253.from_stream),
    0x634fddd1: ('unknown_struct50_0x634fddd1', UnknownStruct50.from_stream),
    0xd1989e0d: ('unknown_0xd1989e0d', UnknownStruct253.from_stream),
    0x7887f42d: ('unknown_0x7887f42d', UnknownStruct253.from_stream),
    0xb29207a6: ('unknown_0xb29207a6', UnknownStruct253.from_stream),
    0xb4c4fd1c: ('unknown_struct50_0xb4c4fd1c', UnknownStruct50.from_stream),
    0xb61afa3b: ('unknown_struct50_0xb61afa3b', UnknownStruct50.from_stream),
    0xb7af0726: ('unknown_struct50_0xb7af0726', UnknownStruct50.from_stream),
    0xb3a6f475: ('unknown_struct50_0xb3a6f475', UnknownStruct50.from_stream),
    0xb2130968: ('unknown_struct50_0xb2130968', UnknownStruct50.from_stream),
    0xb0cd0e4f: ('unknown_struct50_0xb0cd0e4f', UnknownStruct50.from_stream),
    0xb178f352: ('unknown_struct50_0xb178f352', UnknownStruct50.from_stream),
    0xb8dee8e9: ('unknown_struct50_0xb8dee8e9', UnknownStruct50.from_stream),
    0xb96b15f4: ('unknown_struct50_0xb96b15f4', UnknownStruct50.from_stream),
    0xb7a4789f: ('unknown_struct50_0xb7a4789f', UnknownStruct50.from_stream),
    0x4508eb0e: ('unknown_struct50_0x4508eb0e', UnknownStruct50.from_stream),
    0x47d6ec29: ('unknown_struct50_0x47d6ec29', UnknownStruct50.from_stream),
    0x46631134: ('unknown_struct50_0x46631134', UnknownStruct50.from_stream),
    0x426ae267: ('unknown_struct50_0x426ae267', UnknownStruct50.from_stream),
    0x43df1f7a: ('unknown_struct50_0x43df1f7a', UnknownStruct50.from_stream),
    0x4101185d: ('unknown_struct50_0x4101185d', UnknownStruct50.from_stream),
    0x40b4e540: ('unknown_struct50_0x40b4e540', UnknownStruct50.from_stream),
    0x4912fefb: ('unknown_struct50_0x4912fefb', UnknownStruct50.from_stream),
    0x48a703e6: ('unknown_struct50_0x48a703e6', UnknownStruct50.from_stream),
    0x44ecc5c1: ('unknown_struct50_0x44ecc5c1', UnknownStruct50.from_stream),
    0x468b1161: ('unknown_struct50_0x468b1161', UnknownStruct50.from_stream),
}

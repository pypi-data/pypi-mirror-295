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
from retro_data_structures.properties.dkc_returns.archetypes.BirdBossStruct import BirdBossStruct
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct63 import UnknownStruct63
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct64 import UnknownStruct64
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters

if typing.TYPE_CHECKING:
    class BirdBossDataJson(typing_extensions.TypedDict):
        snap_to_spline: bool
        floor_height: float
        gravity: float
        unknown_0x9ab09e44: float
        maximum_twist_speed: float
        unknown_0xa9a4e87c: str
        unknown_0x61348354: float
        unknown_0x4eebc0c9: float
        unknown_0xeb300034: float
        unknown_0x65a1308e: float
        unknown_0x03554c19: float
        unknown_0x62ca94f2: float
        unknown_0xe33f5cd6: float
        unknown_0xd486f8fe: float
        unknown_0x3a18c538: float
        unknown_0xd9080460: float
        unknown_0xae96d690: float
        unknown_0xa8935c73: json_util.JsonObject
        unknown_0x91ebf133: json_util.JsonObject
        unknown_struct63: json_util.JsonObject
        unknown_struct64: json_util.JsonObject
        bird_boss_struct_0x3e67cc4a: json_util.JsonObject
        bird_boss_struct_0xd4e11128: json_util.JsonObject
        bird_boss_struct_0x3bb3a7c9: json_util.JsonObject
        bird_boss_struct_0xda9dadad: json_util.JsonObject
    

@dataclasses.dataclass()
class BirdBossData(BaseProperty):
    snap_to_spline: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x26ecb939, original_name='SnapToSpline'
        ),
    })
    floor_height: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x041da172, original_name='FloorHeight'
        ),
    })
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    unknown_0x9ab09e44: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9ab09e44, original_name='Unknown'
        ),
    })
    maximum_twist_speed: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa0efda8e, original_name='MaximumTwistSpeed'
        ),
    })
    unknown_0xa9a4e87c: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xa9a4e87c, original_name='Unknown'
        ),
    })
    unknown_0x61348354: float = dataclasses.field(default=7.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x61348354, original_name='Unknown'
        ),
    })
    unknown_0x4eebc0c9: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4eebc0c9, original_name='Unknown'
        ),
    })
    unknown_0xeb300034: float = dataclasses.field(default=14.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xeb300034, original_name='Unknown'
        ),
    })
    unknown_0x65a1308e: float = dataclasses.field(default=17.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x65a1308e, original_name='Unknown'
        ),
    })
    unknown_0x03554c19: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x03554c19, original_name='Unknown'
        ),
    })
    unknown_0x62ca94f2: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x62ca94f2, original_name='Unknown'
        ),
    })
    unknown_0xe33f5cd6: float = dataclasses.field(default=-5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe33f5cd6, original_name='Unknown'
        ),
    })
    unknown_0xd486f8fe: float = dataclasses.field(default=-20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd486f8fe, original_name='Unknown'
        ),
    })
    unknown_0x3a18c538: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3a18c538, original_name='Unknown'
        ),
    })
    unknown_0xd9080460: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd9080460, original_name='Unknown'
        ),
    })
    unknown_0xae96d690: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xae96d690, original_name='Unknown'
        ),
    })
    unknown_0xa8935c73: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa8935c73, original_name='Unknown', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    unknown_0x91ebf133: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x91ebf133, original_name='Unknown', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    unknown_struct63: UnknownStruct63 = dataclasses.field(default_factory=UnknownStruct63, metadata={
        'reflection': FieldReflection[UnknownStruct63](
            UnknownStruct63, id=0xf03eb95e, original_name='UnknownStruct63', from_json=UnknownStruct63.from_json, to_json=UnknownStruct63.to_json
        ),
    })
    unknown_struct64: UnknownStruct64 = dataclasses.field(default_factory=UnknownStruct64, metadata={
        'reflection': FieldReflection[UnknownStruct64](
            UnknownStruct64, id=0x5b1c94d1, original_name='UnknownStruct64', from_json=UnknownStruct64.from_json, to_json=UnknownStruct64.to_json
        ),
    })
    bird_boss_struct_0x3e67cc4a: BirdBossStruct = dataclasses.field(default_factory=BirdBossStruct, metadata={
        'reflection': FieldReflection[BirdBossStruct](
            BirdBossStruct, id=0x3e67cc4a, original_name='BirdBossStruct', from_json=BirdBossStruct.from_json, to_json=BirdBossStruct.to_json
        ),
    })
    bird_boss_struct_0xd4e11128: BirdBossStruct = dataclasses.field(default_factory=BirdBossStruct, metadata={
        'reflection': FieldReflection[BirdBossStruct](
            BirdBossStruct, id=0xd4e11128, original_name='BirdBossStruct', from_json=BirdBossStruct.from_json, to_json=BirdBossStruct.to_json
        ),
    })
    bird_boss_struct_0x3bb3a7c9: BirdBossStruct = dataclasses.field(default_factory=BirdBossStruct, metadata={
        'reflection': FieldReflection[BirdBossStruct](
            BirdBossStruct, id=0x3bb3a7c9, original_name='BirdBossStruct', from_json=BirdBossStruct.from_json, to_json=BirdBossStruct.to_json
        ),
    })
    bird_boss_struct_0xda9dadad: BirdBossStruct = dataclasses.field(default_factory=BirdBossStruct, metadata={
        'reflection': FieldReflection[BirdBossStruct](
            BirdBossStruct, id=0xda9dadad, original_name='BirdBossStruct', from_json=BirdBossStruct.from_json, to_json=BirdBossStruct.to_json
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
        if property_count != 25:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26ecb939
        snap_to_spline = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x041da172
        floor_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ab09e44
        unknown_0x9ab09e44 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa0efda8e
        maximum_twist_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa9a4e87c
        unknown_0xa9a4e87c = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x61348354
        unknown_0x61348354 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4eebc0c9
        unknown_0x4eebc0c9 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb300034
        unknown_0xeb300034 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x65a1308e
        unknown_0x65a1308e = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x03554c19
        unknown_0x03554c19 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x62ca94f2
        unknown_0x62ca94f2 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe33f5cd6
        unknown_0xe33f5cd6 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd486f8fe
        unknown_0xd486f8fe = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a18c538
        unknown_0x3a18c538 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9080460
        unknown_0xd9080460 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xae96d690
        unknown_0xae96d690 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa8935c73
        unknown_0xa8935c73 = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x91ebf133
        unknown_0x91ebf133 = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf03eb95e
        unknown_struct63 = UnknownStruct63.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5b1c94d1
        unknown_struct64 = UnknownStruct64.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3e67cc4a
        bird_boss_struct_0x3e67cc4a = BirdBossStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd4e11128
        bird_boss_struct_0xd4e11128 = BirdBossStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3bb3a7c9
        bird_boss_struct_0x3bb3a7c9 = BirdBossStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xda9dadad
        bird_boss_struct_0xda9dadad = BirdBossStruct.from_stream(data, property_size)
    
        return cls(snap_to_spline, floor_height, gravity, unknown_0x9ab09e44, maximum_twist_speed, unknown_0xa9a4e87c, unknown_0x61348354, unknown_0x4eebc0c9, unknown_0xeb300034, unknown_0x65a1308e, unknown_0x03554c19, unknown_0x62ca94f2, unknown_0xe33f5cd6, unknown_0xd486f8fe, unknown_0x3a18c538, unknown_0xd9080460, unknown_0xae96d690, unknown_0xa8935c73, unknown_0x91ebf133, unknown_struct63, unknown_struct64, bird_boss_struct_0x3e67cc4a, bird_boss_struct_0xd4e11128, bird_boss_struct_0x3bb3a7c9, bird_boss_struct_0xda9dadad)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'\x04\x1d\xa1r')  # 0x41da172
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_height))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\x9a\xb0\x9eD')  # 0x9ab09e44
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9ab09e44))

        data.write(b'\xa0\xef\xda\x8e')  # 0xa0efda8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_twist_speed))

        data.write(b'\xa9\xa4\xe8|')  # 0xa9a4e87c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xa9a4e87c.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a4\x83T')  # 0x61348354
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61348354))

        data.write(b'N\xeb\xc0\xc9')  # 0x4eebc0c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4eebc0c9))

        data.write(b'\xeb0\x004')  # 0xeb300034
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xeb300034))

        data.write(b'e\xa10\x8e')  # 0x65a1308e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x65a1308e))

        data.write(b'\x03UL\x19')  # 0x3554c19
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x03554c19))

        data.write(b'b\xca\x94\xf2')  # 0x62ca94f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x62ca94f2))

        data.write(b'\xe3?\\\xd6')  # 0xe33f5cd6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe33f5cd6))

        data.write(b'\xd4\x86\xf8\xfe')  # 0xd486f8fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd486f8fe))

        data.write(b':\x18\xc58')  # 0x3a18c538
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3a18c538))

        data.write(b'\xd9\x08\x04`')  # 0xd9080460
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd9080460))

        data.write(b'\xae\x96\xd6\x90')  # 0xae96d690
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xae96d690))

        data.write(b'\xa8\x93\\s')  # 0xa8935c73
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa8935c73.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91\xeb\xf13')  # 0x91ebf133
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x91ebf133.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0>\xb9^')  # 0xf03eb95e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct63.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[\x1c\x94\xd1')  # 0x5b1c94d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct64.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>g\xccJ')  # 0x3e67cc4a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bird_boss_struct_0x3e67cc4a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd4\xe1\x11(')  # 0xd4e11128
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bird_boss_struct_0xd4e11128.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';\xb3\xa7\xc9')  # 0x3bb3a7c9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bird_boss_struct_0x3bb3a7c9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda\x9d\xad\xad')  # 0xda9dadad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bird_boss_struct_0xda9dadad.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BirdBossDataJson", data)
        return cls(
            snap_to_spline=json_data['snap_to_spline'],
            floor_height=json_data['floor_height'],
            gravity=json_data['gravity'],
            unknown_0x9ab09e44=json_data['unknown_0x9ab09e44'],
            maximum_twist_speed=json_data['maximum_twist_speed'],
            unknown_0xa9a4e87c=json_data['unknown_0xa9a4e87c'],
            unknown_0x61348354=json_data['unknown_0x61348354'],
            unknown_0x4eebc0c9=json_data['unknown_0x4eebc0c9'],
            unknown_0xeb300034=json_data['unknown_0xeb300034'],
            unknown_0x65a1308e=json_data['unknown_0x65a1308e'],
            unknown_0x03554c19=json_data['unknown_0x03554c19'],
            unknown_0x62ca94f2=json_data['unknown_0x62ca94f2'],
            unknown_0xe33f5cd6=json_data['unknown_0xe33f5cd6'],
            unknown_0xd486f8fe=json_data['unknown_0xd486f8fe'],
            unknown_0x3a18c538=json_data['unknown_0x3a18c538'],
            unknown_0xd9080460=json_data['unknown_0xd9080460'],
            unknown_0xae96d690=json_data['unknown_0xae96d690'],
            unknown_0xa8935c73=AnimationParameters.from_json(json_data['unknown_0xa8935c73']),
            unknown_0x91ebf133=AnimationParameters.from_json(json_data['unknown_0x91ebf133']),
            unknown_struct63=UnknownStruct63.from_json(json_data['unknown_struct63']),
            unknown_struct64=UnknownStruct64.from_json(json_data['unknown_struct64']),
            bird_boss_struct_0x3e67cc4a=BirdBossStruct.from_json(json_data['bird_boss_struct_0x3e67cc4a']),
            bird_boss_struct_0xd4e11128=BirdBossStruct.from_json(json_data['bird_boss_struct_0xd4e11128']),
            bird_boss_struct_0x3bb3a7c9=BirdBossStruct.from_json(json_data['bird_boss_struct_0x3bb3a7c9']),
            bird_boss_struct_0xda9dadad=BirdBossStruct.from_json(json_data['bird_boss_struct_0xda9dadad']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'snap_to_spline': self.snap_to_spline,
            'floor_height': self.floor_height,
            'gravity': self.gravity,
            'unknown_0x9ab09e44': self.unknown_0x9ab09e44,
            'maximum_twist_speed': self.maximum_twist_speed,
            'unknown_0xa9a4e87c': self.unknown_0xa9a4e87c,
            'unknown_0x61348354': self.unknown_0x61348354,
            'unknown_0x4eebc0c9': self.unknown_0x4eebc0c9,
            'unknown_0xeb300034': self.unknown_0xeb300034,
            'unknown_0x65a1308e': self.unknown_0x65a1308e,
            'unknown_0x03554c19': self.unknown_0x03554c19,
            'unknown_0x62ca94f2': self.unknown_0x62ca94f2,
            'unknown_0xe33f5cd6': self.unknown_0xe33f5cd6,
            'unknown_0xd486f8fe': self.unknown_0xd486f8fe,
            'unknown_0x3a18c538': self.unknown_0x3a18c538,
            'unknown_0xd9080460': self.unknown_0xd9080460,
            'unknown_0xae96d690': self.unknown_0xae96d690,
            'unknown_0xa8935c73': self.unknown_0xa8935c73.to_json(),
            'unknown_0x91ebf133': self.unknown_0x91ebf133.to_json(),
            'unknown_struct63': self.unknown_struct63.to_json(),
            'unknown_struct64': self.unknown_struct64.to_json(),
            'bird_boss_struct_0x3e67cc4a': self.bird_boss_struct_0x3e67cc4a.to_json(),
            'bird_boss_struct_0xd4e11128': self.bird_boss_struct_0xd4e11128.to_json(),
            'bird_boss_struct_0x3bb3a7c9': self.bird_boss_struct_0x3bb3a7c9.to_json(),
            'bird_boss_struct_0xda9dadad': self.bird_boss_struct_0xda9dadad.to_json(),
        }


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_floor_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9ab09e44(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_twist_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa9a4e87c(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown_0x61348354(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4eebc0c9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xeb300034(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x65a1308e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x03554c19(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x62ca94f2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe33f5cd6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd486f8fe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3a18c538(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd9080460(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xae96d690(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0x41da172: ('floor_height', _decode_floor_height),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x9ab09e44: ('unknown_0x9ab09e44', _decode_unknown_0x9ab09e44),
    0xa0efda8e: ('maximum_twist_speed', _decode_maximum_twist_speed),
    0xa9a4e87c: ('unknown_0xa9a4e87c', _decode_unknown_0xa9a4e87c),
    0x61348354: ('unknown_0x61348354', _decode_unknown_0x61348354),
    0x4eebc0c9: ('unknown_0x4eebc0c9', _decode_unknown_0x4eebc0c9),
    0xeb300034: ('unknown_0xeb300034', _decode_unknown_0xeb300034),
    0x65a1308e: ('unknown_0x65a1308e', _decode_unknown_0x65a1308e),
    0x3554c19: ('unknown_0x03554c19', _decode_unknown_0x03554c19),
    0x62ca94f2: ('unknown_0x62ca94f2', _decode_unknown_0x62ca94f2),
    0xe33f5cd6: ('unknown_0xe33f5cd6', _decode_unknown_0xe33f5cd6),
    0xd486f8fe: ('unknown_0xd486f8fe', _decode_unknown_0xd486f8fe),
    0x3a18c538: ('unknown_0x3a18c538', _decode_unknown_0x3a18c538),
    0xd9080460: ('unknown_0xd9080460', _decode_unknown_0xd9080460),
    0xae96d690: ('unknown_0xae96d690', _decode_unknown_0xae96d690),
    0xa8935c73: ('unknown_0xa8935c73', AnimationParameters.from_stream),
    0x91ebf133: ('unknown_0x91ebf133', AnimationParameters.from_stream),
    0xf03eb95e: ('unknown_struct63', UnknownStruct63.from_stream),
    0x5b1c94d1: ('unknown_struct64', UnknownStruct64.from_stream),
    0x3e67cc4a: ('bird_boss_struct_0x3e67cc4a', BirdBossStruct.from_stream),
    0xd4e11128: ('bird_boss_struct_0xd4e11128', BirdBossStruct.from_stream),
    0x3bb3a7c9: ('bird_boss_struct_0x3bb3a7c9', BirdBossStruct.from_stream),
    0xda9dadad: ('bird_boss_struct_0xda9dadad', BirdBossStruct.from_stream),
}

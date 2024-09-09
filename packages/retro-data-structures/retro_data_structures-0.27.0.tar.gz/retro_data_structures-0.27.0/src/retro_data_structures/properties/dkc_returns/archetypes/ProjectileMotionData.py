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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct196 import UnknownStruct196
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct197 import UnknownStruct197
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct198 import UnknownStruct198
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct199 import UnknownStruct199
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct200 import UnknownStruct200
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct201 import UnknownStruct201

if typing.TYPE_CHECKING:
    class ProjectileMotionDataJson(typing_extensions.TypedDict):
        motion_type: int
        unknown_struct196: json_util.JsonObject
        unknown_struct197: json_util.JsonObject
        unknown_struct198: json_util.JsonObject
        unknown_struct199: json_util.JsonObject
        unknown_struct200: json_util.JsonObject
        unknown_struct201: json_util.JsonObject
    

@dataclasses.dataclass()
class ProjectileMotionData(BaseProperty):
    motion_type: enums.MotionType = dataclasses.field(default=enums.MotionType.Unknown5, metadata={
        'reflection': FieldReflection[enums.MotionType](
            enums.MotionType, id=0x948af571, original_name='MotionType', from_json=enums.MotionType.from_json, to_json=enums.MotionType.to_json
        ),
    })
    unknown_struct196: UnknownStruct196 = dataclasses.field(default_factory=UnknownStruct196, metadata={
        'reflection': FieldReflection[UnknownStruct196](
            UnknownStruct196, id=0xd15df9a6, original_name='UnknownStruct196', from_json=UnknownStruct196.from_json, to_json=UnknownStruct196.to_json
        ),
    })
    unknown_struct197: UnknownStruct197 = dataclasses.field(default_factory=UnknownStruct197, metadata={
        'reflection': FieldReflection[UnknownStruct197](
            UnknownStruct197, id=0xa3a58c06, original_name='UnknownStruct197', from_json=UnknownStruct197.from_json, to_json=UnknownStruct197.to_json
        ),
    })
    unknown_struct198: UnknownStruct198 = dataclasses.field(default_factory=UnknownStruct198, metadata={
        'reflection': FieldReflection[UnknownStruct198](
            UnknownStruct198, id=0x59c61e48, original_name='UnknownStruct198', from_json=UnknownStruct198.from_json, to_json=UnknownStruct198.to_json
        ),
    })
    unknown_struct199: UnknownStruct199 = dataclasses.field(default_factory=UnknownStruct199, metadata={
        'reflection': FieldReflection[UnknownStruct199](
            UnknownStruct199, id=0x8698751f, original_name='UnknownStruct199', from_json=UnknownStruct199.from_json, to_json=UnknownStruct199.to_json
        ),
    })
    unknown_struct200: UnknownStruct200 = dataclasses.field(default_factory=UnknownStruct200, metadata={
        'reflection': FieldReflection[UnknownStruct200](
            UnknownStruct200, id=0xfe9257ce, original_name='UnknownStruct200', from_json=UnknownStruct200.from_json, to_json=UnknownStruct200.to_json
        ),
    })
    unknown_struct201: UnknownStruct201 = dataclasses.field(default_factory=UnknownStruct201, metadata={
        'reflection': FieldReflection[UnknownStruct201](
            UnknownStruct201, id=0x608e1757, original_name='UnknownStruct201', from_json=UnknownStruct201.from_json, to_json=UnknownStruct201.to_json
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
        if property_count != 7:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x948af571
        motion_type = enums.MotionType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd15df9a6
        unknown_struct196 = UnknownStruct196.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa3a58c06
        unknown_struct197 = UnknownStruct197.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59c61e48
        unknown_struct198 = UnknownStruct198.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8698751f
        unknown_struct199 = UnknownStruct199.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe9257ce
        unknown_struct200 = UnknownStruct200.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x608e1757
        unknown_struct201 = UnknownStruct201.from_stream(data, property_size)
    
        return cls(motion_type, unknown_struct196, unknown_struct197, unknown_struct198, unknown_struct199, unknown_struct200, unknown_struct201)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x94\x8a\xf5q')  # 0x948af571
        data.write(b'\x00\x04')  # size
        self.motion_type.to_stream(data)

        data.write(b'\xd1]\xf9\xa6')  # 0xd15df9a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct196.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\xa5\x8c\x06')  # 0xa3a58c06
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct197.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\xc6\x1eH')  # 0x59c61e48
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct198.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\x98u\x1f')  # 0x8698751f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct199.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfe\x92W\xce')  # 0xfe9257ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct200.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'`\x8e\x17W')  # 0x608e1757
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct201.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ProjectileMotionDataJson", data)
        return cls(
            motion_type=enums.MotionType.from_json(json_data['motion_type']),
            unknown_struct196=UnknownStruct196.from_json(json_data['unknown_struct196']),
            unknown_struct197=UnknownStruct197.from_json(json_data['unknown_struct197']),
            unknown_struct198=UnknownStruct198.from_json(json_data['unknown_struct198']),
            unknown_struct199=UnknownStruct199.from_json(json_data['unknown_struct199']),
            unknown_struct200=UnknownStruct200.from_json(json_data['unknown_struct200']),
            unknown_struct201=UnknownStruct201.from_json(json_data['unknown_struct201']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'motion_type': self.motion_type.to_json(),
            'unknown_struct196': self.unknown_struct196.to_json(),
            'unknown_struct197': self.unknown_struct197.to_json(),
            'unknown_struct198': self.unknown_struct198.to_json(),
            'unknown_struct199': self.unknown_struct199.to_json(),
            'unknown_struct200': self.unknown_struct200.to_json(),
            'unknown_struct201': self.unknown_struct201.to_json(),
        }


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return enums.MotionType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x948af571: ('motion_type', _decode_motion_type),
    0xd15df9a6: ('unknown_struct196', UnknownStruct196.from_stream),
    0xa3a58c06: ('unknown_struct197', UnknownStruct197.from_stream),
    0x59c61e48: ('unknown_struct198', UnknownStruct198.from_stream),
    0x8698751f: ('unknown_struct199', UnknownStruct199.from_stream),
    0xfe9257ce: ('unknown_struct200', UnknownStruct200.from_stream),
    0x608e1757: ('unknown_struct201', UnknownStruct201.from_stream),
}

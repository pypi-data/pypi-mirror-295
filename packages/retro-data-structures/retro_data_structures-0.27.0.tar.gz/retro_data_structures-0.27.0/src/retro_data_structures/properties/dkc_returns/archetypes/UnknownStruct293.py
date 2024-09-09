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
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructD import VolcanoBossBodyPartStructD

if typing.TYPE_CHECKING:
    class UnknownStruct293Json(typing_extensions.TypedDict):
        unknown: int
        volcano_boss_body_part_struct_d_0x4266606e: json_util.JsonObject
        volcano_boss_body_part_struct_d_0x06c74576: json_util.JsonObject
        volcano_boss_body_part_struct_d_0x3aa7a67e: json_util.JsonObject
        volcano_boss_body_part_struct_d_0x8f850f46: json_util.JsonObject
        volcano_boss_body_part_struct_d_0xb3e5ec4e: json_util.JsonObject
        volcano_boss_body_part_struct_d_0xf744c956: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct293(BaseProperty):
    unknown: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x06efdab2, original_name='Unknown'
        ),
    })
    volcano_boss_body_part_struct_d_0x4266606e: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructD](
            VolcanoBossBodyPartStructD, id=0x4266606e, original_name='VolcanoBossBodyPartStructD', from_json=VolcanoBossBodyPartStructD.from_json, to_json=VolcanoBossBodyPartStructD.to_json
        ),
    })
    volcano_boss_body_part_struct_d_0x06c74576: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructD](
            VolcanoBossBodyPartStructD, id=0x06c74576, original_name='VolcanoBossBodyPartStructD', from_json=VolcanoBossBodyPartStructD.from_json, to_json=VolcanoBossBodyPartStructD.to_json
        ),
    })
    volcano_boss_body_part_struct_d_0x3aa7a67e: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructD](
            VolcanoBossBodyPartStructD, id=0x3aa7a67e, original_name='VolcanoBossBodyPartStructD', from_json=VolcanoBossBodyPartStructD.from_json, to_json=VolcanoBossBodyPartStructD.to_json
        ),
    })
    volcano_boss_body_part_struct_d_0x8f850f46: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructD](
            VolcanoBossBodyPartStructD, id=0x8f850f46, original_name='VolcanoBossBodyPartStructD', from_json=VolcanoBossBodyPartStructD.from_json, to_json=VolcanoBossBodyPartStructD.to_json
        ),
    })
    volcano_boss_body_part_struct_d_0xb3e5ec4e: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructD](
            VolcanoBossBodyPartStructD, id=0xb3e5ec4e, original_name='VolcanoBossBodyPartStructD', from_json=VolcanoBossBodyPartStructD.from_json, to_json=VolcanoBossBodyPartStructD.to_json
        ),
    })
    volcano_boss_body_part_struct_d_0xf744c956: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructD](
            VolcanoBossBodyPartStructD, id=0xf744c956, original_name='VolcanoBossBodyPartStructD', from_json=VolcanoBossBodyPartStructD.from_json, to_json=VolcanoBossBodyPartStructD.to_json
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
        assert property_id == 0x06efdab2
        unknown = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4266606e
        volcano_boss_body_part_struct_d_0x4266606e = VolcanoBossBodyPartStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x06c74576
        volcano_boss_body_part_struct_d_0x06c74576 = VolcanoBossBodyPartStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3aa7a67e
        volcano_boss_body_part_struct_d_0x3aa7a67e = VolcanoBossBodyPartStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f850f46
        volcano_boss_body_part_struct_d_0x8f850f46 = VolcanoBossBodyPartStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3e5ec4e
        volcano_boss_body_part_struct_d_0xb3e5ec4e = VolcanoBossBodyPartStructD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf744c956
        volcano_boss_body_part_struct_d_0xf744c956 = VolcanoBossBodyPartStructD.from_stream(data, property_size)
    
        return cls(unknown, volcano_boss_body_part_struct_d_0x4266606e, volcano_boss_body_part_struct_d_0x06c74576, volcano_boss_body_part_struct_d_0x3aa7a67e, volcano_boss_body_part_struct_d_0x8f850f46, volcano_boss_body_part_struct_d_0xb3e5ec4e, volcano_boss_body_part_struct_d_0xf744c956)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x06\xef\xda\xb2')  # 0x6efdab2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'Bf`n')  # 0x4266606e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x4266606e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06\xc7Ev')  # 0x6c74576
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x06c74576.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':\xa7\xa6~')  # 0x3aa7a67e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x3aa7a67e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8f\x85\x0fF')  # 0x8f850f46
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x8f850f46.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xe5\xecN')  # 0xb3e5ec4e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0xb3e5ec4e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7D\xc9V')  # 0xf744c956
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0xf744c956.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct293Json", data)
        return cls(
            unknown=json_data['unknown'],
            volcano_boss_body_part_struct_d_0x4266606e=VolcanoBossBodyPartStructD.from_json(json_data['volcano_boss_body_part_struct_d_0x4266606e']),
            volcano_boss_body_part_struct_d_0x06c74576=VolcanoBossBodyPartStructD.from_json(json_data['volcano_boss_body_part_struct_d_0x06c74576']),
            volcano_boss_body_part_struct_d_0x3aa7a67e=VolcanoBossBodyPartStructD.from_json(json_data['volcano_boss_body_part_struct_d_0x3aa7a67e']),
            volcano_boss_body_part_struct_d_0x8f850f46=VolcanoBossBodyPartStructD.from_json(json_data['volcano_boss_body_part_struct_d_0x8f850f46']),
            volcano_boss_body_part_struct_d_0xb3e5ec4e=VolcanoBossBodyPartStructD.from_json(json_data['volcano_boss_body_part_struct_d_0xb3e5ec4e']),
            volcano_boss_body_part_struct_d_0xf744c956=VolcanoBossBodyPartStructD.from_json(json_data['volcano_boss_body_part_struct_d_0xf744c956']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'volcano_boss_body_part_struct_d_0x4266606e': self.volcano_boss_body_part_struct_d_0x4266606e.to_json(),
            'volcano_boss_body_part_struct_d_0x06c74576': self.volcano_boss_body_part_struct_d_0x06c74576.to_json(),
            'volcano_boss_body_part_struct_d_0x3aa7a67e': self.volcano_boss_body_part_struct_d_0x3aa7a67e.to_json(),
            'volcano_boss_body_part_struct_d_0x8f850f46': self.volcano_boss_body_part_struct_d_0x8f850f46.to_json(),
            'volcano_boss_body_part_struct_d_0xb3e5ec4e': self.volcano_boss_body_part_struct_d_0xb3e5ec4e.to_json(),
            'volcano_boss_body_part_struct_d_0xf744c956': self.volcano_boss_body_part_struct_d_0xf744c956.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6efdab2: ('unknown', _decode_unknown),
    0x4266606e: ('volcano_boss_body_part_struct_d_0x4266606e', VolcanoBossBodyPartStructD.from_stream),
    0x6c74576: ('volcano_boss_body_part_struct_d_0x06c74576', VolcanoBossBodyPartStructD.from_stream),
    0x3aa7a67e: ('volcano_boss_body_part_struct_d_0x3aa7a67e', VolcanoBossBodyPartStructD.from_stream),
    0x8f850f46: ('volcano_boss_body_part_struct_d_0x8f850f46', VolcanoBossBodyPartStructD.from_stream),
    0xb3e5ec4e: ('volcano_boss_body_part_struct_d_0xb3e5ec4e', VolcanoBossBodyPartStructD.from_stream),
    0xf744c956: ('volcano_boss_body_part_struct_d_0xf744c956', VolcanoBossBodyPartStructD.from_stream),
}

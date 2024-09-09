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
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructC import VolcanoBossBodyPartStructC

if typing.TYPE_CHECKING:
    class UnknownStruct294Json(typing_extensions.TypedDict):
        volcano_boss_body_part_struct_c_0x92807f97: json_util.JsonObject
        volcano_boss_body_part_struct_c_0x7663abf3: json_util.JsonObject
        volcano_boss_body_part_struct_c_0x8a4c3f96: json_util.JsonObject
        volcano_boss_body_part_struct_c_0x70d8cac0: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct294(BaseProperty):
    volcano_boss_body_part_struct_c_0x92807f97: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructC](
            VolcanoBossBodyPartStructC, id=0x92807f97, original_name='VolcanoBossBodyPartStructC', from_json=VolcanoBossBodyPartStructC.from_json, to_json=VolcanoBossBodyPartStructC.to_json
        ),
    })
    volcano_boss_body_part_struct_c_0x7663abf3: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructC](
            VolcanoBossBodyPartStructC, id=0x7663abf3, original_name='VolcanoBossBodyPartStructC', from_json=VolcanoBossBodyPartStructC.from_json, to_json=VolcanoBossBodyPartStructC.to_json
        ),
    })
    volcano_boss_body_part_struct_c_0x8a4c3f96: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructC](
            VolcanoBossBodyPartStructC, id=0x8a4c3f96, original_name='VolcanoBossBodyPartStructC', from_json=VolcanoBossBodyPartStructC.from_json, to_json=VolcanoBossBodyPartStructC.to_json
        ),
    })
    volcano_boss_body_part_struct_c_0x70d8cac0: VolcanoBossBodyPartStructC = dataclasses.field(default_factory=VolcanoBossBodyPartStructC, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructC](
            VolcanoBossBodyPartStructC, id=0x70d8cac0, original_name='VolcanoBossBodyPartStructC', from_json=VolcanoBossBodyPartStructC.from_json, to_json=VolcanoBossBodyPartStructC.to_json
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
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x92807f97
        volcano_boss_body_part_struct_c_0x92807f97 = VolcanoBossBodyPartStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7663abf3
        volcano_boss_body_part_struct_c_0x7663abf3 = VolcanoBossBodyPartStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8a4c3f96
        volcano_boss_body_part_struct_c_0x8a4c3f96 = VolcanoBossBodyPartStructC.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x70d8cac0
        volcano_boss_body_part_struct_c_0x70d8cac0 = VolcanoBossBodyPartStructC.from_stream(data, property_size)
    
        return cls(volcano_boss_body_part_struct_c_0x92807f97, volcano_boss_body_part_struct_c_0x7663abf3, volcano_boss_body_part_struct_c_0x8a4c3f96, volcano_boss_body_part_struct_c_0x70d8cac0)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x92\x80\x7f\x97')  # 0x92807f97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x92807f97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'vc\xab\xf3')  # 0x7663abf3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x7663abf3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8aL?\x96')  # 0x8a4c3f96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x8a4c3f96.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'p\xd8\xca\xc0')  # 0x70d8cac0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_c_0x70d8cac0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct294Json", data)
        return cls(
            volcano_boss_body_part_struct_c_0x92807f97=VolcanoBossBodyPartStructC.from_json(json_data['volcano_boss_body_part_struct_c_0x92807f97']),
            volcano_boss_body_part_struct_c_0x7663abf3=VolcanoBossBodyPartStructC.from_json(json_data['volcano_boss_body_part_struct_c_0x7663abf3']),
            volcano_boss_body_part_struct_c_0x8a4c3f96=VolcanoBossBodyPartStructC.from_json(json_data['volcano_boss_body_part_struct_c_0x8a4c3f96']),
            volcano_boss_body_part_struct_c_0x70d8cac0=VolcanoBossBodyPartStructC.from_json(json_data['volcano_boss_body_part_struct_c_0x70d8cac0']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'volcano_boss_body_part_struct_c_0x92807f97': self.volcano_boss_body_part_struct_c_0x92807f97.to_json(),
            'volcano_boss_body_part_struct_c_0x7663abf3': self.volcano_boss_body_part_struct_c_0x7663abf3.to_json(),
            'volcano_boss_body_part_struct_c_0x8a4c3f96': self.volcano_boss_body_part_struct_c_0x8a4c3f96.to_json(),
            'volcano_boss_body_part_struct_c_0x70d8cac0': self.volcano_boss_body_part_struct_c_0x70d8cac0.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x92807f97: ('volcano_boss_body_part_struct_c_0x92807f97', VolcanoBossBodyPartStructC.from_stream),
    0x7663abf3: ('volcano_boss_body_part_struct_c_0x7663abf3', VolcanoBossBodyPartStructC.from_stream),
    0x8a4c3f96: ('volcano_boss_body_part_struct_c_0x8a4c3f96', VolcanoBossBodyPartStructC.from_stream),
    0x70d8cac0: ('volcano_boss_body_part_struct_c_0x70d8cac0', VolcanoBossBodyPartStructC.from_stream),
}

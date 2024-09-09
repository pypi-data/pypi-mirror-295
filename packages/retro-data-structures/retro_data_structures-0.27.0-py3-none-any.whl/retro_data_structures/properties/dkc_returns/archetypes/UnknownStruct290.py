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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct289 import UnknownStruct289
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructB import VolcanoBossBodyPartStructB

if typing.TYPE_CHECKING:
    class UnknownStruct290Json(typing_extensions.TypedDict):
        unknown_struct289: json_util.JsonObject
        volcano_boss_body_part_struct_b_0xc3e3ef00: json_util.JsonObject
        volcano_boss_body_part_struct_b_0xfa9b4240: json_util.JsonObject
        volcano_boss_body_part_struct_b_0xedb32680: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct290(BaseProperty):
    unknown_struct289: UnknownStruct289 = dataclasses.field(default_factory=UnknownStruct289, metadata={
        'reflection': FieldReflection[UnknownStruct289](
            UnknownStruct289, id=0x208c69a5, original_name='UnknownStruct289', from_json=UnknownStruct289.from_json, to_json=UnknownStruct289.to_json
        ),
    })
    volcano_boss_body_part_struct_b_0xc3e3ef00: VolcanoBossBodyPartStructB = dataclasses.field(default_factory=VolcanoBossBodyPartStructB, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructB](
            VolcanoBossBodyPartStructB, id=0xc3e3ef00, original_name='VolcanoBossBodyPartStructB', from_json=VolcanoBossBodyPartStructB.from_json, to_json=VolcanoBossBodyPartStructB.to_json
        ),
    })
    volcano_boss_body_part_struct_b_0xfa9b4240: VolcanoBossBodyPartStructB = dataclasses.field(default_factory=VolcanoBossBodyPartStructB, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructB](
            VolcanoBossBodyPartStructB, id=0xfa9b4240, original_name='VolcanoBossBodyPartStructB', from_json=VolcanoBossBodyPartStructB.from_json, to_json=VolcanoBossBodyPartStructB.to_json
        ),
    })
    volcano_boss_body_part_struct_b_0xedb32680: VolcanoBossBodyPartStructB = dataclasses.field(default_factory=VolcanoBossBodyPartStructB, metadata={
        'reflection': FieldReflection[VolcanoBossBodyPartStructB](
            VolcanoBossBodyPartStructB, id=0xedb32680, original_name='VolcanoBossBodyPartStructB', from_json=VolcanoBossBodyPartStructB.from_json, to_json=VolcanoBossBodyPartStructB.to_json
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
        assert property_id == 0x208c69a5
        unknown_struct289 = UnknownStruct289.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc3e3ef00
        volcano_boss_body_part_struct_b_0xc3e3ef00 = VolcanoBossBodyPartStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfa9b4240
        volcano_boss_body_part_struct_b_0xfa9b4240 = VolcanoBossBodyPartStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xedb32680
        volcano_boss_body_part_struct_b_0xedb32680 = VolcanoBossBodyPartStructB.from_stream(data, property_size)
    
        return cls(unknown_struct289, volcano_boss_body_part_struct_b_0xc3e3ef00, volcano_boss_body_part_struct_b_0xfa9b4240, volcano_boss_body_part_struct_b_0xedb32680)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b' \x8ci\xa5')  # 0x208c69a5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct289.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3\xe3\xef\x00')  # 0xc3e3ef00
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_b_0xc3e3ef00.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x9bB@')  # 0xfa9b4240
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_b_0xfa9b4240.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xb3&\x80')  # 0xedb32680
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_b_0xedb32680.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct290Json", data)
        return cls(
            unknown_struct289=UnknownStruct289.from_json(json_data['unknown_struct289']),
            volcano_boss_body_part_struct_b_0xc3e3ef00=VolcanoBossBodyPartStructB.from_json(json_data['volcano_boss_body_part_struct_b_0xc3e3ef00']),
            volcano_boss_body_part_struct_b_0xfa9b4240=VolcanoBossBodyPartStructB.from_json(json_data['volcano_boss_body_part_struct_b_0xfa9b4240']),
            volcano_boss_body_part_struct_b_0xedb32680=VolcanoBossBodyPartStructB.from_json(json_data['volcano_boss_body_part_struct_b_0xedb32680']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct289': self.unknown_struct289.to_json(),
            'volcano_boss_body_part_struct_b_0xc3e3ef00': self.volcano_boss_body_part_struct_b_0xc3e3ef00.to_json(),
            'volcano_boss_body_part_struct_b_0xfa9b4240': self.volcano_boss_body_part_struct_b_0xfa9b4240.to_json(),
            'volcano_boss_body_part_struct_b_0xedb32680': self.volcano_boss_body_part_struct_b_0xedb32680.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x208c69a5: ('unknown_struct289', UnknownStruct289.from_stream),
    0xc3e3ef00: ('volcano_boss_body_part_struct_b_0xc3e3ef00', VolcanoBossBodyPartStructB.from_stream),
    0xfa9b4240: ('volcano_boss_body_part_struct_b_0xfa9b4240', VolcanoBossBodyPartStructB.from_stream),
    0xedb32680: ('volcano_boss_body_part_struct_b_0xedb32680', VolcanoBossBodyPartStructB.from_stream),
}

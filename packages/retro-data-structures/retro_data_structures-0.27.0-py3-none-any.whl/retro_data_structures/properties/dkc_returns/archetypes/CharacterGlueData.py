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
from retro_data_structures.properties.dkc_returns.archetypes.DKBarrelGlueData import DKBarrelGlueData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct138 import UnknownStruct138

if typing.TYPE_CHECKING:
    class CharacterGlueDataJson(typing_extensions.TypedDict):
        glue_type: int
        unknown_struct138: json_util.JsonObject
        dk_barrel_glue_data: json_util.JsonObject
    

@dataclasses.dataclass()
class CharacterGlueData(BaseProperty):
    glue_type: enums.GlueType = dataclasses.field(default=enums.GlueType.Unknown1, metadata={
        'reflection': FieldReflection[enums.GlueType](
            enums.GlueType, id=0x411d0552, original_name='GlueType', from_json=enums.GlueType.from_json, to_json=enums.GlueType.to_json
        ),
    })
    unknown_struct138: UnknownStruct138 = dataclasses.field(default_factory=UnknownStruct138, metadata={
        'reflection': FieldReflection[UnknownStruct138](
            UnknownStruct138, id=0xa46f7341, original_name='UnknownStruct138', from_json=UnknownStruct138.from_json, to_json=UnknownStruct138.to_json
        ),
    })
    dk_barrel_glue_data: DKBarrelGlueData = dataclasses.field(default_factory=DKBarrelGlueData, metadata={
        'reflection': FieldReflection[DKBarrelGlueData](
            DKBarrelGlueData, id=0x36538065, original_name='DKBarrelGlueData', from_json=DKBarrelGlueData.from_json, to_json=DKBarrelGlueData.to_json
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
        if property_count != 3:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x411d0552
        glue_type = enums.GlueType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa46f7341
        unknown_struct138 = UnknownStruct138.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36538065
        dk_barrel_glue_data = DKBarrelGlueData.from_stream(data, property_size)
    
        return cls(glue_type, unknown_struct138, dk_barrel_glue_data)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'A\x1d\x05R')  # 0x411d0552
        data.write(b'\x00\x04')  # size
        self.glue_type.to_stream(data)

        data.write(b'\xa4osA')  # 0xa46f7341
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct138.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6S\x80e')  # 0x36538065
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dk_barrel_glue_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CharacterGlueDataJson", data)
        return cls(
            glue_type=enums.GlueType.from_json(json_data['glue_type']),
            unknown_struct138=UnknownStruct138.from_json(json_data['unknown_struct138']),
            dk_barrel_glue_data=DKBarrelGlueData.from_json(json_data['dk_barrel_glue_data']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'glue_type': self.glue_type.to_json(),
            'unknown_struct138': self.unknown_struct138.to_json(),
            'dk_barrel_glue_data': self.dk_barrel_glue_data.to_json(),
        }


def _decode_glue_type(data: typing.BinaryIO, property_size: int):
    return enums.GlueType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x411d0552: ('glue_type', _decode_glue_type),
    0xa46f7341: ('unknown_struct138', UnknownStruct138.from_stream),
    0x36538065: ('dk_barrel_glue_data', DKBarrelGlueData.from_stream),
}

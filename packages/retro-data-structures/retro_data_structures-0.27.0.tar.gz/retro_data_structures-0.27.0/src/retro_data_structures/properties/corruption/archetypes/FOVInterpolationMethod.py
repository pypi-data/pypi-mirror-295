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
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.InterpolationMethod import InterpolationMethod

if typing.TYPE_CHECKING:
    class FOVInterpolationMethodJson(typing_extensions.TypedDict):
        fov_type: int
        fov_control: json_util.JsonObject
    

@dataclasses.dataclass()
class FOVInterpolationMethod(BaseProperty):
    fov_type: enums.FOVType = dataclasses.field(default=enums.FOVType.Unknown1, metadata={
        'reflection': FieldReflection[enums.FOVType](
            enums.FOVType, id=0x19ea151b, original_name='FOVType', from_json=enums.FOVType.from_json, to_json=enums.FOVType.to_json
        ),
    })
    fov_control: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod, metadata={
        'reflection': FieldReflection[InterpolationMethod](
            InterpolationMethod, id=0x9f90014c, original_name='FOVControl', from_json=InterpolationMethod.from_json, to_json=InterpolationMethod.to_json
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        if property_count != 2:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x19ea151b
        fov_type = enums.FOVType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9f90014c
        fov_control = InterpolationMethod.from_stream(data, property_size)
    
        return cls(fov_type, fov_control)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x19\xea\x15\x1b')  # 0x19ea151b
        data.write(b'\x00\x04')  # size
        self.fov_type.to_stream(data)

        data.write(b'\x9f\x90\x01L')  # 0x9f90014c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("FOVInterpolationMethodJson", data)
        return cls(
            fov_type=enums.FOVType.from_json(json_data['fov_type']),
            fov_control=InterpolationMethod.from_json(json_data['fov_control']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'fov_type': self.fov_type.to_json(),
            'fov_control': self.fov_control.to_json(),
        }


def _decode_fov_type(data: typing.BinaryIO, property_size: int):
    return enums.FOVType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x19ea151b: ('fov_type', _decode_fov_type),
    0x9f90014c: ('fov_control', InterpolationMethod.from_stream),
}

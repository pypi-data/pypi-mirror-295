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
    class OrientationInterpolationMethodJson(typing_extensions.TypedDict):
        orientation_type: int
        orientation_control: json_util.JsonObject
    

@dataclasses.dataclass()
class OrientationInterpolationMethod(BaseProperty):
    orientation_type: enums.OrientationType = dataclasses.field(default=enums.OrientationType.Unknown1, metadata={
        'reflection': FieldReflection[enums.OrientationType](
            enums.OrientationType, id=0x5c72a964, original_name='OrientationType', from_json=enums.OrientationType.from_json, to_json=enums.OrientationType.to_json
        ),
    })
    orientation_control: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod, metadata={
        'reflection': FieldReflection[InterpolationMethod](
            InterpolationMethod, id=0x8654b081, original_name='OrientationControl', from_json=InterpolationMethod.from_json, to_json=InterpolationMethod.to_json
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
        assert property_id == 0x5c72a964
        orientation_type = enums.OrientationType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8654b081
        orientation_control = InterpolationMethod.from_stream(data, property_size)
    
        return cls(orientation_type, orientation_control)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\\r\xa9d')  # 0x5c72a964
        data.write(b'\x00\x04')  # size
        self.orientation_type.to_stream(data)

        data.write(b'\x86T\xb0\x81')  # 0x8654b081
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("OrientationInterpolationMethodJson", data)
        return cls(
            orientation_type=enums.OrientationType.from_json(json_data['orientation_type']),
            orientation_control=InterpolationMethod.from_json(json_data['orientation_control']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'orientation_type': self.orientation_type.to_json(),
            'orientation_control': self.orientation_control.to_json(),
        }


def _decode_orientation_type(data: typing.BinaryIO, property_size: int):
    return enums.OrientationType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5c72a964: ('orientation_type', _decode_orientation_type),
    0x8654b081: ('orientation_control', InterpolationMethod.from_stream),
}

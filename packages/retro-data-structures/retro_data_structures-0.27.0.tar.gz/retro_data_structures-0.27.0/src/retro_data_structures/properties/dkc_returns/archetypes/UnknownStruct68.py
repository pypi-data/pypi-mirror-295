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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct14 import UnknownStruct14
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct67 import UnknownStruct67

if typing.TYPE_CHECKING:
    class UnknownStruct68Json(typing_extensions.TypedDict):
        horizontal_type: int
        unknown_struct67: json_util.JsonObject
        unknown_struct14: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct68(BaseProperty):
    horizontal_type: enums.HorizontalType = dataclasses.field(default=enums.HorizontalType.Unknown1, metadata={
        'reflection': FieldReflection[enums.HorizontalType](
            enums.HorizontalType, id=0x2b7247aa, original_name='HorizontalType', from_json=enums.HorizontalType.from_json, to_json=enums.HorizontalType.to_json
        ),
    })
    unknown_struct67: UnknownStruct67 = dataclasses.field(default_factory=UnknownStruct67, metadata={
        'reflection': FieldReflection[UnknownStruct67](
            UnknownStruct67, id=0xb02aaa53, original_name='UnknownStruct67', from_json=UnknownStruct67.from_json, to_json=UnknownStruct67.to_json
        ),
    })
    unknown_struct14: UnknownStruct14 = dataclasses.field(default_factory=UnknownStruct14, metadata={
        'reflection': FieldReflection[UnknownStruct14](
            UnknownStruct14, id=0x02b79243, original_name='UnknownStruct14', from_json=UnknownStruct14.from_json, to_json=UnknownStruct14.to_json
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
        assert property_id == 0x2b7247aa
        horizontal_type = enums.HorizontalType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb02aaa53
        unknown_struct67 = UnknownStruct67.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x02b79243
        unknown_struct14 = UnknownStruct14.from_stream(data, property_size)
    
        return cls(horizontal_type, unknown_struct67, unknown_struct14)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'+rG\xaa')  # 0x2b7247aa
        data.write(b'\x00\x04')  # size
        self.horizontal_type.to_stream(data)

        data.write(b'\xb0*\xaaS')  # 0xb02aaa53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct67.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\xb7\x92C')  # 0x2b79243
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct68Json", data)
        return cls(
            horizontal_type=enums.HorizontalType.from_json(json_data['horizontal_type']),
            unknown_struct67=UnknownStruct67.from_json(json_data['unknown_struct67']),
            unknown_struct14=UnknownStruct14.from_json(json_data['unknown_struct14']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'horizontal_type': self.horizontal_type.to_json(),
            'unknown_struct67': self.unknown_struct67.to_json(),
            'unknown_struct14': self.unknown_struct14.to_json(),
        }


def _decode_horizontal_type(data: typing.BinaryIO, property_size: int):
    return enums.HorizontalType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2b7247aa: ('horizontal_type', _decode_horizontal_type),
    0xb02aaa53: ('unknown_struct67', UnknownStruct67.from_stream),
    0x2b79243: ('unknown_struct14', UnknownStruct14.from_stream),
}

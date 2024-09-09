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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct15 import UnknownStruct15
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct69 import UnknownStruct69
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct70 import UnknownStruct70

if typing.TYPE_CHECKING:
    class UnknownStruct71Json(typing_extensions.TypedDict):
        vertical_type: int
        unknown_struct69: json_util.JsonObject
        unknown_struct15: json_util.JsonObject
        unknown_struct70: json_util.JsonObject
        unknown_struct14: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct71(BaseProperty):
    vertical_type: enums.VerticalType = dataclasses.field(default=enums.VerticalType.Unknown1, metadata={
        'reflection': FieldReflection[enums.VerticalType](
            enums.VerticalType, id=0xad50d893, original_name='VerticalType', from_json=enums.VerticalType.from_json, to_json=enums.VerticalType.to_json
        ),
    })
    unknown_struct69: UnknownStruct69 = dataclasses.field(default_factory=UnknownStruct69, metadata={
        'reflection': FieldReflection[UnknownStruct69](
            UnknownStruct69, id=0xcffe15a0, original_name='UnknownStruct69', from_json=UnknownStruct69.from_json, to_json=UnknownStruct69.to_json
        ),
    })
    unknown_struct15: UnknownStruct15 = dataclasses.field(default_factory=UnknownStruct15, metadata={
        'reflection': FieldReflection[UnknownStruct15](
            UnknownStruct15, id=0x37c8c046, original_name='UnknownStruct15', from_json=UnknownStruct15.from_json, to_json=UnknownStruct15.to_json
        ),
    })
    unknown_struct70: UnknownStruct70 = dataclasses.field(default_factory=UnknownStruct70, metadata={
        'reflection': FieldReflection[UnknownStruct70](
            UnknownStruct70, id=0x774ba905, original_name='UnknownStruct70', from_json=UnknownStruct70.from_json, to_json=UnknownStruct70.to_json
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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xad50d893
        vertical_type = enums.VerticalType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcffe15a0
        unknown_struct69 = UnknownStruct69.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x37c8c046
        unknown_struct15 = UnknownStruct15.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x774ba905
        unknown_struct70 = UnknownStruct70.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x02b79243
        unknown_struct14 = UnknownStruct14.from_stream(data, property_size)
    
        return cls(vertical_type, unknown_struct69, unknown_struct15, unknown_struct70, unknown_struct14)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xadP\xd8\x93')  # 0xad50d893
        data.write(b'\x00\x04')  # size
        self.vertical_type.to_stream(data)

        data.write(b'\xcf\xfe\x15\xa0')  # 0xcffe15a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct69.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\xc8\xc0F')  # 0x37c8c046
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'wK\xa9\x05')  # 0x774ba905
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct70.to_stream(data)
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
        json_data = typing.cast("UnknownStruct71Json", data)
        return cls(
            vertical_type=enums.VerticalType.from_json(json_data['vertical_type']),
            unknown_struct69=UnknownStruct69.from_json(json_data['unknown_struct69']),
            unknown_struct15=UnknownStruct15.from_json(json_data['unknown_struct15']),
            unknown_struct70=UnknownStruct70.from_json(json_data['unknown_struct70']),
            unknown_struct14=UnknownStruct14.from_json(json_data['unknown_struct14']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'vertical_type': self.vertical_type.to_json(),
            'unknown_struct69': self.unknown_struct69.to_json(),
            'unknown_struct15': self.unknown_struct15.to_json(),
            'unknown_struct70': self.unknown_struct70.to_json(),
            'unknown_struct14': self.unknown_struct14.to_json(),
        }


def _decode_vertical_type(data: typing.BinaryIO, property_size: int):
    return enums.VerticalType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xad50d893: ('vertical_type', _decode_vertical_type),
    0xcffe15a0: ('unknown_struct69', UnknownStruct69.from_stream),
    0x37c8c046: ('unknown_struct15', UnknownStruct15.from_stream),
    0x774ba905: ('unknown_struct70', UnknownStruct70.from_stream),
    0x2b79243: ('unknown_struct14', UnknownStruct14.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct13Json(typing_extensions.TypedDict):
        offset_method: int
        offset_spline: json_util.JsonObject
        unknown: bool
    

@dataclasses.dataclass()
class UnknownStruct13(BaseProperty):
    offset_method: enums.OffsetMethod = dataclasses.field(default=enums.OffsetMethod.Unknown1, metadata={
        'reflection': FieldReflection[enums.OffsetMethod](
            enums.OffsetMethod, id=0x0926929b, original_name='OffsetMethod', from_json=enums.OffsetMethod.from_json, to_json=enums.OffsetMethod.to_json
        ),
    })
    offset_spline: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x19028bd3, original_name='OffsetSpline', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    unknown: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf9fb16a2, original_name='Unknown'
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
        assert property_id == 0x0926929b
        offset_method = enums.OffsetMethod.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x19028bd3
        offset_spline = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf9fb16a2
        unknown = struct.unpack('>?', data.read(1))[0]
    
        return cls(offset_method, offset_spline, unknown)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\t&\x92\x9b')  # 0x926929b
        data.write(b'\x00\x04')  # size
        self.offset_method.to_stream(data)

        data.write(b'\x19\x02\x8b\xd3')  # 0x19028bd3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offset_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xfb\x16\xa2')  # 0xf9fb16a2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct13Json", data)
        return cls(
            offset_method=enums.OffsetMethod.from_json(json_data['offset_method']),
            offset_spline=Spline.from_json(json_data['offset_spline']),
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'offset_method': self.offset_method.to_json(),
            'offset_spline': self.offset_spline.to_json(),
            'unknown': self.unknown,
        }


def _decode_offset_method(data: typing.BinaryIO, property_size: int):
    return enums.OffsetMethod.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x926929b: ('offset_method', _decode_offset_method),
    0x19028bd3: ('offset_spline', Spline.from_stream),
    0xf9fb16a2: ('unknown', _decode_unknown),
}

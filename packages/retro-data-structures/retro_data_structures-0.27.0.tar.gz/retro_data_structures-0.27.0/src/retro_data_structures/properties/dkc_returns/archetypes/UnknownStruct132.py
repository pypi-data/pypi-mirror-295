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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class UnknownStruct132Json(typing_extensions.TypedDict):
        unknown_0x041b3c2b: json_util.JsonValue
        unknown_0x599eacd6: json_util.JsonValue
        minimum_spin_speed: json_util.JsonValue
        maximum_spin_speed: json_util.JsonValue
    

_FAST_FORMAT = None
_FAST_IDS = (0x41b3c2b, 0x599eacd6, 0xf78c8ac7, 0xb69bb541)


@dataclasses.dataclass()
class UnknownStruct132(BaseProperty):
    unknown_0x041b3c2b: Vector = dataclasses.field(default_factory=lambda: Vector(x=10.606200218200684, y=21.21269989013672, z=18.371999740600586), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x041b3c2b, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_0x599eacd6: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.5, y=21.21269989013672, z=18.371999740600586), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x599eacd6, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    minimum_spin_speed: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=13.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xf78c8ac7, original_name='MinimumSpinSpeed', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    maximum_spin_speed: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=15.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xb69bb541, original_name='MaximumSpinSpeed', from_json=Vector.from_json, to_json=Vector.to_json
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfffLHfffLHfffLHfff')
    
        dec = _FAST_FORMAT.unpack(data.read(72))
        assert (dec[0], dec[5], dec[10], dec[15]) == _FAST_IDS
        return cls(
            Vector(*dec[2:5]),
            Vector(*dec[7:10]),
            Vector(*dec[12:15]),
            Vector(*dec[17:20]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x04\x1b<+')  # 0x41b3c2b
        data.write(b'\x00\x0c')  # size
        self.unknown_0x041b3c2b.to_stream(data)

        data.write(b'Y\x9e\xac\xd6')  # 0x599eacd6
        data.write(b'\x00\x0c')  # size
        self.unknown_0x599eacd6.to_stream(data)

        data.write(b'\xf7\x8c\x8a\xc7')  # 0xf78c8ac7
        data.write(b'\x00\x0c')  # size
        self.minimum_spin_speed.to_stream(data)

        data.write(b'\xb6\x9b\xb5A')  # 0xb69bb541
        data.write(b'\x00\x0c')  # size
        self.maximum_spin_speed.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct132Json", data)
        return cls(
            unknown_0x041b3c2b=Vector.from_json(json_data['unknown_0x041b3c2b']),
            unknown_0x599eacd6=Vector.from_json(json_data['unknown_0x599eacd6']),
            minimum_spin_speed=Vector.from_json(json_data['minimum_spin_speed']),
            maximum_spin_speed=Vector.from_json(json_data['maximum_spin_speed']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x041b3c2b': self.unknown_0x041b3c2b.to_json(),
            'unknown_0x599eacd6': self.unknown_0x599eacd6.to_json(),
            'minimum_spin_speed': self.minimum_spin_speed.to_json(),
            'maximum_spin_speed': self.maximum_spin_speed.to_json(),
        }


def _decode_unknown_0x041b3c2b(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x599eacd6(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_minimum_spin_speed(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_maximum_spin_speed(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x41b3c2b: ('unknown_0x041b3c2b', _decode_unknown_0x041b3c2b),
    0x599eacd6: ('unknown_0x599eacd6', _decode_unknown_0x599eacd6),
    0xf78c8ac7: ('minimum_spin_speed', _decode_minimum_spin_speed),
    0xb69bb541: ('maximum_spin_speed', _decode_maximum_spin_speed),
}

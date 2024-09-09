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

if typing.TYPE_CHECKING:
    class UnknownStruct72Json(typing_extensions.TypedDict):
        min_behavior_time: float
        unknown_0xf465a51b: bool
        min_cling_time: float
        unknown_0xe010dc0f: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xad122e5d, 0xf465a51b, 0x42a9e2e4, 0xe010dc0f)


@dataclasses.dataclass()
class UnknownStruct72(BaseProperty):
    min_behavior_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xad122e5d, original_name='MinBehaviorTime'
        ),
    })
    unknown_0xf465a51b: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf465a51b, original_name='Unknown'
        ),
    })
    min_cling_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42a9e2e4, original_name='MinClingTime'
        ),
    })
    unknown_0xe010dc0f: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe010dc0f, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHfLH?LHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(37))
        assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xad\x12.]')  # 0xad122e5d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_behavior_time))

        data.write(b'\xf4e\xa5\x1b')  # 0xf465a51b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf465a51b))

        data.write(b'B\xa9\xe2\xe4')  # 0x42a9e2e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_cling_time))

        data.write(b'\xe0\x10\xdc\x0f')  # 0xe010dc0f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe010dc0f))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct72Json", data)
        return cls(
            min_behavior_time=json_data['min_behavior_time'],
            unknown_0xf465a51b=json_data['unknown_0xf465a51b'],
            min_cling_time=json_data['min_cling_time'],
            unknown_0xe010dc0f=json_data['unknown_0xe010dc0f'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'min_behavior_time': self.min_behavior_time,
            'unknown_0xf465a51b': self.unknown_0xf465a51b,
            'min_cling_time': self.min_cling_time,
            'unknown_0xe010dc0f': self.unknown_0xe010dc0f,
        }


def _decode_min_behavior_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf465a51b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_min_cling_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe010dc0f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xad122e5d: ('min_behavior_time', _decode_min_behavior_time),
    0xf465a51b: ('unknown_0xf465a51b', _decode_unknown_0xf465a51b),
    0x42a9e2e4: ('min_cling_time', _decode_min_cling_time),
    0xe010dc0f: ('unknown_0xe010dc0f', _decode_unknown_0xe010dc0f),
}

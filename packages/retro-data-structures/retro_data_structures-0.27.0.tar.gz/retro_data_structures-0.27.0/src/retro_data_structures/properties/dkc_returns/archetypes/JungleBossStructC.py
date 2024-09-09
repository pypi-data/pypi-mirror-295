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
    class JungleBossStructCJson(typing_extensions.TypedDict):
        unknown_0xcb349144: int
        spawn_delay_time: float
        unknown_0x0ecc390f: float
        unknown_0xc4cfb8de: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xcb349144, 0xc8401fce, 0xecc390f, 0xc4cfb8de)


@dataclasses.dataclass()
class JungleBossStructC(BaseProperty):
    unknown_0xcb349144: int = dataclasses.field(default=3, metadata={
        'reflection': FieldReflection[int](
            int, id=0xcb349144, original_name='Unknown'
        ),
    })
    spawn_delay_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc8401fce, original_name='SpawnDelayTime'
        ),
    })
    unknown_0x0ecc390f: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0ecc390f, original_name='Unknown'
        ),
    })
    unknown_0xc4cfb8de: float = dataclasses.field(default=35.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc4cfb8de, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(40))
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

        data.write(b'\xcb4\x91D')  # 0xcb349144
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xcb349144))

        data.write(b'\xc8@\x1f\xce')  # 0xc8401fce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spawn_delay_time))

        data.write(b'\x0e\xcc9\x0f')  # 0xecc390f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0ecc390f))

        data.write(b'\xc4\xcf\xb8\xde')  # 0xc4cfb8de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc4cfb8de))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("JungleBossStructCJson", data)
        return cls(
            unknown_0xcb349144=json_data['unknown_0xcb349144'],
            spawn_delay_time=json_data['spawn_delay_time'],
            unknown_0x0ecc390f=json_data['unknown_0x0ecc390f'],
            unknown_0xc4cfb8de=json_data['unknown_0xc4cfb8de'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xcb349144': self.unknown_0xcb349144,
            'spawn_delay_time': self.spawn_delay_time,
            'unknown_0x0ecc390f': self.unknown_0x0ecc390f,
            'unknown_0xc4cfb8de': self.unknown_0xc4cfb8de,
        }


def _decode_unknown_0xcb349144(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spawn_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0ecc390f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc4cfb8de(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcb349144: ('unknown_0xcb349144', _decode_unknown_0xcb349144),
    0xc8401fce: ('spawn_delay_time', _decode_spawn_delay_time),
    0xecc390f: ('unknown_0x0ecc390f', _decode_unknown_0x0ecc390f),
    0xc4cfb8de: ('unknown_0xc4cfb8de', _decode_unknown_0xc4cfb8de),
}

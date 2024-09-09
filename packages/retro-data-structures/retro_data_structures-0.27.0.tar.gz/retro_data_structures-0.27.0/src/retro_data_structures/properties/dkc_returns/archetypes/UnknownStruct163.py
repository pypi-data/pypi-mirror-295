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
    class UnknownStruct163Json(typing_extensions.TypedDict):
        initial_duration: float
        show_title_duration: float
        show_buttons_duration: float
        unknown: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x8e6c42f, 0xd84ac0f5, 0x1c5c303b, 0xf0c51c84)


@dataclasses.dataclass()
class UnknownStruct163(BaseProperty):
    initial_duration: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x08e6c42f, original_name='InitialDuration'
        ),
    })
    show_title_duration: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd84ac0f5, original_name='ShowTitleDuration'
        ),
    })
    show_buttons_duration: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1c5c303b, original_name='ShowButtonsDuration'
        ),
    })
    unknown: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf0c51c84, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')
    
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

        data.write(b'\x08\xe6\xc4/')  # 0x8e6c42f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_duration))

        data.write(b'\xd8J\xc0\xf5')  # 0xd84ac0f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.show_title_duration))

        data.write(b'\x1c\\0;')  # 0x1c5c303b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.show_buttons_duration))

        data.write(b'\xf0\xc5\x1c\x84')  # 0xf0c51c84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct163Json", data)
        return cls(
            initial_duration=json_data['initial_duration'],
            show_title_duration=json_data['show_title_duration'],
            show_buttons_duration=json_data['show_buttons_duration'],
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'initial_duration': self.initial_duration,
            'show_title_duration': self.show_title_duration,
            'show_buttons_duration': self.show_buttons_duration,
            'unknown': self.unknown,
        }


def _decode_initial_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_show_title_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_show_buttons_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8e6c42f: ('initial_duration', _decode_initial_duration),
    0xd84ac0f5: ('show_title_duration', _decode_show_title_duration),
    0x1c5c303b: ('show_buttons_duration', _decode_show_buttons_duration),
    0xf0c51c84: ('unknown', _decode_unknown),
}

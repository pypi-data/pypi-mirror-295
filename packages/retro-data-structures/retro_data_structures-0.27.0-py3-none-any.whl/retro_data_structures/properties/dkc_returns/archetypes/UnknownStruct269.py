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
    class UnknownStruct269Json(typing_extensions.TypedDict):
        move: bool
        roll: bool
        ground_pound: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xadd734c9, 0xa71154c2, 0xd25345e8)


@dataclasses.dataclass()
class UnknownStruct269(BaseProperty):
    move: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xadd734c9, original_name='Move'
        ),
    })
    roll: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa71154c2, original_name='Roll'
        ),
    })
    ground_pound: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd25345e8, original_name='GroundPound'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(21))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xad\xd74\xc9')  # 0xadd734c9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.move))

        data.write(b'\xa7\x11T\xc2')  # 0xa71154c2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.roll))

        data.write(b'\xd2SE\xe8')  # 0xd25345e8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ground_pound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct269Json", data)
        return cls(
            move=json_data['move'],
            roll=json_data['roll'],
            ground_pound=json_data['ground_pound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'move': self.move,
            'roll': self.roll,
            'ground_pound': self.ground_pound,
        }


def _decode_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_roll(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xadd734c9: ('move', _decode_move),
    0xa71154c2: ('roll', _decode_roll),
    0xd25345e8: ('ground_pound', _decode_ground_pound),
}

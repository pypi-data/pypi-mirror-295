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
    class PickupRelayStructJson(typing_extensions.TypedDict):
        message1_chance: float
        message2_chance: float
        message3_chance: float
        message4_chance: float
        message5_chance: float
        message6_chance: float
        message7_chance: float
        message8_chance: float
        message9_chance: float
        message10_chance: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xfde3a4f5, 0x8a7d7605, 0x11d83a6a, 0x6540d3e5, 0xfee59f8a, 0x897b4d7a, 0x12de0115, 0x604a9e64, 0xfbefd20b, 0x54e8c18a)


@dataclasses.dataclass()
class PickupRelayStruct(BaseProperty):
    message1_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfde3a4f5, original_name='Message1Chance'
        ),
    })
    message2_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8a7d7605, original_name='Message2Chance'
        ),
    })
    message3_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x11d83a6a, original_name='Message3Chance'
        ),
    })
    message4_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6540d3e5, original_name='Message4Chance'
        ),
    })
    message5_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfee59f8a, original_name='Message5Chance'
        ),
    })
    message6_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x897b4d7a, original_name='Message6Chance'
        ),
    })
    message7_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x12de0115, original_name='Message7Chance'
        ),
    })
    message8_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x604a9e64, original_name='Message8Chance'
        ),
    })
    message9_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfbefd20b, original_name='Message9Chance'
        ),
    })
    message10_chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x54e8c18a, original_name='Message10Chance'
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
        if property_count != 10:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(100))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
            dec[29],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xfd\xe3\xa4\xf5')  # 0xfde3a4f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message1_chance))

        data.write(b'\x8a}v\x05')  # 0x8a7d7605
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message2_chance))

        data.write(b'\x11\xd8:j')  # 0x11d83a6a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message3_chance))

        data.write(b'e@\xd3\xe5')  # 0x6540d3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message4_chance))

        data.write(b'\xfe\xe5\x9f\x8a')  # 0xfee59f8a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message5_chance))

        data.write(b'\x89{Mz')  # 0x897b4d7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message6_chance))

        data.write(b'\x12\xde\x01\x15')  # 0x12de0115
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message7_chance))

        data.write(b'`J\x9ed')  # 0x604a9e64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message8_chance))

        data.write(b'\xfb\xef\xd2\x0b')  # 0xfbefd20b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message9_chance))

        data.write(b'T\xe8\xc1\x8a')  # 0x54e8c18a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.message10_chance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PickupRelayStructJson", data)
        return cls(
            message1_chance=json_data['message1_chance'],
            message2_chance=json_data['message2_chance'],
            message3_chance=json_data['message3_chance'],
            message4_chance=json_data['message4_chance'],
            message5_chance=json_data['message5_chance'],
            message6_chance=json_data['message6_chance'],
            message7_chance=json_data['message7_chance'],
            message8_chance=json_data['message8_chance'],
            message9_chance=json_data['message9_chance'],
            message10_chance=json_data['message10_chance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'message1_chance': self.message1_chance,
            'message2_chance': self.message2_chance,
            'message3_chance': self.message3_chance,
            'message4_chance': self.message4_chance,
            'message5_chance': self.message5_chance,
            'message6_chance': self.message6_chance,
            'message7_chance': self.message7_chance,
            'message8_chance': self.message8_chance,
            'message9_chance': self.message9_chance,
            'message10_chance': self.message10_chance,
        }


def _decode_message1_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message2_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message3_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message4_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message5_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message6_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message7_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message8_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message9_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_message10_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfde3a4f5: ('message1_chance', _decode_message1_chance),
    0x8a7d7605: ('message2_chance', _decode_message2_chance),
    0x11d83a6a: ('message3_chance', _decode_message3_chance),
    0x6540d3e5: ('message4_chance', _decode_message4_chance),
    0xfee59f8a: ('message5_chance', _decode_message5_chance),
    0x897b4d7a: ('message6_chance', _decode_message6_chance),
    0x12de0115: ('message7_chance', _decode_message7_chance),
    0x604a9e64: ('message8_chance', _decode_message8_chance),
    0xfbefd20b: ('message9_chance', _decode_message9_chance),
    0x54e8c18a: ('message10_chance', _decode_message10_chance),
}

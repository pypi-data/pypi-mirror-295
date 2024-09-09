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
    class UnknownStruct239Json(typing_extensions.TypedDict):
        spawn_delay: float
        unknown_0xb1351a96: float
        spawn_hazard_time: float
        flip_time: float
        medium_idle_time: float
        long_idle_time: float
        unknown_0x7850d13c: float
        unknown_0xde1a7739: float
        unknown_0xeddfb002: float
        unknown_0x62ca4939: float
        fake_spawn_delay: float
        unknown_0x086e29df: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xd438739d, 0xb1351a96, 0xa37429ee, 0x40ae4a09, 0x97473dac, 0x2e312774, 0x7850d13c, 0xde1a7739, 0xeddfb002, 0x62ca4939, 0x84d9331a, 0x86e29df)


@dataclasses.dataclass()
class UnknownStruct239(BaseProperty):
    spawn_delay: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd438739d, original_name='SpawnDelay'
        ),
    })
    unknown_0xb1351a96: float = dataclasses.field(default=0.6600000262260437, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb1351a96, original_name='Unknown'
        ),
    })
    spawn_hazard_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa37429ee, original_name='SpawnHazardTime'
        ),
    })
    flip_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x40ae4a09, original_name='FlipTime'
        ),
    })
    medium_idle_time: float = dataclasses.field(default=1.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x97473dac, original_name='MediumIdleTime'
        ),
    })
    long_idle_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2e312774, original_name='LongIdleTime'
        ),
    })
    unknown_0x7850d13c: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7850d13c, original_name='Unknown'
        ),
    })
    unknown_0xde1a7739: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xde1a7739, original_name='Unknown'
        ),
    })
    unknown_0xeddfb002: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xeddfb002, original_name='Unknown'
        ),
    })
    unknown_0x62ca4939: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x62ca4939, original_name='Unknown'
        ),
    })
    fake_spawn_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x84d9331a, original_name='FakeSpawnDelay'
        ),
    })
    unknown_0x086e29df: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x086e29df, original_name='Unknown'
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
        if property_count != 12:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(120))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) == _FAST_IDS
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
            dec[32],
            dec[35],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xd48s\x9d')  # 0xd438739d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spawn_delay))

        data.write(b'\xb15\x1a\x96')  # 0xb1351a96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb1351a96))

        data.write(b'\xa3t)\xee')  # 0xa37429ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spawn_hazard_time))

        data.write(b'@\xaeJ\t')  # 0x40ae4a09
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flip_time))

        data.write(b'\x97G=\xac')  # 0x97473dac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.medium_idle_time))

        data.write(b".1't")  # 0x2e312774
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.long_idle_time))

        data.write(b'xP\xd1<')  # 0x7850d13c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7850d13c))

        data.write(b'\xde\x1aw9')  # 0xde1a7739
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xde1a7739))

        data.write(b'\xed\xdf\xb0\x02')  # 0xeddfb002
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xeddfb002))

        data.write(b'b\xcaI9')  # 0x62ca4939
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x62ca4939))

        data.write(b'\x84\xd93\x1a')  # 0x84d9331a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fake_spawn_delay))

        data.write(b'\x08n)\xdf')  # 0x86e29df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x086e29df))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct239Json", data)
        return cls(
            spawn_delay=json_data['spawn_delay'],
            unknown_0xb1351a96=json_data['unknown_0xb1351a96'],
            spawn_hazard_time=json_data['spawn_hazard_time'],
            flip_time=json_data['flip_time'],
            medium_idle_time=json_data['medium_idle_time'],
            long_idle_time=json_data['long_idle_time'],
            unknown_0x7850d13c=json_data['unknown_0x7850d13c'],
            unknown_0xde1a7739=json_data['unknown_0xde1a7739'],
            unknown_0xeddfb002=json_data['unknown_0xeddfb002'],
            unknown_0x62ca4939=json_data['unknown_0x62ca4939'],
            fake_spawn_delay=json_data['fake_spawn_delay'],
            unknown_0x086e29df=json_data['unknown_0x086e29df'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'spawn_delay': self.spawn_delay,
            'unknown_0xb1351a96': self.unknown_0xb1351a96,
            'spawn_hazard_time': self.spawn_hazard_time,
            'flip_time': self.flip_time,
            'medium_idle_time': self.medium_idle_time,
            'long_idle_time': self.long_idle_time,
            'unknown_0x7850d13c': self.unknown_0x7850d13c,
            'unknown_0xde1a7739': self.unknown_0xde1a7739,
            'unknown_0xeddfb002': self.unknown_0xeddfb002,
            'unknown_0x62ca4939': self.unknown_0x62ca4939,
            'fake_spawn_delay': self.fake_spawn_delay,
            'unknown_0x086e29df': self.unknown_0x086e29df,
        }


def _decode_spawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb1351a96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spawn_hazard_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flip_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_medium_idle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_long_idle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7850d13c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xde1a7739(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xeddfb002(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x62ca4939(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fake_spawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x086e29df(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd438739d: ('spawn_delay', _decode_spawn_delay),
    0xb1351a96: ('unknown_0xb1351a96', _decode_unknown_0xb1351a96),
    0xa37429ee: ('spawn_hazard_time', _decode_spawn_hazard_time),
    0x40ae4a09: ('flip_time', _decode_flip_time),
    0x97473dac: ('medium_idle_time', _decode_medium_idle_time),
    0x2e312774: ('long_idle_time', _decode_long_idle_time),
    0x7850d13c: ('unknown_0x7850d13c', _decode_unknown_0x7850d13c),
    0xde1a7739: ('unknown_0xde1a7739', _decode_unknown_0xde1a7739),
    0xeddfb002: ('unknown_0xeddfb002', _decode_unknown_0xeddfb002),
    0x62ca4939: ('unknown_0x62ca4939', _decode_unknown_0x62ca4939),
    0x84d9331a: ('fake_spawn_delay', _decode_fake_spawn_delay),
    0x86e29df: ('unknown_0x086e29df', _decode_unknown_0x086e29df),
}

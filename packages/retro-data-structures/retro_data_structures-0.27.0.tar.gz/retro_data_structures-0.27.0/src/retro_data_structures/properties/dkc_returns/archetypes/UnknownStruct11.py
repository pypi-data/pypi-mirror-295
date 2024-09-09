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

if typing.TYPE_CHECKING:
    class UnknownStruct11Json(typing_extensions.TypedDict):
        unknown_0xf060eeec: int
        unknown_0x3dd7b303: float
        pre_delay_time: float
        fused_mode: int
        fused_time: float
        coloration: float
        damping: float
        cross_talk: float
        early_gain: float
        fused_gain: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xf060eeec, 0x3dd7b303, 0xf52af9f3, 0x22a0058d, 0xc77a8932, 0x5d6b1084, 0xfcf4aab0, 0xfb11a412, 0x253da9c6, 0x1f5a38e3)


@dataclasses.dataclass()
class UnknownStruct11(BaseProperty):
    unknown_0xf060eeec: int = dataclasses.field(default=3301645737, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf060eeec, original_name='Unknown'
        ),
    })  # Choice
    unknown_0x3dd7b303: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3dd7b303, original_name='Unknown'
        ),
    })
    pre_delay_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf52af9f3, original_name='PreDelayTime'
        ),
    })
    fused_mode: enums.FusedMode = dataclasses.field(default=enums.FusedMode.Unknown1, metadata={
        'reflection': FieldReflection[enums.FusedMode](
            enums.FusedMode, id=0x22a0058d, original_name='FusedMode', from_json=enums.FusedMode.from_json, to_json=enums.FusedMode.to_json
        ),
    })
    fused_time: float = dataclasses.field(default=0.009999999776482582, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc77a8932, original_name='FusedTime'
        ),
    })
    coloration: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5d6b1084, original_name='Coloration'
        ),
    })
    damping: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfcf4aab0, original_name='Damping'
        ),
    })
    cross_talk: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfb11a412, original_name='CrossTalk'
        ),
    })
    early_gain: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x253da9c6, original_name='EarlyGain'
        ),
    })
    fused_gain: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1f5a38e3, original_name='FusedGain'
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
            _FAST_FORMAT = struct.Struct('>LHLLHfLHfLHLLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(100))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            enums.FusedMode(dec[11]),
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

        data.write(b'\xf0`\xee\xec')  # 0xf060eeec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0xf060eeec))

        data.write(b'=\xd7\xb3\x03')  # 0x3dd7b303
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3dd7b303))

        data.write(b'\xf5*\xf9\xf3')  # 0xf52af9f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_delay_time))

        data.write(b'"\xa0\x05\x8d')  # 0x22a0058d
        data.write(b'\x00\x04')  # size
        self.fused_mode.to_stream(data)

        data.write(b'\xc7z\x892')  # 0xc77a8932
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fused_time))

        data.write(b']k\x10\x84')  # 0x5d6b1084
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.coloration))

        data.write(b'\xfc\xf4\xaa\xb0')  # 0xfcf4aab0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damping))

        data.write(b'\xfb\x11\xa4\x12')  # 0xfb11a412
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cross_talk))

        data.write(b'%=\xa9\xc6')  # 0x253da9c6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.early_gain))

        data.write(b'\x1fZ8\xe3')  # 0x1f5a38e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fused_gain))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct11Json", data)
        return cls(
            unknown_0xf060eeec=json_data['unknown_0xf060eeec'],
            unknown_0x3dd7b303=json_data['unknown_0x3dd7b303'],
            pre_delay_time=json_data['pre_delay_time'],
            fused_mode=enums.FusedMode.from_json(json_data['fused_mode']),
            fused_time=json_data['fused_time'],
            coloration=json_data['coloration'],
            damping=json_data['damping'],
            cross_talk=json_data['cross_talk'],
            early_gain=json_data['early_gain'],
            fused_gain=json_data['fused_gain'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xf060eeec': self.unknown_0xf060eeec,
            'unknown_0x3dd7b303': self.unknown_0x3dd7b303,
            'pre_delay_time': self.pre_delay_time,
            'fused_mode': self.fused_mode.to_json(),
            'fused_time': self.fused_time,
            'coloration': self.coloration,
            'damping': self.damping,
            'cross_talk': self.cross_talk,
            'early_gain': self.early_gain,
            'fused_gain': self.fused_gain,
        }


def _decode_unknown_0xf060eeec(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x3dd7b303(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pre_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fused_mode(data: typing.BinaryIO, property_size: int):
    return enums.FusedMode.from_stream(data)


def _decode_fused_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_coloration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cross_talk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_early_gain(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fused_gain(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf060eeec: ('unknown_0xf060eeec', _decode_unknown_0xf060eeec),
    0x3dd7b303: ('unknown_0x3dd7b303', _decode_unknown_0x3dd7b303),
    0xf52af9f3: ('pre_delay_time', _decode_pre_delay_time),
    0x22a0058d: ('fused_mode', _decode_fused_mode),
    0xc77a8932: ('fused_time', _decode_fused_time),
    0x5d6b1084: ('coloration', _decode_coloration),
    0xfcf4aab0: ('damping', _decode_damping),
    0xfb11a412: ('cross_talk', _decode_cross_talk),
    0x253da9c6: ('early_gain', _decode_early_gain),
    0x1f5a38e3: ('fused_gain', _decode_fused_gain),
}

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
    class StunnedByContactRuleDataJson(typing_extensions.TypedDict):
        stun_duration: float
        apply_boost_after_stun: bool
        boost_duration: float
        boost_speed_modifier: float
        can_be_blown: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x2d8db31d, 0x197779d1, 0xba4972fe, 0x85d39cb7, 0xf64e3867)


@dataclasses.dataclass()
class StunnedByContactRuleData(BaseProperty):
    stun_duration: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d8db31d, original_name='StunDuration'
        ),
    })
    apply_boost_after_stun: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x197779d1, original_name='ApplyBoostAfterStun'
        ),
    })
    boost_duration: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xba4972fe, original_name='BoostDuration'
        ),
    })
    boost_speed_modifier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x85d39cb7, original_name='BoostSpeedModifier'
        ),
    })
    can_be_blown: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf64e3867, original_name='CanBeBlown'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLH?LHfLHfLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(44))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

        data.write(b'\x19wy\xd1')  # 0x197779d1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_boost_after_stun))

        data.write(b'\xbaIr\xfe')  # 0xba4972fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_duration))

        data.write(b'\x85\xd3\x9c\xb7')  # 0x85d39cb7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_speed_modifier))

        data.write(b'\xf6N8g')  # 0xf64e3867
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_be_blown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("StunnedByContactRuleDataJson", data)
        return cls(
            stun_duration=json_data['stun_duration'],
            apply_boost_after_stun=json_data['apply_boost_after_stun'],
            boost_duration=json_data['boost_duration'],
            boost_speed_modifier=json_data['boost_speed_modifier'],
            can_be_blown=json_data['can_be_blown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'stun_duration': self.stun_duration,
            'apply_boost_after_stun': self.apply_boost_after_stun,
            'boost_duration': self.boost_duration,
            'boost_speed_modifier': self.boost_speed_modifier,
            'can_be_blown': self.can_be_blown,
        }


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_apply_boost_after_stun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_boost_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_speed_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_be_blown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
    0x197779d1: ('apply_boost_after_stun', _decode_apply_boost_after_stun),
    0xba4972fe: ('boost_duration', _decode_boost_duration),
    0x85d39cb7: ('boost_speed_modifier', _decode_boost_speed_modifier),
    0xf64e3867: ('can_be_blown', _decode_can_be_blown),
}

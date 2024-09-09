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
    class StunnedByGroundPoundBehaviorDataJson(typing_extensions.TypedDict):
        ground_pound_distance_vertical_multiplier: float
        stun_duration: float
        can_un_stun: bool
        minimum_stunned_time: float
        re_stun_delay: float
        apply_boost_after_un_stun: bool
        apply_boost_after_stun: bool
        boost_duration: float
        boost_speed_modifier: float
        stun_only_when_on_ground: bool
        knockback_instead_of_stun: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x62f0cffc, 0x2d8db31d, 0x40a372b6, 0x1ac813b9, 0xbae2755e, 0xc431344, 0x197779d1, 0xba4972fe, 0x85d39cb7, 0x38711325, 0xe38a723d)


@dataclasses.dataclass()
class StunnedByGroundPoundBehaviorData(BaseProperty):
    ground_pound_distance_vertical_multiplier: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x62f0cffc, original_name='GroundPoundDistanceVerticalMultiplier'
        ),
    })
    stun_duration: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d8db31d, original_name='StunDuration'
        ),
    })
    can_un_stun: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x40a372b6, original_name='CanUnStun'
        ),
    })
    minimum_stunned_time: float = dataclasses.field(default=0.33000001311302185, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1ac813b9, original_name='MinimumStunnedTime'
        ),
    })
    re_stun_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbae2755e, original_name='ReStunDelay'
        ),
    })
    apply_boost_after_un_stun: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0c431344, original_name='ApplyBoostAfterUnStun'
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
    stun_only_when_on_ground: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x38711325, original_name='StunOnlyWhenOnGround'
        ),
    })
    knockback_instead_of_stun: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe38a723d, original_name='KnockbackInsteadOfStun'
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
        if property_count != 11:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLH?LHfLHfLH?LH?LHfLHfLH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(95))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) == _FAST_IDS
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
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'b\xf0\xcf\xfc')  # 0x62f0cffc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_distance_vertical_multiplier))

        data.write(b'-\x8d\xb3\x1d')  # 0x2d8db31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_duration))

        data.write(b'@\xa3r\xb6')  # 0x40a372b6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_un_stun))

        data.write(b'\x1a\xc8\x13\xb9')  # 0x1ac813b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_stunned_time))

        data.write(b'\xba\xe2u^')  # 0xbae2755e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.re_stun_delay))

        data.write(b'\x0cC\x13D')  # 0xc431344
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_boost_after_un_stun))

        data.write(b'\x19wy\xd1')  # 0x197779d1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_boost_after_stun))

        data.write(b'\xbaIr\xfe')  # 0xba4972fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_duration))

        data.write(b'\x85\xd3\x9c\xb7')  # 0x85d39cb7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_speed_modifier))

        data.write(b'8q\x13%')  # 0x38711325
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stun_only_when_on_ground))

        data.write(b'\xe3\x8ar=')  # 0xe38a723d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.knockback_instead_of_stun))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("StunnedByGroundPoundBehaviorDataJson", data)
        return cls(
            ground_pound_distance_vertical_multiplier=json_data['ground_pound_distance_vertical_multiplier'],
            stun_duration=json_data['stun_duration'],
            can_un_stun=json_data['can_un_stun'],
            minimum_stunned_time=json_data['minimum_stunned_time'],
            re_stun_delay=json_data['re_stun_delay'],
            apply_boost_after_un_stun=json_data['apply_boost_after_un_stun'],
            apply_boost_after_stun=json_data['apply_boost_after_stun'],
            boost_duration=json_data['boost_duration'],
            boost_speed_modifier=json_data['boost_speed_modifier'],
            stun_only_when_on_ground=json_data['stun_only_when_on_ground'],
            knockback_instead_of_stun=json_data['knockback_instead_of_stun'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'ground_pound_distance_vertical_multiplier': self.ground_pound_distance_vertical_multiplier,
            'stun_duration': self.stun_duration,
            'can_un_stun': self.can_un_stun,
            'minimum_stunned_time': self.minimum_stunned_time,
            're_stun_delay': self.re_stun_delay,
            'apply_boost_after_un_stun': self.apply_boost_after_un_stun,
            'apply_boost_after_stun': self.apply_boost_after_stun,
            'boost_duration': self.boost_duration,
            'boost_speed_modifier': self.boost_speed_modifier,
            'stun_only_when_on_ground': self.stun_only_when_on_ground,
            'knockback_instead_of_stun': self.knockback_instead_of_stun,
        }


def _decode_ground_pound_distance_vertical_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_un_stun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_stunned_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_re_stun_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_apply_boost_after_un_stun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_apply_boost_after_stun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_boost_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_speed_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_only_when_on_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_knockback_instead_of_stun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x62f0cffc: ('ground_pound_distance_vertical_multiplier', _decode_ground_pound_distance_vertical_multiplier),
    0x2d8db31d: ('stun_duration', _decode_stun_duration),
    0x40a372b6: ('can_un_stun', _decode_can_un_stun),
    0x1ac813b9: ('minimum_stunned_time', _decode_minimum_stunned_time),
    0xbae2755e: ('re_stun_delay', _decode_re_stun_delay),
    0xc431344: ('apply_boost_after_un_stun', _decode_apply_boost_after_un_stun),
    0x197779d1: ('apply_boost_after_stun', _decode_apply_boost_after_stun),
    0xba4972fe: ('boost_duration', _decode_boost_duration),
    0x85d39cb7: ('boost_speed_modifier', _decode_boost_speed_modifier),
    0x38711325: ('stun_only_when_on_ground', _decode_stun_only_when_on_ground),
    0xe38a723d: ('knockback_instead_of_stun', _decode_knockback_instead_of_stun),
}

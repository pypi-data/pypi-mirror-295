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
    class PlayerPeanutGunDataJson(typing_extensions.TypedDict):
        is_peanut_gun_owner: bool
        fire_height_offset: float
        can_fire_when_mounted_to_dk: bool
        can_fire_when_mounted_to_rambi: bool
        can_fire_when_mounted_to_dk_on_rambi: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xe0f206d, 0xe02fada2, 0x5574a8ed, 0xe743b2a5, 0xceb209b7)


@dataclasses.dataclass()
class PlayerPeanutGunData(BaseProperty):
    is_peanut_gun_owner: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0e0f206d, original_name='IsPeanutGunOwner'
        ),
    })
    fire_height_offset: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe02fada2, original_name='FireHeightOffset'
        ),
    })
    can_fire_when_mounted_to_dk: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5574a8ed, original_name='CanFireWhenMountedToDK'
        ),
    })
    can_fire_when_mounted_to_rambi: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe743b2a5, original_name='CanFireWhenMountedToRambi'
        ),
    })
    can_fire_when_mounted_to_dk_on_rambi: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xceb209b7, original_name='CanFireWhenMountedToDKOnRambi'
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
            _FAST_FORMAT = struct.Struct('>LH?LHfLH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(38))
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

        data.write(b'\x0e\x0f m')  # 0xe0f206d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_peanut_gun_owner))

        data.write(b'\xe0/\xad\xa2')  # 0xe02fada2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fire_height_offset))

        data.write(b'Ut\xa8\xed')  # 0x5574a8ed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_fire_when_mounted_to_dk))

        data.write(b'\xe7C\xb2\xa5')  # 0xe743b2a5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_fire_when_mounted_to_rambi))

        data.write(b'\xce\xb2\t\xb7')  # 0xceb209b7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_fire_when_mounted_to_dk_on_rambi))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerPeanutGunDataJson", data)
        return cls(
            is_peanut_gun_owner=json_data['is_peanut_gun_owner'],
            fire_height_offset=json_data['fire_height_offset'],
            can_fire_when_mounted_to_dk=json_data['can_fire_when_mounted_to_dk'],
            can_fire_when_mounted_to_rambi=json_data['can_fire_when_mounted_to_rambi'],
            can_fire_when_mounted_to_dk_on_rambi=json_data['can_fire_when_mounted_to_dk_on_rambi'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'is_peanut_gun_owner': self.is_peanut_gun_owner,
            'fire_height_offset': self.fire_height_offset,
            'can_fire_when_mounted_to_dk': self.can_fire_when_mounted_to_dk,
            'can_fire_when_mounted_to_rambi': self.can_fire_when_mounted_to_rambi,
            'can_fire_when_mounted_to_dk_on_rambi': self.can_fire_when_mounted_to_dk_on_rambi,
        }


def _decode_is_peanut_gun_owner(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fire_height_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_fire_when_mounted_to_dk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_fire_when_mounted_to_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_fire_when_mounted_to_dk_on_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe0f206d: ('is_peanut_gun_owner', _decode_is_peanut_gun_owner),
    0xe02fada2: ('fire_height_offset', _decode_fire_height_offset),
    0x5574a8ed: ('can_fire_when_mounted_to_dk', _decode_can_fire_when_mounted_to_dk),
    0xe743b2a5: ('can_fire_when_mounted_to_rambi', _decode_can_fire_when_mounted_to_rambi),
    0xceb209b7: ('can_fire_when_mounted_to_dk_on_rambi', _decode_can_fire_when_mounted_to_dk_on_rambi),
}

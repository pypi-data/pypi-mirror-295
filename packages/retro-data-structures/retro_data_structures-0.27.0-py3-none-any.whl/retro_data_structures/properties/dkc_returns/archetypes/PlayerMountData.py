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
    class PlayerMountDataJson(typing_extensions.TypedDict):
        unknown_0x2b70fd04: int
        unknown_0x138bac93: int
        can_mount_rider: bool
        can_dismount_rider: bool
        rider_must_be_falling: bool
        rider_must_be_above_mount: bool
        slaves_can_trigger_mount: bool
        mount_radius: float
        mount_lerp_speed: float
        dismount_disable_time: float
        dismount_riders_on_death_fall: bool
        allow_struggle_interaction: bool
        should_riders_interact_with_triggers: bool
        riders_handle_their_own_contact: bool
        disallow_recently_grab_detached: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x2b70fd04, 0x138bac93, 0xdd96e915, 0xe5fcd8db, 0x16a4ba22, 0x1e1d08f4, 0x426980fc, 0x73ee7ec2, 0x7abd556d, 0x15e63783, 0x1a518928, 0xdbd1e3bf, 0x4fa972d1, 0x4b79dba9, 0xf98eb36c)


@dataclasses.dataclass()
class PlayerMountData(BaseProperty):
    unknown_0x2b70fd04: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x2b70fd04, original_name='Unknown'
        ),
    })
    unknown_0x138bac93: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x138bac93, original_name='Unknown'
        ),
    })
    can_mount_rider: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdd96e915, original_name='CanMountRider'
        ),
    })
    can_dismount_rider: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe5fcd8db, original_name='CanDismountRider'
        ),
    })
    rider_must_be_falling: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x16a4ba22, original_name='RiderMustBeFalling'
        ),
    })
    rider_must_be_above_mount: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1e1d08f4, original_name='RiderMustBeAboveMount'
        ),
    })
    slaves_can_trigger_mount: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x426980fc, original_name='SlavesCanTriggerMount'
        ),
    })
    mount_radius: float = dataclasses.field(default=1.100000023841858, metadata={
        'reflection': FieldReflection[float](
            float, id=0x73ee7ec2, original_name='MountRadius'
        ),
    })
    mount_lerp_speed: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7abd556d, original_name='MountLerpSpeed'
        ),
    })
    dismount_disable_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x15e63783, original_name='DismountDisableTime'
        ),
    })
    dismount_riders_on_death_fall: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1a518928, original_name='DismountRidersOnDeathFall'
        ),
    })
    allow_struggle_interaction: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdbd1e3bf, original_name='AllowStruggleInteraction'
        ),
    })
    should_riders_interact_with_triggers: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4fa972d1, original_name='ShouldRidersInteractWithTriggers'
        ),
    })
    riders_handle_their_own_contact: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4b79dba9, original_name='RidersHandleTheirOwnContact'
        ),
    })
    disallow_recently_grab_detached: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf98eb36c, original_name='DisallowRecentlyGrabDetached'
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
        if property_count != 15:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHlLHlLH?LH?LH?LH?LH?LHfLHfLHfLH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(120))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42]) == _FAST_IDS
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
            dec[38],
            dec[41],
            dec[44],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'+p\xfd\x04')  # 0x2b70fd04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x2b70fd04))

        data.write(b'\x13\x8b\xac\x93')  # 0x138bac93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x138bac93))

        data.write(b'\xdd\x96\xe9\x15')  # 0xdd96e915
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_mount_rider))

        data.write(b'\xe5\xfc\xd8\xdb')  # 0xe5fcd8db
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_dismount_rider))

        data.write(b'\x16\xa4\xba"')  # 0x16a4ba22
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rider_must_be_falling))

        data.write(b'\x1e\x1d\x08\xf4')  # 0x1e1d08f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.rider_must_be_above_mount))

        data.write(b'Bi\x80\xfc')  # 0x426980fc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.slaves_can_trigger_mount))

        data.write(b's\xee~\xc2')  # 0x73ee7ec2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mount_radius))

        data.write(b'z\xbdUm')  # 0x7abd556d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mount_lerp_speed))

        data.write(b'\x15\xe67\x83')  # 0x15e63783
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dismount_disable_time))

        data.write(b'\x1aQ\x89(')  # 0x1a518928
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.dismount_riders_on_death_fall))

        data.write(b'\xdb\xd1\xe3\xbf')  # 0xdbd1e3bf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_struggle_interaction))

        data.write(b'O\xa9r\xd1')  # 0x4fa972d1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_riders_interact_with_triggers))

        data.write(b'Ky\xdb\xa9')  # 0x4b79dba9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.riders_handle_their_own_contact))

        data.write(b'\xf9\x8e\xb3l')  # 0xf98eb36c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disallow_recently_grab_detached))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerMountDataJson", data)
        return cls(
            unknown_0x2b70fd04=json_data['unknown_0x2b70fd04'],
            unknown_0x138bac93=json_data['unknown_0x138bac93'],
            can_mount_rider=json_data['can_mount_rider'],
            can_dismount_rider=json_data['can_dismount_rider'],
            rider_must_be_falling=json_data['rider_must_be_falling'],
            rider_must_be_above_mount=json_data['rider_must_be_above_mount'],
            slaves_can_trigger_mount=json_data['slaves_can_trigger_mount'],
            mount_radius=json_data['mount_radius'],
            mount_lerp_speed=json_data['mount_lerp_speed'],
            dismount_disable_time=json_data['dismount_disable_time'],
            dismount_riders_on_death_fall=json_data['dismount_riders_on_death_fall'],
            allow_struggle_interaction=json_data['allow_struggle_interaction'],
            should_riders_interact_with_triggers=json_data['should_riders_interact_with_triggers'],
            riders_handle_their_own_contact=json_data['riders_handle_their_own_contact'],
            disallow_recently_grab_detached=json_data['disallow_recently_grab_detached'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x2b70fd04': self.unknown_0x2b70fd04,
            'unknown_0x138bac93': self.unknown_0x138bac93,
            'can_mount_rider': self.can_mount_rider,
            'can_dismount_rider': self.can_dismount_rider,
            'rider_must_be_falling': self.rider_must_be_falling,
            'rider_must_be_above_mount': self.rider_must_be_above_mount,
            'slaves_can_trigger_mount': self.slaves_can_trigger_mount,
            'mount_radius': self.mount_radius,
            'mount_lerp_speed': self.mount_lerp_speed,
            'dismount_disable_time': self.dismount_disable_time,
            'dismount_riders_on_death_fall': self.dismount_riders_on_death_fall,
            'allow_struggle_interaction': self.allow_struggle_interaction,
            'should_riders_interact_with_triggers': self.should_riders_interact_with_triggers,
            'riders_handle_their_own_contact': self.riders_handle_their_own_contact,
            'disallow_recently_grab_detached': self.disallow_recently_grab_detached,
        }


def _decode_unknown_0x2b70fd04(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x138bac93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_can_mount_rider(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_dismount_rider(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rider_must_be_falling(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rider_must_be_above_mount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_slaves_can_trigger_mount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_mount_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mount_lerp_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dismount_disable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dismount_riders_on_death_fall(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_struggle_interaction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_should_riders_interact_with_triggers(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_riders_handle_their_own_contact(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disallow_recently_grab_detached(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2b70fd04: ('unknown_0x2b70fd04', _decode_unknown_0x2b70fd04),
    0x138bac93: ('unknown_0x138bac93', _decode_unknown_0x138bac93),
    0xdd96e915: ('can_mount_rider', _decode_can_mount_rider),
    0xe5fcd8db: ('can_dismount_rider', _decode_can_dismount_rider),
    0x16a4ba22: ('rider_must_be_falling', _decode_rider_must_be_falling),
    0x1e1d08f4: ('rider_must_be_above_mount', _decode_rider_must_be_above_mount),
    0x426980fc: ('slaves_can_trigger_mount', _decode_slaves_can_trigger_mount),
    0x73ee7ec2: ('mount_radius', _decode_mount_radius),
    0x7abd556d: ('mount_lerp_speed', _decode_mount_lerp_speed),
    0x15e63783: ('dismount_disable_time', _decode_dismount_disable_time),
    0x1a518928: ('dismount_riders_on_death_fall', _decode_dismount_riders_on_death_fall),
    0xdbd1e3bf: ('allow_struggle_interaction', _decode_allow_struggle_interaction),
    0x4fa972d1: ('should_riders_interact_with_triggers', _decode_should_riders_interact_with_triggers),
    0x4b79dba9: ('riders_handle_their_own_contact', _decode_riders_handle_their_own_contact),
    0xf98eb36c: ('disallow_recently_grab_detached', _decode_disallow_recently_grab_detached),
}

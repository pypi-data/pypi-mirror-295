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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType

if typing.TYPE_CHECKING:
    class PlayerMountRiderDataJson(typing_extensions.TypedDict):
        character_type: json_util.JsonObject
        mount_locator: str
        alternate_mount_locator: str
        allow_butt_slap_interaction: bool
        allow_grab_detach: bool
        allow_crouch: bool
        generate_arc_motion: bool
        struggle_turn_priority: int
        optional_lerp_duration: float
    

@dataclasses.dataclass()
class PlayerMountRiderData(BaseProperty):
    character_type: PlayerType = dataclasses.field(default_factory=PlayerType, metadata={
        'reflection': FieldReflection[PlayerType](
            PlayerType, id=0x013e35fb, original_name='CharacterType', from_json=PlayerType.from_json, to_json=PlayerType.to_json
        ),
    })
    mount_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xe7f952bd, original_name='MountLocator'
        ),
    })
    alternate_mount_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xb0f79539, original_name='AlternateMountLocator'
        ),
    })
    allow_butt_slap_interaction: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6a1ba66f, original_name='AllowButtSlapInteraction'
        ),
    })
    allow_grab_detach: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1a2e6372, original_name='AllowGrabDetach'
        ),
    })
    allow_crouch: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xab3627b8, original_name='AllowCrouch'
        ),
    })
    generate_arc_motion: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6cdf8683, original_name='GenerateArcMotion'
        ),
    })
    struggle_turn_priority: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x45e44b4e, original_name='StruggleTurnPriority'
        ),
    })
    optional_lerp_duration: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe829969a, original_name='OptionalLerpDuration'
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
        if property_count != 9:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x013e35fb
        character_type = PlayerType.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe7f952bd
        mount_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0f79539
        alternate_mount_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a1ba66f
        allow_butt_slap_interaction = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1a2e6372
        allow_grab_detach = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab3627b8
        allow_crouch = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6cdf8683
        generate_arc_motion = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x45e44b4e
        struggle_turn_priority = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe829969a
        optional_lerp_duration = struct.unpack('>f', data.read(4))[0]
    
        return cls(character_type, mount_locator, alternate_mount_locator, allow_butt_slap_interaction, allow_grab_detach, allow_crouch, generate_arc_motion, struggle_turn_priority, optional_lerp_duration)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x01>5\xfb')  # 0x13e35fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xf9R\xbd')  # 0xe7f952bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.mount_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xf7\x959')  # 0xb0f79539
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.alternate_mount_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j\x1b\xa6o')  # 0x6a1ba66f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_butt_slap_interaction))

        data.write(b'\x1a.cr')  # 0x1a2e6372
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_grab_detach))

        data.write(b"\xab6'\xb8")  # 0xab3627b8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_crouch))

        data.write(b'l\xdf\x86\x83')  # 0x6cdf8683
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.generate_arc_motion))

        data.write(b'E\xe4KN')  # 0x45e44b4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.struggle_turn_priority))

        data.write(b'\xe8)\x96\x9a')  # 0xe829969a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.optional_lerp_duration))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerMountRiderDataJson", data)
        return cls(
            character_type=PlayerType.from_json(json_data['character_type']),
            mount_locator=json_data['mount_locator'],
            alternate_mount_locator=json_data['alternate_mount_locator'],
            allow_butt_slap_interaction=json_data['allow_butt_slap_interaction'],
            allow_grab_detach=json_data['allow_grab_detach'],
            allow_crouch=json_data['allow_crouch'],
            generate_arc_motion=json_data['generate_arc_motion'],
            struggle_turn_priority=json_data['struggle_turn_priority'],
            optional_lerp_duration=json_data['optional_lerp_duration'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'character_type': self.character_type.to_json(),
            'mount_locator': self.mount_locator,
            'alternate_mount_locator': self.alternate_mount_locator,
            'allow_butt_slap_interaction': self.allow_butt_slap_interaction,
            'allow_grab_detach': self.allow_grab_detach,
            'allow_crouch': self.allow_crouch,
            'generate_arc_motion': self.generate_arc_motion,
            'struggle_turn_priority': self.struggle_turn_priority,
            'optional_lerp_duration': self.optional_lerp_duration,
        }


def _decode_mount_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_alternate_mount_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_allow_butt_slap_interaction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_grab_detach(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_crouch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_generate_arc_motion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_struggle_turn_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_optional_lerp_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13e35fb: ('character_type', PlayerType.from_stream),
    0xe7f952bd: ('mount_locator', _decode_mount_locator),
    0xb0f79539: ('alternate_mount_locator', _decode_alternate_mount_locator),
    0x6a1ba66f: ('allow_butt_slap_interaction', _decode_allow_butt_slap_interaction),
    0x1a2e6372: ('allow_grab_detach', _decode_allow_grab_detach),
    0xab3627b8: ('allow_crouch', _decode_allow_crouch),
    0x6cdf8683: ('generate_arc_motion', _decode_generate_arc_motion),
    0x45e44b4e: ('struggle_turn_priority', _decode_struggle_turn_priority),
    0xe829969a: ('optional_lerp_duration', _decode_optional_lerp_duration),
}

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
    class UnknownStruct142Json(typing_extensions.TypedDict):
        unknown_0x0100cedd: bool
        disable_cling: bool
        unknown_0x12aada70: bool
        disable_grab_barrel: bool
        disable_ground_pound: bool
        disable_jump: bool
        disable_movement: bool
        disable_peanut_gun: bool
        unknown_0x8e028566: bool
        disable_swing: bool
        disable_turns: bool
        disable_offscreen_indicator: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x100cedd, 0x22195fbb, 0x12aada70, 0x652136c9, 0x79b86562, 0x140e99c2, 0x395eff6a, 0xa5ace799, 0x8e028566, 0xaf0830b7, 0x79f5a375, 0xdb565031)


@dataclasses.dataclass()
class UnknownStruct142(BaseProperty):
    unknown_0x0100cedd: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0100cedd, original_name='Unknown'
        ),
    })
    disable_cling: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x22195fbb, original_name='DisableCling'
        ),
    })
    unknown_0x12aada70: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x12aada70, original_name='Unknown'
        ),
    })
    disable_grab_barrel: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x652136c9, original_name='DisableGrabBarrel'
        ),
    })
    disable_ground_pound: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x79b86562, original_name='DisableGroundPound'
        ),
    })
    disable_jump: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x140e99c2, original_name='DisableJump'
        ),
    })
    disable_movement: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x395eff6a, original_name='DisableMovement'
        ),
    })
    disable_peanut_gun: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa5ace799, original_name='DisablePeanutGun'
        ),
    })
    unknown_0x8e028566: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8e028566, original_name='Unknown'
        ),
    })
    disable_swing: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xaf0830b7, original_name='DisableSwing'
        ),
    })
    disable_turns: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x79f5a375, original_name='DisableTurns'
        ),
    })
    disable_offscreen_indicator: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdb565031, original_name='DisableOffscreenIndicator'
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
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(84))
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

        data.write(b'\x01\x00\xce\xdd')  # 0x100cedd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x0100cedd))

        data.write(b'"\x19_\xbb')  # 0x22195fbb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_cling))

        data.write(b'\x12\xaa\xdap')  # 0x12aada70
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x12aada70))

        data.write(b'e!6\xc9')  # 0x652136c9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_grab_barrel))

        data.write(b'y\xb8eb')  # 0x79b86562
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_ground_pound))

        data.write(b'\x14\x0e\x99\xc2')  # 0x140e99c2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_jump))

        data.write(b'9^\xffj')  # 0x395eff6a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_movement))

        data.write(b'\xa5\xac\xe7\x99')  # 0xa5ace799
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_peanut_gun))

        data.write(b'\x8e\x02\x85f')  # 0x8e028566
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8e028566))

        data.write(b'\xaf\x080\xb7')  # 0xaf0830b7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_swing))

        data.write(b'y\xf5\xa3u')  # 0x79f5a375
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_turns))

        data.write(b'\xdbVP1')  # 0xdb565031
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_offscreen_indicator))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct142Json", data)
        return cls(
            unknown_0x0100cedd=json_data['unknown_0x0100cedd'],
            disable_cling=json_data['disable_cling'],
            unknown_0x12aada70=json_data['unknown_0x12aada70'],
            disable_grab_barrel=json_data['disable_grab_barrel'],
            disable_ground_pound=json_data['disable_ground_pound'],
            disable_jump=json_data['disable_jump'],
            disable_movement=json_data['disable_movement'],
            disable_peanut_gun=json_data['disable_peanut_gun'],
            unknown_0x8e028566=json_data['unknown_0x8e028566'],
            disable_swing=json_data['disable_swing'],
            disable_turns=json_data['disable_turns'],
            disable_offscreen_indicator=json_data['disable_offscreen_indicator'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x0100cedd': self.unknown_0x0100cedd,
            'disable_cling': self.disable_cling,
            'unknown_0x12aada70': self.unknown_0x12aada70,
            'disable_grab_barrel': self.disable_grab_barrel,
            'disable_ground_pound': self.disable_ground_pound,
            'disable_jump': self.disable_jump,
            'disable_movement': self.disable_movement,
            'disable_peanut_gun': self.disable_peanut_gun,
            'unknown_0x8e028566': self.unknown_0x8e028566,
            'disable_swing': self.disable_swing,
            'disable_turns': self.disable_turns,
            'disable_offscreen_indicator': self.disable_offscreen_indicator,
        }


def _decode_unknown_0x0100cedd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_cling(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x12aada70(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_grab_barrel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_movement(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_peanut_gun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x8e028566(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_swing(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_turns(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_offscreen_indicator(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x100cedd: ('unknown_0x0100cedd', _decode_unknown_0x0100cedd),
    0x22195fbb: ('disable_cling', _decode_disable_cling),
    0x12aada70: ('unknown_0x12aada70', _decode_unknown_0x12aada70),
    0x652136c9: ('disable_grab_barrel', _decode_disable_grab_barrel),
    0x79b86562: ('disable_ground_pound', _decode_disable_ground_pound),
    0x140e99c2: ('disable_jump', _decode_disable_jump),
    0x395eff6a: ('disable_movement', _decode_disable_movement),
    0xa5ace799: ('disable_peanut_gun', _decode_disable_peanut_gun),
    0x8e028566: ('unknown_0x8e028566', _decode_unknown_0x8e028566),
    0xaf0830b7: ('disable_swing', _decode_disable_swing),
    0x79f5a375: ('disable_turns', _decode_disable_turns),
    0xdb565031: ('disable_offscreen_indicator', _decode_disable_offscreen_indicator),
}

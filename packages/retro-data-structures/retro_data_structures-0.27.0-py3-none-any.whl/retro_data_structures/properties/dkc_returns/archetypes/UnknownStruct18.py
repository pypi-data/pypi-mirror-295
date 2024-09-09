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
    class UnknownStruct18Json(typing_extensions.TypedDict):
        slave_platform_motion_knots: bool
        slave_position_in_local_space: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x3a68ee5c, 0x44b331ec)


@dataclasses.dataclass()
class UnknownStruct18(BaseProperty):
    slave_platform_motion_knots: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3a68ee5c, original_name='SlavePlatformMotionKnots'
        ),
    })
    slave_position_in_local_space: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x44b331ec, original_name='SlavePositionInLocalSpace'
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
        if property_count != 2:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(14))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b':h\xee\\')  # 0x3a68ee5c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.slave_platform_motion_knots))

        data.write(b'D\xb31\xec')  # 0x44b331ec
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.slave_position_in_local_space))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct18Json", data)
        return cls(
            slave_platform_motion_knots=json_data['slave_platform_motion_knots'],
            slave_position_in_local_space=json_data['slave_position_in_local_space'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'slave_platform_motion_knots': self.slave_platform_motion_knots,
            'slave_position_in_local_space': self.slave_position_in_local_space,
        }


def _decode_slave_platform_motion_knots(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_slave_position_in_local_space(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3a68ee5c: ('slave_platform_motion_knots', _decode_slave_platform_motion_knots),
    0x44b331ec: ('slave_position_in_local_space', _decode_slave_position_in_local_space),
}

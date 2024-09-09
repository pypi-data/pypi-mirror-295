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
    class UnknownStruct22Json(typing_extensions.TypedDict):
        destroy_timer: float
        respawn_offscreen: bool
        offscreen_respawn_distance: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x21970404, 0x10d28308, 0x27654f46)


@dataclasses.dataclass()
class UnknownStruct22(BaseProperty):
    destroy_timer: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x21970404, original_name='DestroyTimer'
        ),
    })
    respawn_offscreen: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x10d28308, original_name='RespawnOffscreen'
        ),
    })
    offscreen_respawn_distance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x27654f46, original_name='OffscreenRespawnDistance'
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
        if property_count != 3:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLH?LHf')
    
        dec = _FAST_FORMAT.unpack(data.read(27))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'!\x97\x04\x04')  # 0x21970404
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.destroy_timer))

        data.write(b'\x10\xd2\x83\x08')  # 0x10d28308
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.respawn_offscreen))

        data.write(b"'eOF")  # 0x27654f46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.offscreen_respawn_distance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct22Json", data)
        return cls(
            destroy_timer=json_data['destroy_timer'],
            respawn_offscreen=json_data['respawn_offscreen'],
            offscreen_respawn_distance=json_data['offscreen_respawn_distance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'destroy_timer': self.destroy_timer,
            'respawn_offscreen': self.respawn_offscreen,
            'offscreen_respawn_distance': self.offscreen_respawn_distance,
        }


def _decode_destroy_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_respawn_offscreen(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offscreen_respawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x21970404: ('destroy_timer', _decode_destroy_timer),
    0x10d28308: ('respawn_offscreen', _decode_respawn_offscreen),
    0x27654f46: ('offscreen_respawn_distance', _decode_offscreen_respawn_distance),
}

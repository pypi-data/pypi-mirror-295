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
    class VerticalFlightBehaviorDataJson(typing_extensions.TypedDict):
        apex_pause_time: float
        no_actor_collision: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x660e0a30, 0x3bb99c78)


@dataclasses.dataclass()
class VerticalFlightBehaviorData(BaseProperty):
    apex_pause_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x660e0a30, original_name='ApexPauseTime'
        ),
    })
    no_actor_collision: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3bb99c78, original_name='NoActorCollision'
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
            _FAST_FORMAT = struct.Struct('>LHfLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(17))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'f\x0e\n0')  # 0x660e0a30
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.apex_pause_time))

        data.write(b';\xb9\x9cx')  # 0x3bb99c78
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.no_actor_collision))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("VerticalFlightBehaviorDataJson", data)
        return cls(
            apex_pause_time=json_data['apex_pause_time'],
            no_actor_collision=json_data['no_actor_collision'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'apex_pause_time': self.apex_pause_time,
            'no_actor_collision': self.no_actor_collision,
        }


def _decode_apex_pause_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_no_actor_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x660e0a30: ('apex_pause_time', _decode_apex_pause_time),
    0x3bb99c78: ('no_actor_collision', _decode_no_actor_collision),
}

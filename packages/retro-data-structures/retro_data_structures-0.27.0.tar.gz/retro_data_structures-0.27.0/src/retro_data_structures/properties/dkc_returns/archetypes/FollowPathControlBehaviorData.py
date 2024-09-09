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
    class FollowPathControlBehaviorDataJson(typing_extensions.TypedDict):
        reverse_movement: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xffe201a7)


@dataclasses.dataclass()
class FollowPathControlBehaviorData(BaseProperty):
    reverse_movement: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xffe201a7, original_name='ReverseMovement'
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
        if property_count != 1:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(7))
        assert (dec[0]) == _FAST_IDS
        return cls(
            dec[2],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\xff\xe2\x01\xa7')  # 0xffe201a7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.reverse_movement))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("FollowPathControlBehaviorDataJson", data)
        return cls(
            reverse_movement=json_data['reverse_movement'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'reverse_movement': self.reverse_movement,
        }


def _decode_reverse_movement(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xffe201a7: ('reverse_movement', _decode_reverse_movement),
}

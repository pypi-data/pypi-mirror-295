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
import retro_data_structures.enums.dkc_returns as enums

if typing.TYPE_CHECKING:
    class GenericCreatureStructDJson(typing_extensions.TypedDict):
        message: int
        behavior: int
        set: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x13834d6f, 0xd18215aa, 0xb3f7a00)


@dataclasses.dataclass()
class GenericCreatureStructD(BaseProperty):
    message: enums.Message = dataclasses.field(default=enums.Message.Unknown10, metadata={
        'reflection': FieldReflection[enums.Message](
            enums.Message, id=0x13834d6f, original_name='Message', from_json=enums.Message.from_json, to_json=enums.Message.to_json
        ),
    })
    behavior: enums.Behavior = dataclasses.field(default=enums.Behavior.Unknown1, metadata={
        'reflection': FieldReflection[enums.Behavior](
            enums.Behavior, id=0xd18215aa, original_name='Behavior', from_json=enums.Behavior.from_json, to_json=enums.Behavior.to_json
        ),
    })
    set: enums.Set = dataclasses.field(default=enums.Set.Unknown1, metadata={
        'reflection': FieldReflection[enums.Set](
            enums.Set, id=0x0b3f7a00, original_name='Set', from_json=enums.Set.from_json, to_json=enums.Set.to_json
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
            _FAST_FORMAT = struct.Struct('>LHLLHLLHL')
    
        dec = _FAST_FORMAT.unpack(data.read(30))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            enums.Message(dec[2]),
            enums.Behavior(dec[5]),
            enums.Set(dec[8]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x13\x83Mo')  # 0x13834d6f
        data.write(b'\x00\x04')  # size
        self.message.to_stream(data)

        data.write(b'\xd1\x82\x15\xaa')  # 0xd18215aa
        data.write(b'\x00\x04')  # size
        self.behavior.to_stream(data)

        data.write(b'\x0b?z\x00')  # 0xb3f7a00
        data.write(b'\x00\x04')  # size
        self.set.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GenericCreatureStructDJson", data)
        return cls(
            message=enums.Message.from_json(json_data['message']),
            behavior=enums.Behavior.from_json(json_data['behavior']),
            set=enums.Set.from_json(json_data['set']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'message': self.message.to_json(),
            'behavior': self.behavior.to_json(),
            'set': self.set.to_json(),
        }


def _decode_message(data: typing.BinaryIO, property_size: int):
    return enums.Message.from_stream(data)


def _decode_behavior(data: typing.BinaryIO, property_size: int):
    return enums.Behavior.from_stream(data)


def _decode_set(data: typing.BinaryIO, property_size: int):
    return enums.Set.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13834d6f: ('message', _decode_message),
    0xd18215aa: ('behavior', _decode_behavior),
    0xb3f7a00: ('set', _decode_set),
}

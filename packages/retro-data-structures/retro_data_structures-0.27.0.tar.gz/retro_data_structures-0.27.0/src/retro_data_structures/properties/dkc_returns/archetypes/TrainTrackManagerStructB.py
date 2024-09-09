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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct272 import UnknownStruct272

if typing.TYPE_CHECKING:
    class TrainTrackManagerStructBJson(typing_extensions.TypedDict):
        debug_name: str
        chain_string: str
        unknown_struct272: json_util.JsonObject
    

@dataclasses.dataclass()
class TrainTrackManagerStructB(BaseProperty):
    debug_name: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xbd0b7ede, original_name='DebugName'
        ),
    })
    chain_string: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xfcab0249, original_name='ChainString'
        ),
    })
    unknown_struct272: UnknownStruct272 = dataclasses.field(default_factory=UnknownStruct272, metadata={
        'reflection': FieldReflection[UnknownStruct272](
            UnknownStruct272, id=0x31770d3f, original_name='UnknownStruct272', from_json=UnknownStruct272.from_json, to_json=UnknownStruct272.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbd0b7ede
        debug_name = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfcab0249
        chain_string = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x31770d3f
        unknown_struct272 = UnknownStruct272.from_stream(data, property_size)
    
        return cls(debug_name, chain_string, unknown_struct272)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xbd\x0b~\xde')  # 0xbd0b7ede
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.debug_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\xab\x02I')  # 0xfcab0249
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.chain_string.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1w\r?')  # 0x31770d3f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct272.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TrainTrackManagerStructBJson", data)
        return cls(
            debug_name=json_data['debug_name'],
            chain_string=json_data['chain_string'],
            unknown_struct272=UnknownStruct272.from_json(json_data['unknown_struct272']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'debug_name': self.debug_name,
            'chain_string': self.chain_string,
            'unknown_struct272': self.unknown_struct272.to_json(),
        }


def _decode_debug_name(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_chain_string(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbd0b7ede: ('debug_name', _decode_debug_name),
    0xfcab0249: ('chain_string', _decode_chain_string),
    0x31770d3f: ('unknown_struct272', UnknownStruct272.from_stream),
}

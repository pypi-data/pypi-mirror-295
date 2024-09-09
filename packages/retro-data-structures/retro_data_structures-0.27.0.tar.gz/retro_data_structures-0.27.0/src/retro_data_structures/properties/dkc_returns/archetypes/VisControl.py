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
    class VisControlJson(typing_extensions.TypedDict):
        number_of_strings: int
        string1: str
        string2: str
        string3: str
    

@dataclasses.dataclass()
class VisControl(BaseProperty):
    number_of_strings: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xddecee96, original_name='NumberOfStrings'
        ),
    })
    string1: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x87dcd2b9, original_name='String1'
        ),
    })
    string2: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xb634c824, original_name='String2'
        ),
    })
    string3: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x1043c390, original_name='String3'
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
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xddecee96
        number_of_strings = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x87dcd2b9
        string1 = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb634c824
        string2 = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1043c390
        string3 = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(number_of_strings, string1, string2, string3)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xdd\xec\xee\x96')  # 0xddecee96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_strings))

        data.write(b'\x87\xdc\xd2\xb9')  # 0x87dcd2b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.string1.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb64\xc8$')  # 0xb634c824
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.string2.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10C\xc3\x90')  # 0x1043c390
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.string3.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("VisControlJson", data)
        return cls(
            number_of_strings=json_data['number_of_strings'],
            string1=json_data['string1'],
            string2=json_data['string2'],
            string3=json_data['string3'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_strings': self.number_of_strings,
            'string1': self.string1,
            'string2': self.string2,
            'string3': self.string3,
        }


def _decode_number_of_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_string1(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_string2(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_string3(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xddecee96: ('number_of_strings', _decode_number_of_strings),
    0x87dcd2b9: ('string1', _decode_string1),
    0xb634c824: ('string2', _decode_string2),
    0x1043c390: ('string3', _decode_string3),
}

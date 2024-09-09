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
    class UnknownStruct232Json(typing_extensions.TypedDict):
        unknown_0x4cd75db8: float
        unknown_0xefee802b: float
        unknown_0x50ad6480: str
    

@dataclasses.dataclass()
class UnknownStruct232(BaseProperty):
    unknown_0x4cd75db8: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4cd75db8, original_name='Unknown'
        ),
    })
    unknown_0xefee802b: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xefee802b, original_name='Unknown'
        ),
    })
    unknown_0x50ad6480: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x50ad6480, original_name='Unknown'
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
        assert property_id == 0x4cd75db8
        unknown_0x4cd75db8 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xefee802b
        unknown_0xefee802b = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50ad6480
        unknown_0x50ad6480 = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(unknown_0x4cd75db8, unknown_0xefee802b, unknown_0x50ad6480)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'L\xd7]\xb8')  # 0x4cd75db8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4cd75db8))

        data.write(b'\xef\xee\x80+')  # 0xefee802b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xefee802b))

        data.write(b'P\xadd\x80')  # 0x50ad6480
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x50ad6480.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct232Json", data)
        return cls(
            unknown_0x4cd75db8=json_data['unknown_0x4cd75db8'],
            unknown_0xefee802b=json_data['unknown_0xefee802b'],
            unknown_0x50ad6480=json_data['unknown_0x50ad6480'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x4cd75db8': self.unknown_0x4cd75db8,
            'unknown_0xefee802b': self.unknown_0xefee802b,
            'unknown_0x50ad6480': self.unknown_0x50ad6480,
        }


def _decode_unknown_0x4cd75db8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xefee802b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x50ad6480(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4cd75db8: ('unknown_0x4cd75db8', _decode_unknown_0x4cd75db8),
    0xefee802b: ('unknown_0xefee802b', _decode_unknown_0xefee802b),
    0x50ad6480: ('unknown_0x50ad6480', _decode_unknown_0x50ad6480),
}

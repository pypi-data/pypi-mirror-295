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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct53 import UnknownStruct53
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct54 import UnknownStruct54

if typing.TYPE_CHECKING:
    class UnknownStruct55Json(typing_extensions.TypedDict):
        frequency: float
        unknown_struct54_0x8772cb7e: json_util.JsonObject
        unknown_struct54_0x3cadcc64: json_util.JsonObject
        number_of_choices: int
        unknown_struct53_0x5e856665: json_util.JsonObject
        unknown_struct53_0xed114ba6: json_util.JsonObject
        unknown_struct53_0x839d50e7: json_util.JsonObject
        unknown_struct53_0x51481661: json_util.JsonObject
        unknown_struct53_0x3fc40d20: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct55(BaseProperty):
    frequency: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x98cbfedc, original_name='Frequency'
        ),
    })
    unknown_struct54_0x8772cb7e: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54, metadata={
        'reflection': FieldReflection[UnknownStruct54](
            UnknownStruct54, id=0x8772cb7e, original_name='UnknownStruct54', from_json=UnknownStruct54.from_json, to_json=UnknownStruct54.to_json
        ),
    })
    unknown_struct54_0x3cadcc64: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54, metadata={
        'reflection': FieldReflection[UnknownStruct54](
            UnknownStruct54, id=0x3cadcc64, original_name='UnknownStruct54', from_json=UnknownStruct54.from_json, to_json=UnknownStruct54.to_json
        ),
    })
    number_of_choices: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x9156ba5f, original_name='NumberOfChoices'
        ),
    })
    unknown_struct53_0x5e856665: UnknownStruct53 = dataclasses.field(default_factory=UnknownStruct53, metadata={
        'reflection': FieldReflection[UnknownStruct53](
            UnknownStruct53, id=0x5e856665, original_name='UnknownStruct53', from_json=UnknownStruct53.from_json, to_json=UnknownStruct53.to_json
        ),
    })
    unknown_struct53_0xed114ba6: UnknownStruct53 = dataclasses.field(default_factory=UnknownStruct53, metadata={
        'reflection': FieldReflection[UnknownStruct53](
            UnknownStruct53, id=0xed114ba6, original_name='UnknownStruct53', from_json=UnknownStruct53.from_json, to_json=UnknownStruct53.to_json
        ),
    })
    unknown_struct53_0x839d50e7: UnknownStruct53 = dataclasses.field(default_factory=UnknownStruct53, metadata={
        'reflection': FieldReflection[UnknownStruct53](
            UnknownStruct53, id=0x839d50e7, original_name='UnknownStruct53', from_json=UnknownStruct53.from_json, to_json=UnknownStruct53.to_json
        ),
    })
    unknown_struct53_0x51481661: UnknownStruct53 = dataclasses.field(default_factory=UnknownStruct53, metadata={
        'reflection': FieldReflection[UnknownStruct53](
            UnknownStruct53, id=0x51481661, original_name='UnknownStruct53', from_json=UnknownStruct53.from_json, to_json=UnknownStruct53.to_json
        ),
    })
    unknown_struct53_0x3fc40d20: UnknownStruct53 = dataclasses.field(default_factory=UnknownStruct53, metadata={
        'reflection': FieldReflection[UnknownStruct53](
            UnknownStruct53, id=0x3fc40d20, original_name='UnknownStruct53', from_json=UnknownStruct53.from_json, to_json=UnknownStruct53.to_json
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
        assert property_id == 0x98cbfedc
        frequency = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8772cb7e
        unknown_struct54_0x8772cb7e = UnknownStruct54.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3cadcc64
        unknown_struct54_0x3cadcc64 = UnknownStruct54.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9156ba5f
        number_of_choices = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e856665
        unknown_struct53_0x5e856665 = UnknownStruct53.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xed114ba6
        unknown_struct53_0xed114ba6 = UnknownStruct53.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x839d50e7
        unknown_struct53_0x839d50e7 = UnknownStruct53.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x51481661
        unknown_struct53_0x51481661 = UnknownStruct53.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3fc40d20
        unknown_struct53_0x3fc40d20 = UnknownStruct53.from_stream(data, property_size)
    
        return cls(frequency, unknown_struct54_0x8772cb7e, unknown_struct54_0x3cadcc64, number_of_choices, unknown_struct53_0x5e856665, unknown_struct53_0xed114ba6, unknown_struct53_0x839d50e7, unknown_struct53_0x51481661, unknown_struct53_0x3fc40d20)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x98\xcb\xfe\xdc')  # 0x98cbfedc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.frequency))

        data.write(b'\x87r\xcb~')  # 0x8772cb7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54_0x8772cb7e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<\xad\xccd')  # 0x3cadcc64
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54_0x3cadcc64.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91V\xba_')  # 0x9156ba5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_choices))

        data.write(b'^\x85fe')  # 0x5e856665
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct53_0x5e856665.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\x11K\xa6')  # 0xed114ba6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct53_0xed114ba6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83\x9dP\xe7')  # 0x839d50e7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct53_0x839d50e7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'QH\x16a')  # 0x51481661
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct53_0x51481661.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\xc4\r ')  # 0x3fc40d20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct53_0x3fc40d20.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct55Json", data)
        return cls(
            frequency=json_data['frequency'],
            unknown_struct54_0x8772cb7e=UnknownStruct54.from_json(json_data['unknown_struct54_0x8772cb7e']),
            unknown_struct54_0x3cadcc64=UnknownStruct54.from_json(json_data['unknown_struct54_0x3cadcc64']),
            number_of_choices=json_data['number_of_choices'],
            unknown_struct53_0x5e856665=UnknownStruct53.from_json(json_data['unknown_struct53_0x5e856665']),
            unknown_struct53_0xed114ba6=UnknownStruct53.from_json(json_data['unknown_struct53_0xed114ba6']),
            unknown_struct53_0x839d50e7=UnknownStruct53.from_json(json_data['unknown_struct53_0x839d50e7']),
            unknown_struct53_0x51481661=UnknownStruct53.from_json(json_data['unknown_struct53_0x51481661']),
            unknown_struct53_0x3fc40d20=UnknownStruct53.from_json(json_data['unknown_struct53_0x3fc40d20']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'frequency': self.frequency,
            'unknown_struct54_0x8772cb7e': self.unknown_struct54_0x8772cb7e.to_json(),
            'unknown_struct54_0x3cadcc64': self.unknown_struct54_0x3cadcc64.to_json(),
            'number_of_choices': self.number_of_choices,
            'unknown_struct53_0x5e856665': self.unknown_struct53_0x5e856665.to_json(),
            'unknown_struct53_0xed114ba6': self.unknown_struct53_0xed114ba6.to_json(),
            'unknown_struct53_0x839d50e7': self.unknown_struct53_0x839d50e7.to_json(),
            'unknown_struct53_0x51481661': self.unknown_struct53_0x51481661.to_json(),
            'unknown_struct53_0x3fc40d20': self.unknown_struct53_0x3fc40d20.to_json(),
        }


def _decode_frequency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_number_of_choices(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x98cbfedc: ('frequency', _decode_frequency),
    0x8772cb7e: ('unknown_struct54_0x8772cb7e', UnknownStruct54.from_stream),
    0x3cadcc64: ('unknown_struct54_0x3cadcc64', UnknownStruct54.from_stream),
    0x9156ba5f: ('number_of_choices', _decode_number_of_choices),
    0x5e856665: ('unknown_struct53_0x5e856665', UnknownStruct53.from_stream),
    0xed114ba6: ('unknown_struct53_0xed114ba6', UnknownStruct53.from_stream),
    0x839d50e7: ('unknown_struct53_0x839d50e7', UnknownStruct53.from_stream),
    0x51481661: ('unknown_struct53_0x51481661', UnknownStruct53.from_stream),
    0x3fc40d20: ('unknown_struct53_0x3fc40d20', UnknownStruct53.from_stream),
}

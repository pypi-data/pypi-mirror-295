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
from retro_data_structures.properties.dkc_returns.archetypes.SeparateAndReformParts import SeparateAndReformParts

if typing.TYPE_CHECKING:
    class SeparateAndReformBehaviorDataJson(typing_extensions.TypedDict):
        number_of_parts: int
        player_relative: bool
        do_not_wait_for_reform: bool
        part1: json_util.JsonObject
        part2: json_util.JsonObject
        part3: json_util.JsonObject
        part4: json_util.JsonObject
        part5: json_util.JsonObject
        part6: json_util.JsonObject
        part7: json_util.JsonObject
        part8: json_util.JsonObject
        part9: json_util.JsonObject
        part10: json_util.JsonObject
    

@dataclasses.dataclass()
class SeparateAndReformBehaviorData(BaseProperty):
    number_of_parts: int = dataclasses.field(default=10, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8b594611, original_name='NumberOfParts'
        ),
    })
    player_relative: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x60be3c08, original_name='PlayerRelative'
        ),
    })
    do_not_wait_for_reform: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x60f7e83f, original_name='DoNotWaitForReform'
        ),
    })
    part1: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0x36a054c3, original_name='Part1', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part2: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0x40456dfe, original_name='Part2', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part3: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0xdb36872a, original_name='Part3', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part4: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0xad8f1f84, original_name='Part4', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part5: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0x36fcf550, original_name='Part5', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part6: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0x4019cc6d, original_name='Part6', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part7: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0xdb6a26b9, original_name='Part7', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part8: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0xad6afd31, original_name='Part8', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part9: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0x361917e5, original_name='Part9', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
        ),
    })
    part10: SeparateAndReformParts = dataclasses.field(default_factory=SeparateAndReformParts, metadata={
        'reflection': FieldReflection[SeparateAndReformParts](
            SeparateAndReformParts, id=0x30c93088, original_name='Part10', from_json=SeparateAndReformParts.from_json, to_json=SeparateAndReformParts.to_json
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
        if property_count != 13:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8b594611
        number_of_parts = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60be3c08
        player_relative = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60f7e83f
        do_not_wait_for_reform = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36a054c3
        part1 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -2.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x40456dfe
        part2 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -4.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb36872a
        part3 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -6.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xad8f1f84
        part4 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -8.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36fcf550
        part5 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -10.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4019cc6d
        part6 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 2.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb6a26b9
        part7 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 4.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xad6afd31
        part8 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 6.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x361917e5
        part9 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 8.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x30c93088
        part10 = SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 10.0})
    
        return cls(number_of_parts, player_relative, do_not_wait_for_reform, part1, part2, part3, part4, part5, part6, part7, part8, part9, part10)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\x8bYF\x11')  # 0x8b594611
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_parts))

        data.write(b'`\xbe<\x08')  # 0x60be3c08
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player_relative))

        data.write(b'`\xf7\xe8?')  # 0x60f7e83f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.do_not_wait_for_reform))

        data.write(b'6\xa0T\xc3')  # 0x36a054c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part1.to_stream(data, default_override={'offset': -2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@Em\xfe')  # 0x40456dfe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part2.to_stream(data, default_override={'offset': -4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdb6\x87*')  # 0xdb36872a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part3.to_stream(data, default_override={'offset': -6.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\x8f\x1f\x84')  # 0xad8f1f84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part4.to_stream(data, default_override={'offset': -8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xfc\xf5P')  # 0x36fcf550
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part5.to_stream(data, default_override={'offset': -10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@\x19\xccm')  # 0x4019cc6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part6.to_stream(data, default_override={'offset': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdbj&\xb9')  # 0xdb6a26b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part7.to_stream(data, default_override={'offset': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xadj\xfd1')  # 0xad6afd31
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part8.to_stream(data, default_override={'offset': 6.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\x19\x17\xe5')  # 0x361917e5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part9.to_stream(data, default_override={'offset': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\xc90\x88')  # 0x30c93088
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.part10.to_stream(data, default_override={'offset': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SeparateAndReformBehaviorDataJson", data)
        return cls(
            number_of_parts=json_data['number_of_parts'],
            player_relative=json_data['player_relative'],
            do_not_wait_for_reform=json_data['do_not_wait_for_reform'],
            part1=SeparateAndReformParts.from_json(json_data['part1']),
            part2=SeparateAndReformParts.from_json(json_data['part2']),
            part3=SeparateAndReformParts.from_json(json_data['part3']),
            part4=SeparateAndReformParts.from_json(json_data['part4']),
            part5=SeparateAndReformParts.from_json(json_data['part5']),
            part6=SeparateAndReformParts.from_json(json_data['part6']),
            part7=SeparateAndReformParts.from_json(json_data['part7']),
            part8=SeparateAndReformParts.from_json(json_data['part8']),
            part9=SeparateAndReformParts.from_json(json_data['part9']),
            part10=SeparateAndReformParts.from_json(json_data['part10']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_parts': self.number_of_parts,
            'player_relative': self.player_relative,
            'do_not_wait_for_reform': self.do_not_wait_for_reform,
            'part1': self.part1.to_json(),
            'part2': self.part2.to_json(),
            'part3': self.part3.to_json(),
            'part4': self.part4.to_json(),
            'part5': self.part5.to_json(),
            'part6': self.part6.to_json(),
            'part7': self.part7.to_json(),
            'part8': self.part8.to_json(),
            'part9': self.part9.to_json(),
            'part10': self.part10.to_json(),
        }


def _decode_number_of_parts(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_player_relative(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_do_not_wait_for_reform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_part1(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -2.0})


def _decode_part2(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -4.0})


def _decode_part3(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -6.0})


def _decode_part4(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -8.0})


def _decode_part5(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': -10.0})


def _decode_part6(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 2.0})


def _decode_part7(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 4.0})


def _decode_part8(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 6.0})


def _decode_part9(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 8.0})


def _decode_part10(data: typing.BinaryIO, property_size: int):
    return SeparateAndReformParts.from_stream(data, property_size, default_override={'offset': 10.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8b594611: ('number_of_parts', _decode_number_of_parts),
    0x60be3c08: ('player_relative', _decode_player_relative),
    0x60f7e83f: ('do_not_wait_for_reform', _decode_do_not_wait_for_reform),
    0x36a054c3: ('part1', _decode_part1),
    0x40456dfe: ('part2', _decode_part2),
    0xdb36872a: ('part3', _decode_part3),
    0xad8f1f84: ('part4', _decode_part4),
    0x36fcf550: ('part5', _decode_part5),
    0x4019cc6d: ('part6', _decode_part6),
    0xdb6a26b9: ('part7', _decode_part7),
    0xad6afd31: ('part8', _decode_part8),
    0x361917e5: ('part9', _decode_part9),
    0x30c93088: ('part10', _decode_part10),
}

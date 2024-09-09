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
from retro_data_structures.properties.dkc_returns.archetypes.RobotChickenStructA import RobotChickenStructA

if typing.TYPE_CHECKING:
    class UnknownStruct255Json(typing_extensions.TypedDict):
        jump_count: int
        robot_chicken_struct_a_0x8792726d: json_util.JsonObject
        robot_chicken_struct_a_0x229a1901: json_util.JsonObject
        robot_chicken_struct_a_0x419dc025: json_util.JsonObject
        robot_chicken_struct_a_0xb3fbc998: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct255(BaseProperty):
    jump_count: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0xadfd4c91, original_name='JumpCount'
        ),
    })
    robot_chicken_struct_a_0x8792726d: RobotChickenStructA = dataclasses.field(default_factory=RobotChickenStructA, metadata={
        'reflection': FieldReflection[RobotChickenStructA](
            RobotChickenStructA, id=0x8792726d, original_name='RobotChickenStructA', from_json=RobotChickenStructA.from_json, to_json=RobotChickenStructA.to_json
        ),
    })
    robot_chicken_struct_a_0x229a1901: RobotChickenStructA = dataclasses.field(default_factory=RobotChickenStructA, metadata={
        'reflection': FieldReflection[RobotChickenStructA](
            RobotChickenStructA, id=0x229a1901, original_name='RobotChickenStructA', from_json=RobotChickenStructA.from_json, to_json=RobotChickenStructA.to_json
        ),
    })
    robot_chicken_struct_a_0x419dc025: RobotChickenStructA = dataclasses.field(default_factory=RobotChickenStructA, metadata={
        'reflection': FieldReflection[RobotChickenStructA](
            RobotChickenStructA, id=0x419dc025, original_name='RobotChickenStructA', from_json=RobotChickenStructA.from_json, to_json=RobotChickenStructA.to_json
        ),
    })
    robot_chicken_struct_a_0xb3fbc998: RobotChickenStructA = dataclasses.field(default_factory=RobotChickenStructA, metadata={
        'reflection': FieldReflection[RobotChickenStructA](
            RobotChickenStructA, id=0xb3fbc998, original_name='RobotChickenStructA', from_json=RobotChickenStructA.from_json, to_json=RobotChickenStructA.to_json
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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xadfd4c91
        jump_count = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8792726d
        robot_chicken_struct_a_0x8792726d = RobotChickenStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x229a1901
        robot_chicken_struct_a_0x229a1901 = RobotChickenStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x419dc025
        robot_chicken_struct_a_0x419dc025 = RobotChickenStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3fbc998
        robot_chicken_struct_a_0xb3fbc998 = RobotChickenStructA.from_stream(data, property_size)
    
        return cls(jump_count, robot_chicken_struct_a_0x8792726d, robot_chicken_struct_a_0x229a1901, robot_chicken_struct_a_0x419dc025, robot_chicken_struct_a_0xb3fbc998)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xad\xfdL\x91')  # 0xadfd4c91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.jump_count))

        data.write(b'\x87\x92rm')  # 0x8792726d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_a_0x8792726d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'"\x9a\x19\x01')  # 0x229a1901
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_a_0x229a1901.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A\x9d\xc0%')  # 0x419dc025
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_a_0x419dc025.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xfb\xc9\x98')  # 0xb3fbc998
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_a_0xb3fbc998.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct255Json", data)
        return cls(
            jump_count=json_data['jump_count'],
            robot_chicken_struct_a_0x8792726d=RobotChickenStructA.from_json(json_data['robot_chicken_struct_a_0x8792726d']),
            robot_chicken_struct_a_0x229a1901=RobotChickenStructA.from_json(json_data['robot_chicken_struct_a_0x229a1901']),
            robot_chicken_struct_a_0x419dc025=RobotChickenStructA.from_json(json_data['robot_chicken_struct_a_0x419dc025']),
            robot_chicken_struct_a_0xb3fbc998=RobotChickenStructA.from_json(json_data['robot_chicken_struct_a_0xb3fbc998']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'jump_count': self.jump_count,
            'robot_chicken_struct_a_0x8792726d': self.robot_chicken_struct_a_0x8792726d.to_json(),
            'robot_chicken_struct_a_0x229a1901': self.robot_chicken_struct_a_0x229a1901.to_json(),
            'robot_chicken_struct_a_0x419dc025': self.robot_chicken_struct_a_0x419dc025.to_json(),
            'robot_chicken_struct_a_0xb3fbc998': self.robot_chicken_struct_a_0xb3fbc998.to_json(),
        }


def _decode_jump_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xadfd4c91: ('jump_count', _decode_jump_count),
    0x8792726d: ('robot_chicken_struct_a_0x8792726d', RobotChickenStructA.from_stream),
    0x229a1901: ('robot_chicken_struct_a_0x229a1901', RobotChickenStructA.from_stream),
    0x419dc025: ('robot_chicken_struct_a_0x419dc025', RobotChickenStructA.from_stream),
    0xb3fbc998: ('robot_chicken_struct_a_0xb3fbc998', RobotChickenStructA.from_stream),
}

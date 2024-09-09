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
from retro_data_structures.properties.dkc_returns.archetypes.BeatUpHandlerStruct import BeatUpHandlerStruct
from retro_data_structures.properties.dkc_returns.archetypes.ControlCommands import ControlCommands
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class DataJson(typing_extensions.TypedDict):
        left_command: json_util.JsonObject
        control_command: json_util.JsonObject
        swing_delay_same: float
        swing_delay_different: float
        swing_delay_any: float
        randomize_hits: bool
        skip_initial_hit: bool
        allow_both_players_to_hit: bool
        max_beat_up_time: float
        max_multiplier: int
        prize1: json_util.JsonObject
        prize2: json_util.JsonObject
        prize3: json_util.JsonObject
        hit_sound: int
    

@dataclasses.dataclass()
class Data(BaseProperty):
    left_command: ControlCommands = dataclasses.field(default_factory=ControlCommands, metadata={
        'reflection': FieldReflection[ControlCommands](
            ControlCommands, id=0xf6ae5d7c, original_name='LeftCommand', from_json=ControlCommands.from_json, to_json=ControlCommands.to_json
        ),
    })
    control_command: ControlCommands = dataclasses.field(default_factory=ControlCommands, metadata={
        'reflection': FieldReflection[ControlCommands](
            ControlCommands, id=0xd2fd4f74, original_name='ControlCommand', from_json=ControlCommands.from_json, to_json=ControlCommands.to_json
        ),
    })
    swing_delay_same: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x35d40b67, original_name='SwingDelaySame'
        ),
    })
    swing_delay_different: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x82941381, original_name='SwingDelayDifferent'
        ),
    })
    swing_delay_any: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe83776e6, original_name='SwingDelayAny'
        ),
    })
    randomize_hits: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf804d41c, original_name='RandomizeHits'
        ),
    })
    skip_initial_hit: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe399b75a, original_name='SkipInitialHit'
        ),
    })
    allow_both_players_to_hit: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdd31e55a, original_name='AllowBothPlayersToHit'
        ),
    })
    max_beat_up_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb5bbe88a, original_name='MaxBeatUpTime'
        ),
    })
    max_multiplier: int = dataclasses.field(default=100, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb12e58b8, original_name='MaxMultiplier'
        ),
    })
    prize1: BeatUpHandlerStruct = dataclasses.field(default_factory=BeatUpHandlerStruct, metadata={
        'reflection': FieldReflection[BeatUpHandlerStruct](
            BeatUpHandlerStruct, id=0x4289b15b, original_name='Prize1', from_json=BeatUpHandlerStruct.from_json, to_json=BeatUpHandlerStruct.to_json
        ),
    })
    prize2: BeatUpHandlerStruct = dataclasses.field(default_factory=BeatUpHandlerStruct, metadata={
        'reflection': FieldReflection[BeatUpHandlerStruct](
            BeatUpHandlerStruct, id=0x351763ab, original_name='Prize2', from_json=BeatUpHandlerStruct.from_json, to_json=BeatUpHandlerStruct.to_json
        ),
    })
    prize3: BeatUpHandlerStruct = dataclasses.field(default_factory=BeatUpHandlerStruct, metadata={
        'reflection': FieldReflection[BeatUpHandlerStruct](
            BeatUpHandlerStruct, id=0xaeb22fc4, original_name='Prize3', from_json=BeatUpHandlerStruct.from_json, to_json=BeatUpHandlerStruct.to_json
        ),
    })
    hit_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x552db72c, original_name='HitSound'
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
        if property_count != 14:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf6ae5d7c
        left_command = ControlCommands.from_stream(data, property_size, default_override={'command': enums.Command.Unknown8})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd2fd4f74
        control_command = ControlCommands.from_stream(data, property_size, default_override={'command': enums.Command.Unknown9})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x35d40b67
        swing_delay_same = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82941381
        swing_delay_different = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe83776e6
        swing_delay_any = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf804d41c
        randomize_hits = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe399b75a
        skip_initial_hit = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdd31e55a
        allow_both_players_to_hit = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb5bbe88a
        max_beat_up_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb12e58b8
        max_multiplier = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4289b15b
        prize1 = BeatUpHandlerStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x351763ab
        prize2 = BeatUpHandlerStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaeb22fc4
        prize3 = BeatUpHandlerStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x552db72c
        hit_sound = struct.unpack(">Q", data.read(8))[0]
    
        return cls(left_command, control_command, swing_delay_same, swing_delay_different, swing_delay_any, randomize_hits, skip_initial_hit, allow_both_players_to_hit, max_beat_up_time, max_multiplier, prize1, prize2, prize3, hit_sound)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xf6\xae]|')  # 0xf6ae5d7c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.left_command.to_stream(data, default_override={'command': enums.Command.Unknown8})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\xfdOt')  # 0xd2fd4f74
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_command.to_stream(data, default_override={'command': enums.Command.Unknown9})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5\xd4\x0bg')  # 0x35d40b67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_delay_same))

        data.write(b'\x82\x94\x13\x81')  # 0x82941381
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_delay_different))

        data.write(b'\xe87v\xe6')  # 0xe83776e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_delay_any))

        data.write(b'\xf8\x04\xd4\x1c')  # 0xf804d41c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.randomize_hits))

        data.write(b'\xe3\x99\xb7Z')  # 0xe399b75a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.skip_initial_hit))

        data.write(b'\xdd1\xe5Z')  # 0xdd31e55a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_both_players_to_hit))

        data.write(b'\xb5\xbb\xe8\x8a')  # 0xb5bbe88a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_beat_up_time))

        data.write(b'\xb1.X\xb8')  # 0xb12e58b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_multiplier))

        data.write(b'B\x89\xb1[')  # 0x4289b15b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prize1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5\x17c\xab')  # 0x351763ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prize2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xae\xb2/\xc4')  # 0xaeb22fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prize3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U-\xb7,')  # 0x552db72c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hit_sound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("DataJson", data)
        return cls(
            left_command=ControlCommands.from_json(json_data['left_command']),
            control_command=ControlCommands.from_json(json_data['control_command']),
            swing_delay_same=json_data['swing_delay_same'],
            swing_delay_different=json_data['swing_delay_different'],
            swing_delay_any=json_data['swing_delay_any'],
            randomize_hits=json_data['randomize_hits'],
            skip_initial_hit=json_data['skip_initial_hit'],
            allow_both_players_to_hit=json_data['allow_both_players_to_hit'],
            max_beat_up_time=json_data['max_beat_up_time'],
            max_multiplier=json_data['max_multiplier'],
            prize1=BeatUpHandlerStruct.from_json(json_data['prize1']),
            prize2=BeatUpHandlerStruct.from_json(json_data['prize2']),
            prize3=BeatUpHandlerStruct.from_json(json_data['prize3']),
            hit_sound=json_data['hit_sound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'left_command': self.left_command.to_json(),
            'control_command': self.control_command.to_json(),
            'swing_delay_same': self.swing_delay_same,
            'swing_delay_different': self.swing_delay_different,
            'swing_delay_any': self.swing_delay_any,
            'randomize_hits': self.randomize_hits,
            'skip_initial_hit': self.skip_initial_hit,
            'allow_both_players_to_hit': self.allow_both_players_to_hit,
            'max_beat_up_time': self.max_beat_up_time,
            'max_multiplier': self.max_multiplier,
            'prize1': self.prize1.to_json(),
            'prize2': self.prize2.to_json(),
            'prize3': self.prize3.to_json(),
            'hit_sound': self.hit_sound,
        }


def _decode_left_command(data: typing.BinaryIO, property_size: int):
    return ControlCommands.from_stream(data, property_size, default_override={'command': enums.Command.Unknown8})


def _decode_control_command(data: typing.BinaryIO, property_size: int):
    return ControlCommands.from_stream(data, property_size, default_override={'command': enums.Command.Unknown9})


def _decode_swing_delay_same(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_delay_different(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_delay_any(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_randomize_hits(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_skip_initial_hit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_both_players_to_hit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_beat_up_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf6ae5d7c: ('left_command', _decode_left_command),
    0xd2fd4f74: ('control_command', _decode_control_command),
    0x35d40b67: ('swing_delay_same', _decode_swing_delay_same),
    0x82941381: ('swing_delay_different', _decode_swing_delay_different),
    0xe83776e6: ('swing_delay_any', _decode_swing_delay_any),
    0xf804d41c: ('randomize_hits', _decode_randomize_hits),
    0xe399b75a: ('skip_initial_hit', _decode_skip_initial_hit),
    0xdd31e55a: ('allow_both_players_to_hit', _decode_allow_both_players_to_hit),
    0xb5bbe88a: ('max_beat_up_time', _decode_max_beat_up_time),
    0xb12e58b8: ('max_multiplier', _decode_max_multiplier),
    0x4289b15b: ('prize1', BeatUpHandlerStruct.from_stream),
    0x351763ab: ('prize2', BeatUpHandlerStruct.from_stream),
    0xaeb22fc4: ('prize3', BeatUpHandlerStruct.from_stream),
    0x552db72c: ('hit_sound', _decode_hit_sound),
}

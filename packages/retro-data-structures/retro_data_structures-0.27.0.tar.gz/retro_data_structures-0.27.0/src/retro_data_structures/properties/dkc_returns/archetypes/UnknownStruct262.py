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
from retro_data_structures.properties.dkc_returns.archetypes.AnimGridModifierData import AnimGridModifierData
from retro_data_structures.properties.dkc_returns.archetypes.RobotChickenFlyerStructA import RobotChickenFlyerStructA
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct260 import UnknownStruct260
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct261 import UnknownStruct261

if typing.TYPE_CHECKING:
    class UnknownStruct262Json(typing_extensions.TypedDict):
        snap_to_spline: bool
        floor_height: float
        gravity: float
        acceleration: float
        deceleration: float
        maximum_speed: float
        unknown_0xe46e8d01: float
        use_player_crush: bool
        max_children: int
        child_spawn_time: float
        unknown_0xd2d92d71: int
        unknown_0x1cc6b88d: float
        unknown_0x9605aad3: int
        unknown_0x806dc773: float
        unknown_0x101ed799: float
        unknown_0xbbd7c692: float
        robot_chicken_flyer_struct_a_0xe84aa51c: json_util.JsonObject
        robot_chicken_flyer_struct_a_0xa152f46f: json_util.JsonObject
        robot_chicken_flyer_struct_a_0x1f59e2c1: json_util.JsonObject
        robot_chicken_flyer_struct_a_0xc4d0e557: json_util.JsonObject
        unknown_struct260: json_util.JsonObject
        anim_grid: json_util.JsonObject
        unknown_struct261: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct262(BaseProperty):
    snap_to_spline: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x26ecb939, original_name='SnapToSpline'
        ),
    })
    floor_height: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x041da172, original_name='FloorHeight'
        ),
    })
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    acceleration: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39fb7978, original_name='Acceleration'
        ),
    })
    deceleration: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9ec4fc10, original_name='Deceleration'
        ),
    })
    maximum_speed: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x140ef2cc, original_name='MaximumSpeed'
        ),
    })
    unknown_0xe46e8d01: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe46e8d01, original_name='Unknown'
        ),
    })
    use_player_crush: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xea0569d2, original_name='UsePlayerCrush'
        ),
    })
    max_children: int = dataclasses.field(default=6, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8b12f3b0, original_name='MaxChildren'
        ),
    })
    child_spawn_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x68dae7e9, original_name='ChildSpawnTime'
        ),
    })
    unknown_0xd2d92d71: int = dataclasses.field(default=9, metadata={
        'reflection': FieldReflection[int](
            int, id=0xd2d92d71, original_name='Unknown'
        ),
    })
    unknown_0x1cc6b88d: float = dataclasses.field(default=0.8700000047683716, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1cc6b88d, original_name='Unknown'
        ),
    })
    unknown_0x9605aad3: int = dataclasses.field(default=20, metadata={
        'reflection': FieldReflection[int](
            int, id=0x9605aad3, original_name='Unknown'
        ),
    })
    unknown_0x806dc773: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x806dc773, original_name='Unknown'
        ),
    })
    unknown_0x101ed799: float = dataclasses.field(default=9.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x101ed799, original_name='Unknown'
        ),
    })
    unknown_0xbbd7c692: float = dataclasses.field(default=13.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbbd7c692, original_name='Unknown'
        ),
    })
    robot_chicken_flyer_struct_a_0xe84aa51c: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructA](
            RobotChickenFlyerStructA, id=0xe84aa51c, original_name='RobotChickenFlyerStructA', from_json=RobotChickenFlyerStructA.from_json, to_json=RobotChickenFlyerStructA.to_json
        ),
    })
    robot_chicken_flyer_struct_a_0xa152f46f: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructA](
            RobotChickenFlyerStructA, id=0xa152f46f, original_name='RobotChickenFlyerStructA', from_json=RobotChickenFlyerStructA.from_json, to_json=RobotChickenFlyerStructA.to_json
        ),
    })
    robot_chicken_flyer_struct_a_0x1f59e2c1: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructA](
            RobotChickenFlyerStructA, id=0x1f59e2c1, original_name='RobotChickenFlyerStructA', from_json=RobotChickenFlyerStructA.from_json, to_json=RobotChickenFlyerStructA.to_json
        ),
    })
    robot_chicken_flyer_struct_a_0xc4d0e557: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructA](
            RobotChickenFlyerStructA, id=0xc4d0e557, original_name='RobotChickenFlyerStructA', from_json=RobotChickenFlyerStructA.from_json, to_json=RobotChickenFlyerStructA.to_json
        ),
    })
    unknown_struct260: UnknownStruct260 = dataclasses.field(default_factory=UnknownStruct260, metadata={
        'reflection': FieldReflection[UnknownStruct260](
            UnknownStruct260, id=0xf8011ec5, original_name='UnknownStruct260', from_json=UnknownStruct260.from_json, to_json=UnknownStruct260.to_json
        ),
    })
    anim_grid: AnimGridModifierData = dataclasses.field(default_factory=AnimGridModifierData, metadata={
        'reflection': FieldReflection[AnimGridModifierData](
            AnimGridModifierData, id=0x68fd49ae, original_name='AnimGrid', from_json=AnimGridModifierData.from_json, to_json=AnimGridModifierData.to_json
        ),
    })
    unknown_struct261: UnknownStruct261 = dataclasses.field(default_factory=UnknownStruct261, metadata={
        'reflection': FieldReflection[UnknownStruct261](
            UnknownStruct261, id=0x420151f6, original_name='UnknownStruct261', from_json=UnknownStruct261.from_json, to_json=UnknownStruct261.to_json
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
        if property_count != 23:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26ecb939
        snap_to_spline = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x041da172
        floor_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x39fb7978
        acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9ec4fc10
        deceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x140ef2cc
        maximum_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe46e8d01
        unknown_0xe46e8d01 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xea0569d2
        use_player_crush = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8b12f3b0
        max_children = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68dae7e9
        child_spawn_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd2d92d71
        unknown_0xd2d92d71 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1cc6b88d
        unknown_0x1cc6b88d = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9605aad3
        unknown_0x9605aad3 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806dc773
        unknown_0x806dc773 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x101ed799
        unknown_0x101ed799 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbd7c692
        unknown_0xbbd7c692 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe84aa51c
        robot_chicken_flyer_struct_a_0xe84aa51c = RobotChickenFlyerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa152f46f
        robot_chicken_flyer_struct_a_0xa152f46f = RobotChickenFlyerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1f59e2c1
        robot_chicken_flyer_struct_a_0x1f59e2c1 = RobotChickenFlyerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc4d0e557
        robot_chicken_flyer_struct_a_0xc4d0e557 = RobotChickenFlyerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf8011ec5
        unknown_struct260 = UnknownStruct260.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68fd49ae
        anim_grid = AnimGridModifierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x420151f6
        unknown_struct261 = UnknownStruct261.from_stream(data, property_size)
    
        return cls(snap_to_spline, floor_height, gravity, acceleration, deceleration, maximum_speed, unknown_0xe46e8d01, use_player_crush, max_children, child_spawn_time, unknown_0xd2d92d71, unknown_0x1cc6b88d, unknown_0x9605aad3, unknown_0x806dc773, unknown_0x101ed799, unknown_0xbbd7c692, robot_chicken_flyer_struct_a_0xe84aa51c, robot_chicken_flyer_struct_a_0xa152f46f, robot_chicken_flyer_struct_a_0x1f59e2c1, robot_chicken_flyer_struct_a_0xc4d0e557, unknown_struct260, anim_grid, unknown_struct261)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'\x04\x1d\xa1r')  # 0x41da172
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_height))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

        data.write(b'\xe4n\x8d\x01')  # 0xe46e8d01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe46e8d01))

        data.write(b'\xea\x05i\xd2')  # 0xea0569d2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_crush))

        data.write(b'\x8b\x12\xf3\xb0')  # 0x8b12f3b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_children))

        data.write(b'h\xda\xe7\xe9')  # 0x68dae7e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.child_spawn_time))

        data.write(b'\xd2\xd9-q')  # 0xd2d92d71
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd2d92d71))

        data.write(b'\x1c\xc6\xb8\x8d')  # 0x1cc6b88d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1cc6b88d))

        data.write(b'\x96\x05\xaa\xd3')  # 0x9605aad3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9605aad3))

        data.write(b'\x80m\xc7s')  # 0x806dc773
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x806dc773))

        data.write(b'\x10\x1e\xd7\x99')  # 0x101ed799
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x101ed799))

        data.write(b'\xbb\xd7\xc6\x92')  # 0xbbd7c692
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbbd7c692))

        data.write(b'\xe8J\xa5\x1c')  # 0xe84aa51c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0xe84aa51c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1R\xf4o')  # 0xa152f46f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0xa152f46f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1fY\xe2\xc1')  # 0x1f59e2c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0x1f59e2c1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\xd0\xe5W')  # 0xc4d0e557
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0xc4d0e557.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\x01\x1e\xc5')  # 0xf8011ec5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct260.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\xfdI\xae')  # 0x68fd49ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.anim_grid.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x01Q\xf6')  # 0x420151f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct261.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct262Json", data)
        return cls(
            snap_to_spline=json_data['snap_to_spline'],
            floor_height=json_data['floor_height'],
            gravity=json_data['gravity'],
            acceleration=json_data['acceleration'],
            deceleration=json_data['deceleration'],
            maximum_speed=json_data['maximum_speed'],
            unknown_0xe46e8d01=json_data['unknown_0xe46e8d01'],
            use_player_crush=json_data['use_player_crush'],
            max_children=json_data['max_children'],
            child_spawn_time=json_data['child_spawn_time'],
            unknown_0xd2d92d71=json_data['unknown_0xd2d92d71'],
            unknown_0x1cc6b88d=json_data['unknown_0x1cc6b88d'],
            unknown_0x9605aad3=json_data['unknown_0x9605aad3'],
            unknown_0x806dc773=json_data['unknown_0x806dc773'],
            unknown_0x101ed799=json_data['unknown_0x101ed799'],
            unknown_0xbbd7c692=json_data['unknown_0xbbd7c692'],
            robot_chicken_flyer_struct_a_0xe84aa51c=RobotChickenFlyerStructA.from_json(json_data['robot_chicken_flyer_struct_a_0xe84aa51c']),
            robot_chicken_flyer_struct_a_0xa152f46f=RobotChickenFlyerStructA.from_json(json_data['robot_chicken_flyer_struct_a_0xa152f46f']),
            robot_chicken_flyer_struct_a_0x1f59e2c1=RobotChickenFlyerStructA.from_json(json_data['robot_chicken_flyer_struct_a_0x1f59e2c1']),
            robot_chicken_flyer_struct_a_0xc4d0e557=RobotChickenFlyerStructA.from_json(json_data['robot_chicken_flyer_struct_a_0xc4d0e557']),
            unknown_struct260=UnknownStruct260.from_json(json_data['unknown_struct260']),
            anim_grid=AnimGridModifierData.from_json(json_data['anim_grid']),
            unknown_struct261=UnknownStruct261.from_json(json_data['unknown_struct261']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'snap_to_spline': self.snap_to_spline,
            'floor_height': self.floor_height,
            'gravity': self.gravity,
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'maximum_speed': self.maximum_speed,
            'unknown_0xe46e8d01': self.unknown_0xe46e8d01,
            'use_player_crush': self.use_player_crush,
            'max_children': self.max_children,
            'child_spawn_time': self.child_spawn_time,
            'unknown_0xd2d92d71': self.unknown_0xd2d92d71,
            'unknown_0x1cc6b88d': self.unknown_0x1cc6b88d,
            'unknown_0x9605aad3': self.unknown_0x9605aad3,
            'unknown_0x806dc773': self.unknown_0x806dc773,
            'unknown_0x101ed799': self.unknown_0x101ed799,
            'unknown_0xbbd7c692': self.unknown_0xbbd7c692,
            'robot_chicken_flyer_struct_a_0xe84aa51c': self.robot_chicken_flyer_struct_a_0xe84aa51c.to_json(),
            'robot_chicken_flyer_struct_a_0xa152f46f': self.robot_chicken_flyer_struct_a_0xa152f46f.to_json(),
            'robot_chicken_flyer_struct_a_0x1f59e2c1': self.robot_chicken_flyer_struct_a_0x1f59e2c1.to_json(),
            'robot_chicken_flyer_struct_a_0xc4d0e557': self.robot_chicken_flyer_struct_a_0xc4d0e557.to_json(),
            'unknown_struct260': self.unknown_struct260.to_json(),
            'anim_grid': self.anim_grid.to_json(),
            'unknown_struct261': self.unknown_struct261.to_json(),
        }


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_floor_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe46e8d01(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_player_crush(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_children(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_child_spawn_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd2d92d71(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1cc6b88d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9605aad3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x806dc773(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x101ed799(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbbd7c692(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0x41da172: ('floor_height', _decode_floor_height),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
    0xe46e8d01: ('unknown_0xe46e8d01', _decode_unknown_0xe46e8d01),
    0xea0569d2: ('use_player_crush', _decode_use_player_crush),
    0x8b12f3b0: ('max_children', _decode_max_children),
    0x68dae7e9: ('child_spawn_time', _decode_child_spawn_time),
    0xd2d92d71: ('unknown_0xd2d92d71', _decode_unknown_0xd2d92d71),
    0x1cc6b88d: ('unknown_0x1cc6b88d', _decode_unknown_0x1cc6b88d),
    0x9605aad3: ('unknown_0x9605aad3', _decode_unknown_0x9605aad3),
    0x806dc773: ('unknown_0x806dc773', _decode_unknown_0x806dc773),
    0x101ed799: ('unknown_0x101ed799', _decode_unknown_0x101ed799),
    0xbbd7c692: ('unknown_0xbbd7c692', _decode_unknown_0xbbd7c692),
    0xe84aa51c: ('robot_chicken_flyer_struct_a_0xe84aa51c', RobotChickenFlyerStructA.from_stream),
    0xa152f46f: ('robot_chicken_flyer_struct_a_0xa152f46f', RobotChickenFlyerStructA.from_stream),
    0x1f59e2c1: ('robot_chicken_flyer_struct_a_0x1f59e2c1', RobotChickenFlyerStructA.from_stream),
    0xc4d0e557: ('robot_chicken_flyer_struct_a_0xc4d0e557', RobotChickenFlyerStructA.from_stream),
    0xf8011ec5: ('unknown_struct260', UnknownStruct260.from_stream),
    0x68fd49ae: ('anim_grid', AnimGridModifierData.from_stream),
    0x420151f6: ('unknown_struct261', UnknownStruct261.from_stream),
}

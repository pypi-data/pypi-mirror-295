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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMovementParameters import PlayerMovementParameters

if typing.TYPE_CHECKING:
    class PlayerSplineAdvancementDataJson(typing_extensions.TypedDict):
        normal_movement_parameters: json_util.JsonObject
        tar_inhibited_movement_parameters: json_util.JsonObject
        programmatic_turn_speed: float
        has_air_control_damping: bool
        air_damping_time: float
        allow_turn_in_the_air: bool
        keep_jump_momentum: bool
        jump_control_scalar: float
        landing_damping_delay: float
        after_jump_damping_time: float
        after_jump_damping_amount: float
        use_push_ray: bool
        maximum_push_out_of_collision_speed: float
        ledge_stop_max_speed: float
    

@dataclasses.dataclass()
class PlayerSplineAdvancementData(BaseProperty):
    normal_movement_parameters: PlayerMovementParameters = dataclasses.field(default_factory=PlayerMovementParameters, metadata={
        'reflection': FieldReflection[PlayerMovementParameters](
            PlayerMovementParameters, id=0xe29bf306, original_name='NormalMovementParameters', from_json=PlayerMovementParameters.from_json, to_json=PlayerMovementParameters.to_json
        ),
    })
    tar_inhibited_movement_parameters: PlayerMovementParameters = dataclasses.field(default_factory=PlayerMovementParameters, metadata={
        'reflection': FieldReflection[PlayerMovementParameters](
            PlayerMovementParameters, id=0xb0c8b06f, original_name='TarInhibitedMovementParameters', from_json=PlayerMovementParameters.from_json, to_json=PlayerMovementParameters.to_json
        ),
    })
    programmatic_turn_speed: float = dataclasses.field(default=450.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcf03cb0c, original_name='ProgrammaticTurnSpeed'
        ),
    })
    has_air_control_damping: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x038ead53, original_name='HasAirControlDamping'
        ),
    })
    air_damping_time: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x49a33669, original_name='AirDampingTime'
        ),
    })
    allow_turn_in_the_air: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7bf5cd04, original_name='AllowTurnInTheAir'
        ),
    })
    keep_jump_momentum: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x67259b23, original_name='KeepJumpMomentum'
        ),
    })
    jump_control_scalar: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42d71a58, original_name='JumpControlScalar'
        ),
    })
    landing_damping_delay: float = dataclasses.field(default=0.07999999821186066, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5ff2321f, original_name='LandingDampingDelay'
        ),
    })
    after_jump_damping_time: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0xae72a4ff, original_name='AfterJumpDampingTime'
        ),
    })
    after_jump_damping_amount: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xde7532c0, original_name='AfterJumpDampingAmount'
        ),
    })
    use_push_ray: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6f38b02d, original_name='UsePushRay'
        ),
    })
    maximum_push_out_of_collision_speed: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x793ab356, original_name='MaximumPushOutOfCollisionSpeed'
        ),
    })
    ledge_stop_max_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x49494c3b, original_name='LedgeStopMaxSpeed'
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
        assert property_id == 0xe29bf306
        normal_movement_parameters = PlayerMovementParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0c8b06f
        tar_inhibited_movement_parameters = PlayerMovementParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcf03cb0c
        programmatic_turn_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x038ead53
        has_air_control_damping = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x49a33669
        air_damping_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7bf5cd04
        allow_turn_in_the_air = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67259b23
        keep_jump_momentum = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x42d71a58
        jump_control_scalar = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5ff2321f
        landing_damping_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xae72a4ff
        after_jump_damping_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xde7532c0
        after_jump_damping_amount = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6f38b02d
        use_push_ray = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x793ab356
        maximum_push_out_of_collision_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x49494c3b
        ledge_stop_max_speed = struct.unpack('>f', data.read(4))[0]
    
        return cls(normal_movement_parameters, tar_inhibited_movement_parameters, programmatic_turn_speed, has_air_control_damping, air_damping_time, allow_turn_in_the_air, keep_jump_momentum, jump_control_scalar, landing_damping_delay, after_jump_damping_time, after_jump_damping_amount, use_push_ray, maximum_push_out_of_collision_speed, ledge_stop_max_speed)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xe2\x9b\xf3\x06')  # 0xe29bf306
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_movement_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xc8\xb0o')  # 0xb0c8b06f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar_inhibited_movement_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\x03\xcb\x0c')  # 0xcf03cb0c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.programmatic_turn_speed))

        data.write(b'\x03\x8e\xadS')  # 0x38ead53
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.has_air_control_damping))

        data.write(b'I\xa36i')  # 0x49a33669
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_damping_time))

        data.write(b'{\xf5\xcd\x04')  # 0x7bf5cd04
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_turn_in_the_air))

        data.write(b'g%\x9b#')  # 0x67259b23
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.keep_jump_momentum))

        data.write(b'B\xd7\x1aX')  # 0x42d71a58
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_control_scalar))

        data.write(b'_\xf22\x1f')  # 0x5ff2321f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.landing_damping_delay))

        data.write(b'\xaer\xa4\xff')  # 0xae72a4ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.after_jump_damping_time))

        data.write(b'\xdeu2\xc0')  # 0xde7532c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.after_jump_damping_amount))

        data.write(b'o8\xb0-')  # 0x6f38b02d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_push_ray))

        data.write(b'y:\xb3V')  # 0x793ab356
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_push_out_of_collision_speed))

        data.write(b'IIL;')  # 0x49494c3b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ledge_stop_max_speed))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerSplineAdvancementDataJson", data)
        return cls(
            normal_movement_parameters=PlayerMovementParameters.from_json(json_data['normal_movement_parameters']),
            tar_inhibited_movement_parameters=PlayerMovementParameters.from_json(json_data['tar_inhibited_movement_parameters']),
            programmatic_turn_speed=json_data['programmatic_turn_speed'],
            has_air_control_damping=json_data['has_air_control_damping'],
            air_damping_time=json_data['air_damping_time'],
            allow_turn_in_the_air=json_data['allow_turn_in_the_air'],
            keep_jump_momentum=json_data['keep_jump_momentum'],
            jump_control_scalar=json_data['jump_control_scalar'],
            landing_damping_delay=json_data['landing_damping_delay'],
            after_jump_damping_time=json_data['after_jump_damping_time'],
            after_jump_damping_amount=json_data['after_jump_damping_amount'],
            use_push_ray=json_data['use_push_ray'],
            maximum_push_out_of_collision_speed=json_data['maximum_push_out_of_collision_speed'],
            ledge_stop_max_speed=json_data['ledge_stop_max_speed'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'normal_movement_parameters': self.normal_movement_parameters.to_json(),
            'tar_inhibited_movement_parameters': self.tar_inhibited_movement_parameters.to_json(),
            'programmatic_turn_speed': self.programmatic_turn_speed,
            'has_air_control_damping': self.has_air_control_damping,
            'air_damping_time': self.air_damping_time,
            'allow_turn_in_the_air': self.allow_turn_in_the_air,
            'keep_jump_momentum': self.keep_jump_momentum,
            'jump_control_scalar': self.jump_control_scalar,
            'landing_damping_delay': self.landing_damping_delay,
            'after_jump_damping_time': self.after_jump_damping_time,
            'after_jump_damping_amount': self.after_jump_damping_amount,
            'use_push_ray': self.use_push_ray,
            'maximum_push_out_of_collision_speed': self.maximum_push_out_of_collision_speed,
            'ledge_stop_max_speed': self.ledge_stop_max_speed,
        }


def _decode_programmatic_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_has_air_control_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_air_damping_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allow_turn_in_the_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_keep_jump_momentum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_jump_control_scalar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_landing_damping_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_after_jump_damping_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_after_jump_damping_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_push_ray(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_maximum_push_out_of_collision_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ledge_stop_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe29bf306: ('normal_movement_parameters', PlayerMovementParameters.from_stream),
    0xb0c8b06f: ('tar_inhibited_movement_parameters', PlayerMovementParameters.from_stream),
    0xcf03cb0c: ('programmatic_turn_speed', _decode_programmatic_turn_speed),
    0x38ead53: ('has_air_control_damping', _decode_has_air_control_damping),
    0x49a33669: ('air_damping_time', _decode_air_damping_time),
    0x7bf5cd04: ('allow_turn_in_the_air', _decode_allow_turn_in_the_air),
    0x67259b23: ('keep_jump_momentum', _decode_keep_jump_momentum),
    0x42d71a58: ('jump_control_scalar', _decode_jump_control_scalar),
    0x5ff2321f: ('landing_damping_delay', _decode_landing_damping_delay),
    0xae72a4ff: ('after_jump_damping_time', _decode_after_jump_damping_time),
    0xde7532c0: ('after_jump_damping_amount', _decode_after_jump_damping_amount),
    0x6f38b02d: ('use_push_ray', _decode_use_push_ray),
    0x793ab356: ('maximum_push_out_of_collision_speed', _decode_maximum_push_out_of_collision_speed),
    0x49494c3b: ('ledge_stop_max_speed', _decode_ledge_stop_max_speed),
}

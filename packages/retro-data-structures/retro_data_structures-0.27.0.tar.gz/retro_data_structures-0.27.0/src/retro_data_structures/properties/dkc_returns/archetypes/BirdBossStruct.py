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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct48 import UnknownStruct48

if typing.TYPE_CHECKING:
    class BirdBossStructJson(typing_extensions.TypedDict):
        attack_selector: int
        health: float
        acceleration: float
        deceleration: float
        maximum_speed: float
        unknown_0x40ec2d6f: int
        unknown_0x11acfd8e: int
        unknown_0xe2217298: int
        unknown_0xd87c0c65: float
        unknown_0x8f5ab554: float
        unknown_struct48_0x67490fee: json_util.JsonObject
        unknown_struct48_0xc41f8947: json_util.JsonObject
        unknown_struct48_0x13fd091f: json_util.JsonObject
        unknown_struct48_0x59c38254: json_util.JsonObject
        unknown_struct48_0x8e21020c: json_util.JsonObject
        unknown_struct48_0x2d7784a5: json_util.JsonObject
        unknown_struct48_0xfa9504fd: json_util.JsonObject
    

@dataclasses.dataclass()
class BirdBossStruct(BaseProperty):
    attack_selector: enums.RobotChickenEnum = dataclasses.field(default=enums.RobotChickenEnum.Unknown1, metadata={
        'reflection': FieldReflection[enums.RobotChickenEnum](
            enums.RobotChickenEnum, id=0x97d30f8b, original_name='AttackSelector', from_json=enums.RobotChickenEnum.from_json, to_json=enums.RobotChickenEnum.to_json
        ),
    })
    health: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf0668919, original_name='Health'
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
    unknown_0x40ec2d6f: int = dataclasses.field(default=2, metadata={
        'reflection': FieldReflection[int](
            int, id=0x40ec2d6f, original_name='Unknown'
        ),
    })
    unknown_0x11acfd8e: int = dataclasses.field(default=2, metadata={
        'reflection': FieldReflection[int](
            int, id=0x11acfd8e, original_name='Unknown'
        ),
    })
    unknown_0xe2217298: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0xe2217298, original_name='Unknown'
        ),
    })
    unknown_0xd87c0c65: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd87c0c65, original_name='Unknown'
        ),
    })
    unknown_0x8f5ab554: float = dataclasses.field(default=0.699999988079071, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8f5ab554, original_name='Unknown'
        ),
    })
    unknown_struct48_0x67490fee: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0x67490fee, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
        ),
    })
    unknown_struct48_0xc41f8947: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0xc41f8947, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
        ),
    })
    unknown_struct48_0x13fd091f: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0x13fd091f, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
        ),
    })
    unknown_struct48_0x59c38254: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0x59c38254, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
        ),
    })
    unknown_struct48_0x8e21020c: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0x8e21020c, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
        ),
    })
    unknown_struct48_0x2d7784a5: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0x2d7784a5, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
        ),
    })
    unknown_struct48_0xfa9504fd: UnknownStruct48 = dataclasses.field(default_factory=UnknownStruct48, metadata={
        'reflection': FieldReflection[UnknownStruct48](
            UnknownStruct48, id=0xfa9504fd, original_name='UnknownStruct48', from_json=UnknownStruct48.from_json, to_json=UnknownStruct48.to_json
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
        if property_count != 17:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x97d30f8b
        attack_selector = enums.RobotChickenEnum.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0668919
        health = struct.unpack('>f', data.read(4))[0]
    
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
        assert property_id == 0x40ec2d6f
        unknown_0x40ec2d6f = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x11acfd8e
        unknown_0x11acfd8e = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2217298
        unknown_0xe2217298 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd87c0c65
        unknown_0xd87c0c65 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f5ab554
        unknown_0x8f5ab554 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67490fee
        unknown_struct48_0x67490fee = UnknownStruct48.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc41f8947
        unknown_struct48_0xc41f8947 = UnknownStruct48.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x13fd091f
        unknown_struct48_0x13fd091f = UnknownStruct48.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59c38254
        unknown_struct48_0x59c38254 = UnknownStruct48.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8e21020c
        unknown_struct48_0x8e21020c = UnknownStruct48.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2d7784a5
        unknown_struct48_0x2d7784a5 = UnknownStruct48.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfa9504fd
        unknown_struct48_0xfa9504fd = UnknownStruct48.from_stream(data, property_size)
    
        return cls(attack_selector, health, acceleration, deceleration, maximum_speed, unknown_0x40ec2d6f, unknown_0x11acfd8e, unknown_0xe2217298, unknown_0xd87c0c65, unknown_0x8f5ab554, unknown_struct48_0x67490fee, unknown_struct48_0xc41f8947, unknown_struct48_0x13fd091f, unknown_struct48_0x59c38254, unknown_struct48_0x8e21020c, unknown_struct48_0x2d7784a5, unknown_struct48_0xfa9504fd)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'\x97\xd3\x0f\x8b')  # 0x97d30f8b
        data.write(b'\x00\x04')  # size
        self.attack_selector.to_stream(data)

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

        data.write(b'@\xec-o')  # 0x40ec2d6f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x40ec2d6f))

        data.write(b'\x11\xac\xfd\x8e')  # 0x11acfd8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x11acfd8e))

        data.write(b'\xe2!r\x98')  # 0xe2217298
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe2217298))

        data.write(b'\xd8|\x0ce')  # 0xd87c0c65
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd87c0c65))

        data.write(b'\x8fZ\xb5T')  # 0x8f5ab554
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f5ab554))

        data.write(b'gI\x0f\xee')  # 0x67490fee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0x67490fee.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\x1f\x89G')  # 0xc41f8947
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0xc41f8947.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\xfd\t\x1f')  # 0x13fd091f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0x13fd091f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\xc3\x82T')  # 0x59c38254
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0x59c38254.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8e!\x02\x0c')  # 0x8e21020c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0x8e21020c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-w\x84\xa5')  # 0x2d7784a5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0x2d7784a5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x95\x04\xfd')  # 0xfa9504fd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct48_0xfa9504fd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BirdBossStructJson", data)
        return cls(
            attack_selector=enums.RobotChickenEnum.from_json(json_data['attack_selector']),
            health=json_data['health'],
            acceleration=json_data['acceleration'],
            deceleration=json_data['deceleration'],
            maximum_speed=json_data['maximum_speed'],
            unknown_0x40ec2d6f=json_data['unknown_0x40ec2d6f'],
            unknown_0x11acfd8e=json_data['unknown_0x11acfd8e'],
            unknown_0xe2217298=json_data['unknown_0xe2217298'],
            unknown_0xd87c0c65=json_data['unknown_0xd87c0c65'],
            unknown_0x8f5ab554=json_data['unknown_0x8f5ab554'],
            unknown_struct48_0x67490fee=UnknownStruct48.from_json(json_data['unknown_struct48_0x67490fee']),
            unknown_struct48_0xc41f8947=UnknownStruct48.from_json(json_data['unknown_struct48_0xc41f8947']),
            unknown_struct48_0x13fd091f=UnknownStruct48.from_json(json_data['unknown_struct48_0x13fd091f']),
            unknown_struct48_0x59c38254=UnknownStruct48.from_json(json_data['unknown_struct48_0x59c38254']),
            unknown_struct48_0x8e21020c=UnknownStruct48.from_json(json_data['unknown_struct48_0x8e21020c']),
            unknown_struct48_0x2d7784a5=UnknownStruct48.from_json(json_data['unknown_struct48_0x2d7784a5']),
            unknown_struct48_0xfa9504fd=UnknownStruct48.from_json(json_data['unknown_struct48_0xfa9504fd']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attack_selector': self.attack_selector.to_json(),
            'health': self.health,
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'maximum_speed': self.maximum_speed,
            'unknown_0x40ec2d6f': self.unknown_0x40ec2d6f,
            'unknown_0x11acfd8e': self.unknown_0x11acfd8e,
            'unknown_0xe2217298': self.unknown_0xe2217298,
            'unknown_0xd87c0c65': self.unknown_0xd87c0c65,
            'unknown_0x8f5ab554': self.unknown_0x8f5ab554,
            'unknown_struct48_0x67490fee': self.unknown_struct48_0x67490fee.to_json(),
            'unknown_struct48_0xc41f8947': self.unknown_struct48_0xc41f8947.to_json(),
            'unknown_struct48_0x13fd091f': self.unknown_struct48_0x13fd091f.to_json(),
            'unknown_struct48_0x59c38254': self.unknown_struct48_0x59c38254.to_json(),
            'unknown_struct48_0x8e21020c': self.unknown_struct48_0x8e21020c.to_json(),
            'unknown_struct48_0x2d7784a5': self.unknown_struct48_0x2d7784a5.to_json(),
            'unknown_struct48_0xfa9504fd': self.unknown_struct48_0xfa9504fd.to_json(),
        }


def _decode_attack_selector(data: typing.BinaryIO, property_size: int):
    return enums.RobotChickenEnum.from_stream(data)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x40ec2d6f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x11acfd8e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xe2217298(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd87c0c65(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f5ab554(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97d30f8b: ('attack_selector', _decode_attack_selector),
    0xf0668919: ('health', _decode_health),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
    0x40ec2d6f: ('unknown_0x40ec2d6f', _decode_unknown_0x40ec2d6f),
    0x11acfd8e: ('unknown_0x11acfd8e', _decode_unknown_0x11acfd8e),
    0xe2217298: ('unknown_0xe2217298', _decode_unknown_0xe2217298),
    0xd87c0c65: ('unknown_0xd87c0c65', _decode_unknown_0xd87c0c65),
    0x8f5ab554: ('unknown_0x8f5ab554', _decode_unknown_0x8f5ab554),
    0x67490fee: ('unknown_struct48_0x67490fee', UnknownStruct48.from_stream),
    0xc41f8947: ('unknown_struct48_0xc41f8947', UnknownStruct48.from_stream),
    0x13fd091f: ('unknown_struct48_0x13fd091f', UnknownStruct48.from_stream),
    0x59c38254: ('unknown_struct48_0x59c38254', UnknownStruct48.from_stream),
    0x8e21020c: ('unknown_struct48_0x8e21020c', UnknownStruct48.from_stream),
    0x2d7784a5: ('unknown_struct48_0x2d7784a5', UnknownStruct48.from_stream),
    0xfa9504fd: ('unknown_struct48_0xfa9504fd', UnknownStruct48.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.MoleTrainManagerStructB import MoleTrainManagerStructB

if typing.TYPE_CHECKING:
    class UnknownStruct238Json(typing_extensions.TypedDict):
        unknown_0x5d57fc7c: float
        unknown_0xe205412c: float
        cart_speed: float
        unknown_0x2d3c5998: float
        sequence_count: int
        mole_train_manager_struct_b_0x9aecdc44: json_util.JsonObject
        mole_train_manager_struct_b_0x2978f187: json_util.JsonObject
        mole_train_manager_struct_b_0x47f4eac6: json_util.JsonObject
        mole_train_manager_struct_b_0x9521ac40: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct238(BaseProperty):
    unknown_0x5d57fc7c: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5d57fc7c, original_name='Unknown'
        ),
    })
    unknown_0xe205412c: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe205412c, original_name='Unknown'
        ),
    })
    cart_speed: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3994be14, original_name='CartSpeed'
        ),
    })
    unknown_0x2d3c5998: float = dataclasses.field(default=2.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2d3c5998, original_name='Unknown'
        ),
    })
    sequence_count: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x65eceb7a, original_name='SequenceCount'
        ),
    })
    mole_train_manager_struct_b_0x9aecdc44: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB, metadata={
        'reflection': FieldReflection[MoleTrainManagerStructB](
            MoleTrainManagerStructB, id=0x9aecdc44, original_name='MoleTrainManagerStructB', from_json=MoleTrainManagerStructB.from_json, to_json=MoleTrainManagerStructB.to_json
        ),
    })
    mole_train_manager_struct_b_0x2978f187: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB, metadata={
        'reflection': FieldReflection[MoleTrainManagerStructB](
            MoleTrainManagerStructB, id=0x2978f187, original_name='MoleTrainManagerStructB', from_json=MoleTrainManagerStructB.from_json, to_json=MoleTrainManagerStructB.to_json
        ),
    })
    mole_train_manager_struct_b_0x47f4eac6: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB, metadata={
        'reflection': FieldReflection[MoleTrainManagerStructB](
            MoleTrainManagerStructB, id=0x47f4eac6, original_name='MoleTrainManagerStructB', from_json=MoleTrainManagerStructB.from_json, to_json=MoleTrainManagerStructB.to_json
        ),
    })
    mole_train_manager_struct_b_0x9521ac40: MoleTrainManagerStructB = dataclasses.field(default_factory=MoleTrainManagerStructB, metadata={
        'reflection': FieldReflection[MoleTrainManagerStructB](
            MoleTrainManagerStructB, id=0x9521ac40, original_name='MoleTrainManagerStructB', from_json=MoleTrainManagerStructB.from_json, to_json=MoleTrainManagerStructB.to_json
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
        assert property_id == 0x5d57fc7c
        unknown_0x5d57fc7c = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe205412c
        unknown_0xe205412c = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3994be14
        cart_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2d3c5998
        unknown_0x2d3c5998 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x65eceb7a
        sequence_count = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9aecdc44
        mole_train_manager_struct_b_0x9aecdc44 = MoleTrainManagerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2978f187
        mole_train_manager_struct_b_0x2978f187 = MoleTrainManagerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47f4eac6
        mole_train_manager_struct_b_0x47f4eac6 = MoleTrainManagerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9521ac40
        mole_train_manager_struct_b_0x9521ac40 = MoleTrainManagerStructB.from_stream(data, property_size)
    
        return cls(unknown_0x5d57fc7c, unknown_0xe205412c, cart_speed, unknown_0x2d3c5998, sequence_count, mole_train_manager_struct_b_0x9aecdc44, mole_train_manager_struct_b_0x2978f187, mole_train_manager_struct_b_0x47f4eac6, mole_train_manager_struct_b_0x9521ac40)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b']W\xfc|')  # 0x5d57fc7c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d57fc7c))

        data.write(b'\xe2\x05A,')  # 0xe205412c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe205412c))

        data.write(b'9\x94\xbe\x14')  # 0x3994be14
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cart_speed))

        data.write(b'-<Y\x98')  # 0x2d3c5998
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d3c5998))

        data.write(b'e\xec\xebz')  # 0x65eceb7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sequence_count))

        data.write(b'\x9a\xec\xdcD')  # 0x9aecdc44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x9aecdc44.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')x\xf1\x87')  # 0x2978f187
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x2978f187.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\xf4\xea\xc6')  # 0x47f4eac6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x47f4eac6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95!\xac@')  # 0x9521ac40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_train_manager_struct_b_0x9521ac40.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct238Json", data)
        return cls(
            unknown_0x5d57fc7c=json_data['unknown_0x5d57fc7c'],
            unknown_0xe205412c=json_data['unknown_0xe205412c'],
            cart_speed=json_data['cart_speed'],
            unknown_0x2d3c5998=json_data['unknown_0x2d3c5998'],
            sequence_count=json_data['sequence_count'],
            mole_train_manager_struct_b_0x9aecdc44=MoleTrainManagerStructB.from_json(json_data['mole_train_manager_struct_b_0x9aecdc44']),
            mole_train_manager_struct_b_0x2978f187=MoleTrainManagerStructB.from_json(json_data['mole_train_manager_struct_b_0x2978f187']),
            mole_train_manager_struct_b_0x47f4eac6=MoleTrainManagerStructB.from_json(json_data['mole_train_manager_struct_b_0x47f4eac6']),
            mole_train_manager_struct_b_0x9521ac40=MoleTrainManagerStructB.from_json(json_data['mole_train_manager_struct_b_0x9521ac40']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x5d57fc7c': self.unknown_0x5d57fc7c,
            'unknown_0xe205412c': self.unknown_0xe205412c,
            'cart_speed': self.cart_speed,
            'unknown_0x2d3c5998': self.unknown_0x2d3c5998,
            'sequence_count': self.sequence_count,
            'mole_train_manager_struct_b_0x9aecdc44': self.mole_train_manager_struct_b_0x9aecdc44.to_json(),
            'mole_train_manager_struct_b_0x2978f187': self.mole_train_manager_struct_b_0x2978f187.to_json(),
            'mole_train_manager_struct_b_0x47f4eac6': self.mole_train_manager_struct_b_0x47f4eac6.to_json(),
            'mole_train_manager_struct_b_0x9521ac40': self.mole_train_manager_struct_b_0x9521ac40.to_json(),
        }


def _decode_unknown_0x5d57fc7c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe205412c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cart_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d3c5998(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sequence_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d57fc7c: ('unknown_0x5d57fc7c', _decode_unknown_0x5d57fc7c),
    0xe205412c: ('unknown_0xe205412c', _decode_unknown_0xe205412c),
    0x3994be14: ('cart_speed', _decode_cart_speed),
    0x2d3c5998: ('unknown_0x2d3c5998', _decode_unknown_0x2d3c5998),
    0x65eceb7a: ('sequence_count', _decode_sequence_count),
    0x9aecdc44: ('mole_train_manager_struct_b_0x9aecdc44', MoleTrainManagerStructB.from_stream),
    0x2978f187: ('mole_train_manager_struct_b_0x2978f187', MoleTrainManagerStructB.from_stream),
    0x47f4eac6: ('mole_train_manager_struct_b_0x47f4eac6', MoleTrainManagerStructB.from_stream),
    0x9521ac40: ('mole_train_manager_struct_b_0x9521ac40', MoleTrainManagerStructB.from_stream),
}

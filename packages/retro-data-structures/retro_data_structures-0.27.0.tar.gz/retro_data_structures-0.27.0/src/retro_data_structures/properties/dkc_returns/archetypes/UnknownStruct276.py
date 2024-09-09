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
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct276Json(typing_extensions.TypedDict):
        unknown: json_util.JsonObject
        pound_disable_time: float
        launch_delay: float
        target_height: float
    

@dataclasses.dataclass()
class UnknownStruct276(BaseProperty):
    unknown: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x2a8fd6d0, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    pound_disable_time: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x95ee9687, original_name='PoundDisableTime'
        ),
    })
    launch_delay: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4655a9c5, original_name='LaunchDelay'
        ),
    })
    target_height: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbdba191e, original_name='TargetHeight'
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
        assert property_id == 0x2a8fd6d0
        unknown = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x95ee9687
        pound_disable_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4655a9c5
        launch_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbdba191e
        target_height = struct.unpack('>f', data.read(4))[0]
    
        return cls(unknown, pound_disable_time, launch_delay, target_height)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'*\x8f\xd6\xd0')  # 0x2a8fd6d0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xee\x96\x87')  # 0x95ee9687
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pound_disable_time))

        data.write(b'FU\xa9\xc5')  # 0x4655a9c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_delay))

        data.write(b'\xbd\xba\x19\x1e')  # 0xbdba191e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_height))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct276Json", data)
        return cls(
            unknown=Spline.from_json(json_data['unknown']),
            pound_disable_time=json_data['pound_disable_time'],
            launch_delay=json_data['launch_delay'],
            target_height=json_data['target_height'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown.to_json(),
            'pound_disable_time': self.pound_disable_time,
            'launch_delay': self.launch_delay,
            'target_height': self.target_height,
        }


def _decode_pound_disable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2a8fd6d0: ('unknown', Spline.from_stream),
    0x95ee9687: ('pound_disable_time', _decode_pound_disable_time),
    0x4655a9c5: ('launch_delay', _decode_launch_delay),
    0xbdba191e: ('target_height', _decode_target_height),
}

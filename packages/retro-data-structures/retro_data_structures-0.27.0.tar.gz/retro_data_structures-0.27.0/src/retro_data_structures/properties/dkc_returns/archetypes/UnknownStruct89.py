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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct85 import UnknownStruct85
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct86 import UnknownStruct86
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct87 import UnknownStruct87
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct88 import UnknownStruct88

if typing.TYPE_CHECKING:
    class UnknownStruct89Json(typing_extensions.TypedDict):
        gravity: float
        snap_to_spline: bool
        unknown_0xdaccc7de: bool
        unknown_0xcff6090d: float
        disable_attack_time: float
        minimum_toss_distance: float
        unknown_0xedf6ba25: float
        unknown_0x268ea25f: int
        anger_duration: float
        anim_grid: json_util.JsonObject
        unknown_struct85: json_util.JsonObject
        unknown_struct86: json_util.JsonObject
        unknown_struct87: json_util.JsonObject
        unknown_struct88: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct89(BaseProperty):
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    snap_to_spline: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x26ecb939, original_name='SnapToSpline'
        ),
    })
    unknown_0xdaccc7de: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdaccc7de, original_name='Unknown'
        ),
    })
    unknown_0xcff6090d: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcff6090d, original_name='Unknown'
        ),
    })
    disable_attack_time: float = dataclasses.field(default=0.6600000262260437, metadata={
        'reflection': FieldReflection[float](
            float, id=0x774ac83c, original_name='DisableAttackTime'
        ),
    })
    minimum_toss_distance: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7b95ab47, original_name='MinimumTossDistance'
        ),
    })
    unknown_0xedf6ba25: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xedf6ba25, original_name='Unknown'
        ),
    })
    unknown_0x268ea25f: int = dataclasses.field(default=5, metadata={
        'reflection': FieldReflection[int](
            int, id=0x268ea25f, original_name='Unknown'
        ),
    })
    anger_duration: float = dataclasses.field(default=3.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3a20fb9b, original_name='AngerDuration'
        ),
    })
    anim_grid: AnimGridModifierData = dataclasses.field(default_factory=AnimGridModifierData, metadata={
        'reflection': FieldReflection[AnimGridModifierData](
            AnimGridModifierData, id=0x68fd49ae, original_name='AnimGrid', from_json=AnimGridModifierData.from_json, to_json=AnimGridModifierData.to_json
        ),
    })
    unknown_struct85: UnknownStruct85 = dataclasses.field(default_factory=UnknownStruct85, metadata={
        'reflection': FieldReflection[UnknownStruct85](
            UnknownStruct85, id=0x00a81f44, original_name='UnknownStruct85', from_json=UnknownStruct85.from_json, to_json=UnknownStruct85.to_json
        ),
    })
    unknown_struct86: UnknownStruct86 = dataclasses.field(default_factory=UnknownStruct86, metadata={
        'reflection': FieldReflection[UnknownStruct86](
            UnknownStruct86, id=0xaceef42b, original_name='UnknownStruct86', from_json=UnknownStruct86.from_json, to_json=UnknownStruct86.to_json
        ),
    })
    unknown_struct87: UnknownStruct87 = dataclasses.field(default_factory=UnknownStruct87, metadata={
        'reflection': FieldReflection[UnknownStruct87](
            UnknownStruct87, id=0x1e64b8df, original_name='UnknownStruct87', from_json=UnknownStruct87.from_json, to_json=UnknownStruct87.to_json
        ),
    })
    unknown_struct88: UnknownStruct88 = dataclasses.field(default_factory=UnknownStruct88, metadata={
        'reflection': FieldReflection[UnknownStruct88](
            UnknownStruct88, id=0x04dedf14, original_name='UnknownStruct88', from_json=UnknownStruct88.from_json, to_json=UnknownStruct88.to_json
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
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26ecb939
        snap_to_spline = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdaccc7de
        unknown_0xdaccc7de = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcff6090d
        unknown_0xcff6090d = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x774ac83c
        disable_attack_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b95ab47
        minimum_toss_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xedf6ba25
        unknown_0xedf6ba25 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x268ea25f
        unknown_0x268ea25f = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a20fb9b
        anger_duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68fd49ae
        anim_grid = AnimGridModifierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00a81f44
        unknown_struct85 = UnknownStruct85.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaceef42b
        unknown_struct86 = UnknownStruct86.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1e64b8df
        unknown_struct87 = UnknownStruct87.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x04dedf14
        unknown_struct88 = UnknownStruct88.from_stream(data, property_size)
    
        return cls(gravity, snap_to_spline, unknown_0xdaccc7de, unknown_0xcff6090d, disable_attack_time, minimum_toss_distance, unknown_0xedf6ba25, unknown_0x268ea25f, anger_duration, anim_grid, unknown_struct85, unknown_struct86, unknown_struct87, unknown_struct88)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'\xda\xcc\xc7\xde')  # 0xdaccc7de
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdaccc7de))

        data.write(b'\xcf\xf6\t\r')  # 0xcff6090d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcff6090d))

        data.write(b'wJ\xc8<')  # 0x774ac83c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_attack_time))

        data.write(b'{\x95\xabG')  # 0x7b95ab47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_toss_distance))

        data.write(b'\xed\xf6\xba%')  # 0xedf6ba25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xedf6ba25))

        data.write(b'&\x8e\xa2_')  # 0x268ea25f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x268ea25f))

        data.write(b': \xfb\x9b')  # 0x3a20fb9b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anger_duration))

        data.write(b'h\xfdI\xae')  # 0x68fd49ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.anim_grid.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xa8\x1fD')  # 0xa81f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct85.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xac\xee\xf4+')  # 0xaceef42b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct86.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1ed\xb8\xdf')  # 0x1e64b8df
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x04\xde\xdf\x14')  # 0x4dedf14
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct88.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct89Json", data)
        return cls(
            gravity=json_data['gravity'],
            snap_to_spline=json_data['snap_to_spline'],
            unknown_0xdaccc7de=json_data['unknown_0xdaccc7de'],
            unknown_0xcff6090d=json_data['unknown_0xcff6090d'],
            disable_attack_time=json_data['disable_attack_time'],
            minimum_toss_distance=json_data['minimum_toss_distance'],
            unknown_0xedf6ba25=json_data['unknown_0xedf6ba25'],
            unknown_0x268ea25f=json_data['unknown_0x268ea25f'],
            anger_duration=json_data['anger_duration'],
            anim_grid=AnimGridModifierData.from_json(json_data['anim_grid']),
            unknown_struct85=UnknownStruct85.from_json(json_data['unknown_struct85']),
            unknown_struct86=UnknownStruct86.from_json(json_data['unknown_struct86']),
            unknown_struct87=UnknownStruct87.from_json(json_data['unknown_struct87']),
            unknown_struct88=UnknownStruct88.from_json(json_data['unknown_struct88']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gravity': self.gravity,
            'snap_to_spline': self.snap_to_spline,
            'unknown_0xdaccc7de': self.unknown_0xdaccc7de,
            'unknown_0xcff6090d': self.unknown_0xcff6090d,
            'disable_attack_time': self.disable_attack_time,
            'minimum_toss_distance': self.minimum_toss_distance,
            'unknown_0xedf6ba25': self.unknown_0xedf6ba25,
            'unknown_0x268ea25f': self.unknown_0x268ea25f,
            'anger_duration': self.anger_duration,
            'anim_grid': self.anim_grid.to_json(),
            'unknown_struct85': self.unknown_struct85.to_json(),
            'unknown_struct86': self.unknown_struct86.to_json(),
            'unknown_struct87': self.unknown_struct87.to_json(),
            'unknown_struct88': self.unknown_struct88.to_json(),
        }


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xdaccc7de(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xcff6090d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_toss_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xedf6ba25(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x268ea25f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_anger_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0xdaccc7de: ('unknown_0xdaccc7de', _decode_unknown_0xdaccc7de),
    0xcff6090d: ('unknown_0xcff6090d', _decode_unknown_0xcff6090d),
    0x774ac83c: ('disable_attack_time', _decode_disable_attack_time),
    0x7b95ab47: ('minimum_toss_distance', _decode_minimum_toss_distance),
    0xedf6ba25: ('unknown_0xedf6ba25', _decode_unknown_0xedf6ba25),
    0x268ea25f: ('unknown_0x268ea25f', _decode_unknown_0x268ea25f),
    0x3a20fb9b: ('anger_duration', _decode_anger_duration),
    0x68fd49ae: ('anim_grid', AnimGridModifierData.from_stream),
    0xa81f44: ('unknown_struct85', UnknownStruct85.from_stream),
    0xaceef42b: ('unknown_struct86', UnknownStruct86.from_stream),
    0x1e64b8df: ('unknown_struct87', UnknownStruct87.from_stream),
    0x4dedf14: ('unknown_struct88', UnknownStruct88.from_stream),
}

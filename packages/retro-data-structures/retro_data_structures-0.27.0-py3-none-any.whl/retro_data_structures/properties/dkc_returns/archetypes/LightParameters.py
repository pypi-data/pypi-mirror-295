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
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class LightParametersJson(typing_extensions.TypedDict):
        ambient_color: json_util.JsonValue
        world_lighting_options: int
        unknown_0x3dc5f0c6: bool
        light_recalculation: int
        lighting_position_offset: json_util.JsonValue
        unknown_0xa71810e9: bool
        unknown_0x287de7be: bool
        unknown_0xc1b12bb4: bool
        ignore_ambient_lighting: bool
        unknown_0xb772d4c1: bool
        num_dynamic_lights: int
        num_area_lights: int
        unknown_0x9fdf211a: float
        use_light_set: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xa33e5b0e, 0x6b5e7509, 0x3dc5f0c6, 0x628e6ac3, 0xd19de775, 0xa71810e9, 0x287de7be, 0xc1b12bb4, 0x61a940d6, 0xb772d4c1, 0xcac1e778, 0x67f4d3de, 0x9fdf211a, 0x1f715fd3)


@dataclasses.dataclass()
class LightParameters(BaseProperty):
    ambient_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xa33e5b0e, original_name='AmbientColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    world_lighting_options: enums.WorldLightingOptions = dataclasses.field(default=enums.WorldLightingOptions.NormalWorldLighting, metadata={
        'reflection': FieldReflection[enums.WorldLightingOptions](
            enums.WorldLightingOptions, id=0x6b5e7509, original_name='World Lighting Options', from_json=enums.WorldLightingOptions.from_json, to_json=enums.WorldLightingOptions.to_json
        ),
    })
    unknown_0x3dc5f0c6: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3dc5f0c6, original_name='Unknown'
        ),
    })
    light_recalculation: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x628e6ac3, original_name='LightRecalculation'
        ),
    })
    lighting_position_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xd19de775, original_name='LightingPositionOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_0xa71810e9: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa71810e9, original_name='Unknown'
        ),
    })
    unknown_0x287de7be: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x287de7be, original_name='Unknown'
        ),
    })
    unknown_0xc1b12bb4: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc1b12bb4, original_name='Unknown'
        ),
    })
    ignore_ambient_lighting: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x61a940d6, original_name='IgnoreAmbientLighting'
        ),
    })
    unknown_0xb772d4c1: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xb772d4c1, original_name='Unknown'
        ),
    })
    num_dynamic_lights: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0xcac1e778, original_name='NumDynamicLights'
        ),
    })
    num_area_lights: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0x67f4d3de, original_name='NumAreaLights'
        ),
    })
    unknown_0x9fdf211a: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9fdf211a, original_name='Unknown'
        ),
    })
    use_light_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x1f715fd3, original_name='UseLightSet'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHffffLHLLH?LHlLHfffLH?LH?LH?LH?LH?LHlLHlLHfLHl')
    
        dec = _FAST_FORMAT.unpack(data.read(142))
        assert (dec[0], dec[6], dec[9], dec[12], dec[15], dec[20], dec[23], dec[26], dec[29], dec[32], dec[35], dec[38], dec[41], dec[44]) == _FAST_IDS
        return cls(
            Color(*dec[2:6]),
            enums.WorldLightingOptions(dec[8]),
            dec[11],
            dec[14],
            Vector(*dec[17:20]),
            dec[22],
            dec[25],
            dec[28],
            dec[31],
            dec[34],
            dec[37],
            dec[40],
            dec[43],
            dec[46],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xa3>[\x0e')  # 0xa33e5b0e
        data.write(b'\x00\x10')  # size
        self.ambient_color.to_stream(data)

        data.write(b'k^u\t')  # 0x6b5e7509
        data.write(b'\x00\x04')  # size
        self.world_lighting_options.to_stream(data)

        data.write(b'=\xc5\xf0\xc6')  # 0x3dc5f0c6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3dc5f0c6))

        data.write(b'b\x8ej\xc3')  # 0x628e6ac3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_recalculation))

        data.write(b'\xd1\x9d\xe7u')  # 0xd19de775
        data.write(b'\x00\x0c')  # size
        self.lighting_position_offset.to_stream(data)

        data.write(b'\xa7\x18\x10\xe9')  # 0xa71810e9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa71810e9))

        data.write(b'(}\xe7\xbe')  # 0x287de7be
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x287de7be))

        data.write(b'\xc1\xb1+\xb4')  # 0xc1b12bb4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc1b12bb4))

        data.write(b'a\xa9@\xd6')  # 0x61a940d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_ambient_lighting))

        data.write(b'\xb7r\xd4\xc1')  # 0xb772d4c1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb772d4c1))

        data.write(b'\xca\xc1\xe7x')  # 0xcac1e778
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_dynamic_lights))

        data.write(b'g\xf4\xd3\xde')  # 0x67f4d3de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_area_lights))

        data.write(b'\x9f\xdf!\x1a')  # 0x9fdf211a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9fdf211a))

        data.write(b'\x1fq_\xd3')  # 0x1f715fd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.use_light_set))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("LightParametersJson", data)
        return cls(
            ambient_color=Color.from_json(json_data['ambient_color']),
            world_lighting_options=enums.WorldLightingOptions.from_json(json_data['world_lighting_options']),
            unknown_0x3dc5f0c6=json_data['unknown_0x3dc5f0c6'],
            light_recalculation=json_data['light_recalculation'],
            lighting_position_offset=Vector.from_json(json_data['lighting_position_offset']),
            unknown_0xa71810e9=json_data['unknown_0xa71810e9'],
            unknown_0x287de7be=json_data['unknown_0x287de7be'],
            unknown_0xc1b12bb4=json_data['unknown_0xc1b12bb4'],
            ignore_ambient_lighting=json_data['ignore_ambient_lighting'],
            unknown_0xb772d4c1=json_data['unknown_0xb772d4c1'],
            num_dynamic_lights=json_data['num_dynamic_lights'],
            num_area_lights=json_data['num_area_lights'],
            unknown_0x9fdf211a=json_data['unknown_0x9fdf211a'],
            use_light_set=json_data['use_light_set'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'ambient_color': self.ambient_color.to_json(),
            'world_lighting_options': self.world_lighting_options.to_json(),
            'unknown_0x3dc5f0c6': self.unknown_0x3dc5f0c6,
            'light_recalculation': self.light_recalculation,
            'lighting_position_offset': self.lighting_position_offset.to_json(),
            'unknown_0xa71810e9': self.unknown_0xa71810e9,
            'unknown_0x287de7be': self.unknown_0x287de7be,
            'unknown_0xc1b12bb4': self.unknown_0xc1b12bb4,
            'ignore_ambient_lighting': self.ignore_ambient_lighting,
            'unknown_0xb772d4c1': self.unknown_0xb772d4c1,
            'num_dynamic_lights': self.num_dynamic_lights,
            'num_area_lights': self.num_area_lights,
            'unknown_0x9fdf211a': self.unknown_0x9fdf211a,
            'use_light_set': self.use_light_set,
        }


def _decode_ambient_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_world_lighting_options(data: typing.BinaryIO, property_size: int):
    return enums.WorldLightingOptions.from_stream(data)


def _decode_unknown_0x3dc5f0c6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_light_recalculation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_lighting_position_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0xa71810e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x287de7be(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xc1b12bb4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_ambient_lighting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb772d4c1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_num_dynamic_lights(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_num_area_lights(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x9fdf211a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_light_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa33e5b0e: ('ambient_color', _decode_ambient_color),
    0x6b5e7509: ('world_lighting_options', _decode_world_lighting_options),
    0x3dc5f0c6: ('unknown_0x3dc5f0c6', _decode_unknown_0x3dc5f0c6),
    0x628e6ac3: ('light_recalculation', _decode_light_recalculation),
    0xd19de775: ('lighting_position_offset', _decode_lighting_position_offset),
    0xa71810e9: ('unknown_0xa71810e9', _decode_unknown_0xa71810e9),
    0x287de7be: ('unknown_0x287de7be', _decode_unknown_0x287de7be),
    0xc1b12bb4: ('unknown_0xc1b12bb4', _decode_unknown_0xc1b12bb4),
    0x61a940d6: ('ignore_ambient_lighting', _decode_ignore_ambient_lighting),
    0xb772d4c1: ('unknown_0xb772d4c1', _decode_unknown_0xb772d4c1),
    0xcac1e778: ('num_dynamic_lights', _decode_num_dynamic_lights),
    0x67f4d3de: ('num_area_lights', _decode_num_area_lights),
    0x9fdf211a: ('unknown_0x9fdf211a', _decode_unknown_0x9fdf211a),
    0x1f715fd3: ('use_light_set', _decode_use_light_set),
}

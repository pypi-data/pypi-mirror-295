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
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class TandemBeamJson(typing_extensions.TypedDict):
        tandem_beam_type: int
        maximum_beam_time: float
        activation_spline: json_util.JsonObject
        beam_width: float
        beam_default_length: float
        beam_sound: int
        beam_texture: int
        beam_telegraph_texture: int
        damage: json_util.JsonObject
        beam_telegraph_length: float
        beam_scroll_direction: int
        beam_scroll_speed: float
        beam_texture_uv_flip_speed: float
        alternate_beam_texture_v_coordinate: bool
        number_of_beam_texture_u_slots: int
        beam_texture_u0: float
        beam_texture_u1: float
        beam_texture_u2: float
        beam_texture_u3: float
    

@dataclasses.dataclass()
class TandemBeam(BaseProperty):
    tandem_beam_type: enums.TandemBeamType = dataclasses.field(default=enums.TandemBeamType.Unknown1, metadata={
        'reflection': FieldReflection[enums.TandemBeamType](
            enums.TandemBeamType, id=0xd045a194, original_name='TandemBeamType', from_json=enums.TandemBeamType.from_json, to_json=enums.TandemBeamType.to_json
        ),
    })
    maximum_beam_time: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb8d62ddf, original_name='MaximumBeamTime'
        ),
    })
    activation_spline: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x92708c7e, original_name='ActivationSpline', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    beam_width: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb956f379, original_name='BeamWidth'
        ),
    })
    beam_default_length: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x67a08f89, original_name='BeamDefaultLength'
        ),
    })
    beam_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0cd01c0e, original_name='BeamSound'
        ),
    })
    beam_texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc6f229c6, original_name='BeamTexture'
        ),
    })
    beam_telegraph_texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1b248c33, original_name='BeamTelegraphTexture'
        ),
    })
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0x337f9524, original_name='Damage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    beam_telegraph_length: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xaa7ae2ed, original_name='BeamTelegraphLength'
        ),
    })
    beam_scroll_direction: enums.BeamScrollDirection = dataclasses.field(default=enums.BeamScrollDirection.Unknown1, metadata={
        'reflection': FieldReflection[enums.BeamScrollDirection](
            enums.BeamScrollDirection, id=0xa5a3ef63, original_name='BeamScrollDirection', from_json=enums.BeamScrollDirection.from_json, to_json=enums.BeamScrollDirection.to_json
        ),
    })
    beam_scroll_speed: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xabf9f6fd, original_name='BeamScrollSpeed'
        ),
    })
    beam_texture_uv_flip_speed: float = dataclasses.field(default=0.0625, metadata={
        'reflection': FieldReflection[float](
            float, id=0xdb64abe3, original_name='BeamTextureUVFlipSpeed'
        ),
    })
    alternate_beam_texture_v_coordinate: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x82054423, original_name='AlternateBeamTextureVCoordinate'
        ),
    })
    number_of_beam_texture_u_slots: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0xadd9a3b6, original_name='NumberOfBeamTextureUSlots'
        ),
    })
    beam_texture_u0: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe40723ff, original_name='BeamTextureU0'
        ),
    })
    beam_texture_u1: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f5bf05a, original_name='BeamTextureU1'
        ),
    })
    beam_texture_u2: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa9cf82f4, original_name='BeamTextureU2'
        ),
    })
    beam_texture_u3: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0x62935151, original_name='BeamTextureU3'
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
        if property_count != 19:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd045a194
        tandem_beam_type = enums.TandemBeamType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb8d62ddf
        maximum_beam_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x92708c7e
        activation_spline = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb956f379
        beam_width = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67a08f89
        beam_default_length = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0cd01c0e
        beam_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc6f229c6
        beam_texture = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b248c33
        beam_telegraph_texture = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x337f9524
        damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaa7ae2ed
        beam_telegraph_length = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa5a3ef63
        beam_scroll_direction = enums.BeamScrollDirection.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xabf9f6fd
        beam_scroll_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb64abe3
        beam_texture_uv_flip_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82054423
        alternate_beam_texture_v_coordinate = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xadd9a3b6
        number_of_beam_texture_u_slots = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe40723ff
        beam_texture_u0 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f5bf05a
        beam_texture_u1 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa9cf82f4
        beam_texture_u2 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x62935151
        beam_texture_u3 = struct.unpack('>f', data.read(4))[0]
    
        return cls(tandem_beam_type, maximum_beam_time, activation_spline, beam_width, beam_default_length, beam_sound, beam_texture, beam_telegraph_texture, damage, beam_telegraph_length, beam_scroll_direction, beam_scroll_speed, beam_texture_uv_flip_speed, alternate_beam_texture_v_coordinate, number_of_beam_texture_u_slots, beam_texture_u0, beam_texture_u1, beam_texture_u2, beam_texture_u3)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'\xd0E\xa1\x94')  # 0xd045a194
        data.write(b'\x00\x04')  # size
        self.tandem_beam_type.to_stream(data)

        data.write(b'\xb8\xd6-\xdf')  # 0xb8d62ddf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_beam_time))

        data.write(b'\x92p\x8c~')  # 0x92708c7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.activation_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9V\xf3y')  # 0xb956f379
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_width))

        data.write(b'g\xa0\x8f\x89')  # 0x67a08f89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_default_length))

        data.write(b'\x0c\xd0\x1c\x0e')  # 0xcd01c0e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_sound))

        data.write(b'\xc6\xf2)\xc6')  # 0xc6f229c6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_texture))

        data.write(b'\x1b$\x8c3')  # 0x1b248c33
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.beam_telegraph_texture))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaaz\xe2\xed')  # 0xaa7ae2ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_telegraph_length))

        data.write(b'\xa5\xa3\xefc')  # 0xa5a3ef63
        data.write(b'\x00\x04')  # size
        self.beam_scroll_direction.to_stream(data)

        data.write(b'\xab\xf9\xf6\xfd')  # 0xabf9f6fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_scroll_speed))

        data.write(b'\xdbd\xab\xe3')  # 0xdb64abe3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_uv_flip_speed))

        data.write(b'\x82\x05D#')  # 0x82054423
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.alternate_beam_texture_v_coordinate))

        data.write(b'\xad\xd9\xa3\xb6')  # 0xadd9a3b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_beam_texture_u_slots))

        data.write(b'\xe4\x07#\xff')  # 0xe40723ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u0))

        data.write(b'/[\xf0Z')  # 0x2f5bf05a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u1))

        data.write(b'\xa9\xcf\x82\xf4')  # 0xa9cf82f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u2))

        data.write(b'b\x93QQ')  # 0x62935151
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_texture_u3))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TandemBeamJson", data)
        return cls(
            tandem_beam_type=enums.TandemBeamType.from_json(json_data['tandem_beam_type']),
            maximum_beam_time=json_data['maximum_beam_time'],
            activation_spline=Spline.from_json(json_data['activation_spline']),
            beam_width=json_data['beam_width'],
            beam_default_length=json_data['beam_default_length'],
            beam_sound=json_data['beam_sound'],
            beam_texture=json_data['beam_texture'],
            beam_telegraph_texture=json_data['beam_telegraph_texture'],
            damage=DamageInfo.from_json(json_data['damage']),
            beam_telegraph_length=json_data['beam_telegraph_length'],
            beam_scroll_direction=enums.BeamScrollDirection.from_json(json_data['beam_scroll_direction']),
            beam_scroll_speed=json_data['beam_scroll_speed'],
            beam_texture_uv_flip_speed=json_data['beam_texture_uv_flip_speed'],
            alternate_beam_texture_v_coordinate=json_data['alternate_beam_texture_v_coordinate'],
            number_of_beam_texture_u_slots=json_data['number_of_beam_texture_u_slots'],
            beam_texture_u0=json_data['beam_texture_u0'],
            beam_texture_u1=json_data['beam_texture_u1'],
            beam_texture_u2=json_data['beam_texture_u2'],
            beam_texture_u3=json_data['beam_texture_u3'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'tandem_beam_type': self.tandem_beam_type.to_json(),
            'maximum_beam_time': self.maximum_beam_time,
            'activation_spline': self.activation_spline.to_json(),
            'beam_width': self.beam_width,
            'beam_default_length': self.beam_default_length,
            'beam_sound': self.beam_sound,
            'beam_texture': self.beam_texture,
            'beam_telegraph_texture': self.beam_telegraph_texture,
            'damage': self.damage.to_json(),
            'beam_telegraph_length': self.beam_telegraph_length,
            'beam_scroll_direction': self.beam_scroll_direction.to_json(),
            'beam_scroll_speed': self.beam_scroll_speed,
            'beam_texture_uv_flip_speed': self.beam_texture_uv_flip_speed,
            'alternate_beam_texture_v_coordinate': self.alternate_beam_texture_v_coordinate,
            'number_of_beam_texture_u_slots': self.number_of_beam_texture_u_slots,
            'beam_texture_u0': self.beam_texture_u0,
            'beam_texture_u1': self.beam_texture_u1,
            'beam_texture_u2': self.beam_texture_u2,
            'beam_texture_u3': self.beam_texture_u3,
        }


def _decode_tandem_beam_type(data: typing.BinaryIO, property_size: int):
    return enums.TandemBeamType.from_stream(data)


def _decode_maximum_beam_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_default_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_telegraph_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_beam_telegraph_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_scroll_direction(data: typing.BinaryIO, property_size: int):
    return enums.BeamScrollDirection.from_stream(data)


def _decode_beam_scroll_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_uv_flip_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alternate_beam_texture_v_coordinate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_number_of_beam_texture_u_slots(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_beam_texture_u0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_u1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_u2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_texture_u3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd045a194: ('tandem_beam_type', _decode_tandem_beam_type),
    0xb8d62ddf: ('maximum_beam_time', _decode_maximum_beam_time),
    0x92708c7e: ('activation_spline', Spline.from_stream),
    0xb956f379: ('beam_width', _decode_beam_width),
    0x67a08f89: ('beam_default_length', _decode_beam_default_length),
    0xcd01c0e: ('beam_sound', _decode_beam_sound),
    0xc6f229c6: ('beam_texture', _decode_beam_texture),
    0x1b248c33: ('beam_telegraph_texture', _decode_beam_telegraph_texture),
    0x337f9524: ('damage', DamageInfo.from_stream),
    0xaa7ae2ed: ('beam_telegraph_length', _decode_beam_telegraph_length),
    0xa5a3ef63: ('beam_scroll_direction', _decode_beam_scroll_direction),
    0xabf9f6fd: ('beam_scroll_speed', _decode_beam_scroll_speed),
    0xdb64abe3: ('beam_texture_uv_flip_speed', _decode_beam_texture_uv_flip_speed),
    0x82054423: ('alternate_beam_texture_v_coordinate', _decode_alternate_beam_texture_v_coordinate),
    0xadd9a3b6: ('number_of_beam_texture_u_slots', _decode_number_of_beam_texture_u_slots),
    0xe40723ff: ('beam_texture_u0', _decode_beam_texture_u0),
    0x2f5bf05a: ('beam_texture_u1', _decode_beam_texture_u1),
    0xa9cf82f4: ('beam_texture_u2', _decode_beam_texture_u2),
    0x62935151: ('beam_texture_u3', _decode_beam_texture_u3),
}

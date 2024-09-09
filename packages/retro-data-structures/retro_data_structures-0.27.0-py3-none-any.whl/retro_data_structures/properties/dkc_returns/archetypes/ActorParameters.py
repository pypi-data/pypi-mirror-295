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
from retro_data_structures.properties.dkc_returns.archetypes.LightParameters import LightParameters

if typing.TYPE_CHECKING:
    class ActorParametersJson(typing_extensions.TypedDict):
        lighting: json_util.JsonObject
        use_global_render_time: bool
        fade_in_time: float
        fade_out_time: float
        force_render_unsorted: bool
        takes_projected_shadow: bool
        actor_material_type: int
        is_camera_blocker: bool
        is_camera_target: bool
        deactivate_on_death: bool
    

@dataclasses.dataclass()
class ActorParameters(BaseProperty):
    lighting: LightParameters = dataclasses.field(default_factory=LightParameters, metadata={
        'reflection': FieldReflection[LightParameters](
            LightParameters, id=0xb028db0e, original_name='Lighting', from_json=LightParameters.from_json, to_json=LightParameters.to_json
        ),
    })
    use_global_render_time: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1499803c, original_name='UseGlobalRenderTime'
        ),
    })
    fade_in_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x90aa341f, original_name='FadeInTime'
        ),
    })
    fade_out_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7c269ebc, original_name='FadeOutTime'
        ),
    })
    force_render_unsorted: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x799263f1, original_name='ForceRenderUnsorted'
        ),
    })
    takes_projected_shadow: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xed3a6e87, original_name='TakesProjectedShadow'
        ),
    })
    actor_material_type: enums.UnknownEnum1 = dataclasses.field(default=enums.UnknownEnum1.Unknown1, metadata={
        'reflection': FieldReflection[enums.UnknownEnum1](
            enums.UnknownEnum1, id=0xe315ee72, original_name='ActorMaterialType', from_json=enums.UnknownEnum1.from_json, to_json=enums.UnknownEnum1.to_json
        ),
    })
    is_camera_blocker: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6da86200, original_name='IsCameraBlocker'
        ),
    })
    is_camera_target: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1bcab75c, original_name='IsCameraTarget'
        ),
    })
    deactivate_on_death: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x101ea33e, original_name='DeactivateOnDeath'
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
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb028db0e
        lighting = LightParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1499803c
        use_global_render_time = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x90aa341f
        fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c269ebc
        fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x799263f1
        force_render_unsorted = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xed3a6e87
        takes_projected_shadow = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe315ee72
        actor_material_type = enums.UnknownEnum1.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6da86200
        is_camera_blocker = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1bcab75c
        is_camera_target = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x101ea33e
        deactivate_on_death = struct.unpack('>?', data.read(1))[0]
    
        return cls(lighting, use_global_render_time, fade_in_time, fade_out_time, force_render_unsorted, takes_projected_shadow, actor_material_type, is_camera_blocker, is_camera_target, deactivate_on_death)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xb0(\xdb\x0e')  # 0xb028db0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lighting.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x14\x99\x80<')  # 0x1499803c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_global_render_time))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'y\x92c\xf1')  # 0x799263f1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_render_unsorted))

        data.write(b'\xed:n\x87')  # 0xed3a6e87
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.takes_projected_shadow))

        data.write(b'\xe3\x15\xeer')  # 0xe315ee72
        data.write(b'\x00\x04')  # size
        self.actor_material_type.to_stream(data)

        data.write(b'm\xa8b\x00')  # 0x6da86200
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_camera_blocker))

        data.write(b'\x1b\xca\xb7\\')  # 0x1bcab75c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_camera_target))

        data.write(b'\x10\x1e\xa3>')  # 0x101ea33e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.deactivate_on_death))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ActorParametersJson", data)
        return cls(
            lighting=LightParameters.from_json(json_data['lighting']),
            use_global_render_time=json_data['use_global_render_time'],
            fade_in_time=json_data['fade_in_time'],
            fade_out_time=json_data['fade_out_time'],
            force_render_unsorted=json_data['force_render_unsorted'],
            takes_projected_shadow=json_data['takes_projected_shadow'],
            actor_material_type=enums.UnknownEnum1.from_json(json_data['actor_material_type']),
            is_camera_blocker=json_data['is_camera_blocker'],
            is_camera_target=json_data['is_camera_target'],
            deactivate_on_death=json_data['deactivate_on_death'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'lighting': self.lighting.to_json(),
            'use_global_render_time': self.use_global_render_time,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'force_render_unsorted': self.force_render_unsorted,
            'takes_projected_shadow': self.takes_projected_shadow,
            'actor_material_type': self.actor_material_type.to_json(),
            'is_camera_blocker': self.is_camera_blocker,
            'is_camera_target': self.is_camera_target,
            'deactivate_on_death': self.deactivate_on_death,
        }


def _decode_use_global_render_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_force_render_unsorted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_takes_projected_shadow(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_actor_material_type(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum1.from_stream(data)


def _decode_is_camera_blocker(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_camera_target(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_deactivate_on_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb028db0e: ('lighting', LightParameters.from_stream),
    0x1499803c: ('use_global_render_time', _decode_use_global_render_time),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0x799263f1: ('force_render_unsorted', _decode_force_render_unsorted),
    0xed3a6e87: ('takes_projected_shadow', _decode_takes_projected_shadow),
    0xe315ee72: ('actor_material_type', _decode_actor_material_type),
    0x6da86200: ('is_camera_blocker', _decode_is_camera_blocker),
    0x1bcab75c: ('is_camera_target', _decode_is_camera_target),
    0x101ea33e: ('deactivate_on_death', _decode_deactivate_on_death),
}

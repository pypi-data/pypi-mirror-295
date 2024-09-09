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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct248Json(typing_extensions.TypedDict):
        camera_fade: bool
        camera_fade_out_delay_time: float
        camera_fade_out_delay_time_after_deathfall: float
        camera_fade_out_time: float
        camera_fade_in_time: float
        death_transition_time: float
        superguide_death_transition_time: float
        volume_fade_out_time: float
        volume_fade_in_time: float
        unknown: str
        balloon_decrement_sound: int
    

@dataclasses.dataclass()
class UnknownStruct248(BaseProperty):
    camera_fade: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9a6210d3, original_name='CameraFade'
        ),
    })
    camera_fade_out_delay_time: float = dataclasses.field(default=0.800000011920929, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7466f048, original_name='CameraFadeOutDelayTime'
        ),
    })
    camera_fade_out_delay_time_after_deathfall: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb0af3909, original_name='CameraFadeOutDelayTimeAfterDeathfall'
        ),
    })
    camera_fade_out_time: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc3dd8389, original_name='CameraFadeOutTime'
        ),
    })
    camera_fade_in_time: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbbd6172c, original_name='CameraFadeInTime'
        ),
    })
    death_transition_time: float = dataclasses.field(default=2.1500000953674316, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6f332701, original_name='DeathTransitionTime'
        ),
    })
    superguide_death_transition_time: float = dataclasses.field(default=3.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd3c7a4fa, original_name='SuperguideDeathTransitionTime'
        ),
    })
    volume_fade_out_time: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f9ded4b, original_name='VolumeFadeOutTime'
        ),
    })
    volume_fade_in_time: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0x984af3ed, original_name='VolumeFadeInTime'
        ),
    })
    unknown: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x2bd2ae32, original_name='Unknown'
        ),
    })
    balloon_decrement_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7c519662, original_name='BalloonDecrementSound'
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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a6210d3
        camera_fade = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7466f048
        camera_fade_out_delay_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0af3909
        camera_fade_out_delay_time_after_deathfall = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc3dd8389
        camera_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbd6172c
        camera_fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6f332701
        death_transition_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd3c7a4fa
        superguide_death_transition_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f9ded4b
        volume_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x984af3ed
        volume_fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2bd2ae32
        unknown = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c519662
        balloon_decrement_sound = struct.unpack(">Q", data.read(8))[0]
    
        return cls(camera_fade, camera_fade_out_delay_time, camera_fade_out_delay_time_after_deathfall, camera_fade_out_time, camera_fade_in_time, death_transition_time, superguide_death_transition_time, volume_fade_out_time, volume_fade_in_time, unknown, balloon_decrement_sound)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\x9ab\x10\xd3')  # 0x9a6210d3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.camera_fade))

        data.write(b'tf\xf0H')  # 0x7466f048
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_delay_time))

        data.write(b'\xb0\xaf9\t')  # 0xb0af3909
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_delay_time_after_deathfall))

        data.write(b'\xc3\xdd\x83\x89')  # 0xc3dd8389
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_time))

        data.write(b'\xbb\xd6\x17,')  # 0xbbd6172c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_in_time))

        data.write(b"o3'\x01")  # 0x6f332701
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.death_transition_time))

        data.write(b'\xd3\xc7\xa4\xfa')  # 0xd3c7a4fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.superguide_death_transition_time))

        data.write(b'/\x9d\xedK')  # 0x2f9ded4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume_fade_out_time))

        data.write(b'\x98J\xf3\xed')  # 0x984af3ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume_fade_in_time))

        data.write(b'+\xd2\xae2')  # 0x2bd2ae32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|Q\x96b')  # 0x7c519662
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.balloon_decrement_sound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct248Json", data)
        return cls(
            camera_fade=json_data['camera_fade'],
            camera_fade_out_delay_time=json_data['camera_fade_out_delay_time'],
            camera_fade_out_delay_time_after_deathfall=json_data['camera_fade_out_delay_time_after_deathfall'],
            camera_fade_out_time=json_data['camera_fade_out_time'],
            camera_fade_in_time=json_data['camera_fade_in_time'],
            death_transition_time=json_data['death_transition_time'],
            superguide_death_transition_time=json_data['superguide_death_transition_time'],
            volume_fade_out_time=json_data['volume_fade_out_time'],
            volume_fade_in_time=json_data['volume_fade_in_time'],
            unknown=json_data['unknown'],
            balloon_decrement_sound=json_data['balloon_decrement_sound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'camera_fade': self.camera_fade,
            'camera_fade_out_delay_time': self.camera_fade_out_delay_time,
            'camera_fade_out_delay_time_after_deathfall': self.camera_fade_out_delay_time_after_deathfall,
            'camera_fade_out_time': self.camera_fade_out_time,
            'camera_fade_in_time': self.camera_fade_in_time,
            'death_transition_time': self.death_transition_time,
            'superguide_death_transition_time': self.superguide_death_transition_time,
            'volume_fade_out_time': self.volume_fade_out_time,
            'volume_fade_in_time': self.volume_fade_in_time,
            'unknown': self.unknown,
            'balloon_decrement_sound': self.balloon_decrement_sound,
        }


def _decode_camera_fade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_camera_fade_out_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_fade_out_delay_time_after_deathfall(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_transition_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_superguide_death_transition_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_balloon_decrement_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9a6210d3: ('camera_fade', _decode_camera_fade),
    0x7466f048: ('camera_fade_out_delay_time', _decode_camera_fade_out_delay_time),
    0xb0af3909: ('camera_fade_out_delay_time_after_deathfall', _decode_camera_fade_out_delay_time_after_deathfall),
    0xc3dd8389: ('camera_fade_out_time', _decode_camera_fade_out_time),
    0xbbd6172c: ('camera_fade_in_time', _decode_camera_fade_in_time),
    0x6f332701: ('death_transition_time', _decode_death_transition_time),
    0xd3c7a4fa: ('superguide_death_transition_time', _decode_superguide_death_transition_time),
    0x2f9ded4b: ('volume_fade_out_time', _decode_volume_fade_out_time),
    0x984af3ed: ('volume_fade_in_time', _decode_volume_fade_in_time),
    0x2bd2ae32: ('unknown', _decode_unknown),
    0x7c519662: ('balloon_decrement_sound', _decode_balloon_decrement_sound),
}

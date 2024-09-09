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

if typing.TYPE_CHECKING:
    class UnknownStruct249Json(typing_extensions.TypedDict):
        music_fade: bool
        music_fade_out_time: float
        play_jingle: bool
        camera_fade: bool
        camera_fade_out_delay_time: float
        camera_fade_out_time: float
        interface_delay_time: float
        volume_fade_out_time: float
        unknown: str
    

@dataclasses.dataclass()
class UnknownStruct249(BaseProperty):
    music_fade: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xed5ec8a1, original_name='MusicFade'
        ),
    })
    music_fade_out_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8dcea34f, original_name='MusicFadeOutTime'
        ),
    })
    play_jingle: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0397dcf7, original_name='PlayJingle'
        ),
    })
    camera_fade: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9a6210d3, original_name='CameraFade'
        ),
    })
    camera_fade_out_delay_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7466f048, original_name='CameraFadeOutDelayTime'
        ),
    })
    camera_fade_out_time: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc3dd8389, original_name='CameraFadeOutTime'
        ),
    })
    interface_delay_time: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x746a13e9, original_name='InterfaceDelayTime'
        ),
    })
    volume_fade_out_time: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f9ded4b, original_name='VolumeFadeOutTime'
        ),
    })
    unknown: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x2bd2ae32, original_name='Unknown'
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
        assert property_id == 0xed5ec8a1
        music_fade = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8dcea34f
        music_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0397dcf7
        play_jingle = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a6210d3
        camera_fade = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7466f048
        camera_fade_out_delay_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc3dd8389
        camera_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x746a13e9
        interface_delay_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f9ded4b
        volume_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2bd2ae32
        unknown = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(music_fade, music_fade_out_time, play_jingle, camera_fade, camera_fade_out_delay_time, camera_fade_out_time, interface_delay_time, volume_fade_out_time, unknown)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xed^\xc8\xa1')  # 0xed5ec8a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.music_fade))

        data.write(b'\x8d\xce\xa3O')  # 0x8dcea34f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.music_fade_out_time))

        data.write(b'\x03\x97\xdc\xf7')  # 0x397dcf7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.play_jingle))

        data.write(b'\x9ab\x10\xd3')  # 0x9a6210d3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.camera_fade))

        data.write(b'tf\xf0H')  # 0x7466f048
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_delay_time))

        data.write(b'\xc3\xdd\x83\x89')  # 0xc3dd8389
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_time))

        data.write(b'tj\x13\xe9')  # 0x746a13e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.interface_delay_time))

        data.write(b'/\x9d\xedK')  # 0x2f9ded4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume_fade_out_time))

        data.write(b'+\xd2\xae2')  # 0x2bd2ae32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct249Json", data)
        return cls(
            music_fade=json_data['music_fade'],
            music_fade_out_time=json_data['music_fade_out_time'],
            play_jingle=json_data['play_jingle'],
            camera_fade=json_data['camera_fade'],
            camera_fade_out_delay_time=json_data['camera_fade_out_delay_time'],
            camera_fade_out_time=json_data['camera_fade_out_time'],
            interface_delay_time=json_data['interface_delay_time'],
            volume_fade_out_time=json_data['volume_fade_out_time'],
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'music_fade': self.music_fade,
            'music_fade_out_time': self.music_fade_out_time,
            'play_jingle': self.play_jingle,
            'camera_fade': self.camera_fade,
            'camera_fade_out_delay_time': self.camera_fade_out_delay_time,
            'camera_fade_out_time': self.camera_fade_out_time,
            'interface_delay_time': self.interface_delay_time,
            'volume_fade_out_time': self.volume_fade_out_time,
            'unknown': self.unknown,
        }


def _decode_music_fade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_music_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_play_jingle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_camera_fade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_camera_fade_out_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_interface_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xed5ec8a1: ('music_fade', _decode_music_fade),
    0x8dcea34f: ('music_fade_out_time', _decode_music_fade_out_time),
    0x397dcf7: ('play_jingle', _decode_play_jingle),
    0x9a6210d3: ('camera_fade', _decode_camera_fade),
    0x7466f048: ('camera_fade_out_delay_time', _decode_camera_fade_out_delay_time),
    0xc3dd8389: ('camera_fade_out_time', _decode_camera_fade_out_time),
    0x746a13e9: ('interface_delay_time', _decode_interface_delay_time),
    0x2f9ded4b: ('volume_fade_out_time', _decode_volume_fade_out_time),
    0x2bd2ae32: ('unknown', _decode_unknown),
}

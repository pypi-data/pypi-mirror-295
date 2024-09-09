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

if typing.TYPE_CHECKING:
    class UnknownStruct241Json(typing_extensions.TypedDict):
        part_of_music_system: bool
        auto_buffer: bool
        auto_buffer_when_stopped: bool
        auto_play_when_buffered: bool
        fade_in_time: float
        fade_out_time: float
        volume: float
        save_preload_data: bool
        start_delay: float
        music_system_area_state: int
        volume_type: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x2e7c745f, 0xc03ec271, 0xe687518, 0xea8d54f4, 0x90aa341f, 0x7c269ebc, 0xc7a7f189, 0xd74245a4, 0x196e17d9, 0xfb8f0b1f, 0x9558711e)


@dataclasses.dataclass()
class UnknownStruct241(BaseProperty):
    part_of_music_system: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2e7c745f, original_name='PartOfMusicSystem'
        ),
    })
    auto_buffer: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc03ec271, original_name='AutoBuffer'
        ),
    })
    auto_buffer_when_stopped: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0e687518, original_name='AutoBufferWhenStopped'
        ),
    })
    auto_play_when_buffered: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xea8d54f4, original_name='AutoPlayWhenBuffered'
        ),
    })
    fade_in_time: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0x90aa341f, original_name='FadeInTime'
        ),
    })
    fade_out_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7c269ebc, original_name='FadeOutTime'
        ),
    })
    volume: float = dataclasses.field(default=-6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc7a7f189, original_name='Volume'
        ),
    })
    save_preload_data: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd74245a4, original_name='SavePreloadData'
        ),
    })
    start_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x196e17d9, original_name='StartDelay'
        ),
    })
    music_system_area_state: enums.MusicEnumB = dataclasses.field(default=enums.MusicEnumB.Unknown1, metadata={
        'reflection': FieldReflection[enums.MusicEnumB](
            enums.MusicEnumB, id=0xfb8f0b1f, original_name='MusicSystemAreaState', from_json=enums.MusicEnumB.from_json, to_json=enums.MusicEnumB.to_json
        ),
    })
    volume_type: enums.MusicEnumA = dataclasses.field(default=enums.MusicEnumA.Unknown2, metadata={
        'reflection': FieldReflection[enums.MusicEnumA](
            enums.MusicEnumA, id=0x9558711e, original_name='VolumeType', from_json=enums.MusicEnumA.from_json, to_json=enums.MusicEnumA.to_json
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LHfLHfLHfLH?LHfLHLLHL')
    
        dec = _FAST_FORMAT.unpack(data.read(95))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
            enums.MusicEnumB(dec[29]),
            enums.MusicEnumA(dec[32]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'.|t_')  # 0x2e7c745f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.part_of_music_system))

        data.write(b'\xc0>\xc2q')  # 0xc03ec271
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_buffer))

        data.write(b'\x0ehu\x18')  # 0xe687518
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_buffer_when_stopped))

        data.write(b'\xea\x8dT\xf4')  # 0xea8d54f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_play_when_buffered))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xc7\xa7\xf1\x89')  # 0xc7a7f189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume))

        data.write(b'\xd7BE\xa4')  # 0xd74245a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.save_preload_data))

        data.write(b'\x19n\x17\xd9')  # 0x196e17d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_delay))

        data.write(b'\xfb\x8f\x0b\x1f')  # 0xfb8f0b1f
        data.write(b'\x00\x04')  # size
        self.music_system_area_state.to_stream(data)

        data.write(b'\x95Xq\x1e')  # 0x9558711e
        data.write(b'\x00\x04')  # size
        self.volume_type.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct241Json", data)
        return cls(
            part_of_music_system=json_data['part_of_music_system'],
            auto_buffer=json_data['auto_buffer'],
            auto_buffer_when_stopped=json_data['auto_buffer_when_stopped'],
            auto_play_when_buffered=json_data['auto_play_when_buffered'],
            fade_in_time=json_data['fade_in_time'],
            fade_out_time=json_data['fade_out_time'],
            volume=json_data['volume'],
            save_preload_data=json_data['save_preload_data'],
            start_delay=json_data['start_delay'],
            music_system_area_state=enums.MusicEnumB.from_json(json_data['music_system_area_state']),
            volume_type=enums.MusicEnumA.from_json(json_data['volume_type']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'part_of_music_system': self.part_of_music_system,
            'auto_buffer': self.auto_buffer,
            'auto_buffer_when_stopped': self.auto_buffer_when_stopped,
            'auto_play_when_buffered': self.auto_play_when_buffered,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'volume': self.volume,
            'save_preload_data': self.save_preload_data,
            'start_delay': self.start_delay,
            'music_system_area_state': self.music_system_area_state.to_json(),
            'volume_type': self.volume_type.to_json(),
        }


def _decode_part_of_music_system(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_buffer_when_stopped(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_play_when_buffered(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_save_preload_data(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_music_system_area_state(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumB.from_stream(data)


def _decode_volume_type(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumA.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2e7c745f: ('part_of_music_system', _decode_part_of_music_system),
    0xc03ec271: ('auto_buffer', _decode_auto_buffer),
    0xe687518: ('auto_buffer_when_stopped', _decode_auto_buffer_when_stopped),
    0xea8d54f4: ('auto_play_when_buffered', _decode_auto_play_when_buffered),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xc7a7f189: ('volume', _decode_volume),
    0xd74245a4: ('save_preload_data', _decode_save_preload_data),
    0x196e17d9: ('start_delay', _decode_start_delay),
    0xfb8f0b1f: ('music_system_area_state', _decode_music_system_area_state),
    0x9558711e: ('volume_type', _decode_volume_type),
}

# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.field_reflection import FieldReflection
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class StreamedAudioJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        song_file: int
        dvd_file: str
        auto_buffer: bool
        auto_buffer_when_stopped: bool
        auto_play_when_buffered: bool
        start_faded_out: bool
        fade_in_time: float
        fade_out_time: float
        volume: float
        pan: float
        positional: bool
        min_audible_distance: float
        max_audible_distance: float
        fall_off: float
        use_room_acoustics: bool
        start_sample: int
        is_default_retronome_music: bool
        part_of_music_system: bool
        save_preload_data: bool
        sound_group_names: str
        start_delay: float
        music_system_area_state: int
        volume_type: int
    

@dataclasses.dataclass()
class StreamedAudio(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    song_file: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRM'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9d1a67a8, original_name='SongFile'
        ),
    })
    dvd_file: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xb417064a, original_name='DvdFile'
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
    start_faded_out: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xeb250a0b, original_name='StartFadedOut'
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
    pan: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xdf4353a3, original_name='Pan'
        ),
    })
    positional: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6e0e81f8, original_name='Positional'
        ),
    })
    min_audible_distance: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x25d4798a, original_name='MinAudibleDistance'
        ),
    })
    max_audible_distance: float = dataclasses.field(default=75.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x214e48a0, original_name='MaxAudibleDistance'
        ),
    })
    fall_off: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x72531867, original_name='FallOff'
        ),
    })
    use_room_acoustics: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x85707354, original_name='UseRoomAcoustics'
        ),
    })
    start_sample: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xe88ff377, original_name='StartSample'
        ),
    })
    is_default_retronome_music: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0794c3eb, original_name='IsDefaultRetronomeMusic'
        ),
    })
    part_of_music_system: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2e7c745f, original_name='PartOfMusicSystem'
        ),
    })
    save_preload_data: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd74245a4, original_name='SavePreloadData'
        ),
    })
    sound_group_names: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xc871bd1b, original_name='SoundGroupNames'
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

    def get_name(self) -> str | None:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'STAU'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 24:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9d1a67a8
        song_file = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb417064a
        dvd_file = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc03ec271
        auto_buffer = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0e687518
        auto_buffer_when_stopped = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xea8d54f4
        auto_play_when_buffered = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb250a0b
        start_faded_out = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x90aa341f
        fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c269ebc
        fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc7a7f189
        volume = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdf4353a3
        pan = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6e0e81f8
        positional = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x25d4798a
        min_audible_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x214e48a0
        max_audible_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x72531867
        fall_off = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x85707354
        use_room_acoustics = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe88ff377
        start_sample = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0794c3eb
        is_default_retronome_music = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e7c745f
        part_of_music_system = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd74245a4
        save_preload_data = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc871bd1b
        sound_group_names = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x196e17d9
        start_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfb8f0b1f
        music_system_area_state = enums.MusicEnumB.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9558711e
        volume_type = enums.MusicEnumA.from_stream(data)
    
        return cls(editor_properties, song_file, dvd_file, auto_buffer, auto_buffer_when_stopped, auto_play_when_buffered, start_faded_out, fade_in_time, fade_out_time, volume, pan, positional, min_audible_distance, max_audible_distance, fall_off, use_room_acoustics, start_sample, is_default_retronome_music, part_of_music_system, save_preload_data, sound_group_names, start_delay, music_system_area_state, volume_type)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\x1ag\xa8')  # 0x9d1a67a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.song_file))

        data.write(b'\xb4\x17\x06J')  # 0xb417064a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.dvd_file.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0>\xc2q')  # 0xc03ec271
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_buffer))

        data.write(b'\x0ehu\x18')  # 0xe687518
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_buffer_when_stopped))

        data.write(b'\xea\x8dT\xf4')  # 0xea8d54f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_play_when_buffered))

        data.write(b'\xeb%\n\x0b')  # 0xeb250a0b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_faded_out))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xc7\xa7\xf1\x89')  # 0xc7a7f189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume))

        data.write(b'\xdfCS\xa3')  # 0xdf4353a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pan))

        data.write(b'n\x0e\x81\xf8')  # 0x6e0e81f8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.positional))

        data.write(b'%\xd4y\x8a')  # 0x25d4798a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_audible_distance))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'rS\x18g')  # 0x72531867
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fall_off))

        data.write(b'\x85psT')  # 0x85707354
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_room_acoustics))

        data.write(b'\xe8\x8f\xf3w')  # 0xe88ff377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.start_sample))

        data.write(b'\x07\x94\xc3\xeb')  # 0x794c3eb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_default_retronome_music))

        data.write(b'.|t_')  # 0x2e7c745f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.part_of_music_system))

        data.write(b'\xd7BE\xa4')  # 0xd74245a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.save_preload_data))

        data.write(b'\xc8q\xbd\x1b')  # 0xc871bd1b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.sound_group_names.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19n\x17\xd9')  # 0x196e17d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_delay))

        data.write(b'\xfb\x8f\x0b\x1f')  # 0xfb8f0b1f
        data.write(b'\x00\x04')  # size
        self.music_system_area_state.to_stream(data)

        data.write(b'\x95Xq\x1e')  # 0x9558711e
        data.write(b'\x00\x04')  # size
        self.volume_type.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("StreamedAudioJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            song_file=json_data['song_file'],
            dvd_file=json_data['dvd_file'],
            auto_buffer=json_data['auto_buffer'],
            auto_buffer_when_stopped=json_data['auto_buffer_when_stopped'],
            auto_play_when_buffered=json_data['auto_play_when_buffered'],
            start_faded_out=json_data['start_faded_out'],
            fade_in_time=json_data['fade_in_time'],
            fade_out_time=json_data['fade_out_time'],
            volume=json_data['volume'],
            pan=json_data['pan'],
            positional=json_data['positional'],
            min_audible_distance=json_data['min_audible_distance'],
            max_audible_distance=json_data['max_audible_distance'],
            fall_off=json_data['fall_off'],
            use_room_acoustics=json_data['use_room_acoustics'],
            start_sample=json_data['start_sample'],
            is_default_retronome_music=json_data['is_default_retronome_music'],
            part_of_music_system=json_data['part_of_music_system'],
            save_preload_data=json_data['save_preload_data'],
            sound_group_names=json_data['sound_group_names'],
            start_delay=json_data['start_delay'],
            music_system_area_state=enums.MusicEnumB.from_json(json_data['music_system_area_state']),
            volume_type=enums.MusicEnumA.from_json(json_data['volume_type']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'song_file': self.song_file,
            'dvd_file': self.dvd_file,
            'auto_buffer': self.auto_buffer,
            'auto_buffer_when_stopped': self.auto_buffer_when_stopped,
            'auto_play_when_buffered': self.auto_play_when_buffered,
            'start_faded_out': self.start_faded_out,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'volume': self.volume,
            'pan': self.pan,
            'positional': self.positional,
            'min_audible_distance': self.min_audible_distance,
            'max_audible_distance': self.max_audible_distance,
            'fall_off': self.fall_off,
            'use_room_acoustics': self.use_room_acoustics,
            'start_sample': self.start_sample,
            'is_default_retronome_music': self.is_default_retronome_music,
            'part_of_music_system': self.part_of_music_system,
            'save_preload_data': self.save_preload_data,
            'sound_group_names': self.sound_group_names,
            'start_delay': self.start_delay,
            'music_system_area_state': self.music_system_area_state.to_json(),
            'volume_type': self.volume_type.to_json(),
        }


def _decode_song_file(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dvd_file(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_auto_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_buffer_when_stopped(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_play_when_buffered(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_faded_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pan(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_positional(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_min_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fall_off(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_room_acoustics(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_sample(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_is_default_retronome_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_part_of_music_system(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_save_preload_data(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sound_group_names(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_start_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_music_system_area_state(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumB.from_stream(data)


def _decode_volume_type(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumA.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x9d1a67a8: ('song_file', _decode_song_file),
    0xb417064a: ('dvd_file', _decode_dvd_file),
    0xc03ec271: ('auto_buffer', _decode_auto_buffer),
    0xe687518: ('auto_buffer_when_stopped', _decode_auto_buffer_when_stopped),
    0xea8d54f4: ('auto_play_when_buffered', _decode_auto_play_when_buffered),
    0xeb250a0b: ('start_faded_out', _decode_start_faded_out),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xc7a7f189: ('volume', _decode_volume),
    0xdf4353a3: ('pan', _decode_pan),
    0x6e0e81f8: ('positional', _decode_positional),
    0x25d4798a: ('min_audible_distance', _decode_min_audible_distance),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x72531867: ('fall_off', _decode_fall_off),
    0x85707354: ('use_room_acoustics', _decode_use_room_acoustics),
    0xe88ff377: ('start_sample', _decode_start_sample),
    0x794c3eb: ('is_default_retronome_music', _decode_is_default_retronome_music),
    0x2e7c745f: ('part_of_music_system', _decode_part_of_music_system),
    0xd74245a4: ('save_preload_data', _decode_save_preload_data),
    0xc871bd1b: ('sound_group_names', _decode_sound_group_names),
    0x196e17d9: ('start_delay', _decode_start_delay),
    0xfb8f0b1f: ('music_system_area_state', _decode_music_system_area_state),
    0x9558711e: ('volume_type', _decode_volume_type),
}

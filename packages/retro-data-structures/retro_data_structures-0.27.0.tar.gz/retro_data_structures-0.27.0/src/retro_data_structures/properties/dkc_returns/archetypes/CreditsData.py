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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class CreditsDataJson(typing_extensions.TypedDict):
        credits_time: float
        normal_share_lines: int
        extra_share_per_line: float
        penultimate_share_bonus: float
        pre_penultimate_delay: float
        post_penultimate_delay: float
        final_share_bonus: float
        text_fade_in_time: float
        text_fade_out_time: float
        image_fade_in_time: float
        image_fade_out_time: float
        unknown_struct26_0xba717f32: json_util.JsonObject
        unknown_struct26_0xc344a09a: json_util.JsonObject
        unknown_struct26_0xd834e949: json_util.JsonObject
        unknown_struct26_0x917857a0: json_util.JsonObject
        unknown_struct26_0x7dfaff15: json_util.JsonObject
        unknown_struct26_0xe60799c8: json_util.JsonObject
        unknown_struct26_0x45511f61: json_util.JsonObject
        unknown_struct26_0x92b39f39: json_util.JsonObject
        unlock_message_total_time: float
        unlock_message_fade_in_time: float
        unlock_message_fade_out_time: float
        unknown_struct26_0xa45e5b13: json_util.JsonObject
        unlock_concept_art: int
        unlock_music: int
        unlock_diorama: int
        unlock_message_post_delay: float
    

@dataclasses.dataclass()
class CreditsData(BaseProperty):
    credits_time: float = dataclasses.field(default=180.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc7a734ce, original_name='CreditsTime'
        ),
    })
    normal_share_lines: int = dataclasses.field(default=4, metadata={
        'reflection': FieldReflection[int](
            int, id=0x4efe6cde, original_name='NormalShareLines'
        ),
    })
    extra_share_per_line: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7a54cb5e, original_name='ExtraSharePerLine'
        ),
    })
    penultimate_share_bonus: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfca1515c, original_name='PenultimateShareBonus'
        ),
    })
    pre_penultimate_delay: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb1133a84, original_name='PrePenultimateDelay'
        ),
    })
    post_penultimate_delay: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5f230c67, original_name='PostPenultimateDelay'
        ),
    })
    final_share_bonus: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9a9a7d1f, original_name='FinalShareBonus'
        ),
    })
    text_fade_in_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa091f393, original_name='TextFadeInTime'
        ),
    })
    text_fade_out_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x98186a70, original_name='TextFadeOutTime'
        ),
    })
    image_fade_in_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc1b9eef1, original_name='ImageFadeInTime'
        ),
    })
    image_fade_out_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3bc54219, original_name='ImageFadeOutTime'
        ),
    })
    unknown_struct26_0xba717f32: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xba717f32, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0xc344a09a: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xc344a09a, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0xd834e949: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xd834e949, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x917857a0: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x917857a0, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x7dfaff15: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x7dfaff15, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0xe60799c8: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xe60799c8, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x45511f61: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x45511f61, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x92b39f39: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x92b39f39, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unlock_message_total_time: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb54b9d25, original_name='UnlockMessageTotalTime'
        ),
    })
    unlock_message_fade_in_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8fdc9487, original_name='UnlockMessageFadeInTime'
        ),
    })
    unlock_message_fade_out_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x82edf36a, original_name='UnlockMessageFadeOutTime'
        ),
    })
    unknown_struct26_0xa45e5b13: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xa45e5b13, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unlock_concept_art: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x79589bf4, original_name='UnlockConceptArt'
        ),
    })
    unlock_music: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0af707df, original_name='UnlockMusic'
        ),
    })
    unlock_diorama: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5ce2a9a9, original_name='UnlockDiorama'
        ),
    })
    unlock_message_post_delay: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x994aa27d, original_name='UnlockMessagePostDelay'
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
        if property_count != 27:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc7a734ce
        credits_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4efe6cde
        normal_share_lines = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7a54cb5e
        extra_share_per_line = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfca1515c
        penultimate_share_bonus = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb1133a84
        pre_penultimate_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5f230c67
        post_penultimate_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a9a7d1f
        final_share_bonus = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa091f393
        text_fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x98186a70
        text_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc1b9eef1
        image_fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3bc54219
        image_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xba717f32
        unknown_struct26_0xba717f32 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc344a09a
        unknown_struct26_0xc344a09a = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd834e949
        unknown_struct26_0xd834e949 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x917857a0
        unknown_struct26_0x917857a0 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7dfaff15
        unknown_struct26_0x7dfaff15 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe60799c8
        unknown_struct26_0xe60799c8 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x45511f61
        unknown_struct26_0x45511f61 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x92b39f39
        unknown_struct26_0x92b39f39 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb54b9d25
        unlock_message_total_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8fdc9487
        unlock_message_fade_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82edf36a
        unlock_message_fade_out_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa45e5b13
        unknown_struct26_0xa45e5b13 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x79589bf4
        unlock_concept_art = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0af707df
        unlock_music = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5ce2a9a9
        unlock_diorama = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x994aa27d
        unlock_message_post_delay = struct.unpack('>f', data.read(4))[0]
    
        return cls(credits_time, normal_share_lines, extra_share_per_line, penultimate_share_bonus, pre_penultimate_delay, post_penultimate_delay, final_share_bonus, text_fade_in_time, text_fade_out_time, image_fade_in_time, image_fade_out_time, unknown_struct26_0xba717f32, unknown_struct26_0xc344a09a, unknown_struct26_0xd834e949, unknown_struct26_0x917857a0, unknown_struct26_0x7dfaff15, unknown_struct26_0xe60799c8, unknown_struct26_0x45511f61, unknown_struct26_0x92b39f39, unlock_message_total_time, unlock_message_fade_in_time, unlock_message_fade_out_time, unknown_struct26_0xa45e5b13, unlock_concept_art, unlock_music, unlock_diorama, unlock_message_post_delay)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'\xc7\xa74\xce')  # 0xc7a734ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.credits_time))

        data.write(b'N\xfel\xde')  # 0x4efe6cde
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.normal_share_lines))

        data.write(b'zT\xcb^')  # 0x7a54cb5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.extra_share_per_line))

        data.write(b'\xfc\xa1Q\\')  # 0xfca1515c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.penultimate_share_bonus))

        data.write(b'\xb1\x13:\x84')  # 0xb1133a84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_penultimate_delay))

        data.write(b'_#\x0cg')  # 0x5f230c67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.post_penultimate_delay))

        data.write(b'\x9a\x9a}\x1f')  # 0x9a9a7d1f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.final_share_bonus))

        data.write(b'\xa0\x91\xf3\x93')  # 0xa091f393
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_fade_in_time))

        data.write(b'\x98\x18jp')  # 0x98186a70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_fade_out_time))

        data.write(b'\xc1\xb9\xee\xf1')  # 0xc1b9eef1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.image_fade_in_time))

        data.write(b';\xc5B\x19')  # 0x3bc54219
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.image_fade_out_time))

        data.write(b'\xbaq\x7f2')  # 0xba717f32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xba717f32.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3D\xa0\x9a')  # 0xc344a09a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xc344a09a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd84\xe9I')  # 0xd834e949
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xd834e949.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91xW\xa0')  # 0x917857a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x917857a0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\xfa\xff\x15')  # 0x7dfaff15
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x7dfaff15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\x07\x99\xc8')  # 0xe60799c8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xe60799c8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'EQ\x1fa')  # 0x45511f61
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x45511f61.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x92\xb3\x9f9')  # 0x92b39f39
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x92b39f39.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb5K\x9d%')  # 0xb54b9d25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_total_time))

        data.write(b'\x8f\xdc\x94\x87')  # 0x8fdc9487
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_fade_in_time))

        data.write(b'\x82\xed\xf3j')  # 0x82edf36a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_fade_out_time))

        data.write(b'\xa4^[\x13')  # 0xa45e5b13
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xa45e5b13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'yX\x9b\xf4')  # 0x79589bf4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_concept_art))

        data.write(b'\n\xf7\x07\xdf')  # 0xaf707df
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_music))

        data.write(b'\\\xe2\xa9\xa9')  # 0x5ce2a9a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_diorama))

        data.write(b'\x99J\xa2}')  # 0x994aa27d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unlock_message_post_delay))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CreditsDataJson", data)
        return cls(
            credits_time=json_data['credits_time'],
            normal_share_lines=json_data['normal_share_lines'],
            extra_share_per_line=json_data['extra_share_per_line'],
            penultimate_share_bonus=json_data['penultimate_share_bonus'],
            pre_penultimate_delay=json_data['pre_penultimate_delay'],
            post_penultimate_delay=json_data['post_penultimate_delay'],
            final_share_bonus=json_data['final_share_bonus'],
            text_fade_in_time=json_data['text_fade_in_time'],
            text_fade_out_time=json_data['text_fade_out_time'],
            image_fade_in_time=json_data['image_fade_in_time'],
            image_fade_out_time=json_data['image_fade_out_time'],
            unknown_struct26_0xba717f32=UnknownStruct26.from_json(json_data['unknown_struct26_0xba717f32']),
            unknown_struct26_0xc344a09a=UnknownStruct26.from_json(json_data['unknown_struct26_0xc344a09a']),
            unknown_struct26_0xd834e949=UnknownStruct26.from_json(json_data['unknown_struct26_0xd834e949']),
            unknown_struct26_0x917857a0=UnknownStruct26.from_json(json_data['unknown_struct26_0x917857a0']),
            unknown_struct26_0x7dfaff15=UnknownStruct26.from_json(json_data['unknown_struct26_0x7dfaff15']),
            unknown_struct26_0xe60799c8=UnknownStruct26.from_json(json_data['unknown_struct26_0xe60799c8']),
            unknown_struct26_0x45511f61=UnknownStruct26.from_json(json_data['unknown_struct26_0x45511f61']),
            unknown_struct26_0x92b39f39=UnknownStruct26.from_json(json_data['unknown_struct26_0x92b39f39']),
            unlock_message_total_time=json_data['unlock_message_total_time'],
            unlock_message_fade_in_time=json_data['unlock_message_fade_in_time'],
            unlock_message_fade_out_time=json_data['unlock_message_fade_out_time'],
            unknown_struct26_0xa45e5b13=UnknownStruct26.from_json(json_data['unknown_struct26_0xa45e5b13']),
            unlock_concept_art=json_data['unlock_concept_art'],
            unlock_music=json_data['unlock_music'],
            unlock_diorama=json_data['unlock_diorama'],
            unlock_message_post_delay=json_data['unlock_message_post_delay'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'credits_time': self.credits_time,
            'normal_share_lines': self.normal_share_lines,
            'extra_share_per_line': self.extra_share_per_line,
            'penultimate_share_bonus': self.penultimate_share_bonus,
            'pre_penultimate_delay': self.pre_penultimate_delay,
            'post_penultimate_delay': self.post_penultimate_delay,
            'final_share_bonus': self.final_share_bonus,
            'text_fade_in_time': self.text_fade_in_time,
            'text_fade_out_time': self.text_fade_out_time,
            'image_fade_in_time': self.image_fade_in_time,
            'image_fade_out_time': self.image_fade_out_time,
            'unknown_struct26_0xba717f32': self.unknown_struct26_0xba717f32.to_json(),
            'unknown_struct26_0xc344a09a': self.unknown_struct26_0xc344a09a.to_json(),
            'unknown_struct26_0xd834e949': self.unknown_struct26_0xd834e949.to_json(),
            'unknown_struct26_0x917857a0': self.unknown_struct26_0x917857a0.to_json(),
            'unknown_struct26_0x7dfaff15': self.unknown_struct26_0x7dfaff15.to_json(),
            'unknown_struct26_0xe60799c8': self.unknown_struct26_0xe60799c8.to_json(),
            'unknown_struct26_0x45511f61': self.unknown_struct26_0x45511f61.to_json(),
            'unknown_struct26_0x92b39f39': self.unknown_struct26_0x92b39f39.to_json(),
            'unlock_message_total_time': self.unlock_message_total_time,
            'unlock_message_fade_in_time': self.unlock_message_fade_in_time,
            'unlock_message_fade_out_time': self.unlock_message_fade_out_time,
            'unknown_struct26_0xa45e5b13': self.unknown_struct26_0xa45e5b13.to_json(),
            'unlock_concept_art': self.unlock_concept_art,
            'unlock_music': self.unlock_music,
            'unlock_diorama': self.unlock_diorama,
            'unlock_message_post_delay': self.unlock_message_post_delay,
        }


def _decode_credits_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_share_lines(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_extra_share_per_line(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_penultimate_share_bonus(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pre_penultimate_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_post_penultimate_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_final_share_bonus(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_image_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_image_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_message_total_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_message_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_message_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unlock_concept_art(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_diorama(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_message_post_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc7a734ce: ('credits_time', _decode_credits_time),
    0x4efe6cde: ('normal_share_lines', _decode_normal_share_lines),
    0x7a54cb5e: ('extra_share_per_line', _decode_extra_share_per_line),
    0xfca1515c: ('penultimate_share_bonus', _decode_penultimate_share_bonus),
    0xb1133a84: ('pre_penultimate_delay', _decode_pre_penultimate_delay),
    0x5f230c67: ('post_penultimate_delay', _decode_post_penultimate_delay),
    0x9a9a7d1f: ('final_share_bonus', _decode_final_share_bonus),
    0xa091f393: ('text_fade_in_time', _decode_text_fade_in_time),
    0x98186a70: ('text_fade_out_time', _decode_text_fade_out_time),
    0xc1b9eef1: ('image_fade_in_time', _decode_image_fade_in_time),
    0x3bc54219: ('image_fade_out_time', _decode_image_fade_out_time),
    0xba717f32: ('unknown_struct26_0xba717f32', UnknownStruct26.from_stream),
    0xc344a09a: ('unknown_struct26_0xc344a09a', UnknownStruct26.from_stream),
    0xd834e949: ('unknown_struct26_0xd834e949', UnknownStruct26.from_stream),
    0x917857a0: ('unknown_struct26_0x917857a0', UnknownStruct26.from_stream),
    0x7dfaff15: ('unknown_struct26_0x7dfaff15', UnknownStruct26.from_stream),
    0xe60799c8: ('unknown_struct26_0xe60799c8', UnknownStruct26.from_stream),
    0x45511f61: ('unknown_struct26_0x45511f61', UnknownStruct26.from_stream),
    0x92b39f39: ('unknown_struct26_0x92b39f39', UnknownStruct26.from_stream),
    0xb54b9d25: ('unlock_message_total_time', _decode_unlock_message_total_time),
    0x8fdc9487: ('unlock_message_fade_in_time', _decode_unlock_message_fade_in_time),
    0x82edf36a: ('unlock_message_fade_out_time', _decode_unlock_message_fade_out_time),
    0xa45e5b13: ('unknown_struct26_0xa45e5b13', UnknownStruct26.from_stream),
    0x79589bf4: ('unlock_concept_art', _decode_unlock_concept_art),
    0xaf707df: ('unlock_music', _decode_unlock_music),
    0x5ce2a9a9: ('unlock_diorama', _decode_unlock_diorama),
    0x994aa27d: ('unlock_message_post_delay', _decode_unlock_message_post_delay),
}

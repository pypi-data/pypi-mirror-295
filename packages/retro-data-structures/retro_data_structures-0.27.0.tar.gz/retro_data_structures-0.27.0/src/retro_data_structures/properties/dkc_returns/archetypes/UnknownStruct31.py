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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct31Json(typing_extensions.TypedDict):
        unknown_struct29: json_util.JsonObject
        title: int
        back: int
        back_core: int
        music: int
        sound_fx: int
        left_arrow: int
        right_arrow: int
        left_arrow_pressed: int
        right_arrow_pressed: int
        appear_sound: int
        disappear_sound: int
        in_place_sound: int
        up_sound: int
        down_sound: int
        cancel_sound: int
        inc_sound: int
        dec_sound: int
        error_sound: int
        text_background: int
    

@dataclasses.dataclass()
class UnknownStruct31(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29, metadata={
        'reflection': FieldReflection[UnknownStruct29](
            UnknownStruct29, id=0x305b3232, original_name='UnknownStruct29', from_json=UnknownStruct29.from_json, to_json=UnknownStruct29.to_json
        ),
    })
    title: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa4f20c17, original_name='Title'
        ),
    })
    back: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe9336455, original_name='Back'
        ),
    })
    back_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x770bcd3b, original_name='BackCore'
        ),
    })
    music: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbb19d2f3, original_name='Music'
        ),
    })
    sound_fx: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xdf080ea1, original_name='SoundFX'
        ),
    })
    left_arrow: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x314cdc24, original_name='LeftArrow'
        ),
    })
    right_arrow: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd1918347, original_name='RightArrow'
        ),
    })
    left_arrow_pressed: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb4510efe, original_name='LeftArrowPressed'
        ),
    })
    right_arrow_pressed: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x54cd1874, original_name='RightArrowPressed'
        ),
    })
    appear_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc02c234f, original_name='AppearSound'
        ),
    })
    disappear_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6d267e88, original_name='DisappearSound'
        ),
    })
    in_place_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2f90d257, original_name='InPlaceSound'
        ),
    })
    up_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x67f87d00, original_name='UpSound'
        ),
    })
    down_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb48a1f83, original_name='DownSound'
        ),
    })
    cancel_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x485f2008, original_name='CancelSound'
        ),
    })
    inc_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7bee566e, original_name='IncSound'
        ),
    })
    dec_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4d50921e, original_name='DecSound'
        ),
    })
    error_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4559a4fd, original_name='ErrorSound'
        ),
    })
    text_background: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe119319b, original_name='TextBackground'
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
        if property_count != 20:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x305b3232
        unknown_struct29 = UnknownStruct29.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa4f20c17
        title = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9336455
        back = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x770bcd3b
        back_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbb19d2f3
        music = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdf080ea1
        sound_fx = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x314cdc24
        left_arrow = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1918347
        right_arrow = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb4510efe
        left_arrow_pressed = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x54cd1874
        right_arrow_pressed = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc02c234f
        appear_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6d267e88
        disappear_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f90d257
        in_place_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67f87d00
        up_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb48a1f83
        down_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x485f2008
        cancel_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7bee566e
        inc_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4d50921e
        dec_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4559a4fd
        error_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe119319b
        text_background = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_struct29, title, back, back_core, music, sound_fx, left_arrow, right_arrow, left_arrow_pressed, right_arrow_pressed, appear_sound, disappear_sound, in_place_sound, up_sound, down_sound, cancel_sound, inc_sound, dec_sound, error_sound, text_background)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'0[22')  # 0x305b3232
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\xbb\x19\xd2\xf3')  # 0xbb19d2f3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.music))

        data.write(b'\xdf\x08\x0e\xa1')  # 0xdf080ea1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_fx))

        data.write(b'1L\xdc$')  # 0x314cdc24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow))

        data.write(b'\xd1\x91\x83G')  # 0xd1918347
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow))

        data.write(b'\xb4Q\x0e\xfe')  # 0xb4510efe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow_pressed))

        data.write(b'T\xcd\x18t')  # 0x54cd1874
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow_pressed))

        data.write(b'\xc0,#O')  # 0xc02c234f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.appear_sound))

        data.write(b'm&~\x88')  # 0x6d267e88
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disappear_sound))

        data.write(b'/\x90\xd2W')  # 0x2f90d257
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.in_place_sound))

        data.write(b'g\xf8}\x00')  # 0x67f87d00
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.up_sound))

        data.write(b'\xb4\x8a\x1f\x83')  # 0xb48a1f83
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.down_sound))

        data.write(b'H_ \x08')  # 0x485f2008
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel_sound))

        data.write(b'{\xeeVn')  # 0x7bee566e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inc_sound))

        data.write(b'MP\x92\x1e')  # 0x4d50921e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dec_sound))

        data.write(b'EY\xa4\xfd')  # 0x4559a4fd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.error_sound))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct31Json", data)
        return cls(
            unknown_struct29=UnknownStruct29.from_json(json_data['unknown_struct29']),
            title=json_data['title'],
            back=json_data['back'],
            back_core=json_data['back_core'],
            music=json_data['music'],
            sound_fx=json_data['sound_fx'],
            left_arrow=json_data['left_arrow'],
            right_arrow=json_data['right_arrow'],
            left_arrow_pressed=json_data['left_arrow_pressed'],
            right_arrow_pressed=json_data['right_arrow_pressed'],
            appear_sound=json_data['appear_sound'],
            disappear_sound=json_data['disappear_sound'],
            in_place_sound=json_data['in_place_sound'],
            up_sound=json_data['up_sound'],
            down_sound=json_data['down_sound'],
            cancel_sound=json_data['cancel_sound'],
            inc_sound=json_data['inc_sound'],
            dec_sound=json_data['dec_sound'],
            error_sound=json_data['error_sound'],
            text_background=json_data['text_background'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title': self.title,
            'back': self.back,
            'back_core': self.back_core,
            'music': self.music,
            'sound_fx': self.sound_fx,
            'left_arrow': self.left_arrow,
            'right_arrow': self.right_arrow,
            'left_arrow_pressed': self.left_arrow_pressed,
            'right_arrow_pressed': self.right_arrow_pressed,
            'appear_sound': self.appear_sound,
            'disappear_sound': self.disappear_sound,
            'in_place_sound': self.in_place_sound,
            'up_sound': self.up_sound,
            'down_sound': self.down_sound,
            'cancel_sound': self.cancel_sound,
            'inc_sound': self.inc_sound,
            'dec_sound': self.dec_sound,
            'error_sound': self.error_sound,
            'text_background': self.text_background,
        }


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_fx(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_appear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disappear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_in_place_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_up_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_down_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inc_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dec_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_error_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', UnknownStruct29.from_stream),
    0xa4f20c17: ('title', _decode_title),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0xbb19d2f3: ('music', _decode_music),
    0xdf080ea1: ('sound_fx', _decode_sound_fx),
    0x314cdc24: ('left_arrow', _decode_left_arrow),
    0xd1918347: ('right_arrow', _decode_right_arrow),
    0xb4510efe: ('left_arrow_pressed', _decode_left_arrow_pressed),
    0x54cd1874: ('right_arrow_pressed', _decode_right_arrow_pressed),
    0xc02c234f: ('appear_sound', _decode_appear_sound),
    0x6d267e88: ('disappear_sound', _decode_disappear_sound),
    0x2f90d257: ('in_place_sound', _decode_in_place_sound),
    0x67f87d00: ('up_sound', _decode_up_sound),
    0xb48a1f83: ('down_sound', _decode_down_sound),
    0x485f2008: ('cancel_sound', _decode_cancel_sound),
    0x7bee566e: ('inc_sound', _decode_inc_sound),
    0x4d50921e: ('dec_sound', _decode_dec_sound),
    0x4559a4fd: ('error_sound', _decode_error_sound),
    0xe119319b: ('text_background', _decode_text_background),
}

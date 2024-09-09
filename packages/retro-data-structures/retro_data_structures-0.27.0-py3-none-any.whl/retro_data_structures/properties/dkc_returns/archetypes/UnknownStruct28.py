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
    class UnknownStruct28Json(typing_extensions.TypedDict):
        hud_frame: int
        appear_sound: int
        no_sound: int
        yes_sound: int
        animated_appear: int
        caud_0x0c9c9c3b: int
        caud_0x6a6aa42e: int
        animated_disappear: int
        no: int
        no_core: int
        yes: int
        yes_core: int
        ok: int
        ok_core: int
        unknown_struct26: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct28(BaseProperty):
    hud_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf2299ed6, original_name='HUDFrame'
        ),
    })
    appear_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc02c234f, original_name='AppearSound'
        ),
    })
    no_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x277c04ff, original_name='NoSound'
        ),
    })
    yes_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x108d9071, original_name='YesSound'
        ),
    })
    animated_appear: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x75ac683c, original_name='AnimatedAppear'
        ),
    })
    caud_0x0c9c9c3b: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0c9c9c3b, original_name='CAUD'
        ),
    })
    caud_0x6a6aa42e: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6a6aa42e, original_name='CAUD'
        ),
    })
    animated_disappear: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x078c819f, original_name='AnimatedDisappear'
        ),
    })
    no: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4b883e6b, original_name='No'
        ),
    })
    no_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x393d5c78, original_name='NoCore'
        ),
    })
    yes: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x40017917, original_name='Yes'
        ),
    })
    yes_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x10922293, original_name='YesCore'
        ),
    })
    ok: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x766e77c9, original_name='Ok'
        ),
    })
    ok_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf15823c2, original_name='OkCore'
        ),
    })
    unknown_struct26: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x6a598a9b, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
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
        if property_count != 15:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf2299ed6
        hud_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc02c234f
        appear_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x277c04ff
        no_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x108d9071
        yes_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x75ac683c
        animated_appear = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0c9c9c3b
        caud_0x0c9c9c3b = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a6aa42e
        caud_0x6a6aa42e = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x078c819f
        animated_disappear = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4b883e6b
        no = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x393d5c78
        no_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x40017917
        yes = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x10922293
        yes_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x766e77c9
        ok = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf15823c2
        ok_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a598a9b
        unknown_struct26 = UnknownStruct26.from_stream(data, property_size)
    
        return cls(hud_frame, appear_sound, no_sound, yes_sound, animated_appear, caud_0x0c9c9c3b, caud_0x6a6aa42e, animated_disappear, no, no_core, yes, yes_core, ok, ok_core, unknown_struct26)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\xc0,#O')  # 0xc02c234f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.appear_sound))

        data.write(b"'|\x04\xff")  # 0x277c04ff
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_sound))

        data.write(b'\x10\x8d\x90q')  # 0x108d9071
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes_sound))

        data.write(b'u\xach<')  # 0x75ac683c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.animated_appear))

        data.write(b'\x0c\x9c\x9c;')  # 0xc9c9c3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x0c9c9c3b))

        data.write(b'jj\xa4.')  # 0x6a6aa42e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x6a6aa42e))

        data.write(b'\x07\x8c\x81\x9f')  # 0x78c819f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.animated_disappear))

        data.write(b'K\x88>k')  # 0x4b883e6b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no))

        data.write(b'9=\\x')  # 0x393d5c78
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_core))

        data.write(b'@\x01y\x17')  # 0x40017917
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes))

        data.write(b'\x10\x92"\x93')  # 0x10922293
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes_core))

        data.write(b'vnw\xc9')  # 0x766e77c9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ok))

        data.write(b'\xf1X#\xc2')  # 0xf15823c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ok_core))

        data.write(b'jY\x8a\x9b')  # 0x6a598a9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct28Json", data)
        return cls(
            hud_frame=json_data['hud_frame'],
            appear_sound=json_data['appear_sound'],
            no_sound=json_data['no_sound'],
            yes_sound=json_data['yes_sound'],
            animated_appear=json_data['animated_appear'],
            caud_0x0c9c9c3b=json_data['caud_0x0c9c9c3b'],
            caud_0x6a6aa42e=json_data['caud_0x6a6aa42e'],
            animated_disappear=json_data['animated_disappear'],
            no=json_data['no'],
            no_core=json_data['no_core'],
            yes=json_data['yes'],
            yes_core=json_data['yes_core'],
            ok=json_data['ok'],
            ok_core=json_data['ok_core'],
            unknown_struct26=UnknownStruct26.from_json(json_data['unknown_struct26']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'hud_frame': self.hud_frame,
            'appear_sound': self.appear_sound,
            'no_sound': self.no_sound,
            'yes_sound': self.yes_sound,
            'animated_appear': self.animated_appear,
            'caud_0x0c9c9c3b': self.caud_0x0c9c9c3b,
            'caud_0x6a6aa42e': self.caud_0x6a6aa42e,
            'animated_disappear': self.animated_disappear,
            'no': self.no,
            'no_core': self.no_core,
            'yes': self.yes,
            'yes_core': self.yes_core,
            'ok': self.ok,
            'ok_core': self.ok_core,
            'unknown_struct26': self.unknown_struct26.to_json(),
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_appear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animated_appear(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x0c9c9c3b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x6a6aa42e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animated_disappear(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ok(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ok_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0xc02c234f: ('appear_sound', _decode_appear_sound),
    0x277c04ff: ('no_sound', _decode_no_sound),
    0x108d9071: ('yes_sound', _decode_yes_sound),
    0x75ac683c: ('animated_appear', _decode_animated_appear),
    0xc9c9c3b: ('caud_0x0c9c9c3b', _decode_caud_0x0c9c9c3b),
    0x6a6aa42e: ('caud_0x6a6aa42e', _decode_caud_0x6a6aa42e),
    0x78c819f: ('animated_disappear', _decode_animated_disappear),
    0x4b883e6b: ('no', _decode_no),
    0x393d5c78: ('no_core', _decode_no_core),
    0x40017917: ('yes', _decode_yes),
    0x10922293: ('yes_core', _decode_yes_core),
    0x766e77c9: ('ok', _decode_ok),
    0xf15823c2: ('ok_core', _decode_ok_core),
    0x6a598a9b: ('unknown_struct26', UnknownStruct26.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.IslandHudStruct import IslandHudStruct
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct170 import UnknownStruct170
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct171 import UnknownStruct171
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct172 import UnknownStruct172
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct173 import UnknownStruct173
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct174Json(typing_extensions.TypedDict):
        gui_frame: int
        unknown_struct27: json_util.JsonObject
        title: int
        images: int
        music: int
        unlocked: int
        back: int
        back_core: int
        text_background: int
        island_hud_struct_0x800073b8: json_util.JsonObject
        island_hud_struct_0x5f71338f: json_util.JsonObject
        island_hud_struct_0x01be492e: json_util.JsonObject
        unknown_struct170: json_util.JsonObject
        unknown_struct171: json_util.JsonObject
        unknown_struct172: json_util.JsonObject
        unknown_struct173: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct174(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
        ),
    })
    title: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa4f20c17, original_name='Title'
        ),
    })
    images: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1ce76b90, original_name='Images'
        ),
    })
    music: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbb19d2f3, original_name='Music'
        ),
    })
    unlocked: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x39665bc8, original_name='Unlocked'
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
    text_background: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe119319b, original_name='TextBackground'
        ),
    })
    island_hud_struct_0x800073b8: IslandHudStruct = dataclasses.field(default_factory=IslandHudStruct, metadata={
        'reflection': FieldReflection[IslandHudStruct](
            IslandHudStruct, id=0x800073b8, original_name='IslandHudStruct', from_json=IslandHudStruct.from_json, to_json=IslandHudStruct.to_json
        ),
    })
    island_hud_struct_0x5f71338f: IslandHudStruct = dataclasses.field(default_factory=IslandHudStruct, metadata={
        'reflection': FieldReflection[IslandHudStruct](
            IslandHudStruct, id=0x5f71338f, original_name='IslandHudStruct', from_json=IslandHudStruct.from_json, to_json=IslandHudStruct.to_json
        ),
    })
    island_hud_struct_0x01be492e: IslandHudStruct = dataclasses.field(default_factory=IslandHudStruct, metadata={
        'reflection': FieldReflection[IslandHudStruct](
            IslandHudStruct, id=0x01be492e, original_name='IslandHudStruct', from_json=IslandHudStruct.from_json, to_json=IslandHudStruct.to_json
        ),
    })
    unknown_struct170: UnknownStruct170 = dataclasses.field(default_factory=UnknownStruct170, metadata={
        'reflection': FieldReflection[UnknownStruct170](
            UnknownStruct170, id=0x98e01824, original_name='UnknownStruct170', from_json=UnknownStruct170.from_json, to_json=UnknownStruct170.to_json
        ),
    })
    unknown_struct171: UnknownStruct171 = dataclasses.field(default_factory=UnknownStruct171, metadata={
        'reflection': FieldReflection[UnknownStruct171](
            UnknownStruct171, id=0xf8e5788c, original_name='UnknownStruct171', from_json=UnknownStruct171.from_json, to_json=UnknownStruct171.to_json
        ),
    })
    unknown_struct172: UnknownStruct172 = dataclasses.field(default_factory=UnknownStruct172, metadata={
        'reflection': FieldReflection[UnknownStruct172](
            UnknownStruct172, id=0x4983b29a, original_name='UnknownStruct172', from_json=UnknownStruct172.from_json, to_json=UnknownStruct172.to_json
        ),
    })
    unknown_struct173: UnknownStruct173 = dataclasses.field(default_factory=UnknownStruct173, metadata={
        'reflection': FieldReflection[UnknownStruct173](
            UnknownStruct173, id=0x851be4be, original_name='UnknownStruct173', from_json=UnknownStruct173.from_json, to_json=UnknownStruct173.to_json
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
        if property_count != 16:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa4f20c17
        title = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1ce76b90
        images = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbb19d2f3
        music = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x39665bc8
        unlocked = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9336455
        back = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x770bcd3b
        back_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe119319b
        text_background = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x800073b8
        island_hud_struct_0x800073b8 = IslandHudStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5f71338f
        island_hud_struct_0x5f71338f = IslandHudStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x01be492e
        island_hud_struct_0x01be492e = IslandHudStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x98e01824
        unknown_struct170 = UnknownStruct170.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf8e5788c
        unknown_struct171 = UnknownStruct171.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4983b29a
        unknown_struct172 = UnknownStruct172.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x851be4be
        unknown_struct173 = UnknownStruct173.from_stream(data, property_size)
    
        return cls(gui_frame, unknown_struct27, title, images, music, unlocked, back, back_core, text_background, island_hud_struct_0x800073b8, island_hud_struct_0x5f71338f, island_hud_struct_0x01be492e, unknown_struct170, unknown_struct171, unknown_struct172, unknown_struct173)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\x1c\xe7k\x90')  # 0x1ce76b90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.images))

        data.write(b'\xbb\x19\xd2\xf3')  # 0xbb19d2f3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.music))

        data.write(b'9f[\xc8')  # 0x39665bc8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlocked))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

        data.write(b'\x80\x00s\xb8')  # 0x800073b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_hud_struct_0x800073b8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_q3\x8f')  # 0x5f71338f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_hud_struct_0x5f71338f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\xbeI.')  # 0x1be492e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_hud_struct_0x01be492e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xe0\x18$')  # 0x98e01824
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct170.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xe5x\x8c')  # 0xf8e5788c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct171.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'I\x83\xb2\x9a')  # 0x4983b29a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct172.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85\x1b\xe4\xbe')  # 0x851be4be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct173.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct174Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            title=json_data['title'],
            images=json_data['images'],
            music=json_data['music'],
            unlocked=json_data['unlocked'],
            back=json_data['back'],
            back_core=json_data['back_core'],
            text_background=json_data['text_background'],
            island_hud_struct_0x800073b8=IslandHudStruct.from_json(json_data['island_hud_struct_0x800073b8']),
            island_hud_struct_0x5f71338f=IslandHudStruct.from_json(json_data['island_hud_struct_0x5f71338f']),
            island_hud_struct_0x01be492e=IslandHudStruct.from_json(json_data['island_hud_struct_0x01be492e']),
            unknown_struct170=UnknownStruct170.from_json(json_data['unknown_struct170']),
            unknown_struct171=UnknownStruct171.from_json(json_data['unknown_struct171']),
            unknown_struct172=UnknownStruct172.from_json(json_data['unknown_struct172']),
            unknown_struct173=UnknownStruct173.from_json(json_data['unknown_struct173']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'title': self.title,
            'images': self.images,
            'music': self.music,
            'unlocked': self.unlocked,
            'back': self.back,
            'back_core': self.back_core,
            'text_background': self.text_background,
            'island_hud_struct_0x800073b8': self.island_hud_struct_0x800073b8.to_json(),
            'island_hud_struct_0x5f71338f': self.island_hud_struct_0x5f71338f.to_json(),
            'island_hud_struct_0x01be492e': self.island_hud_struct_0x01be492e.to_json(),
            'unknown_struct170': self.unknown_struct170.to_json(),
            'unknown_struct171': self.unknown_struct171.to_json(),
            'unknown_struct172': self.unknown_struct172.to_json(),
            'unknown_struct173': self.unknown_struct173.to_json(),
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_images(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlocked(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0xa4f20c17: ('title', _decode_title),
    0x1ce76b90: ('images', _decode_images),
    0xbb19d2f3: ('music', _decode_music),
    0x39665bc8: ('unlocked', _decode_unlocked),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0xe119319b: ('text_background', _decode_text_background),
    0x800073b8: ('island_hud_struct_0x800073b8', IslandHudStruct.from_stream),
    0x5f71338f: ('island_hud_struct_0x5f71338f', IslandHudStruct.from_stream),
    0x1be492e: ('island_hud_struct_0x01be492e', IslandHudStruct.from_stream),
    0x98e01824: ('unknown_struct170', UnknownStruct170.from_stream),
    0xf8e5788c: ('unknown_struct171', UnknownStruct171.from_stream),
    0x4983b29a: ('unknown_struct172', UnknownStruct172.from_stream),
    0x851be4be: ('unknown_struct173', UnknownStruct173.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct144 import UnknownStruct144
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct145 import UnknownStruct145
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct146 import UnknownStruct146
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct30Json(typing_extensions.TypedDict):
        unknown_struct29: json_util.JsonObject
        title: int
        back: int
        back_core: int
        strg_0x916baa3c: int
        horizontal_mode: int
        strg_0x52b89ddf: int
        horizontal_selected: int
        unknown_struct144: json_util.JsonObject
        unknown_struct145: json_util.JsonObject
        unknown_struct146: json_util.JsonObject
        text_background: int
    

@dataclasses.dataclass()
class UnknownStruct30(BaseProperty):
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
    strg_0x916baa3c: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x916baa3c, original_name='STRG'
        ),
    })
    horizontal_mode: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd3c126f7, original_name='HorizontalMode'
        ),
    })
    strg_0x52b89ddf: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x52b89ddf, original_name='STRG'
        ),
    })
    horizontal_selected: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd7e162e3, original_name='HorizontalSelected'
        ),
    })
    unknown_struct144: UnknownStruct144 = dataclasses.field(default_factory=UnknownStruct144, metadata={
        'reflection': FieldReflection[UnknownStruct144](
            UnknownStruct144, id=0xfe23018f, original_name='UnknownStruct144', from_json=UnknownStruct144.from_json, to_json=UnknownStruct144.to_json
        ),
    })
    unknown_struct145: UnknownStruct145 = dataclasses.field(default_factory=UnknownStruct145, metadata={
        'reflection': FieldReflection[UnknownStruct145](
            UnknownStruct145, id=0xf7d3e6c2, original_name='UnknownStruct145', from_json=UnknownStruct145.from_json, to_json=UnknownStruct145.to_json
        ),
    })
    unknown_struct146: UnknownStruct146 = dataclasses.field(default_factory=UnknownStruct146, metadata={
        'reflection': FieldReflection[UnknownStruct146](
            UnknownStruct146, id=0x0c3b97b8, original_name='UnknownStruct146', from_json=UnknownStruct146.from_json, to_json=UnknownStruct146.to_json
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
        if property_count != 12:
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
        assert property_id == 0x916baa3c
        strg_0x916baa3c = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd3c126f7
        horizontal_mode = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x52b89ddf
        strg_0x52b89ddf = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd7e162e3
        horizontal_selected = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe23018f
        unknown_struct144 = UnknownStruct144.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf7d3e6c2
        unknown_struct145 = UnknownStruct145.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0c3b97b8
        unknown_struct146 = UnknownStruct146.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe119319b
        text_background = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_struct29, title, back, back_core, strg_0x916baa3c, horizontal_mode, strg_0x52b89ddf, horizontal_selected, unknown_struct144, unknown_struct145, unknown_struct146, text_background)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

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

        data.write(b'\x91k\xaa<')  # 0x916baa3c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x916baa3c))

        data.write(b'\xd3\xc1&\xf7')  # 0xd3c126f7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.horizontal_mode))

        data.write(b'R\xb8\x9d\xdf')  # 0x52b89ddf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x52b89ddf))

        data.write(b'\xd7\xe1b\xe3')  # 0xd7e162e3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.horizontal_selected))

        data.write(b'\xfe#\x01\x8f')  # 0xfe23018f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct144.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\xd3\xe6\xc2')  # 0xf7d3e6c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct145.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c;\x97\xb8')  # 0xc3b97b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct146.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct30Json", data)
        return cls(
            unknown_struct29=UnknownStruct29.from_json(json_data['unknown_struct29']),
            title=json_data['title'],
            back=json_data['back'],
            back_core=json_data['back_core'],
            strg_0x916baa3c=json_data['strg_0x916baa3c'],
            horizontal_mode=json_data['horizontal_mode'],
            strg_0x52b89ddf=json_data['strg_0x52b89ddf'],
            horizontal_selected=json_data['horizontal_selected'],
            unknown_struct144=UnknownStruct144.from_json(json_data['unknown_struct144']),
            unknown_struct145=UnknownStruct145.from_json(json_data['unknown_struct145']),
            unknown_struct146=UnknownStruct146.from_json(json_data['unknown_struct146']),
            text_background=json_data['text_background'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title': self.title,
            'back': self.back,
            'back_core': self.back_core,
            'strg_0x916baa3c': self.strg_0x916baa3c,
            'horizontal_mode': self.horizontal_mode,
            'strg_0x52b89ddf': self.strg_0x52b89ddf,
            'horizontal_selected': self.horizontal_selected,
            'unknown_struct144': self.unknown_struct144.to_json(),
            'unknown_struct145': self.unknown_struct145.to_json(),
            'unknown_struct146': self.unknown_struct146.to_json(),
            'text_background': self.text_background,
        }


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x916baa3c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_horizontal_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x52b89ddf(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_horizontal_selected(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', UnknownStruct29.from_stream),
    0xa4f20c17: ('title', _decode_title),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0x916baa3c: ('strg_0x916baa3c', _decode_strg_0x916baa3c),
    0xd3c126f7: ('horizontal_mode', _decode_horizontal_mode),
    0x52b89ddf: ('strg_0x52b89ddf', _decode_strg_0x52b89ddf),
    0xd7e162e3: ('horizontal_selected', _decode_horizontal_selected),
    0xfe23018f: ('unknown_struct144', UnknownStruct144.from_stream),
    0xf7d3e6c2: ('unknown_struct145', UnknownStruct145.from_stream),
    0xc3b97b8: ('unknown_struct146', UnknownStruct146.from_stream),
    0xe119319b: ('text_background', _decode_text_background),
}

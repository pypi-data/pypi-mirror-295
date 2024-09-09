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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct180Json(typing_extensions.TypedDict):
        gui_frame: int
        unknown_struct27: json_util.JsonObject
        title: int
        hidden_name: int
        left_arrow: int
        left_arrow_pressed: int
        right_arrow: int
        right_arrow_pressed: int
        return_: int
        return_core: int
    

@dataclasses.dataclass()
class UnknownStruct180(BaseProperty):
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
    hidden_name: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x78a2b4b0, original_name='HiddenName'
        ),
    })
    left_arrow: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x314cdc24, original_name='LeftArrow'
        ),
    })
    left_arrow_pressed: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb4510efe, original_name='LeftArrowPressed'
        ),
    })
    right_arrow: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd1918347, original_name='RightArrow'
        ),
    })
    right_arrow_pressed: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x54cd1874, original_name='RightArrowPressed'
        ),
    })
    return_: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x471fea86, original_name='Return'
        ),
    })
    return_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa01e0887, original_name='ReturnCore'
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
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa4f20c17
        title = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x78a2b4b0
        hidden_name = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x314cdc24
        left_arrow = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb4510efe
        left_arrow_pressed = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1918347
        right_arrow = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x54cd1874
        right_arrow_pressed = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x471fea86
        return_ = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa01e0887
        return_core = struct.unpack(">Q", data.read(8))[0]
    
        return cls(gui_frame, unknown_struct27, title, hidden_name, left_arrow, left_arrow_pressed, right_arrow, right_arrow_pressed, return_, return_core)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\n')  # 10 properties

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

        data.write(b'x\xa2\xb4\xb0')  # 0x78a2b4b0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hidden_name))

        data.write(b'1L\xdc$')  # 0x314cdc24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow))

        data.write(b'\xb4Q\x0e\xfe')  # 0xb4510efe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow_pressed))

        data.write(b'\xd1\x91\x83G')  # 0xd1918347
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow))

        data.write(b'T\xcd\x18t')  # 0x54cd1874
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow_pressed))

        data.write(b'G\x1f\xea\x86')  # 0x471fea86
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_))

        data.write(b'\xa0\x1e\x08\x87')  # 0xa01e0887
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_core))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct180Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            title=json_data['title'],
            hidden_name=json_data['hidden_name'],
            left_arrow=json_data['left_arrow'],
            left_arrow_pressed=json_data['left_arrow_pressed'],
            right_arrow=json_data['right_arrow'],
            right_arrow_pressed=json_data['right_arrow_pressed'],
            return_=json_data['return_'],
            return_core=json_data['return_core'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'title': self.title,
            'hidden_name': self.hidden_name,
            'left_arrow': self.left_arrow,
            'left_arrow_pressed': self.left_arrow_pressed,
            'right_arrow': self.right_arrow,
            'right_arrow_pressed': self.right_arrow_pressed,
            'return_': self.return_,
            'return_core': self.return_core,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hidden_name(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0xa4f20c17: ('title', _decode_title),
    0x78a2b4b0: ('hidden_name', _decode_hidden_name),
    0x314cdc24: ('left_arrow', _decode_left_arrow),
    0xb4510efe: ('left_arrow_pressed', _decode_left_arrow_pressed),
    0xd1918347: ('right_arrow', _decode_right_arrow),
    0x54cd1874: ('right_arrow_pressed', _decode_right_arrow_pressed),
    0x471fea86: ('return_', _decode_return_),
    0xa01e0887: ('return_core', _decode_return_core),
}

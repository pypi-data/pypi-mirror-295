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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct158 import UnknownStruct158
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct159Json(typing_extensions.TypedDict):
        gui_frame: int
        unknown_struct26_0xf0f0840b: json_util.JsonObject
        unknown_struct26_0x3397f5e0: json_util.JsonObject
        unknown_struct26_0x95833e87: json_util.JsonObject
        strg_0x518dd3da: int
        strg_0xd374144c: int
        strg_0x6a89715b: int
        unknown_struct158: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct159(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    unknown_struct26_0xf0f0840b: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xf0f0840b, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x3397f5e0: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x3397f5e0, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x95833e87: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x95833e87, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    strg_0x518dd3da: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x518dd3da, original_name='STRG'
        ),
    })
    strg_0xd374144c: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd374144c, original_name='STRG'
        ),
    })
    strg_0x6a89715b: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6a89715b, original_name='STRG'
        ),
    })
    unknown_struct158: UnknownStruct158 = dataclasses.field(default_factory=UnknownStruct158, metadata={
        'reflection': FieldReflection[UnknownStruct158](
            UnknownStruct158, id=0x52363fb6, original_name='UnknownStruct158', from_json=UnknownStruct158.from_json, to_json=UnknownStruct158.to_json
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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0f0840b
        unknown_struct26_0xf0f0840b = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3397f5e0
        unknown_struct26_0x3397f5e0 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x95833e87
        unknown_struct26_0x95833e87 = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x518dd3da
        strg_0x518dd3da = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd374144c
        strg_0xd374144c = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a89715b
        strg_0x6a89715b = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x52363fb6
        unknown_struct158 = UnknownStruct158.from_stream(data, property_size)
    
        return cls(gui_frame, unknown_struct26_0xf0f0840b, unknown_struct26_0x3397f5e0, unknown_struct26_0x95833e87, strg_0x518dd3da, strg_0xd374144c, strg_0x6a89715b, unknown_struct158)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xf0\xf0\x84\x0b')  # 0xf0f0840b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xf0f0840b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\x97\xf5\xe0')  # 0x3397f5e0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x3397f5e0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\x83>\x87')  # 0x95833e87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x95833e87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x8d\xd3\xda')  # 0x518dd3da
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x518dd3da))

        data.write(b'\xd3t\x14L')  # 0xd374144c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xd374144c))

        data.write(b'j\x89q[')  # 0x6a89715b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x6a89715b))

        data.write(b'R6?\xb6')  # 0x52363fb6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct158.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct159Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            unknown_struct26_0xf0f0840b=UnknownStruct26.from_json(json_data['unknown_struct26_0xf0f0840b']),
            unknown_struct26_0x3397f5e0=UnknownStruct26.from_json(json_data['unknown_struct26_0x3397f5e0']),
            unknown_struct26_0x95833e87=UnknownStruct26.from_json(json_data['unknown_struct26_0x95833e87']),
            strg_0x518dd3da=json_data['strg_0x518dd3da'],
            strg_0xd374144c=json_data['strg_0xd374144c'],
            strg_0x6a89715b=json_data['strg_0x6a89715b'],
            unknown_struct158=UnknownStruct158.from_json(json_data['unknown_struct158']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct26_0xf0f0840b': self.unknown_struct26_0xf0f0840b.to_json(),
            'unknown_struct26_0x3397f5e0': self.unknown_struct26_0x3397f5e0.to_json(),
            'unknown_struct26_0x95833e87': self.unknown_struct26_0x95833e87.to_json(),
            'strg_0x518dd3da': self.strg_0x518dd3da,
            'strg_0xd374144c': self.strg_0xd374144c,
            'strg_0x6a89715b': self.strg_0x6a89715b,
            'unknown_struct158': self.unknown_struct158.to_json(),
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x518dd3da(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xd374144c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x6a89715b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xf0f0840b: ('unknown_struct26_0xf0f0840b', UnknownStruct26.from_stream),
    0x3397f5e0: ('unknown_struct26_0x3397f5e0', UnknownStruct26.from_stream),
    0x95833e87: ('unknown_struct26_0x95833e87', UnknownStruct26.from_stream),
    0x518dd3da: ('strg_0x518dd3da', _decode_strg_0x518dd3da),
    0xd374144c: ('strg_0xd374144c', _decode_strg_0xd374144c),
    0x6a89715b: ('strg_0x6a89715b', _decode_strg_0x6a89715b),
    0x52363fb6: ('unknown_struct158', UnknownStruct158.from_stream),
}

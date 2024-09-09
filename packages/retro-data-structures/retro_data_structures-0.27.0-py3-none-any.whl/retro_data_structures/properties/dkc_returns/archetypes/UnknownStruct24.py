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
from retro_data_structures.properties.dkc_returns.archetypes.LayerToggle import LayerToggle

if typing.TYPE_CHECKING:
    class UnknownStruct24Json(typing_extensions.TypedDict):
        num_layers: int
        layer_switch_0x5a8b108c: json_util.JsonObject
        layer_switch_0xc12e5ce3: json_util.JsonObject
        layer_switch_0xb6b08e13: json_util.JsonObject
        layer_switch_0x2d15c27c: json_util.JsonObject
        layer_switch_0x598d2bf3: json_util.JsonObject
        layer_switch_0xc228679c: json_util.JsonObject
        layer_switch_0xb5b6b56c: json_util.JsonObject
        layer_switch_0x2e13f903: json_util.JsonObject
        layer_switch_0x5c876672: json_util.JsonObject
        layer_switch_0xc7222a1d: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct24(BaseProperty):
    num_layers: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xe2b2c856, original_name='NumLayers'
        ),
    })
    layer_switch_0x5a8b108c: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0x5a8b108c, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0xc12e5ce3: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0xc12e5ce3, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0xb6b08e13: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0xb6b08e13, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0x2d15c27c: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0x2d15c27c, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0x598d2bf3: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0x598d2bf3, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0xc228679c: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0xc228679c, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0xb5b6b56c: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0xb5b6b56c, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0x2e13f903: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0x2e13f903, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0x5c876672: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0x5c876672, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
        ),
    })
    layer_switch_0xc7222a1d: LayerToggle = dataclasses.field(default_factory=LayerToggle, metadata={
        'reflection': FieldReflection[LayerToggle](
            LayerToggle, id=0xc7222a1d, original_name='LayerSwitch', from_json=LayerToggle.from_json, to_json=LayerToggle.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2b2c856
        num_layers = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5a8b108c
        layer_switch_0x5a8b108c = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc12e5ce3
        layer_switch_0xc12e5ce3 = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb6b08e13
        layer_switch_0xb6b08e13 = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2d15c27c
        layer_switch_0x2d15c27c = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x598d2bf3
        layer_switch_0x598d2bf3 = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc228679c
        layer_switch_0xc228679c = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb5b6b56c
        layer_switch_0xb5b6b56c = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e13f903
        layer_switch_0x2e13f903 = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5c876672
        layer_switch_0x5c876672 = LayerToggle.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc7222a1d
        layer_switch_0xc7222a1d = LayerToggle.from_stream(data, property_size)
    
        return cls(num_layers, layer_switch_0x5a8b108c, layer_switch_0xc12e5ce3, layer_switch_0xb6b08e13, layer_switch_0x2d15c27c, layer_switch_0x598d2bf3, layer_switch_0xc228679c, layer_switch_0xb5b6b56c, layer_switch_0x2e13f903, layer_switch_0x5c876672, layer_switch_0xc7222a1d)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xe2\xb2\xc8V')  # 0xe2b2c856
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_layers))

        data.write(b'Z\x8b\x10\x8c')  # 0x5a8b108c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x5a8b108c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1.\\\xe3')  # 0xc12e5ce3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xc12e5ce3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\xb0\x8e\x13')  # 0xb6b08e13
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xb6b08e13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\x15\xc2|')  # 0x2d15c27c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x2d15c27c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Y\x8d+\xf3')  # 0x598d2bf3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x598d2bf3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2(g\x9c')  # 0xc228679c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xc228679c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb5\xb6\xb5l')  # 0xb5b6b56c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xb5b6b56c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.\x13\xf9\x03')  # 0x2e13f903
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x2e13f903.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\x87fr')  # 0x5c876672
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0x5c876672.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7"*\x1d')  # 0xc7222a1d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_switch_0xc7222a1d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct24Json", data)
        return cls(
            num_layers=json_data['num_layers'],
            layer_switch_0x5a8b108c=LayerToggle.from_json(json_data['layer_switch_0x5a8b108c']),
            layer_switch_0xc12e5ce3=LayerToggle.from_json(json_data['layer_switch_0xc12e5ce3']),
            layer_switch_0xb6b08e13=LayerToggle.from_json(json_data['layer_switch_0xb6b08e13']),
            layer_switch_0x2d15c27c=LayerToggle.from_json(json_data['layer_switch_0x2d15c27c']),
            layer_switch_0x598d2bf3=LayerToggle.from_json(json_data['layer_switch_0x598d2bf3']),
            layer_switch_0xc228679c=LayerToggle.from_json(json_data['layer_switch_0xc228679c']),
            layer_switch_0xb5b6b56c=LayerToggle.from_json(json_data['layer_switch_0xb5b6b56c']),
            layer_switch_0x2e13f903=LayerToggle.from_json(json_data['layer_switch_0x2e13f903']),
            layer_switch_0x5c876672=LayerToggle.from_json(json_data['layer_switch_0x5c876672']),
            layer_switch_0xc7222a1d=LayerToggle.from_json(json_data['layer_switch_0xc7222a1d']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'num_layers': self.num_layers,
            'layer_switch_0x5a8b108c': self.layer_switch_0x5a8b108c.to_json(),
            'layer_switch_0xc12e5ce3': self.layer_switch_0xc12e5ce3.to_json(),
            'layer_switch_0xb6b08e13': self.layer_switch_0xb6b08e13.to_json(),
            'layer_switch_0x2d15c27c': self.layer_switch_0x2d15c27c.to_json(),
            'layer_switch_0x598d2bf3': self.layer_switch_0x598d2bf3.to_json(),
            'layer_switch_0xc228679c': self.layer_switch_0xc228679c.to_json(),
            'layer_switch_0xb5b6b56c': self.layer_switch_0xb5b6b56c.to_json(),
            'layer_switch_0x2e13f903': self.layer_switch_0x2e13f903.to_json(),
            'layer_switch_0x5c876672': self.layer_switch_0x5c876672.to_json(),
            'layer_switch_0xc7222a1d': self.layer_switch_0xc7222a1d.to_json(),
        }


def _decode_num_layers(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe2b2c856: ('num_layers', _decode_num_layers),
    0x5a8b108c: ('layer_switch_0x5a8b108c', LayerToggle.from_stream),
    0xc12e5ce3: ('layer_switch_0xc12e5ce3', LayerToggle.from_stream),
    0xb6b08e13: ('layer_switch_0xb6b08e13', LayerToggle.from_stream),
    0x2d15c27c: ('layer_switch_0x2d15c27c', LayerToggle.from_stream),
    0x598d2bf3: ('layer_switch_0x598d2bf3', LayerToggle.from_stream),
    0xc228679c: ('layer_switch_0xc228679c', LayerToggle.from_stream),
    0xb5b6b56c: ('layer_switch_0xb5b6b56c', LayerToggle.from_stream),
    0x2e13f903: ('layer_switch_0x2e13f903', LayerToggle.from_stream),
    0x5c876672: ('layer_switch_0x5c876672', LayerToggle.from_stream),
    0xc7222a1d: ('layer_switch_0xc7222a1d', LayerToggle.from_stream),
}

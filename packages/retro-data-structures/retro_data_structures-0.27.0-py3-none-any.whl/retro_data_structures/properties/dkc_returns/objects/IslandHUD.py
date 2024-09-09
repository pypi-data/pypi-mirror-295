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
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct182 import UnknownStruct182
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct183 import UnknownStruct183
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct36 import UnknownStruct36
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class IslandHUDJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        cursor_model: int
        disabled_cursor_model: int
        secondary_cursor_model: int
        unknown_struct182: json_util.JsonObject
        unknown_struct36: json_util.JsonObject
        unknown_struct183: json_util.JsonObject
        unknown_struct28_0xc68bc9ec: json_util.JsonObject
        unknown_struct28_0x6bdd8b7a: json_util.JsonObject
        unknown_struct28_0xcc53c738: json_util.JsonObject
        unknown_struct28_0xbcf93a2a: json_util.JsonObject
        unknown_struct28_0x6549e3f9: json_util.JsonObject
    

@dataclasses.dataclass()
class IslandHUD(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    cursor_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0f94806a, original_name='CursorModel'
        ),
    })
    disabled_cursor_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xd02fb1a1, original_name='DisabledCursorModel'
        ),
    })
    secondary_cursor_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa74065ce, original_name='SecondaryCursorModel'
        ),
    })
    unknown_struct182: UnknownStruct182 = dataclasses.field(default_factory=UnknownStruct182, metadata={
        'reflection': FieldReflection[UnknownStruct182](
            UnknownStruct182, id=0x1743b770, original_name='UnknownStruct182', from_json=UnknownStruct182.from_json, to_json=UnknownStruct182.to_json
        ),
    })
    unknown_struct36: UnknownStruct36 = dataclasses.field(default_factory=UnknownStruct36, metadata={
        'reflection': FieldReflection[UnknownStruct36](
            UnknownStruct36, id=0x3f88e900, original_name='UnknownStruct36', from_json=UnknownStruct36.from_json, to_json=UnknownStruct36.to_json
        ),
    })
    unknown_struct183: UnknownStruct183 = dataclasses.field(default_factory=UnknownStruct183, metadata={
        'reflection': FieldReflection[UnknownStruct183](
            UnknownStruct183, id=0xeb7c1bf2, original_name='UnknownStruct183', from_json=UnknownStruct183.from_json, to_json=UnknownStruct183.to_json
        ),
    })
    unknown_struct28_0xc68bc9ec: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0xc68bc9ec, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0x6bdd8b7a: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x6bdd8b7a, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0xcc53c738: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0xcc53c738, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0xbcf93a2a: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0xbcf93a2a, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    unknown_struct28_0x6549e3f9: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x6549e3f9, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
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
        return 'IHUD'

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
        if property_count != 12:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0f94806a
        cursor_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd02fb1a1
        disabled_cursor_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa74065ce
        secondary_cursor_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1743b770
        unknown_struct182 = UnknownStruct182.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3f88e900
        unknown_struct36 = UnknownStruct36.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb7c1bf2
        unknown_struct183 = UnknownStruct183.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc68bc9ec
        unknown_struct28_0xc68bc9ec = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6bdd8b7a
        unknown_struct28_0x6bdd8b7a = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcc53c738
        unknown_struct28_0xcc53c738 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbcf93a2a
        unknown_struct28_0xbcf93a2a = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6549e3f9
        unknown_struct28_0x6549e3f9 = UnknownStruct28.from_stream(data, property_size)
    
        return cls(editor_properties, cursor_model, disabled_cursor_model, secondary_cursor_model, unknown_struct182, unknown_struct36, unknown_struct183, unknown_struct28_0xc68bc9ec, unknown_struct28_0x6bdd8b7a, unknown_struct28_0xcc53c738, unknown_struct28_0xbcf93a2a, unknown_struct28_0x6549e3f9)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0f\x94\x80j')  # 0xf94806a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cursor_model))

        data.write(b'\xd0/\xb1\xa1')  # 0xd02fb1a1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disabled_cursor_model))

        data.write(b'\xa7@e\xce')  # 0xa74065ce
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.secondary_cursor_model))

        data.write(b'\x17C\xb7p')  # 0x1743b770
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct182.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\x88\xe9\x00')  # 0x3f88e900
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct36.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb|\x1b\xf2')  # 0xeb7c1bf2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct183.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x8b\xc9\xec')  # 0xc68bc9ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xc68bc9ec.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'k\xdd\x8bz')  # 0x6bdd8b7a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x6bdd8b7a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xccS\xc78')  # 0xcc53c738
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xcc53c738.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\xf9:*')  # 0xbcf93a2a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xbcf93a2a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'eI\xe3\xf9')  # 0x6549e3f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x6549e3f9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("IslandHUDJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            cursor_model=json_data['cursor_model'],
            disabled_cursor_model=json_data['disabled_cursor_model'],
            secondary_cursor_model=json_data['secondary_cursor_model'],
            unknown_struct182=UnknownStruct182.from_json(json_data['unknown_struct182']),
            unknown_struct36=UnknownStruct36.from_json(json_data['unknown_struct36']),
            unknown_struct183=UnknownStruct183.from_json(json_data['unknown_struct183']),
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(json_data['unknown_struct28_0xc68bc9ec']),
            unknown_struct28_0x6bdd8b7a=UnknownStruct28.from_json(json_data['unknown_struct28_0x6bdd8b7a']),
            unknown_struct28_0xcc53c738=UnknownStruct28.from_json(json_data['unknown_struct28_0xcc53c738']),
            unknown_struct28_0xbcf93a2a=UnknownStruct28.from_json(json_data['unknown_struct28_0xbcf93a2a']),
            unknown_struct28_0x6549e3f9=UnknownStruct28.from_json(json_data['unknown_struct28_0x6549e3f9']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'cursor_model': self.cursor_model,
            'disabled_cursor_model': self.disabled_cursor_model,
            'secondary_cursor_model': self.secondary_cursor_model,
            'unknown_struct182': self.unknown_struct182.to_json(),
            'unknown_struct36': self.unknown_struct36.to_json(),
            'unknown_struct183': self.unknown_struct183.to_json(),
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_struct28_0x6bdd8b7a': self.unknown_struct28_0x6bdd8b7a.to_json(),
            'unknown_struct28_0xcc53c738': self.unknown_struct28_0xcc53c738.to_json(),
            'unknown_struct28_0xbcf93a2a': self.unknown_struct28_0xbcf93a2a.to_json(),
            'unknown_struct28_0x6549e3f9': self.unknown_struct28_0x6549e3f9.to_json(),
        }


def _decode_cursor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disabled_cursor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_secondary_cursor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xf94806a: ('cursor_model', _decode_cursor_model),
    0xd02fb1a1: ('disabled_cursor_model', _decode_disabled_cursor_model),
    0xa74065ce: ('secondary_cursor_model', _decode_secondary_cursor_model),
    0x1743b770: ('unknown_struct182', UnknownStruct182.from_stream),
    0x3f88e900: ('unknown_struct36', UnknownStruct36.from_stream),
    0xeb7c1bf2: ('unknown_struct183', UnknownStruct183.from_stream),
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', UnknownStruct28.from_stream),
    0x6bdd8b7a: ('unknown_struct28_0x6bdd8b7a', UnknownStruct28.from_stream),
    0xcc53c738: ('unknown_struct28_0xcc53c738', UnknownStruct28.from_stream),
    0xbcf93a2a: ('unknown_struct28_0xbcf93a2a', UnknownStruct28.from_stream),
    0x6549e3f9: ('unknown_struct28_0x6549e3f9', UnknownStruct28.from_stream),
}

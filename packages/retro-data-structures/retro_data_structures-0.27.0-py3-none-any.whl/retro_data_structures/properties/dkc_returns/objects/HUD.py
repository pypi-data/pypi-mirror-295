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
from retro_data_structures.properties.dkc_returns.archetypes.BossHUD import BossHUD
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.PauseHUD import PauseHUD
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct147 import UnknownStruct147
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct156 import UnknownStruct156
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct157 import UnknownStruct157
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct159 import UnknownStruct159
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct162 import UnknownStruct162
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct164 import UnknownStruct164
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct36 import UnknownStruct36

if typing.TYPE_CHECKING:
    class HUDJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        unknown_struct147: json_util.JsonObject
        pause_hud: json_util.JsonObject
        boss_hud: json_util.JsonObject
        unknown_struct156: json_util.JsonObject
        unknown_struct157: json_util.JsonObject
        unknown_struct159: json_util.JsonObject
        unknown_struct162: json_util.JsonObject
        unknown_struct164: json_util.JsonObject
        unknown_struct28_0xc68bc9ec: json_util.JsonObject
        unknown_struct28_0x6bdd8b7a: json_util.JsonObject
        unknown_struct36: json_util.JsonObject
    

@dataclasses.dataclass()
class HUD(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    unknown_struct147: UnknownStruct147 = dataclasses.field(default_factory=UnknownStruct147, metadata={
        'reflection': FieldReflection[UnknownStruct147](
            UnknownStruct147, id=0x5d9c85da, original_name='UnknownStruct147', from_json=UnknownStruct147.from_json, to_json=UnknownStruct147.to_json
        ),
    })
    pause_hud: PauseHUD = dataclasses.field(default_factory=PauseHUD, metadata={
        'reflection': FieldReflection[PauseHUD](
            PauseHUD, id=0x10659639, original_name='PauseHUD', from_json=PauseHUD.from_json, to_json=PauseHUD.to_json
        ),
    })
    boss_hud: BossHUD = dataclasses.field(default_factory=BossHUD, metadata={
        'reflection': FieldReflection[BossHUD](
            BossHUD, id=0xae41eed1, original_name='BossHUD', from_json=BossHUD.from_json, to_json=BossHUD.to_json
        ),
    })
    unknown_struct156: UnknownStruct156 = dataclasses.field(default_factory=UnknownStruct156, metadata={
        'reflection': FieldReflection[UnknownStruct156](
            UnknownStruct156, id=0xb914bd82, original_name='UnknownStruct156', from_json=UnknownStruct156.from_json, to_json=UnknownStruct156.to_json
        ),
    })
    unknown_struct157: UnknownStruct157 = dataclasses.field(default_factory=UnknownStruct157, metadata={
        'reflection': FieldReflection[UnknownStruct157](
            UnknownStruct157, id=0x0b594741, original_name='UnknownStruct157', from_json=UnknownStruct157.from_json, to_json=UnknownStruct157.to_json
        ),
    })
    unknown_struct159: UnknownStruct159 = dataclasses.field(default_factory=UnknownStruct159, metadata={
        'reflection': FieldReflection[UnknownStruct159](
            UnknownStruct159, id=0x51841c6d, original_name='UnknownStruct159', from_json=UnknownStruct159.from_json, to_json=UnknownStruct159.to_json
        ),
    })
    unknown_struct162: UnknownStruct162 = dataclasses.field(default_factory=UnknownStruct162, metadata={
        'reflection': FieldReflection[UnknownStruct162](
            UnknownStruct162, id=0x106b3089, original_name='UnknownStruct162', from_json=UnknownStruct162.from_json, to_json=UnknownStruct162.to_json
        ),
    })
    unknown_struct164: UnknownStruct164 = dataclasses.field(default_factory=UnknownStruct164, metadata={
        'reflection': FieldReflection[UnknownStruct164](
            UnknownStruct164, id=0x3c280e64, original_name='UnknownStruct164', from_json=UnknownStruct164.from_json, to_json=UnknownStruct164.to_json
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
    unknown_struct36: UnknownStruct36 = dataclasses.field(default_factory=UnknownStruct36, metadata={
        'reflection': FieldReflection[UnknownStruct36](
            UnknownStruct36, id=0x3f88e900, original_name='UnknownStruct36', from_json=UnknownStruct36.from_json, to_json=UnknownStruct36.to_json
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
        return 'HUDD'

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
        assert property_id == 0x5d9c85da
        unknown_struct147 = UnknownStruct147.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x10659639
        pause_hud = PauseHUD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xae41eed1
        boss_hud = BossHUD.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb914bd82
        unknown_struct156 = UnknownStruct156.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0b594741
        unknown_struct157 = UnknownStruct157.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x51841c6d
        unknown_struct159 = UnknownStruct159.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x106b3089
        unknown_struct162 = UnknownStruct162.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3c280e64
        unknown_struct164 = UnknownStruct164.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc68bc9ec
        unknown_struct28_0xc68bc9ec = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6bdd8b7a
        unknown_struct28_0x6bdd8b7a = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3f88e900
        unknown_struct36 = UnknownStruct36.from_stream(data, property_size)
    
        return cls(editor_properties, unknown_struct147, pause_hud, boss_hud, unknown_struct156, unknown_struct157, unknown_struct159, unknown_struct162, unknown_struct164, unknown_struct28_0xc68bc9ec, unknown_struct28_0x6bdd8b7a, unknown_struct36)

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

        data.write(b']\x9c\x85\xda')  # 0x5d9c85da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct147.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10e\x969')  # 0x10659639
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pause_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaeA\xee\xd1')  # 0xae41eed1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boss_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9\x14\xbd\x82')  # 0xb914bd82
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct156.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0bYGA')  # 0xb594741
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct157.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x84\x1cm')  # 0x51841c6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct159.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10k0\x89')  # 0x106b3089
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct162.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<(\x0ed')  # 0x3c280e64
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct164.to_stream(data)
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

        data.write(b'?\x88\xe9\x00')  # 0x3f88e900
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct36.to_stream(data)
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
        json_data = typing.cast("HUDJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            unknown_struct147=UnknownStruct147.from_json(json_data['unknown_struct147']),
            pause_hud=PauseHUD.from_json(json_data['pause_hud']),
            boss_hud=BossHUD.from_json(json_data['boss_hud']),
            unknown_struct156=UnknownStruct156.from_json(json_data['unknown_struct156']),
            unknown_struct157=UnknownStruct157.from_json(json_data['unknown_struct157']),
            unknown_struct159=UnknownStruct159.from_json(json_data['unknown_struct159']),
            unknown_struct162=UnknownStruct162.from_json(json_data['unknown_struct162']),
            unknown_struct164=UnknownStruct164.from_json(json_data['unknown_struct164']),
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(json_data['unknown_struct28_0xc68bc9ec']),
            unknown_struct28_0x6bdd8b7a=UnknownStruct28.from_json(json_data['unknown_struct28_0x6bdd8b7a']),
            unknown_struct36=UnknownStruct36.from_json(json_data['unknown_struct36']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct147': self.unknown_struct147.to_json(),
            'pause_hud': self.pause_hud.to_json(),
            'boss_hud': self.boss_hud.to_json(),
            'unknown_struct156': self.unknown_struct156.to_json(),
            'unknown_struct157': self.unknown_struct157.to_json(),
            'unknown_struct159': self.unknown_struct159.to_json(),
            'unknown_struct162': self.unknown_struct162.to_json(),
            'unknown_struct164': self.unknown_struct164.to_json(),
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_struct28_0x6bdd8b7a': self.unknown_struct28_0x6bdd8b7a.to_json(),
            'unknown_struct36': self.unknown_struct36.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x5d9c85da: ('unknown_struct147', UnknownStruct147.from_stream),
    0x10659639: ('pause_hud', PauseHUD.from_stream),
    0xae41eed1: ('boss_hud', BossHUD.from_stream),
    0xb914bd82: ('unknown_struct156', UnknownStruct156.from_stream),
    0xb594741: ('unknown_struct157', UnknownStruct157.from_stream),
    0x51841c6d: ('unknown_struct159', UnknownStruct159.from_stream),
    0x106b3089: ('unknown_struct162', UnknownStruct162.from_stream),
    0x3c280e64: ('unknown_struct164', UnknownStruct164.from_stream),
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', UnknownStruct28.from_stream),
    0x6bdd8b7a: ('unknown_struct28_0x6bdd8b7a', UnknownStruct28.from_stream),
    0x3f88e900: ('unknown_struct36', UnknownStruct36.from_stream),
}

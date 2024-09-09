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
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.KongData import KongData
from retro_data_structures.properties.dkc_returns.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAlternateSkin import PlayerAlternateSkin
from retro_data_structures.properties.dkc_returns.archetypes.ShadowData import ShadowData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct import UnknownStruct
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct227 import UnknownStruct227

if typing.TYPE_CHECKING:
    class KongJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        shadow_data: json_util.JsonObject
        actor_information: json_util.JsonObject
        unknown_struct: json_util.JsonObject
        patterned_info: json_util.JsonObject
        alternate_skins: json_util.JsonObject
        kong_data: json_util.JsonObject
        unknown_struct227: json_util.JsonObject
    

@dataclasses.dataclass()
class Kong(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    shadow_data: ShadowData = dataclasses.field(default_factory=ShadowData, metadata={
        'reflection': FieldReflection[ShadowData](
            ShadowData, id=0xbf81c83e, original_name='ShadowData', from_json=ShadowData.from_json, to_json=ShadowData.to_json
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    unknown_struct: UnknownStruct = dataclasses.field(default_factory=UnknownStruct, metadata={
        'reflection': FieldReflection[UnknownStruct](
            UnknownStruct, id=0x0063f638, original_name='UnknownStruct', from_json=UnknownStruct.from_json, to_json=UnknownStruct.to_json
        ),
    })
    patterned_info: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef, metadata={
        'reflection': FieldReflection[PatternedAITypedef](
            PatternedAITypedef, id=0x43bbb1dd, original_name='PatternedInfo', from_json=PatternedAITypedef.from_json, to_json=PatternedAITypedef.to_json
        ),
    })
    alternate_skins: PlayerAlternateSkin = dataclasses.field(default_factory=PlayerAlternateSkin, metadata={
        'reflection': FieldReflection[PlayerAlternateSkin](
            PlayerAlternateSkin, id=0x2e9827ad, original_name='AlternateSkins', from_json=PlayerAlternateSkin.from_json, to_json=PlayerAlternateSkin.to_json
        ),
    })
    kong_data: KongData = dataclasses.field(default_factory=KongData, metadata={
        'reflection': FieldReflection[KongData](
            KongData, id=0x6f7438cf, original_name='KongData', from_json=KongData.from_json, to_json=KongData.to_json
        ),
    })
    unknown_struct227: UnknownStruct227 = dataclasses.field(default_factory=UnknownStruct227, metadata={
        'reflection': FieldReflection[UnknownStruct227](
            UnknownStruct227, id=0x9c7e9051, original_name='UnknownStruct227', from_json=UnknownStruct227.from_json, to_json=UnknownStruct227.to_json
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
        return 'KONG'

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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf81c83e
        shadow_data = ShadowData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0063f638
        unknown_struct = UnknownStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43bbb1dd
        patterned_info = PatternedAITypedef.from_stream(data, property_size, default_override={'step_up_height': 0.25})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e9827ad
        alternate_skins = PlayerAlternateSkin.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6f7438cf
        kong_data = KongData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9c7e9051
        unknown_struct227 = UnknownStruct227.from_stream(data, property_size)
    
        return cls(editor_properties, shadow_data, actor_information, unknown_struct, patterned_info, alternate_skins, kong_data, unknown_struct227)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x81\xc8>')  # 0xbf81c83e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shadow_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00c\xf68')  # 0x63f638
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xbb\xb1\xdd')  # 0x43bbb1dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_info.to_stream(data, default_override={'step_up_height': 0.25})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b".\x98'\xad")  # 0x2e9827ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.alternate_skins.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ot8\xcf')  # 0x6f7438cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kong_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c~\x90Q')  # 0x9c7e9051
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct227.to_stream(data)
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
        json_data = typing.cast("KongJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            shadow_data=ShadowData.from_json(json_data['shadow_data']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            unknown_struct=UnknownStruct.from_json(json_data['unknown_struct']),
            patterned_info=PatternedAITypedef.from_json(json_data['patterned_info']),
            alternate_skins=PlayerAlternateSkin.from_json(json_data['alternate_skins']),
            kong_data=KongData.from_json(json_data['kong_data']),
            unknown_struct227=UnknownStruct227.from_json(json_data['unknown_struct227']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'shadow_data': self.shadow_data.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_struct': self.unknown_struct.to_json(),
            'patterned_info': self.patterned_info.to_json(),
            'alternate_skins': self.alternate_skins.to_json(),
            'kong_data': self.kong_data.to_json(),
            'unknown_struct227': self.unknown_struct227.to_json(),
        }


def _decode_patterned_info(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'step_up_height': 0.25})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xbf81c83e: ('shadow_data', ShadowData.from_stream),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0x63f638: ('unknown_struct', UnknownStruct.from_stream),
    0x43bbb1dd: ('patterned_info', _decode_patterned_info),
    0x2e9827ad: ('alternate_skins', PlayerAlternateSkin.from_stream),
    0x6f7438cf: ('kong_data', KongData.from_stream),
    0x9c7e9051: ('unknown_struct227', UnknownStruct227.from_stream),
}

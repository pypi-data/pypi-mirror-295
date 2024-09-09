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
from retro_data_structures.properties.dkc_returns.archetypes.BehaviorsData import BehaviorsData
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.GenericCreatureData import GenericCreatureData
from retro_data_structures.properties.dkc_returns.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.dkc_returns.archetypes.RetronomeMessage import RetronomeMessage
from retro_data_structures.properties.dkc_returns.archetypes.ShadowData import ShadowData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct140 import UnknownStruct140

if typing.TYPE_CHECKING:
    class GenericCreatureJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        shadow_data: json_util.JsonObject
        actor_information: json_util.JsonObject
        patterned: json_util.JsonObject
        generic_creature: json_util.JsonObject
        behaviors: json_util.JsonObject
        unknown_struct140: json_util.JsonObject
        retronome_message: json_util.JsonObject
    

@dataclasses.dataclass()
class GenericCreature(BaseObjectType):
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
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef, metadata={
        'reflection': FieldReflection[PatternedAITypedef](
            PatternedAITypedef, id=0xb3774750, original_name='Patterned', from_json=PatternedAITypedef.from_json, to_json=PatternedAITypedef.to_json
        ),
    })
    generic_creature: GenericCreatureData = dataclasses.field(default_factory=GenericCreatureData, metadata={
        'reflection': FieldReflection[GenericCreatureData](
            GenericCreatureData, id=0x633fa4a9, original_name='GenericCreature', from_json=GenericCreatureData.from_json, to_json=GenericCreatureData.to_json
        ),
    })
    behaviors: BehaviorsData = dataclasses.field(default_factory=BehaviorsData, metadata={
        'reflection': FieldReflection[BehaviorsData](
            BehaviorsData, id=0x55a73403, original_name='Behaviors', from_json=BehaviorsData.from_json, to_json=BehaviorsData.to_json
        ),
    })
    unknown_struct140: UnknownStruct140 = dataclasses.field(default_factory=UnknownStruct140, metadata={
        'reflection': FieldReflection[UnknownStruct140](
            UnknownStruct140, id=0x571eb1ef, original_name='UnknownStruct140', from_json=UnknownStruct140.from_json, to_json=UnknownStruct140.to_json
        ),
    })
    retronome_message: RetronomeMessage = dataclasses.field(default_factory=RetronomeMessage, metadata={
        'reflection': FieldReflection[RetronomeMessage](
            RetronomeMessage, id=0x89916395, original_name='RetronomeMessage', from_json=RetronomeMessage.from_json, to_json=RetronomeMessage.to_json
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
        return 'GCTR'

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
        assert property_id == 0xb3774750
        patterned = PatternedAITypedef.from_stream(data, property_size, default_override={'collision_height': 1.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x633fa4a9
        generic_creature = GenericCreatureData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x55a73403
        behaviors = BehaviorsData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x571eb1ef
        unknown_struct140 = UnknownStruct140.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x89916395
        retronome_message = RetronomeMessage.from_stream(data, property_size)
    
        return cls(editor_properties, shadow_data, actor_information, patterned, generic_creature, behaviors, unknown_struct140, retronome_message)

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

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'collision_height': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c?\xa4\xa9')  # 0x633fa4a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.generic_creature.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U\xa74\x03')  # 0x55a73403
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behaviors.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'W\x1e\xb1\xef')  # 0x571eb1ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct140.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x89\x91c\x95')  # 0x89916395
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.retronome_message.to_stream(data)
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
        json_data = typing.cast("GenericCreatureJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            shadow_data=ShadowData.from_json(json_data['shadow_data']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            patterned=PatternedAITypedef.from_json(json_data['patterned']),
            generic_creature=GenericCreatureData.from_json(json_data['generic_creature']),
            behaviors=BehaviorsData.from_json(json_data['behaviors']),
            unknown_struct140=UnknownStruct140.from_json(json_data['unknown_struct140']),
            retronome_message=RetronomeMessage.from_json(json_data['retronome_message']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'shadow_data': self.shadow_data.to_json(),
            'actor_information': self.actor_information.to_json(),
            'patterned': self.patterned.to_json(),
            'generic_creature': self.generic_creature.to_json(),
            'behaviors': self.behaviors.to_json(),
            'unknown_struct140': self.unknown_struct140.to_json(),
            'retronome_message': self.retronome_message.to_json(),
        }


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'collision_height': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xbf81c83e: ('shadow_data', ShadowData.from_stream),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0xb3774750: ('patterned', _decode_patterned),
    0x633fa4a9: ('generic_creature', GenericCreatureData.from_stream),
    0x55a73403: ('behaviors', BehaviorsData.from_stream),
    0x571eb1ef: ('unknown_struct140', UnknownStruct140.from_stream),
    0x89916395: ('retronome_message', RetronomeMessage.from_stream),
}

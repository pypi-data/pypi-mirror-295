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
from retro_data_structures.properties.dkc_returns.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.dkc_returns.archetypes.TrackObjectModuleData import TrackObjectModuleData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct236 import UnknownStruct236

if typing.TYPE_CHECKING:
    class MoleJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        actor_information: json_util.JsonObject
        patterned: json_util.JsonObject
        unknown_struct236: json_util.JsonObject
        track_object_module_data: json_util.JsonObject
    

@dataclasses.dataclass()
class Mole(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
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
    unknown_struct236: UnknownStruct236 = dataclasses.field(default_factory=UnknownStruct236, metadata={
        'reflection': FieldReflection[UnknownStruct236](
            UnknownStruct236, id=0xcc43cded, original_name='UnknownStruct236', from_json=UnknownStruct236.from_json, to_json=UnknownStruct236.to_json
        ),
    })
    track_object_module_data: TrackObjectModuleData = dataclasses.field(default_factory=TrackObjectModuleData, metadata={
        'reflection': FieldReflection[TrackObjectModuleData](
            TrackObjectModuleData, id=0x0b16ced2, original_name='TrackObjectModuleData', from_json=TrackObjectModuleData.from_json, to_json=TrackObjectModuleData.to_json
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
        return 'MOLE'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_MoleTrain.rso']

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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3774750
        patterned = PatternedAITypedef.from_stream(data, property_size, default_override={'collision_height': 1.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcc43cded
        unknown_struct236 = UnknownStruct236.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0b16ced2
        track_object_module_data = TrackObjectModuleData.from_stream(data, property_size)
    
        return cls(editor_properties, actor_information, patterned, unknown_struct236, track_object_module_data)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
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

        data.write(b'\xccC\xcd\xed')  # 0xcc43cded
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct236.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b\x16\xce\xd2')  # 0xb16ced2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.track_object_module_data.to_stream(data)
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
        json_data = typing.cast("MoleJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            patterned=PatternedAITypedef.from_json(json_data['patterned']),
            unknown_struct236=UnknownStruct236.from_json(json_data['unknown_struct236']),
            track_object_module_data=TrackObjectModuleData.from_json(json_data['track_object_module_data']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'patterned': self.patterned.to_json(),
            'unknown_struct236': self.unknown_struct236.to_json(),
            'track_object_module_data': self.track_object_module_data.to_json(),
        }


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'collision_height': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0xb3774750: ('patterned', _decode_patterned),
    0xcc43cded: ('unknown_struct236', UnknownStruct236.from_stream),
    0xb16ced2: ('track_object_module_data', TrackObjectModuleData.from_stream),
}

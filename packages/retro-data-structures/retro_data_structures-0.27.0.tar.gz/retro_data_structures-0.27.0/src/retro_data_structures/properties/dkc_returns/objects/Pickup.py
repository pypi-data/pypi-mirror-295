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
from retro_data_structures.properties.dkc_returns.archetypes.PickupData import PickupData
from retro_data_structures.properties.dkc_returns.archetypes.SavedStateID import SavedStateID
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct244 import UnknownStruct244
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class PickupJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        object_id: json_util.JsonObject
        collision_size: json_util.JsonValue
        collision_offset: json_util.JsonValue
        model: int
        character_animation_information: json_util.JsonObject
        ghost_model: int
        ghost_character_animation_information: json_util.JsonObject
        actor_information: json_util.JsonObject
        pickup_data: json_util.JsonObject
        can_cause_damage: bool
        unknown_struct244: json_util.JsonObject
    

@dataclasses.dataclass()
class Pickup(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    object_id: SavedStateID = dataclasses.field(default_factory=SavedStateID, metadata={
        'reflection': FieldReflection[SavedStateID](
            SavedStateID, id=0x16d9a75d, original_name='ObjectId', from_json=SavedStateID.from_json, to_json=SavedStateID.to_json
        ),
    })
    collision_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x3a3e03ba, original_name='CollisionSize', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x2e686c2a, original_name='CollisionOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc27ffa8f, original_name='Model'
        ),
    })
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa244c9d8, original_name='CharacterAnimationInformation', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    ghost_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2cf40978, original_name='GhostModel'
        ),
    })
    ghost_character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x3128976f, original_name='GhostCharacterAnimationInformation', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    pickup_data: PickupData = dataclasses.field(default_factory=PickupData, metadata={
        'reflection': FieldReflection[PickupData](
            PickupData, id=0xd545f36b, original_name='PickupData', from_json=PickupData.from_json, to_json=PickupData.to_json
        ),
    })
    can_cause_damage: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xb0374d34, original_name='CanCauseDamage'
        ),
    })
    unknown_struct244: UnknownStruct244 = dataclasses.field(default_factory=UnknownStruct244, metadata={
        'reflection': FieldReflection[UnknownStruct244](
            UnknownStruct244, id=0x9da7abfa, original_name='UnknownStruct244', from_json=UnknownStruct244.from_json, to_json=UnknownStruct244.to_json
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
        return 'PCKP'

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
        assert property_id == 0x16d9a75d
        object_id = SavedStateID.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a3e03ba
        collision_size = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e686c2a
        collision_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc27ffa8f
        model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa244c9d8
        character_animation_information = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2cf40978
        ghost_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3128976f
        ghost_character_animation_information = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd545f36b
        pickup_data = PickupData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0374d34
        can_cause_damage = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9da7abfa
        unknown_struct244 = UnknownStruct244.from_stream(data, property_size)
    
        return cls(editor_properties, object_id, collision_size, collision_offset, model, character_animation_information, ghost_model, ghost_character_animation_information, actor_information, pickup_data, can_cause_damage, unknown_struct244)

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

        data.write(b'\x16\xd9\xa7]')  # 0x16d9a75d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.object_id.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':>\x03\xba')  # 0x3a3e03ba
        data.write(b'\x00\x0c')  # size
        self.collision_size.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',\xf4\tx')  # 0x2cf40978
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ghost_model))

        data.write(b'1(\x97o')  # 0x3128976f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghost_character_animation_information.to_stream(data)
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

        data.write(b'\xd5E\xf3k')  # 0xd545f36b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pickup_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb07M4')  # 0xb0374d34
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_cause_damage))

        data.write(b'\x9d\xa7\xab\xfa')  # 0x9da7abfa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct244.to_stream(data)
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
        json_data = typing.cast("PickupJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            object_id=SavedStateID.from_json(json_data['object_id']),
            collision_size=Vector.from_json(json_data['collision_size']),
            collision_offset=Vector.from_json(json_data['collision_offset']),
            model=json_data['model'],
            character_animation_information=AnimationParameters.from_json(json_data['character_animation_information']),
            ghost_model=json_data['ghost_model'],
            ghost_character_animation_information=AnimationParameters.from_json(json_data['ghost_character_animation_information']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            pickup_data=PickupData.from_json(json_data['pickup_data']),
            can_cause_damage=json_data['can_cause_damage'],
            unknown_struct244=UnknownStruct244.from_json(json_data['unknown_struct244']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'object_id': self.object_id.to_json(),
            'collision_size': self.collision_size.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'model': self.model,
            'character_animation_information': self.character_animation_information.to_json(),
            'ghost_model': self.ghost_model,
            'ghost_character_animation_information': self.ghost_character_animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'pickup_data': self.pickup_data.to_json(),
            'can_cause_damage': self.can_cause_damage,
            'unknown_struct244': self.unknown_struct244.to_json(),
        }


def _decode_collision_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ghost_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_can_cause_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x16d9a75d: ('object_id', SavedStateID.from_stream),
    0x3a3e03ba: ('collision_size', _decode_collision_size),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', AnimationParameters.from_stream),
    0x2cf40978: ('ghost_model', _decode_ghost_model),
    0x3128976f: ('ghost_character_animation_information', AnimationParameters.from_stream),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0xd545f36b: ('pickup_data', PickupData.from_stream),
    0xb0374d34: ('can_cause_damage', _decode_can_cause_damage),
    0x9da7abfa: ('unknown_struct244', UnknownStruct244.from_stream),
}

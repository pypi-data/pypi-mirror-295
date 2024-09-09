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
from retro_data_structures.properties.dkc_returns.archetypes.ReactiveActorBehaviors import ReactiveActorBehaviors
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class ReactiveActorJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        detection_box: json_util.JsonValue
        detection_offset: json_util.JsonValue
        model: int
        character: json_util.JsonObject
        actor_information: json_util.JsonObject
        start_enabled: bool
        texture_set: int
        behaviors: json_util.JsonObject
    

@dataclasses.dataclass()
class ReactiveActor(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    detection_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x6c447ff0, original_name='DetectionBox', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    detection_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x3daf5302, original_name='DetectionOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc27ffa8f, original_name='Model'
        ),
    })
    character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x7bc2f6cf, original_name='Character', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    start_enabled: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2f7c59dc, original_name='StartEnabled'
        ),
    })
    texture_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6b40acef, original_name='TextureSet'
        ),
    })
    behaviors: ReactiveActorBehaviors = dataclasses.field(default_factory=ReactiveActorBehaviors, metadata={
        'reflection': FieldReflection[ReactiveActorBehaviors](
            ReactiveActorBehaviors, id=0xc7bd1022, original_name='Behaviors', from_json=ReactiveActorBehaviors.from_json, to_json=ReactiveActorBehaviors.to_json
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
        return 'REAC'

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
        if property_count != 9:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6c447ff0
        detection_box = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3daf5302
        detection_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc27ffa8f
        model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7bc2f6cf
        character = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f7c59dc
        start_enabled = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b40acef
        texture_set = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc7bd1022
        behaviors = ReactiveActorBehaviors.from_stream(data, property_size)
    
        return cls(editor_properties, detection_box, detection_offset, model, character, actor_information, start_enabled, texture_set, behaviors)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'lD\x7f\xf0')  # 0x6c447ff0
        data.write(b'\x00\x0c')  # size
        self.detection_box.to_stream(data)

        data.write(b'=\xafS\x02')  # 0x3daf5302
        data.write(b'\x00\x0c')  # size
        self.detection_offset.to_stream(data)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'{\xc2\xf6\xcf')  # 0x7bc2f6cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character.to_stream(data)
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

        data.write(b'/|Y\xdc')  # 0x2f7c59dc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_enabled))

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'\xc7\xbd\x10"')  # 0xc7bd1022
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behaviors.to_stream(data)
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
        json_data = typing.cast("ReactiveActorJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            detection_box=Vector.from_json(json_data['detection_box']),
            detection_offset=Vector.from_json(json_data['detection_offset']),
            model=json_data['model'],
            character=AnimationParameters.from_json(json_data['character']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            start_enabled=json_data['start_enabled'],
            texture_set=json_data['texture_set'],
            behaviors=ReactiveActorBehaviors.from_json(json_data['behaviors']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'detection_box': self.detection_box.to_json(),
            'detection_offset': self.detection_offset.to_json(),
            'model': self.model,
            'character': self.character.to_json(),
            'actor_information': self.actor_information.to_json(),
            'start_enabled': self.start_enabled,
            'texture_set': self.texture_set,
            'behaviors': self.behaviors.to_json(),
        }


def _decode_detection_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_detection_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_start_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x6c447ff0: ('detection_box', _decode_detection_box),
    0x3daf5302: ('detection_offset', _decode_detection_offset),
    0xc27ffa8f: ('model', _decode_model),
    0x7bc2f6cf: ('character', AnimationParameters.from_stream),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0x2f7c59dc: ('start_enabled', _decode_start_enabled),
    0x6b40acef: ('texture_set', _decode_texture_set),
    0xc7bd1022: ('behaviors', ReactiveActorBehaviors.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.ScaleSplines import ScaleSplines
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class PlayerTokenJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        model: int
        character_animation_information: json_util.JsonObject
        unknown_0xa9eb0fc8: json_util.JsonObject
        unknown_0x0b30ecae: json_util.JsonObject
        unknown_0x7ca5b474: json_util.JsonObject
        unknown_0xf9786405: int
        actor_information: json_util.JsonObject
        scale_controls: json_util.JsonObject
        scale_splines: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerToken(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
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
    unknown_0xa9eb0fc8: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa9eb0fc8, original_name='Unknown', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    unknown_0x0b30ecae: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x0b30ecae, original_name='Unknown', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    unknown_0x7ca5b474: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x7ca5b474, original_name='Unknown', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    unknown_0xf9786405: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xf9786405, original_name='Unknown'
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    scale_controls: ScaleSplines = dataclasses.field(default_factory=ScaleSplines, metadata={
        'reflection': FieldReflection[ScaleSplines](
            ScaleSplines, id=0x2f7ec0a2, original_name='ScaleControls', from_json=ScaleSplines.from_json, to_json=ScaleSplines.to_json
        ),
    })
    scale_splines: ScaleSplines = dataclasses.field(default_factory=ScaleSplines, metadata={
        'reflection': FieldReflection[ScaleSplines](
            ScaleSplines, id=0x680e96ea, original_name='ScaleSplines', from_json=ScaleSplines.from_json, to_json=ScaleSplines.to_json
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
        return 'PTOK'

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
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc27ffa8f
        model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa244c9d8
        character_animation_information = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa9eb0fc8
        unknown_0xa9eb0fc8 = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0b30ecae
        unknown_0x0b30ecae = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7ca5b474
        unknown_0x7ca5b474 = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf9786405
        unknown_0xf9786405 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f7ec0a2
        scale_controls = ScaleSplines.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x680e96ea
        scale_splines = ScaleSplines.from_stream(data, property_size)
    
        return cls(editor_properties, model, character_animation_information, unknown_0xa9eb0fc8, unknown_0x0b30ecae, unknown_0x7ca5b474, unknown_0xf9786405, actor_information, scale_controls, scale_splines)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\n')  # 10 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

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

        data.write(b'\xa9\xeb\x0f\xc8')  # 0xa9eb0fc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa9eb0fc8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b0\xec\xae')  # 0xb30ecae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x0b30ecae.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\xa5\xb4t')  # 0x7ca5b474
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7ca5b474.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9xd\x05')  # 0xf9786405
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf9786405))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/~\xc0\xa2')  # 0x2f7ec0a2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\x0e\x96\xea')  # 0x680e96ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_splines.to_stream(data)
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
        json_data = typing.cast("PlayerTokenJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            model=json_data['model'],
            character_animation_information=AnimationParameters.from_json(json_data['character_animation_information']),
            unknown_0xa9eb0fc8=AnimationParameters.from_json(json_data['unknown_0xa9eb0fc8']),
            unknown_0x0b30ecae=AnimationParameters.from_json(json_data['unknown_0x0b30ecae']),
            unknown_0x7ca5b474=AnimationParameters.from_json(json_data['unknown_0x7ca5b474']),
            unknown_0xf9786405=json_data['unknown_0xf9786405'],
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            scale_controls=ScaleSplines.from_json(json_data['scale_controls']),
            scale_splines=ScaleSplines.from_json(json_data['scale_splines']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'model': self.model,
            'character_animation_information': self.character_animation_information.to_json(),
            'unknown_0xa9eb0fc8': self.unknown_0xa9eb0fc8.to_json(),
            'unknown_0x0b30ecae': self.unknown_0x0b30ecae.to_json(),
            'unknown_0x7ca5b474': self.unknown_0x7ca5b474.to_json(),
            'unknown_0xf9786405': self.unknown_0xf9786405,
            'actor_information': self.actor_information.to_json(),
            'scale_controls': self.scale_controls.to_json(),
            'scale_splines': self.scale_splines.to_json(),
        }


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf9786405(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', AnimationParameters.from_stream),
    0xa9eb0fc8: ('unknown_0xa9eb0fc8', AnimationParameters.from_stream),
    0xb30ecae: ('unknown_0x0b30ecae', AnimationParameters.from_stream),
    0x7ca5b474: ('unknown_0x7ca5b474', AnimationParameters.from_stream),
    0xf9786405: ('unknown_0xf9786405', _decode_unknown_0xf9786405),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0x2f7ec0a2: ('scale_controls', ScaleSplines.from_stream),
    0x680e96ea: ('scale_splines', ScaleSplines.from_stream),
}

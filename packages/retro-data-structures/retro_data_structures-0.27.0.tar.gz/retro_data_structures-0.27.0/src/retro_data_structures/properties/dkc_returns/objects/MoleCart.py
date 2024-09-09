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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct228 import UnknownStruct228
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct229 import UnknownStruct229
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class MoleCartJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        collision_box: json_util.JsonValue
        collision_offset: json_util.JsonValue
        actor_information: json_util.JsonObject
        model: int
        collision_model: int
        animation: json_util.JsonObject
        fsmc: int
        cart_type: int
        unknown_struct228: json_util.JsonObject
        unknown_struct229: json_util.JsonObject
    

@dataclasses.dataclass()
class MoleCart(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xf344c0b0, original_name='CollisionBox', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x2e686c2a, original_name='CollisionOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc27ffa8f, original_name='Model'
        ),
    })
    collision_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['DCLN'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x0fc966dc, original_name='CollisionModel'
        ),
    })
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa3d63f44, original_name='Animation', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    fsmc: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FSMC'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1b21eeb2, original_name='FSMC'
        ),
    })
    cart_type: enums.CartType = dataclasses.field(default=enums.CartType.Unknown2, metadata={
        'reflection': FieldReflection[enums.CartType](
            enums.CartType, id=0xd0e83e61, original_name='CartType', from_json=enums.CartType.from_json, to_json=enums.CartType.to_json
        ),
    })
    unknown_struct228: UnknownStruct228 = dataclasses.field(default_factory=UnknownStruct228, metadata={
        'reflection': FieldReflection[UnknownStruct228](
            UnknownStruct228, id=0xb9fcde3b, original_name='UnknownStruct228', from_json=UnknownStruct228.from_json, to_json=UnknownStruct228.to_json
        ),
    })
    unknown_struct229: UnknownStruct229 = dataclasses.field(default_factory=UnknownStruct229, metadata={
        'reflection': FieldReflection[UnknownStruct229](
            UnknownStruct229, id=0xc9425e4b, original_name='UnknownStruct229', from_json=UnknownStruct229.from_json, to_json=UnknownStruct229.to_json
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
        return 'MOLC'

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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf344c0b0
        collision_box = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e686c2a
        collision_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc27ffa8f
        model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0fc966dc
        collision_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa3d63f44
        animation = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b21eeb2
        fsmc = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd0e83e61
        cart_type = enums.CartType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb9fcde3b
        unknown_struct228 = UnknownStruct228.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc9425e4b
        unknown_struct229 = UnknownStruct229.from_stream(data, property_size)
    
        return cls(editor_properties, collision_box, collision_offset, actor_information, model, collision_model, animation, fsmc, cart_type, unknown_struct228, unknown_struct229)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3D\xc0\xb0')  # 0xf344c0b0
        data.write(b'\x00\x0c')  # size
        self.collision_box.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b!\xee\xb2')  # 0x1b21eeb2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fsmc))

        data.write(b'\xd0\xe8>a')  # 0xd0e83e61
        data.write(b'\x00\x04')  # size
        self.cart_type.to_stream(data)

        data.write(b'\xb9\xfc\xde;')  # 0xb9fcde3b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct228.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9B^K')  # 0xc9425e4b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct229.to_stream(data)
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
        json_data = typing.cast("MoleCartJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            collision_box=Vector.from_json(json_data['collision_box']),
            collision_offset=Vector.from_json(json_data['collision_offset']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            model=json_data['model'],
            collision_model=json_data['collision_model'],
            animation=AnimationParameters.from_json(json_data['animation']),
            fsmc=json_data['fsmc'],
            cart_type=enums.CartType.from_json(json_data['cart_type']),
            unknown_struct228=UnknownStruct228.from_json(json_data['unknown_struct228']),
            unknown_struct229=UnknownStruct229.from_json(json_data['unknown_struct229']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'actor_information': self.actor_information.to_json(),
            'model': self.model,
            'collision_model': self.collision_model,
            'animation': self.animation.to_json(),
            'fsmc': self.fsmc,
            'cart_type': self.cart_type.to_json(),
            'unknown_struct228': self.unknown_struct228.to_json(),
            'unknown_struct229': self.unknown_struct229.to_json(),
        }


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fsmc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cart_type(data: typing.BinaryIO, property_size: int):
    return enums.CartType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0xc27ffa8f: ('model', _decode_model),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xa3d63f44: ('animation', AnimationParameters.from_stream),
    0x1b21eeb2: ('fsmc', _decode_fsmc),
    0xd0e83e61: ('cart_type', _decode_cart_type),
    0xb9fcde3b: ('unknown_struct228', UnknownStruct228.from_stream),
    0xc9425e4b: ('unknown_struct229', UnknownStruct229.from_stream),
}

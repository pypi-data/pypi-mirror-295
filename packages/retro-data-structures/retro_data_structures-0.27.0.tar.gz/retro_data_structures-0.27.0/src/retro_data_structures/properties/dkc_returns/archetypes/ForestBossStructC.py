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
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class ForestBossStructCJson(typing_extensions.TypedDict):
        scale: json_util.JsonValue
        scale_locator: str
        connector_locator: str
        center_locator: str
        glowing_texture: int
        flee_texture: int
        unknown_0x749b5d80: str
        render_push: float
        unknown_0xcb3fd764: float
        unknown_0x5b604872: float
        actor_information: json_util.JsonObject
        patterned: json_util.JsonObject
    

@dataclasses.dataclass()
class ForestBossStructC(BaseProperty):
    scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xf726e5da, original_name='Scale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    scale_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x24426aef, original_name='ScaleLocator'
        ),
    })
    connector_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x0d920de2, original_name='ConnectorLocator'
        ),
    })
    center_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xf15b9fb8, original_name='CenterLocator'
        ),
    })
    glowing_texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1b5dfadf, original_name='GlowingTexture'
        ),
    })
    flee_texture: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x271e2e58, original_name='FleeTexture'
        ),
    })
    unknown_0x749b5d80: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x749b5d80, original_name='Unknown'
        ),
    })
    render_push: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xaa719632, original_name='RenderPush'
        ),
    })
    unknown_0xcb3fd764: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcb3fd764, original_name='Unknown'
        ),
    })
    unknown_0x5b604872: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5b604872, original_name='Unknown'
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
        if property_count != 12:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf726e5da
        scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x24426aef
        scale_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0d920de2
        connector_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf15b9fb8
        center_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b5dfadf
        glowing_texture = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x271e2e58
        flee_texture = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x749b5d80
        unknown_0x749b5d80 = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaa719632
        render_push = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcb3fd764
        unknown_0xcb3fd764 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5b604872
        unknown_0x5b604872 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3774750
        patterned = PatternedAITypedef.from_stream(data, property_size, default_override={'collision_height': 1.0})
    
        return cls(scale, scale_locator, connector_locator, center_locator, glowing_texture, flee_texture, unknown_0x749b5d80, render_push, unknown_0xcb3fd764, unknown_0x5b604872, actor_information, patterned)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xf7&\xe5\xda')  # 0xf726e5da
        data.write(b'\x00\x0c')  # size
        self.scale.to_stream(data)

        data.write(b'$Bj\xef')  # 0x24426aef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.scale_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\r\x92\r\xe2')  # 0xd920de2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.connector_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1[\x9f\xb8')  # 0xf15b9fb8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.center_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b]\xfa\xdf')  # 0x1b5dfadf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.glowing_texture))

        data.write(b"'\x1e.X")  # 0x271e2e58
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flee_texture))

        data.write(b't\x9b]\x80')  # 0x749b5d80
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x749b5d80.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaaq\x962')  # 0xaa719632
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.render_push))

        data.write(b'\xcb?\xd7d')  # 0xcb3fd764
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcb3fd764))

        data.write(b'[`Hr')  # 0x5b604872
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5b604872))

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

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ForestBossStructCJson", data)
        return cls(
            scale=Vector.from_json(json_data['scale']),
            scale_locator=json_data['scale_locator'],
            connector_locator=json_data['connector_locator'],
            center_locator=json_data['center_locator'],
            glowing_texture=json_data['glowing_texture'],
            flee_texture=json_data['flee_texture'],
            unknown_0x749b5d80=json_data['unknown_0x749b5d80'],
            render_push=json_data['render_push'],
            unknown_0xcb3fd764=json_data['unknown_0xcb3fd764'],
            unknown_0x5b604872=json_data['unknown_0x5b604872'],
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            patterned=PatternedAITypedef.from_json(json_data['patterned']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'scale': self.scale.to_json(),
            'scale_locator': self.scale_locator,
            'connector_locator': self.connector_locator,
            'center_locator': self.center_locator,
            'glowing_texture': self.glowing_texture,
            'flee_texture': self.flee_texture,
            'unknown_0x749b5d80': self.unknown_0x749b5d80,
            'render_push': self.render_push,
            'unknown_0xcb3fd764': self.unknown_0xcb3fd764,
            'unknown_0x5b604872': self.unknown_0x5b604872,
            'actor_information': self.actor_information.to_json(),
            'patterned': self.patterned.to_json(),
        }


def _decode_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_scale_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_connector_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_center_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_glowing_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flee_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x749b5d80(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_render_push(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcb3fd764(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5b604872(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'collision_height': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf726e5da: ('scale', _decode_scale),
    0x24426aef: ('scale_locator', _decode_scale_locator),
    0xd920de2: ('connector_locator', _decode_connector_locator),
    0xf15b9fb8: ('center_locator', _decode_center_locator),
    0x1b5dfadf: ('glowing_texture', _decode_glowing_texture),
    0x271e2e58: ('flee_texture', _decode_flee_texture),
    0x749b5d80: ('unknown_0x749b5d80', _decode_unknown_0x749b5d80),
    0xaa719632: ('render_push', _decode_render_push),
    0xcb3fd764: ('unknown_0xcb3fd764', _decode_unknown_0xcb3fd764),
    0x5b604872: ('unknown_0x5b604872', _decode_unknown_0x5b604872),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0xb3774750: ('patterned', _decode_patterned),
}

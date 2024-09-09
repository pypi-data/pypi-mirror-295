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
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters

if typing.TYPE_CHECKING:
    class PlayerAlternateSkinJson(typing_extensions.TypedDict):
        texture_set: int
        alternate: json_util.JsonObject
        tar: json_util.JsonObject
        super_guide: json_util.JsonObject
        super_guide_alternate: json_util.JsonObject
        invulnerable: json_util.JsonObject
        invulnerable_alternate: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerAlternateSkin(BaseProperty):
    texture_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6b40acef, original_name='TextureSet'
        ),
    })
    alternate: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x2fae047a, original_name='Alternate', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    tar: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x21cf023a, original_name='Tar', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    super_guide: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x47eb5a68, original_name='SuperGuide', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    super_guide_alternate: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xfc0929f0, original_name='SuperGuideAlternate', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    invulnerable: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x359b8513, original_name='Invulnerable', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    invulnerable_alternate: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xfb406ca9, original_name='InvulnerableAlternate', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
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
        if property_count != 7:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b40acef
        texture_set = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2fae047a
        alternate = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x21cf023a
        tar = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47eb5a68
        super_guide = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfc0929f0
        super_guide_alternate = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x359b8513
        invulnerable = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfb406ca9
        invulnerable_alternate = AnimationParameters.from_stream(data, property_size)
    
        return cls(texture_set, alternate, tar, super_guide, super_guide_alternate, invulnerable, invulnerable_alternate)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'/\xae\x04z')  # 0x2fae047a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.alternate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\xcf\x02:')  # 0x21cf023a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\xebZh')  # 0x47eb5a68
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_guide.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfc\t)\xf0')  # 0xfc0929f0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_guide_alternate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5\x9b\x85\x13')  # 0x359b8513
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.invulnerable.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb@l\xa9')  # 0xfb406ca9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.invulnerable_alternate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerAlternateSkinJson", data)
        return cls(
            texture_set=json_data['texture_set'],
            alternate=AnimationParameters.from_json(json_data['alternate']),
            tar=AnimationParameters.from_json(json_data['tar']),
            super_guide=AnimationParameters.from_json(json_data['super_guide']),
            super_guide_alternate=AnimationParameters.from_json(json_data['super_guide_alternate']),
            invulnerable=AnimationParameters.from_json(json_data['invulnerable']),
            invulnerable_alternate=AnimationParameters.from_json(json_data['invulnerable_alternate']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'texture_set': self.texture_set,
            'alternate': self.alternate.to_json(),
            'tar': self.tar.to_json(),
            'super_guide': self.super_guide.to_json(),
            'super_guide_alternate': self.super_guide_alternate.to_json(),
            'invulnerable': self.invulnerable.to_json(),
            'invulnerable_alternate': self.invulnerable_alternate.to_json(),
        }


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6b40acef: ('texture_set', _decode_texture_set),
    0x2fae047a: ('alternate', AnimationParameters.from_stream),
    0x21cf023a: ('tar', AnimationParameters.from_stream),
    0x47eb5a68: ('super_guide', AnimationParameters.from_stream),
    0xfc0929f0: ('super_guide_alternate', AnimationParameters.from_stream),
    0x359b8513: ('invulnerable', AnimationParameters.from_stream),
    0xfb406ca9: ('invulnerable_alternate', AnimationParameters.from_stream),
}

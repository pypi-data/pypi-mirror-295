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
from retro_data_structures.properties.dkc_returns.archetypes.ForestBossStructA import ForestBossStructA
from retro_data_structures.properties.dkc_returns.archetypes.ForestBossStructB import ForestBossStructB
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct94 import UnknownStruct94

if typing.TYPE_CHECKING:
    class UnknownStruct95Json(typing_extensions.TypedDict):
        head_locator: str
        unknown_0x97e757ed: str
        scale_locator: str
        render_push: float
        initial_offset: float
        reset_offset: float
        unknown_0x493f3dd8: float
        unknown_0xcb3fd764: float
        unknown_0x5b604872: float
        forest_boss_struct_a_0xca62889e: json_util.JsonObject
        forest_boss_struct_a_0xda392607: json_util.JsonObject
        forest_boss_struct_a_0x30059956: json_util.JsonObject
        forest_boss_struct_a_0x81c8ca71: json_util.JsonObject
        unknown_struct94: json_util.JsonObject
        forest_boss_struct_b_0xc99a740e: json_util.JsonObject
        forest_boss_struct_b_0x663339c4: json_util.JsonObject
        forest_boss_struct_b_0x03540282: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct95(BaseProperty):
    head_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xda075c18, original_name='HeadLocator'
        ),
    })
    unknown_0x97e757ed: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x97e757ed, original_name='Unknown'
        ),
    })
    scale_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x24426aef, original_name='ScaleLocator'
        ),
    })
    render_push: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xaa719632, original_name='RenderPush'
        ),
    })
    initial_offset: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8e52eb54, original_name='InitialOffset'
        ),
    })
    reset_offset: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5dcf95c3, original_name='ResetOffset'
        ),
    })
    unknown_0x493f3dd8: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x493f3dd8, original_name='Unknown'
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
    forest_boss_struct_a_0xca62889e: ForestBossStructA = dataclasses.field(default_factory=ForestBossStructA, metadata={
        'reflection': FieldReflection[ForestBossStructA](
            ForestBossStructA, id=0xca62889e, original_name='ForestBossStructA', from_json=ForestBossStructA.from_json, to_json=ForestBossStructA.to_json
        ),
    })
    forest_boss_struct_a_0xda392607: ForestBossStructA = dataclasses.field(default_factory=ForestBossStructA, metadata={
        'reflection': FieldReflection[ForestBossStructA](
            ForestBossStructA, id=0xda392607, original_name='ForestBossStructA', from_json=ForestBossStructA.from_json, to_json=ForestBossStructA.to_json
        ),
    })
    forest_boss_struct_a_0x30059956: ForestBossStructA = dataclasses.field(default_factory=ForestBossStructA, metadata={
        'reflection': FieldReflection[ForestBossStructA](
            ForestBossStructA, id=0x30059956, original_name='ForestBossStructA', from_json=ForestBossStructA.from_json, to_json=ForestBossStructA.to_json
        ),
    })
    forest_boss_struct_a_0x81c8ca71: ForestBossStructA = dataclasses.field(default_factory=ForestBossStructA, metadata={
        'reflection': FieldReflection[ForestBossStructA](
            ForestBossStructA, id=0x81c8ca71, original_name='ForestBossStructA', from_json=ForestBossStructA.from_json, to_json=ForestBossStructA.to_json
        ),
    })
    unknown_struct94: UnknownStruct94 = dataclasses.field(default_factory=UnknownStruct94, metadata={
        'reflection': FieldReflection[UnknownStruct94](
            UnknownStruct94, id=0x645ffad4, original_name='UnknownStruct94', from_json=UnknownStruct94.from_json, to_json=UnknownStruct94.to_json
        ),
    })
    forest_boss_struct_b_0xc99a740e: ForestBossStructB = dataclasses.field(default_factory=ForestBossStructB, metadata={
        'reflection': FieldReflection[ForestBossStructB](
            ForestBossStructB, id=0xc99a740e, original_name='ForestBossStructB', from_json=ForestBossStructB.from_json, to_json=ForestBossStructB.to_json
        ),
    })
    forest_boss_struct_b_0x663339c4: ForestBossStructB = dataclasses.field(default_factory=ForestBossStructB, metadata={
        'reflection': FieldReflection[ForestBossStructB](
            ForestBossStructB, id=0x663339c4, original_name='ForestBossStructB', from_json=ForestBossStructB.from_json, to_json=ForestBossStructB.to_json
        ),
    })
    forest_boss_struct_b_0x03540282: ForestBossStructB = dataclasses.field(default_factory=ForestBossStructB, metadata={
        'reflection': FieldReflection[ForestBossStructB](
            ForestBossStructB, id=0x03540282, original_name='ForestBossStructB', from_json=ForestBossStructB.from_json, to_json=ForestBossStructB.to_json
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
        if property_count != 17:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xda075c18
        head_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x97e757ed
        unknown_0x97e757ed = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x24426aef
        scale_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaa719632
        render_push = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8e52eb54
        initial_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5dcf95c3
        reset_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x493f3dd8
        unknown_0x493f3dd8 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcb3fd764
        unknown_0xcb3fd764 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5b604872
        unknown_0x5b604872 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xca62889e
        forest_boss_struct_a_0xca62889e = ForestBossStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xda392607
        forest_boss_struct_a_0xda392607 = ForestBossStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x30059956
        forest_boss_struct_a_0x30059956 = ForestBossStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x81c8ca71
        forest_boss_struct_a_0x81c8ca71 = ForestBossStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x645ffad4
        unknown_struct94 = UnknownStruct94.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc99a740e
        forest_boss_struct_b_0xc99a740e = ForestBossStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x663339c4
        forest_boss_struct_b_0x663339c4 = ForestBossStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x03540282
        forest_boss_struct_b_0x03540282 = ForestBossStructB.from_stream(data, property_size)
    
        return cls(head_locator, unknown_0x97e757ed, scale_locator, render_push, initial_offset, reset_offset, unknown_0x493f3dd8, unknown_0xcb3fd764, unknown_0x5b604872, forest_boss_struct_a_0xca62889e, forest_boss_struct_a_0xda392607, forest_boss_struct_a_0x30059956, forest_boss_struct_a_0x81c8ca71, unknown_struct94, forest_boss_struct_b_0xc99a740e, forest_boss_struct_b_0x663339c4, forest_boss_struct_b_0x03540282)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'\xda\x07\\\x18')  # 0xda075c18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.head_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\xe7W\xed')  # 0x97e757ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x97e757ed.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$Bj\xef')  # 0x24426aef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.scale_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaaq\x962')  # 0xaa719632
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.render_push))

        data.write(b'\x8eR\xebT')  # 0x8e52eb54
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_offset))

        data.write(b']\xcf\x95\xc3')  # 0x5dcf95c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reset_offset))

        data.write(b'I?=\xd8')  # 0x493f3dd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x493f3dd8))

        data.write(b'\xcb?\xd7d')  # 0xcb3fd764
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcb3fd764))

        data.write(b'[`Hr')  # 0x5b604872
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5b604872))

        data.write(b'\xcab\x88\x9e')  # 0xca62889e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_a_0xca62889e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda9&\x07')  # 0xda392607
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_a_0xda392607.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\x05\x99V')  # 0x30059956
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_a_0x30059956.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\xc8\xcaq')  # 0x81c8ca71
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_a_0x81c8ca71.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd_\xfa\xd4')  # 0x645ffad4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct94.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9\x9at\x0e')  # 0xc99a740e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_b_0xc99a740e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f39\xc4')  # 0x663339c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_b_0x663339c4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03T\x02\x82')  # 0x3540282
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_b_0x03540282.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct95Json", data)
        return cls(
            head_locator=json_data['head_locator'],
            unknown_0x97e757ed=json_data['unknown_0x97e757ed'],
            scale_locator=json_data['scale_locator'],
            render_push=json_data['render_push'],
            initial_offset=json_data['initial_offset'],
            reset_offset=json_data['reset_offset'],
            unknown_0x493f3dd8=json_data['unknown_0x493f3dd8'],
            unknown_0xcb3fd764=json_data['unknown_0xcb3fd764'],
            unknown_0x5b604872=json_data['unknown_0x5b604872'],
            forest_boss_struct_a_0xca62889e=ForestBossStructA.from_json(json_data['forest_boss_struct_a_0xca62889e']),
            forest_boss_struct_a_0xda392607=ForestBossStructA.from_json(json_data['forest_boss_struct_a_0xda392607']),
            forest_boss_struct_a_0x30059956=ForestBossStructA.from_json(json_data['forest_boss_struct_a_0x30059956']),
            forest_boss_struct_a_0x81c8ca71=ForestBossStructA.from_json(json_data['forest_boss_struct_a_0x81c8ca71']),
            unknown_struct94=UnknownStruct94.from_json(json_data['unknown_struct94']),
            forest_boss_struct_b_0xc99a740e=ForestBossStructB.from_json(json_data['forest_boss_struct_b_0xc99a740e']),
            forest_boss_struct_b_0x663339c4=ForestBossStructB.from_json(json_data['forest_boss_struct_b_0x663339c4']),
            forest_boss_struct_b_0x03540282=ForestBossStructB.from_json(json_data['forest_boss_struct_b_0x03540282']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'head_locator': self.head_locator,
            'unknown_0x97e757ed': self.unknown_0x97e757ed,
            'scale_locator': self.scale_locator,
            'render_push': self.render_push,
            'initial_offset': self.initial_offset,
            'reset_offset': self.reset_offset,
            'unknown_0x493f3dd8': self.unknown_0x493f3dd8,
            'unknown_0xcb3fd764': self.unknown_0xcb3fd764,
            'unknown_0x5b604872': self.unknown_0x5b604872,
            'forest_boss_struct_a_0xca62889e': self.forest_boss_struct_a_0xca62889e.to_json(),
            'forest_boss_struct_a_0xda392607': self.forest_boss_struct_a_0xda392607.to_json(),
            'forest_boss_struct_a_0x30059956': self.forest_boss_struct_a_0x30059956.to_json(),
            'forest_boss_struct_a_0x81c8ca71': self.forest_boss_struct_a_0x81c8ca71.to_json(),
            'unknown_struct94': self.unknown_struct94.to_json(),
            'forest_boss_struct_b_0xc99a740e': self.forest_boss_struct_b_0xc99a740e.to_json(),
            'forest_boss_struct_b_0x663339c4': self.forest_boss_struct_b_0x663339c4.to_json(),
            'forest_boss_struct_b_0x03540282': self.forest_boss_struct_b_0x03540282.to_json(),
        }


def _decode_head_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown_0x97e757ed(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_scale_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_render_push(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reset_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x493f3dd8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcb3fd764(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5b604872(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xda075c18: ('head_locator', _decode_head_locator),
    0x97e757ed: ('unknown_0x97e757ed', _decode_unknown_0x97e757ed),
    0x24426aef: ('scale_locator', _decode_scale_locator),
    0xaa719632: ('render_push', _decode_render_push),
    0x8e52eb54: ('initial_offset', _decode_initial_offset),
    0x5dcf95c3: ('reset_offset', _decode_reset_offset),
    0x493f3dd8: ('unknown_0x493f3dd8', _decode_unknown_0x493f3dd8),
    0xcb3fd764: ('unknown_0xcb3fd764', _decode_unknown_0xcb3fd764),
    0x5b604872: ('unknown_0x5b604872', _decode_unknown_0x5b604872),
    0xca62889e: ('forest_boss_struct_a_0xca62889e', ForestBossStructA.from_stream),
    0xda392607: ('forest_boss_struct_a_0xda392607', ForestBossStructA.from_stream),
    0x30059956: ('forest_boss_struct_a_0x30059956', ForestBossStructA.from_stream),
    0x81c8ca71: ('forest_boss_struct_a_0x81c8ca71', ForestBossStructA.from_stream),
    0x645ffad4: ('unknown_struct94', UnknownStruct94.from_stream),
    0xc99a740e: ('forest_boss_struct_b_0xc99a740e', ForestBossStructB.from_stream),
    0x663339c4: ('forest_boss_struct_b_0x663339c4', ForestBossStructB.from_stream),
    0x3540282: ('forest_boss_struct_b_0x03540282', ForestBossStructB.from_stream),
}

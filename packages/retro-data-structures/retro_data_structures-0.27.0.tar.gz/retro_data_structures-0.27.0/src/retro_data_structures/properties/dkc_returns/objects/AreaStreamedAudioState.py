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
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties

if typing.TYPE_CHECKING:
    class AreaStreamedAudioStateJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        area_state: int
        auto_set: bool
        global_: bool
        unknown_0xeb9f334c: bool
        increment_delay: float
        decrement_delay: float
        unknown_0xcab4886b: bool
        custom_increment_fade_in: float
        custom_increment_fade_out: float
        unknown_0x8c95539a: bool
        custom_decrement_fade_in: float
        custom_decrement_fade_out: float
        unknown_0x250142a2: bool
    

@dataclasses.dataclass()
class AreaStreamedAudioState(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    area_state: enums.MusicEnumB = dataclasses.field(default=enums.MusicEnumB.Unknown1, metadata={
        'reflection': FieldReflection[enums.MusicEnumB](
            enums.MusicEnumB, id=0xe7d8d823, original_name='AreaState', from_json=enums.MusicEnumB.from_json, to_json=enums.MusicEnumB.to_json
        ),
    })
    auto_set: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x05c9246c, original_name='AutoSet'
        ),
    })
    global_: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2409b906, original_name='Global'
        ),
    })
    unknown_0xeb9f334c: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xeb9f334c, original_name='Unknown'
        ),
    })
    increment_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xeeb39069, original_name='IncrementDelay'
        ),
    })
    decrement_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x244f7338, original_name='DecrementDelay'
        ),
    })
    unknown_0xcab4886b: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcab4886b, original_name='Unknown'
        ),
    })
    custom_increment_fade_in: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1bb81937, original_name='CustomIncrementFadeIn'
        ),
    })
    custom_increment_fade_out: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6748b641, original_name='CustomIncrementFadeOut'
        ),
    })
    unknown_0x8c95539a: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8c95539a, original_name='Unknown'
        ),
    })
    custom_decrement_fade_in: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x071e84b6, original_name='CustomDecrementFadeIn'
        ),
    })
    custom_decrement_fade_out: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfdeba36a, original_name='CustomDecrementFadeOut'
        ),
    })
    unknown_0x250142a2: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x250142a2, original_name='Unknown'
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
        return 'ASAS'

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
        if property_count != 14:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe7d8d823
        area_state = enums.MusicEnumB.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x05c9246c
        auto_set = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2409b906
        global_ = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb9f334c
        unknown_0xeb9f334c = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeeb39069
        increment_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x244f7338
        decrement_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcab4886b
        unknown_0xcab4886b = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1bb81937
        custom_increment_fade_in = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6748b641
        custom_increment_fade_out = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8c95539a
        unknown_0x8c95539a = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x071e84b6
        custom_decrement_fade_in = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfdeba36a
        custom_decrement_fade_out = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x250142a2
        unknown_0x250142a2 = struct.unpack('>?', data.read(1))[0]
    
        return cls(editor_properties, area_state, auto_set, global_, unknown_0xeb9f334c, increment_delay, decrement_delay, unknown_0xcab4886b, custom_increment_fade_in, custom_increment_fade_out, unknown_0x8c95539a, custom_decrement_fade_in, custom_decrement_fade_out, unknown_0x250142a2)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xd8\xd8#')  # 0xe7d8d823
        data.write(b'\x00\x04')  # size
        self.area_state.to_stream(data)

        data.write(b'\x05\xc9$l')  # 0x5c9246c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_set))

        data.write(b'$\t\xb9\x06')  # 0x2409b906
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.global_))

        data.write(b'\xeb\x9f3L')  # 0xeb9f334c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xeb9f334c))

        data.write(b'\xee\xb3\x90i')  # 0xeeb39069
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.increment_delay))

        data.write(b'$Os8')  # 0x244f7338
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.decrement_delay))

        data.write(b'\xca\xb4\x88k')  # 0xcab4886b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcab4886b))

        data.write(b'\x1b\xb8\x197')  # 0x1bb81937
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_increment_fade_in))

        data.write(b'gH\xb6A')  # 0x6748b641
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_increment_fade_out))

        data.write(b'\x8c\x95S\x9a')  # 0x8c95539a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8c95539a))

        data.write(b'\x07\x1e\x84\xb6')  # 0x71e84b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_decrement_fade_in))

        data.write(b'\xfd\xeb\xa3j')  # 0xfdeba36a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_decrement_fade_out))

        data.write(b'%\x01B\xa2')  # 0x250142a2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x250142a2))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("AreaStreamedAudioStateJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            area_state=enums.MusicEnumB.from_json(json_data['area_state']),
            auto_set=json_data['auto_set'],
            global_=json_data['global_'],
            unknown_0xeb9f334c=json_data['unknown_0xeb9f334c'],
            increment_delay=json_data['increment_delay'],
            decrement_delay=json_data['decrement_delay'],
            unknown_0xcab4886b=json_data['unknown_0xcab4886b'],
            custom_increment_fade_in=json_data['custom_increment_fade_in'],
            custom_increment_fade_out=json_data['custom_increment_fade_out'],
            unknown_0x8c95539a=json_data['unknown_0x8c95539a'],
            custom_decrement_fade_in=json_data['custom_decrement_fade_in'],
            custom_decrement_fade_out=json_data['custom_decrement_fade_out'],
            unknown_0x250142a2=json_data['unknown_0x250142a2'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'area_state': self.area_state.to_json(),
            'auto_set': self.auto_set,
            'global_': self.global_,
            'unknown_0xeb9f334c': self.unknown_0xeb9f334c,
            'increment_delay': self.increment_delay,
            'decrement_delay': self.decrement_delay,
            'unknown_0xcab4886b': self.unknown_0xcab4886b,
            'custom_increment_fade_in': self.custom_increment_fade_in,
            'custom_increment_fade_out': self.custom_increment_fade_out,
            'unknown_0x8c95539a': self.unknown_0x8c95539a,
            'custom_decrement_fade_in': self.custom_decrement_fade_in,
            'custom_decrement_fade_out': self.custom_decrement_fade_out,
            'unknown_0x250142a2': self.unknown_0x250142a2,
        }


def _decode_area_state(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumB.from_stream(data)


def _decode_auto_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_global_(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xeb9f334c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_increment_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_decrement_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcab4886b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_custom_increment_fade_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_custom_increment_fade_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8c95539a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_custom_decrement_fade_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_custom_decrement_fade_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x250142a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xe7d8d823: ('area_state', _decode_area_state),
    0x5c9246c: ('auto_set', _decode_auto_set),
    0x2409b906: ('global_', _decode_global_),
    0xeb9f334c: ('unknown_0xeb9f334c', _decode_unknown_0xeb9f334c),
    0xeeb39069: ('increment_delay', _decode_increment_delay),
    0x244f7338: ('decrement_delay', _decode_decrement_delay),
    0xcab4886b: ('unknown_0xcab4886b', _decode_unknown_0xcab4886b),
    0x1bb81937: ('custom_increment_fade_in', _decode_custom_increment_fade_in),
    0x6748b641: ('custom_increment_fade_out', _decode_custom_increment_fade_out),
    0x8c95539a: ('unknown_0x8c95539a', _decode_unknown_0x8c95539a),
    0x71e84b6: ('custom_decrement_fade_in', _decode_custom_decrement_fade_in),
    0xfdeba36a: ('custom_decrement_fade_out', _decode_custom_decrement_fade_out),
    0x250142a2: ('unknown_0x250142a2', _decode_unknown_0x250142a2),
}

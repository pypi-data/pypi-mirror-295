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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct11 import UnknownStruct11
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct12 import UnknownStruct12
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct16 import UnknownStruct16

if typing.TYPE_CHECKING:
    class AcousticsJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        is_global: bool
        exclude_listener: bool
        start_incremented: bool
        auto_increment: bool
        auto_decrement: bool
        effect_volume: float
        effect_type: int
        unknown_struct11: json_util.JsonObject
        unknown_struct12: json_util.JsonObject
        unknown_struct16: json_util.JsonObject
    

@dataclasses.dataclass()
class Acoustics(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    is_global: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x765cae8c, original_name='IsGlobal'
        ),
    })
    exclude_listener: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc78b91fa, original_name='ExcludeListener'
        ),
    })
    start_incremented: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa6bcdf8e, original_name='StartIncremented'
        ),
    })
    auto_increment: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x11aa184b, original_name='AutoIncrement'
        ),
    })
    auto_decrement: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2714dc3b, original_name='AutoDecrement'
        ),
    })
    effect_volume: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5a38a08d, original_name='EffectVolume'
        ),
    })
    effect_type: enums.EffectType = dataclasses.field(default=enums.EffectType.Unknown1, metadata={
        'reflection': FieldReflection[enums.EffectType](
            enums.EffectType, id=0xe9ad286a, original_name='EffectType', from_json=enums.EffectType.from_json, to_json=enums.EffectType.to_json
        ),
    })
    unknown_struct11: UnknownStruct11 = dataclasses.field(default_factory=UnknownStruct11, metadata={
        'reflection': FieldReflection[UnknownStruct11](
            UnknownStruct11, id=0xa383e10b, original_name='UnknownStruct11', from_json=UnknownStruct11.from_json, to_json=UnknownStruct11.to_json
        ),
    })
    unknown_struct12: UnknownStruct12 = dataclasses.field(default_factory=UnknownStruct12, metadata={
        'reflection': FieldReflection[UnknownStruct12](
            UnknownStruct12, id=0x6530e9cf, original_name='UnknownStruct12', from_json=UnknownStruct12.from_json, to_json=UnknownStruct12.to_json
        ),
    })
    unknown_struct16: UnknownStruct16 = dataclasses.field(default_factory=UnknownStruct16, metadata={
        'reflection': FieldReflection[UnknownStruct16](
            UnknownStruct16, id=0x3bc9da35, original_name='UnknownStruct16', from_json=UnknownStruct16.from_json, to_json=UnknownStruct16.to_json
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
        return 'ACOU'

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
        assert property_id == 0x765cae8c
        is_global = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc78b91fa
        exclude_listener = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa6bcdf8e
        start_incremented = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x11aa184b
        auto_increment = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2714dc3b
        auto_decrement = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5a38a08d
        effect_volume = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9ad286a
        effect_type = enums.EffectType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa383e10b
        unknown_struct11 = UnknownStruct11.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6530e9cf
        unknown_struct12 = UnknownStruct12.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3bc9da35
        unknown_struct16 = UnknownStruct16.from_stream(data, property_size)
    
        return cls(editor_properties, is_global, exclude_listener, start_incremented, auto_increment, auto_decrement, effect_volume, effect_type, unknown_struct11, unknown_struct12, unknown_struct16)

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

        data.write(b'v\\\xae\x8c')  # 0x765cae8c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_global))

        data.write(b'\xc7\x8b\x91\xfa')  # 0xc78b91fa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.exclude_listener))

        data.write(b'\xa6\xbc\xdf\x8e')  # 0xa6bcdf8e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_incremented))

        data.write(b'\x11\xaa\x18K')  # 0x11aa184b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_increment))

        data.write(b"'\x14\xdc;")  # 0x2714dc3b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_decrement))

        data.write(b'Z8\xa0\x8d')  # 0x5a38a08d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.effect_volume))

        data.write(b'\xe9\xad(j')  # 0xe9ad286a
        data.write(b'\x00\x04')  # size
        self.effect_type.to_stream(data)

        data.write(b'\xa3\x83\xe1\x0b')  # 0xa383e10b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct11.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'e0\xe9\xcf')  # 0x6530e9cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct12.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';\xc9\xda5')  # 0x3bc9da35
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct16.to_stream(data)
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
        json_data = typing.cast("AcousticsJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            is_global=json_data['is_global'],
            exclude_listener=json_data['exclude_listener'],
            start_incremented=json_data['start_incremented'],
            auto_increment=json_data['auto_increment'],
            auto_decrement=json_data['auto_decrement'],
            effect_volume=json_data['effect_volume'],
            effect_type=enums.EffectType.from_json(json_data['effect_type']),
            unknown_struct11=UnknownStruct11.from_json(json_data['unknown_struct11']),
            unknown_struct12=UnknownStruct12.from_json(json_data['unknown_struct12']),
            unknown_struct16=UnknownStruct16.from_json(json_data['unknown_struct16']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'is_global': self.is_global,
            'exclude_listener': self.exclude_listener,
            'start_incremented': self.start_incremented,
            'auto_increment': self.auto_increment,
            'auto_decrement': self.auto_decrement,
            'effect_volume': self.effect_volume,
            'effect_type': self.effect_type.to_json(),
            'unknown_struct11': self.unknown_struct11.to_json(),
            'unknown_struct12': self.unknown_struct12.to_json(),
            'unknown_struct16': self.unknown_struct16.to_json(),
        }


def _decode_is_global(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_exclude_listener(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_incremented(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_increment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_decrement(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_effect_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_effect_type(data: typing.BinaryIO, property_size: int):
    return enums.EffectType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x765cae8c: ('is_global', _decode_is_global),
    0xc78b91fa: ('exclude_listener', _decode_exclude_listener),
    0xa6bcdf8e: ('start_incremented', _decode_start_incremented),
    0x11aa184b: ('auto_increment', _decode_auto_increment),
    0x2714dc3b: ('auto_decrement', _decode_auto_decrement),
    0x5a38a08d: ('effect_volume', _decode_effect_volume),
    0xe9ad286a: ('effect_type', _decode_effect_type),
    0xa383e10b: ('unknown_struct11', UnknownStruct11.from_stream),
    0x6530e9cf: ('unknown_struct12', UnknownStruct12.from_stream),
    0x3bc9da35: ('unknown_struct16', UnknownStruct16.from_stream),
}

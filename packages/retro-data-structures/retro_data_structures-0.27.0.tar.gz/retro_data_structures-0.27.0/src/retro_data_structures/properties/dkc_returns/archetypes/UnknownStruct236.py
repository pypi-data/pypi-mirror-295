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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct231 import UnknownStruct231
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct235 import UnknownStruct235

if typing.TYPE_CHECKING:
    class UnknownStruct236Json(typing_extensions.TypedDict):
        mole_type: int
        damage_bounds_scale_z: float
        unknown: str
        unknown_struct231: json_util.JsonObject
        unknown_struct235: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct236(BaseProperty):
    mole_type: enums.MoleType = dataclasses.field(default=enums.MoleType.Unknown1, metadata={
        'reflection': FieldReflection[enums.MoleType](
            enums.MoleType, id=0xe9732110, original_name='MoleType', from_json=enums.MoleType.from_json, to_json=enums.MoleType.to_json
        ),
    })
    damage_bounds_scale_z: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc336a4ef, original_name='DamageBoundsScaleZ'
        ),
    })
    unknown: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x15870845, original_name='Unknown'
        ),
    })
    unknown_struct231: UnknownStruct231 = dataclasses.field(default_factory=UnknownStruct231, metadata={
        'reflection': FieldReflection[UnknownStruct231](
            UnknownStruct231, id=0x4673c93c, original_name='UnknownStruct231', from_json=UnknownStruct231.from_json, to_json=UnknownStruct231.to_json
        ),
    })
    unknown_struct235: UnknownStruct235 = dataclasses.field(default_factory=UnknownStruct235, metadata={
        'reflection': FieldReflection[UnknownStruct235](
            UnknownStruct235, id=0xa694e8ca, original_name='UnknownStruct235', from_json=UnknownStruct235.from_json, to_json=UnknownStruct235.to_json
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
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9732110
        mole_type = enums.MoleType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc336a4ef
        damage_bounds_scale_z = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x15870845
        unknown = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4673c93c
        unknown_struct231 = UnknownStruct231.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa694e8ca
        unknown_struct235 = UnknownStruct235.from_stream(data, property_size)
    
        return cls(mole_type, damage_bounds_scale_z, unknown, unknown_struct231, unknown_struct235)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xe9s!\x10')  # 0xe9732110
        data.write(b'\x00\x04')  # size
        self.mole_type.to_stream(data)

        data.write(b'\xc36\xa4\xef')  # 0xc336a4ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_bounds_scale_z))

        data.write(b'\x15\x87\x08E')  # 0x15870845
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Fs\xc9<')  # 0x4673c93c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct231.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6\x94\xe8\xca')  # 0xa694e8ca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct235.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct236Json", data)
        return cls(
            mole_type=enums.MoleType.from_json(json_data['mole_type']),
            damage_bounds_scale_z=json_data['damage_bounds_scale_z'],
            unknown=json_data['unknown'],
            unknown_struct231=UnknownStruct231.from_json(json_data['unknown_struct231']),
            unknown_struct235=UnknownStruct235.from_json(json_data['unknown_struct235']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'mole_type': self.mole_type.to_json(),
            'damage_bounds_scale_z': self.damage_bounds_scale_z,
            'unknown': self.unknown,
            'unknown_struct231': self.unknown_struct231.to_json(),
            'unknown_struct235': self.unknown_struct235.to_json(),
        }


def _decode_mole_type(data: typing.BinaryIO, property_size: int):
    return enums.MoleType.from_stream(data)


def _decode_damage_bounds_scale_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe9732110: ('mole_type', _decode_mole_type),
    0xc336a4ef: ('damage_bounds_scale_z', _decode_damage_bounds_scale_z),
    0x15870845: ('unknown', _decode_unknown),
    0x4673c93c: ('unknown_struct231', UnknownStruct231.from_stream),
    0xa694e8ca: ('unknown_struct235', UnknownStruct235.from_stream),
}

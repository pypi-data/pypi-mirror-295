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
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters

if typing.TYPE_CHECKING:
    class RambiCrateDataJson(typing_extensions.TypedDict):
        animation: json_util.JsonObject
        unknown_0xa2dc645a: int
        unknown_0x456b0545: int
        vulnerability: json_util.JsonObject
        unknown_0xfa8ca261: float
        min_reactivate_distance: float
        max_reactivate_distance: float
    

@dataclasses.dataclass()
class RambiCrateData(BaseProperty):
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xa3d63f44, original_name='Animation', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    unknown_0xa2dc645a: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xa2dc645a, original_name='Unknown'
        ),
    })
    unknown_0x456b0545: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x456b0545, original_name='Unknown'
        ),
    })
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability, metadata={
        'reflection': FieldReflection[DamageVulnerability](
            DamageVulnerability, id=0x7b71ae90, original_name='Vulnerability', from_json=DamageVulnerability.from_json, to_json=DamageVulnerability.to_json
        ),
    })
    unknown_0xfa8ca261: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfa8ca261, original_name='Unknown'
        ),
    })
    min_reactivate_distance: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc55566db, original_name='MinReactivateDistance'
        ),
    })
    max_reactivate_distance: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2608d801, original_name='MaxReactivateDistance'
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
        assert property_id == 0xa3d63f44
        animation = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa2dc645a
        unknown_0xa2dc645a = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x456b0545
        unknown_0x456b0545 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b71ae90
        vulnerability = DamageVulnerability.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfa8ca261
        unknown_0xfa8ca261 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc55566db
        min_reactivate_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2608d801
        max_reactivate_distance = struct.unpack('>f', data.read(4))[0]
    
        return cls(animation, unknown_0xa2dc645a, unknown_0x456b0545, vulnerability, unknown_0xfa8ca261, min_reactivate_distance, max_reactivate_distance)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\xdcdZ')  # 0xa2dc645a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa2dc645a))

        data.write(b'Ek\x05E')  # 0x456b0545
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x456b0545))

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\x8c\xa2a')  # 0xfa8ca261
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfa8ca261))

        data.write(b'\xc5Uf\xdb')  # 0xc55566db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_reactivate_distance))

        data.write(b'&\x08\xd8\x01')  # 0x2608d801
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_reactivate_distance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("RambiCrateDataJson", data)
        return cls(
            animation=AnimationParameters.from_json(json_data['animation']),
            unknown_0xa2dc645a=json_data['unknown_0xa2dc645a'],
            unknown_0x456b0545=json_data['unknown_0x456b0545'],
            vulnerability=DamageVulnerability.from_json(json_data['vulnerability']),
            unknown_0xfa8ca261=json_data['unknown_0xfa8ca261'],
            min_reactivate_distance=json_data['min_reactivate_distance'],
            max_reactivate_distance=json_data['max_reactivate_distance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'animation': self.animation.to_json(),
            'unknown_0xa2dc645a': self.unknown_0xa2dc645a,
            'unknown_0x456b0545': self.unknown_0x456b0545,
            'vulnerability': self.vulnerability.to_json(),
            'unknown_0xfa8ca261': self.unknown_0xfa8ca261,
            'min_reactivate_distance': self.min_reactivate_distance,
            'max_reactivate_distance': self.max_reactivate_distance,
        }


def _decode_unknown_0xa2dc645a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x456b0545(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xfa8ca261(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_reactivate_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_reactivate_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa3d63f44: ('animation', AnimationParameters.from_stream),
    0xa2dc645a: ('unknown_0xa2dc645a', _decode_unknown_0xa2dc645a),
    0x456b0545: ('unknown_0x456b0545', _decode_unknown_0x456b0545),
    0x7b71ae90: ('vulnerability', DamageVulnerability.from_stream),
    0xfa8ca261: ('unknown_0xfa8ca261', _decode_unknown_0xfa8ca261),
    0xc55566db: ('min_reactivate_distance', _decode_min_reactivate_distance),
    0x2608d801: ('max_reactivate_distance', _decode_max_reactivate_distance),
}

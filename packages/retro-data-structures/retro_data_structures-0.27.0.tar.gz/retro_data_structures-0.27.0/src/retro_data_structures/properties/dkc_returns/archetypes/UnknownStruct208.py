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
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct202 import UnknownStruct202
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct203 import UnknownStruct203
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct204 import UnknownStruct204
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct206 import UnknownStruct206
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct207 import UnknownStruct207
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct208Json(typing_extensions.TypedDict):
        boss_type: int
        unknown_struct202: json_util.JsonObject
        unknown_struct203: json_util.JsonObject
        unknown_struct204: json_util.JsonObject
        fire_beam_damage: json_util.JsonObject
        unknown_struct206: json_util.JsonObject
        unknown_struct207: json_util.JsonObject
        gravity: float
        terminal_velocity: float
        unknown_0x880adc23: int
        unknown_0x5d1de4ae: float
        unknown_0x59f65627: float
        spit_distance: float
        spit_height: float
        unknown_0x1e3cbfc2: float
        unknown_0xee382651: float
        unknown_0xc4043234: float
        caud_0x06b3ef54: int
        caud_0xc4dbea19: int
    

@dataclasses.dataclass()
class UnknownStruct208(BaseProperty):
    boss_type: enums.BossType = dataclasses.field(default=enums.BossType.Unknown1, metadata={
        'reflection': FieldReflection[enums.BossType](
            enums.BossType, id=0x92985fff, original_name='BossType', from_json=enums.BossType.from_json, to_json=enums.BossType.to_json
        ),
    })
    unknown_struct202: UnknownStruct202 = dataclasses.field(default_factory=UnknownStruct202, metadata={
        'reflection': FieldReflection[UnknownStruct202](
            UnknownStruct202, id=0x039ce09a, original_name='UnknownStruct202', from_json=UnknownStruct202.from_json, to_json=UnknownStruct202.to_json
        ),
    })
    unknown_struct203: UnknownStruct203 = dataclasses.field(default_factory=UnknownStruct203, metadata={
        'reflection': FieldReflection[UnknownStruct203](
            UnknownStruct203, id=0xef3e4da5, original_name='UnknownStruct203', from_json=UnknownStruct203.from_json, to_json=UnknownStruct203.to_json
        ),
    })
    unknown_struct204: UnknownStruct204 = dataclasses.field(default_factory=UnknownStruct204, metadata={
        'reflection': FieldReflection[UnknownStruct204](
            UnknownStruct204, id=0x45c4c44c, original_name='UnknownStruct204', from_json=UnknownStruct204.from_json, to_json=UnknownStruct204.to_json
        ),
    })
    fire_beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0x9e8f9696, original_name='FireBeamDamage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    unknown_struct206: UnknownStruct206 = dataclasses.field(default_factory=UnknownStruct206, metadata={
        'reflection': FieldReflection[UnknownStruct206](
            UnknownStruct206, id=0xcd9de8cc, original_name='UnknownStruct206', from_json=UnknownStruct206.from_json, to_json=UnknownStruct206.to_json
        ),
    })
    unknown_struct207: UnknownStruct207 = dataclasses.field(default_factory=UnknownStruct207, metadata={
        'reflection': FieldReflection[UnknownStruct207](
            UnknownStruct207, id=0x307ce7e4, original_name='UnknownStruct207', from_json=UnknownStruct207.from_json, to_json=UnknownStruct207.to_json
        ),
    })
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    terminal_velocity: float = dataclasses.field(default=35.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xab9566a2, original_name='TerminalVelocity'
        ),
    })
    unknown_0x880adc23: int = dataclasses.field(default=10, metadata={
        'reflection': FieldReflection[int](
            int, id=0x880adc23, original_name='Unknown'
        ),
    })
    unknown_0x5d1de4ae: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5d1de4ae, original_name='Unknown'
        ),
    })
    unknown_0x59f65627: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x59f65627, original_name='Unknown'
        ),
    })
    spit_distance: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x04408e47, original_name='SpitDistance'
        ),
    })
    spit_height: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa54be635, original_name='SpitHeight'
        ),
    })
    unknown_0x1e3cbfc2: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1e3cbfc2, original_name='Unknown'
        ),
    })
    unknown_0xee382651: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xee382651, original_name='Unknown'
        ),
    })
    unknown_0xc4043234: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc4043234, original_name='Unknown'
        ),
    })
    caud_0x06b3ef54: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x06b3ef54, original_name='CAUD'
        ),
    })
    caud_0xc4dbea19: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc4dbea19, original_name='CAUD'
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
        if property_count != 19:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x92985fff
        boss_type = enums.BossType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x039ce09a
        unknown_struct202 = UnknownStruct202.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xef3e4da5
        unknown_struct203 = UnknownStruct203.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x45c4c44c
        unknown_struct204 = UnknownStruct204.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9e8f9696
        fire_beam_damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcd9de8cc
        unknown_struct206 = UnknownStruct206.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x307ce7e4
        unknown_struct207 = UnknownStruct207.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab9566a2
        terminal_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x880adc23
        unknown_0x880adc23 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5d1de4ae
        unknown_0x5d1de4ae = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59f65627
        unknown_0x59f65627 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x04408e47
        spit_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa54be635
        spit_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1e3cbfc2
        unknown_0x1e3cbfc2 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xee382651
        unknown_0xee382651 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc4043234
        unknown_0xc4043234 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x06b3ef54
        caud_0x06b3ef54 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc4dbea19
        caud_0xc4dbea19 = struct.unpack(">Q", data.read(8))[0]
    
        return cls(boss_type, unknown_struct202, unknown_struct203, unknown_struct204, fire_beam_damage, unknown_struct206, unknown_struct207, gravity, terminal_velocity, unknown_0x880adc23, unknown_0x5d1de4ae, unknown_0x59f65627, spit_distance, spit_height, unknown_0x1e3cbfc2, unknown_0xee382651, unknown_0xc4043234, caud_0x06b3ef54, caud_0xc4dbea19)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'\x92\x98_\xff')  # 0x92985fff
        data.write(b'\x00\x04')  # size
        self.boss_type.to_stream(data)

        data.write(b'\x03\x9c\xe0\x9a')  # 0x39ce09a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct202.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xef>M\xa5')  # 0xef3e4da5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct203.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'E\xc4\xc4L')  # 0x45c4c44c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct204.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\x8f\x96\x96')  # 0x9e8f9696
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fire_beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\x9d\xe8\xcc')  # 0xcd9de8cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct206.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0|\xe7\xe4')  # 0x307ce7e4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct207.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xab\x95f\xa2')  # 0xab9566a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terminal_velocity))

        data.write(b'\x88\n\xdc#')  # 0x880adc23
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x880adc23))

        data.write(b']\x1d\xe4\xae')  # 0x5d1de4ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d1de4ae))

        data.write(b"Y\xf6V'")  # 0x59f65627
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x59f65627))

        data.write(b'\x04@\x8eG')  # 0x4408e47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_distance))

        data.write(b'\xa5K\xe65')  # 0xa54be635
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_height))

        data.write(b'\x1e<\xbf\xc2')  # 0x1e3cbfc2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1e3cbfc2))

        data.write(b'\xee8&Q')  # 0xee382651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xee382651))

        data.write(b'\xc4\x0424')  # 0xc4043234
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc4043234))

        data.write(b'\x06\xb3\xefT')  # 0x6b3ef54
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x06b3ef54))

        data.write(b'\xc4\xdb\xea\x19')  # 0xc4dbea19
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xc4dbea19))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct208Json", data)
        return cls(
            boss_type=enums.BossType.from_json(json_data['boss_type']),
            unknown_struct202=UnknownStruct202.from_json(json_data['unknown_struct202']),
            unknown_struct203=UnknownStruct203.from_json(json_data['unknown_struct203']),
            unknown_struct204=UnknownStruct204.from_json(json_data['unknown_struct204']),
            fire_beam_damage=DamageInfo.from_json(json_data['fire_beam_damage']),
            unknown_struct206=UnknownStruct206.from_json(json_data['unknown_struct206']),
            unknown_struct207=UnknownStruct207.from_json(json_data['unknown_struct207']),
            gravity=json_data['gravity'],
            terminal_velocity=json_data['terminal_velocity'],
            unknown_0x880adc23=json_data['unknown_0x880adc23'],
            unknown_0x5d1de4ae=json_data['unknown_0x5d1de4ae'],
            unknown_0x59f65627=json_data['unknown_0x59f65627'],
            spit_distance=json_data['spit_distance'],
            spit_height=json_data['spit_height'],
            unknown_0x1e3cbfc2=json_data['unknown_0x1e3cbfc2'],
            unknown_0xee382651=json_data['unknown_0xee382651'],
            unknown_0xc4043234=json_data['unknown_0xc4043234'],
            caud_0x06b3ef54=json_data['caud_0x06b3ef54'],
            caud_0xc4dbea19=json_data['caud_0xc4dbea19'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'boss_type': self.boss_type.to_json(),
            'unknown_struct202': self.unknown_struct202.to_json(),
            'unknown_struct203': self.unknown_struct203.to_json(),
            'unknown_struct204': self.unknown_struct204.to_json(),
            'fire_beam_damage': self.fire_beam_damage.to_json(),
            'unknown_struct206': self.unknown_struct206.to_json(),
            'unknown_struct207': self.unknown_struct207.to_json(),
            'gravity': self.gravity,
            'terminal_velocity': self.terminal_velocity,
            'unknown_0x880adc23': self.unknown_0x880adc23,
            'unknown_0x5d1de4ae': self.unknown_0x5d1de4ae,
            'unknown_0x59f65627': self.unknown_0x59f65627,
            'spit_distance': self.spit_distance,
            'spit_height': self.spit_height,
            'unknown_0x1e3cbfc2': self.unknown_0x1e3cbfc2,
            'unknown_0xee382651': self.unknown_0xee382651,
            'unknown_0xc4043234': self.unknown_0xc4043234,
            'caud_0x06b3ef54': self.caud_0x06b3ef54,
            'caud_0xc4dbea19': self.caud_0xc4dbea19,
        }


def _decode_boss_type(data: typing.BinaryIO, property_size: int):
    return enums.BossType.from_stream(data)


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terminal_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x880adc23(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x5d1de4ae(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x59f65627(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1e3cbfc2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xee382651(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc4043234(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_caud_0x06b3ef54(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xc4dbea19(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x92985fff: ('boss_type', _decode_boss_type),
    0x39ce09a: ('unknown_struct202', UnknownStruct202.from_stream),
    0xef3e4da5: ('unknown_struct203', UnknownStruct203.from_stream),
    0x45c4c44c: ('unknown_struct204', UnknownStruct204.from_stream),
    0x9e8f9696: ('fire_beam_damage', DamageInfo.from_stream),
    0xcd9de8cc: ('unknown_struct206', UnknownStruct206.from_stream),
    0x307ce7e4: ('unknown_struct207', UnknownStruct207.from_stream),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xab9566a2: ('terminal_velocity', _decode_terminal_velocity),
    0x880adc23: ('unknown_0x880adc23', _decode_unknown_0x880adc23),
    0x5d1de4ae: ('unknown_0x5d1de4ae', _decode_unknown_0x5d1de4ae),
    0x59f65627: ('unknown_0x59f65627', _decode_unknown_0x59f65627),
    0x4408e47: ('spit_distance', _decode_spit_distance),
    0xa54be635: ('spit_height', _decode_spit_height),
    0x1e3cbfc2: ('unknown_0x1e3cbfc2', _decode_unknown_0x1e3cbfc2),
    0xee382651: ('unknown_0xee382651', _decode_unknown_0xee382651),
    0xc4043234: ('unknown_0xc4043234', _decode_unknown_0xc4043234),
    0x6b3ef54: ('caud_0x06b3ef54', _decode_caud_0x06b3ef54),
    0xc4dbea19: ('caud_0xc4dbea19', _decode_caud_0xc4dbea19),
}

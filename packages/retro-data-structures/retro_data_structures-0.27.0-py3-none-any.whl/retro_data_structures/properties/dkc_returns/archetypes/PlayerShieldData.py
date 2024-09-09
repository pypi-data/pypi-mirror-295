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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerShieldSplineData import PlayerShieldSplineData

if typing.TYPE_CHECKING:
    class PlayerShieldDataJson(typing_extensions.TypedDict):
        num_splines: int
        spline1: json_util.JsonObject
        spline2: json_util.JsonObject
        spline3: json_util.JsonObject
        spline4: json_util.JsonObject
        spline5: json_util.JsonObject
        spline6: json_util.JsonObject
        spline7: json_util.JsonObject
        spline8: json_util.JsonObject
        spline9: json_util.JsonObject
        spline10: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerShieldData(BaseProperty):
    num_splines: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x5a15d127, original_name='NumSplines'
        ),
    })
    spline1: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0xcd420d23, original_name='Spline1', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline2: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0xbba7341e, original_name='Spline2', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline3: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0x20d4deca, original_name='Spline3', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline4: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0x566d4664, original_name='Spline4', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline5: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0xcd1eacb0, original_name='Spline5', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline6: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0xbbfb958d, original_name='Spline6', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline7: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0x20887f59, original_name='Spline7', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline8: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0x5688a4d1, original_name='Spline8', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline9: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0xcdfb4e05, original_name='Spline9', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
        ),
    })
    spline10: PlayerShieldSplineData = dataclasses.field(default_factory=PlayerShieldSplineData, metadata={
        'reflection': FieldReflection[PlayerShieldSplineData](
            PlayerShieldSplineData, id=0xec7b7c4d, original_name='Spline10', from_json=PlayerShieldSplineData.from_json, to_json=PlayerShieldSplineData.to_json
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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5a15d127
        num_splines = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcd420d23
        spline1 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbba7341e
        spline2 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x20d4deca
        spline3 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x566d4664
        spline4 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcd1eacb0
        spline5 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbfb958d
        spline6 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x20887f59
        spline7 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5688a4d1
        spline8 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcdfb4e05
        spline9 = PlayerShieldSplineData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xec7b7c4d
        spline10 = PlayerShieldSplineData.from_stream(data, property_size)
    
        return cls(num_splines, spline1, spline2, spline3, spline4, spline5, spline6, spline7, spline8, spline9, spline10)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b"Z\x15\xd1'")  # 0x5a15d127
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_splines))

        data.write(b'\xcdB\r#')  # 0xcd420d23
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xa74\x1e')  # 0xbba7341e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \xd4\xde\xca')  # 0x20d4deca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'VmFd')  # 0x566d4664
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\x1e\xac\xb0')  # 0xcd1eacb0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xfb\x95\x8d')  # 0xbbfb958d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \x88\x7fY')  # 0x20887f59
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x88\xa4\xd1')  # 0x5688a4d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\xfbN\x05')  # 0xcdfb4e05
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec{|M')  # 0xec7b7c4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline10.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerShieldDataJson", data)
        return cls(
            num_splines=json_data['num_splines'],
            spline1=PlayerShieldSplineData.from_json(json_data['spline1']),
            spline2=PlayerShieldSplineData.from_json(json_data['spline2']),
            spline3=PlayerShieldSplineData.from_json(json_data['spline3']),
            spline4=PlayerShieldSplineData.from_json(json_data['spline4']),
            spline5=PlayerShieldSplineData.from_json(json_data['spline5']),
            spline6=PlayerShieldSplineData.from_json(json_data['spline6']),
            spline7=PlayerShieldSplineData.from_json(json_data['spline7']),
            spline8=PlayerShieldSplineData.from_json(json_data['spline8']),
            spline9=PlayerShieldSplineData.from_json(json_data['spline9']),
            spline10=PlayerShieldSplineData.from_json(json_data['spline10']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'num_splines': self.num_splines,
            'spline1': self.spline1.to_json(),
            'spline2': self.spline2.to_json(),
            'spline3': self.spline3.to_json(),
            'spline4': self.spline4.to_json(),
            'spline5': self.spline5.to_json(),
            'spline6': self.spline6.to_json(),
            'spline7': self.spline7.to_json(),
            'spline8': self.spline8.to_json(),
            'spline9': self.spline9.to_json(),
            'spline10': self.spline10.to_json(),
        }


def _decode_num_splines(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5a15d127: ('num_splines', _decode_num_splines),
    0xcd420d23: ('spline1', PlayerShieldSplineData.from_stream),
    0xbba7341e: ('spline2', PlayerShieldSplineData.from_stream),
    0x20d4deca: ('spline3', PlayerShieldSplineData.from_stream),
    0x566d4664: ('spline4', PlayerShieldSplineData.from_stream),
    0xcd1eacb0: ('spline5', PlayerShieldSplineData.from_stream),
    0xbbfb958d: ('spline6', PlayerShieldSplineData.from_stream),
    0x20887f59: ('spline7', PlayerShieldSplineData.from_stream),
    0x5688a4d1: ('spline8', PlayerShieldSplineData.from_stream),
    0xcdfb4e05: ('spline9', PlayerShieldSplineData.from_stream),
    0xec7b7c4d: ('spline10', PlayerShieldSplineData.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.MoleCartStruct import MoleCartStruct

if typing.TYPE_CHECKING:
    class UnknownStruct229Json(typing_extensions.TypedDict):
        num_sounds: int
        mole_cart_struct_0x5df3f980: json_util.JsonObject
        mole_cart_struct_0x2b16c0bd: json_util.JsonObject
        mole_cart_struct_0xb0652a69: json_util.JsonObject
        mole_cart_struct_0xc6dcb2c7: json_util.JsonObject
        mole_cart_struct_0x5daf5813: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct229(BaseProperty):
    num_sounds: int = dataclasses.field(default=2, metadata={
        'reflection': FieldReflection[int](
            int, id=0xc686af51, original_name='NumSounds'
        ),
    })
    mole_cart_struct_0x5df3f980: MoleCartStruct = dataclasses.field(default_factory=MoleCartStruct, metadata={
        'reflection': FieldReflection[MoleCartStruct](
            MoleCartStruct, id=0x5df3f980, original_name='MoleCartStruct', from_json=MoleCartStruct.from_json, to_json=MoleCartStruct.to_json
        ),
    })
    mole_cart_struct_0x2b16c0bd: MoleCartStruct = dataclasses.field(default_factory=MoleCartStruct, metadata={
        'reflection': FieldReflection[MoleCartStruct](
            MoleCartStruct, id=0x2b16c0bd, original_name='MoleCartStruct', from_json=MoleCartStruct.from_json, to_json=MoleCartStruct.to_json
        ),
    })
    mole_cart_struct_0xb0652a69: MoleCartStruct = dataclasses.field(default_factory=MoleCartStruct, metadata={
        'reflection': FieldReflection[MoleCartStruct](
            MoleCartStruct, id=0xb0652a69, original_name='MoleCartStruct', from_json=MoleCartStruct.from_json, to_json=MoleCartStruct.to_json
        ),
    })
    mole_cart_struct_0xc6dcb2c7: MoleCartStruct = dataclasses.field(default_factory=MoleCartStruct, metadata={
        'reflection': FieldReflection[MoleCartStruct](
            MoleCartStruct, id=0xc6dcb2c7, original_name='MoleCartStruct', from_json=MoleCartStruct.from_json, to_json=MoleCartStruct.to_json
        ),
    })
    mole_cart_struct_0x5daf5813: MoleCartStruct = dataclasses.field(default_factory=MoleCartStruct, metadata={
        'reflection': FieldReflection[MoleCartStruct](
            MoleCartStruct, id=0x5daf5813, original_name='MoleCartStruct', from_json=MoleCartStruct.from_json, to_json=MoleCartStruct.to_json
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
        if property_count != 6:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc686af51
        num_sounds = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5df3f980
        mole_cart_struct_0x5df3f980 = MoleCartStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2b16c0bd
        mole_cart_struct_0x2b16c0bd = MoleCartStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0652a69
        mole_cart_struct_0xb0652a69 = MoleCartStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc6dcb2c7
        mole_cart_struct_0xc6dcb2c7 = MoleCartStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5daf5813
        mole_cart_struct_0x5daf5813 = MoleCartStruct.from_stream(data, property_size)
    
        return cls(num_sounds, mole_cart_struct_0x5df3f980, mole_cart_struct_0x2b16c0bd, mole_cart_struct_0xb0652a69, mole_cart_struct_0xc6dcb2c7, mole_cart_struct_0x5daf5813)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xc6\x86\xafQ')  # 0xc686af51
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_sounds))

        data.write(b']\xf3\xf9\x80')  # 0x5df3f980
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_cart_struct_0x5df3f980.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+\x16\xc0\xbd')  # 0x2b16c0bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_cart_struct_0x2b16c0bd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0e*i')  # 0xb0652a69
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_cart_struct_0xb0652a69.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xdc\xb2\xc7')  # 0xc6dcb2c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_cart_struct_0xc6dcb2c7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\xafX\x13')  # 0x5daf5813
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mole_cart_struct_0x5daf5813.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct229Json", data)
        return cls(
            num_sounds=json_data['num_sounds'],
            mole_cart_struct_0x5df3f980=MoleCartStruct.from_json(json_data['mole_cart_struct_0x5df3f980']),
            mole_cart_struct_0x2b16c0bd=MoleCartStruct.from_json(json_data['mole_cart_struct_0x2b16c0bd']),
            mole_cart_struct_0xb0652a69=MoleCartStruct.from_json(json_data['mole_cart_struct_0xb0652a69']),
            mole_cart_struct_0xc6dcb2c7=MoleCartStruct.from_json(json_data['mole_cart_struct_0xc6dcb2c7']),
            mole_cart_struct_0x5daf5813=MoleCartStruct.from_json(json_data['mole_cart_struct_0x5daf5813']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'num_sounds': self.num_sounds,
            'mole_cart_struct_0x5df3f980': self.mole_cart_struct_0x5df3f980.to_json(),
            'mole_cart_struct_0x2b16c0bd': self.mole_cart_struct_0x2b16c0bd.to_json(),
            'mole_cart_struct_0xb0652a69': self.mole_cart_struct_0xb0652a69.to_json(),
            'mole_cart_struct_0xc6dcb2c7': self.mole_cart_struct_0xc6dcb2c7.to_json(),
            'mole_cart_struct_0x5daf5813': self.mole_cart_struct_0x5daf5813.to_json(),
        }


def _decode_num_sounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc686af51: ('num_sounds', _decode_num_sounds),
    0x5df3f980: ('mole_cart_struct_0x5df3f980', MoleCartStruct.from_stream),
    0x2b16c0bd: ('mole_cart_struct_0x2b16c0bd', MoleCartStruct.from_stream),
    0xb0652a69: ('mole_cart_struct_0xb0652a69', MoleCartStruct.from_stream),
    0xc6dcb2c7: ('mole_cart_struct_0xc6dcb2c7', MoleCartStruct.from_stream),
    0x5daf5813: ('mole_cart_struct_0x5daf5813', MoleCartStruct.from_stream),
}

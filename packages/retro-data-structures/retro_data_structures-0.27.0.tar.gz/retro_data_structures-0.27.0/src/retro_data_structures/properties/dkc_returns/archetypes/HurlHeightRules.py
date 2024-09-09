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

if typing.TYPE_CHECKING:
    class HurlHeightRulesJson(typing_extensions.TypedDict):
        number_of_hurl_heights: int
        hurl_height1: float
        hurl_height2: float
        hurl_height3: float
        hurl_height4: float
        hurl_height5: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x2187c17e, 0x3d2ea760, 0xbbbad5ce, 0x70e6066b, 0x6de336d3, 0xa6bfe576)


@dataclasses.dataclass()
class HurlHeightRules(BaseProperty):
    number_of_hurl_heights: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x2187c17e, original_name='NumberOfHurlHeights'
        ),
    })
    hurl_height1: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3d2ea760, original_name='HurlHeight1'
        ),
    })
    hurl_height2: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbbbad5ce, original_name='HurlHeight2'
        ),
    })
    hurl_height3: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x70e6066b, original_name='HurlHeight3'
        ),
    })
    hurl_height4: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6de336d3, original_name='HurlHeight4'
        ),
    })
    hurl_height5: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa6bfe576, original_name='HurlHeight5'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(60))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'!\x87\xc1~')  # 0x2187c17e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_hurl_heights))

        data.write(b'=.\xa7`')  # 0x3d2ea760
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height1))

        data.write(b'\xbb\xba\xd5\xce')  # 0xbbbad5ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height2))

        data.write(b'p\xe6\x06k')  # 0x70e6066b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height3))

        data.write(b'm\xe36\xd3')  # 0x6de336d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height4))

        data.write(b'\xa6\xbf\xe5v')  # 0xa6bfe576
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height5))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("HurlHeightRulesJson", data)
        return cls(
            number_of_hurl_heights=json_data['number_of_hurl_heights'],
            hurl_height1=json_data['hurl_height1'],
            hurl_height2=json_data['hurl_height2'],
            hurl_height3=json_data['hurl_height3'],
            hurl_height4=json_data['hurl_height4'],
            hurl_height5=json_data['hurl_height5'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_hurl_heights': self.number_of_hurl_heights,
            'hurl_height1': self.hurl_height1,
            'hurl_height2': self.hurl_height2,
            'hurl_height3': self.hurl_height3,
            'hurl_height4': self.hurl_height4,
            'hurl_height5': self.hurl_height5,
        }


def _decode_number_of_hurl_heights(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hurl_height1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2187c17e: ('number_of_hurl_heights', _decode_number_of_hurl_heights),
    0x3d2ea760: ('hurl_height1', _decode_hurl_height1),
    0xbbbad5ce: ('hurl_height2', _decode_hurl_height2),
    0x70e6066b: ('hurl_height3', _decode_hurl_height3),
    0x6de336d3: ('hurl_height4', _decode_hurl_height4),
    0xa6bfe576: ('hurl_height5', _decode_hurl_height5),
}

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

if typing.TYPE_CHECKING:
    class TidalWaveDataJson(typing_extensions.TypedDict):
        adjust_each_frame: bool
        offset_using: int
        offset_plane: int
        offset_u_coord: bool
        offset_v_coord: bool
        scale_using: int
        scale_plane: int
        scale_u_coord: bool
        scale_v_coord: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xb4783f01, 0xd381e63e, 0x75a29df1, 0xccb532db, 0x278289d8, 0x2ac21a04, 0x8ce161cb, 0xa40a895, 0xe1771396)


@dataclasses.dataclass()
class TidalWaveData(BaseProperty):
    adjust_each_frame: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xb4783f01, original_name='AdjustEachFrame'
        ),
    })
    offset_using: enums.OffsetUsing = dataclasses.field(default=enums.OffsetUsing.Unknown1, metadata={
        'reflection': FieldReflection[enums.OffsetUsing](
            enums.OffsetUsing, id=0xd381e63e, original_name='OffsetUsing', from_json=enums.OffsetUsing.from_json, to_json=enums.OffsetUsing.to_json
        ),
    })
    offset_plane: enums.OffsetPlane = dataclasses.field(default=enums.OffsetPlane.Unknown1, metadata={
        'reflection': FieldReflection[enums.OffsetPlane](
            enums.OffsetPlane, id=0x75a29df1, original_name='OffsetPlane', from_json=enums.OffsetPlane.from_json, to_json=enums.OffsetPlane.to_json
        ),
    })
    offset_u_coord: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xccb532db, original_name='OffsetUCoord'
        ),
    })
    offset_v_coord: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x278289d8, original_name='OffsetVCoord'
        ),
    })
    scale_using: enums.ScaleUsing = dataclasses.field(default=enums.ScaleUsing.Unknown1, metadata={
        'reflection': FieldReflection[enums.ScaleUsing](
            enums.ScaleUsing, id=0x2ac21a04, original_name='ScaleUsing', from_json=enums.ScaleUsing.from_json, to_json=enums.ScaleUsing.to_json
        ),
    })
    scale_plane: enums.ScalePlane = dataclasses.field(default=enums.ScalePlane.Unknown1, metadata={
        'reflection': FieldReflection[enums.ScalePlane](
            enums.ScalePlane, id=0x8ce161cb, original_name='ScalePlane', from_json=enums.ScalePlane.from_json, to_json=enums.ScalePlane.to_json
        ),
    })
    scale_u_coord: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0a40a895, original_name='ScaleUCoord'
        ),
    })
    scale_v_coord: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe1771396, original_name='ScaleVCoord'
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
        if property_count != 9:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LHLLHLLH?LH?LHLLHLLH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(75))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) == _FAST_IDS
        return cls(
            dec[2],
            enums.OffsetUsing(dec[5]),
            enums.OffsetPlane(dec[8]),
            dec[11],
            dec[14],
            enums.ScaleUsing(dec[17]),
            enums.ScalePlane(dec[20]),
            dec[23],
            dec[26],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xb4x?\x01')  # 0xb4783f01
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.adjust_each_frame))

        data.write(b'\xd3\x81\xe6>')  # 0xd381e63e
        data.write(b'\x00\x04')  # size
        self.offset_using.to_stream(data)

        data.write(b'u\xa2\x9d\xf1')  # 0x75a29df1
        data.write(b'\x00\x04')  # size
        self.offset_plane.to_stream(data)

        data.write(b'\xcc\xb52\xdb')  # 0xccb532db
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.offset_u_coord))

        data.write(b"'\x82\x89\xd8")  # 0x278289d8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.offset_v_coord))

        data.write(b'*\xc2\x1a\x04')  # 0x2ac21a04
        data.write(b'\x00\x04')  # size
        self.scale_using.to_stream(data)

        data.write(b'\x8c\xe1a\xcb')  # 0x8ce161cb
        data.write(b'\x00\x04')  # size
        self.scale_plane.to_stream(data)

        data.write(b'\n@\xa8\x95')  # 0xa40a895
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scale_u_coord))

        data.write(b'\xe1w\x13\x96')  # 0xe1771396
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scale_v_coord))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TidalWaveDataJson", data)
        return cls(
            adjust_each_frame=json_data['adjust_each_frame'],
            offset_using=enums.OffsetUsing.from_json(json_data['offset_using']),
            offset_plane=enums.OffsetPlane.from_json(json_data['offset_plane']),
            offset_u_coord=json_data['offset_u_coord'],
            offset_v_coord=json_data['offset_v_coord'],
            scale_using=enums.ScaleUsing.from_json(json_data['scale_using']),
            scale_plane=enums.ScalePlane.from_json(json_data['scale_plane']),
            scale_u_coord=json_data['scale_u_coord'],
            scale_v_coord=json_data['scale_v_coord'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'adjust_each_frame': self.adjust_each_frame,
            'offset_using': self.offset_using.to_json(),
            'offset_plane': self.offset_plane.to_json(),
            'offset_u_coord': self.offset_u_coord,
            'offset_v_coord': self.offset_v_coord,
            'scale_using': self.scale_using.to_json(),
            'scale_plane': self.scale_plane.to_json(),
            'scale_u_coord': self.scale_u_coord,
            'scale_v_coord': self.scale_v_coord,
        }


def _decode_adjust_each_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offset_using(data: typing.BinaryIO, property_size: int):
    return enums.OffsetUsing.from_stream(data)


def _decode_offset_plane(data: typing.BinaryIO, property_size: int):
    return enums.OffsetPlane.from_stream(data)


def _decode_offset_u_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offset_v_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_using(data: typing.BinaryIO, property_size: int):
    return enums.ScaleUsing.from_stream(data)


def _decode_scale_plane(data: typing.BinaryIO, property_size: int):
    return enums.ScalePlane.from_stream(data)


def _decode_scale_u_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_scale_v_coord(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb4783f01: ('adjust_each_frame', _decode_adjust_each_frame),
    0xd381e63e: ('offset_using', _decode_offset_using),
    0x75a29df1: ('offset_plane', _decode_offset_plane),
    0xccb532db: ('offset_u_coord', _decode_offset_u_coord),
    0x278289d8: ('offset_v_coord', _decode_offset_v_coord),
    0x2ac21a04: ('scale_using', _decode_scale_using),
    0x8ce161cb: ('scale_plane', _decode_scale_plane),
    0xa40a895: ('scale_u_coord', _decode_scale_u_coord),
    0xe1771396: ('scale_v_coord', _decode_scale_v_coord),
}

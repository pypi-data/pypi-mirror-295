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
    class CameraTrackingJson(typing_extensions.TypedDict):
        tracking_type: int
        tracking_axis: int
        update_line_of_sight: bool
        use_bounds_for_non_players: bool
        ignore_players_in_bounds: bool
        attack_bounce_considered_on_ground: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x5bfed7db, 0x2abd251, 0xbbb489d0, 0x7ebdd66c, 0x8fa9689c, 0xe265ed56)


@dataclasses.dataclass()
class CameraTracking(BaseProperty):
    tracking_type: enums.TrackingType = dataclasses.field(default=enums.TrackingType.Unknown2, metadata={
        'reflection': FieldReflection[enums.TrackingType](
            enums.TrackingType, id=0x5bfed7db, original_name='TrackingType', from_json=enums.TrackingType.from_json, to_json=enums.TrackingType.to_json
        ),
    })
    tracking_axis: enums.TrackingAxis = dataclasses.field(default=enums.TrackingAxis.Unknown1, metadata={
        'reflection': FieldReflection[enums.TrackingAxis](
            enums.TrackingAxis, id=0x02abd251, original_name='TrackingAxis', from_json=enums.TrackingAxis.from_json, to_json=enums.TrackingAxis.to_json
        ),
    })
    update_line_of_sight: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbbb489d0, original_name='UpdateLineOfSight'
        ),
    })
    use_bounds_for_non_players: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7ebdd66c, original_name='UseBoundsForNonPlayers'
        ),
    })
    ignore_players_in_bounds: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8fa9689c, original_name='IgnorePlayersInBounds'
        ),
    })
    attack_bounce_considered_on_ground: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe265ed56, original_name='AttackBounceConsideredOnGround'
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
            _FAST_FORMAT = struct.Struct('>LHLLHLLH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(48))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) == _FAST_IDS
        return cls(
            enums.TrackingType(dec[2]),
            enums.TrackingAxis(dec[5]),
            dec[8],
            dec[11],
            dec[14],
            dec[17],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'[\xfe\xd7\xdb')  # 0x5bfed7db
        data.write(b'\x00\x04')  # size
        self.tracking_type.to_stream(data)

        data.write(b'\x02\xab\xd2Q')  # 0x2abd251
        data.write(b'\x00\x04')  # size
        self.tracking_axis.to_stream(data)

        data.write(b'\xbb\xb4\x89\xd0')  # 0xbbb489d0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.update_line_of_sight))

        data.write(b'~\xbd\xd6l')  # 0x7ebdd66c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_bounds_for_non_players))

        data.write(b'\x8f\xa9h\x9c')  # 0x8fa9689c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_players_in_bounds))

        data.write(b'\xe2e\xedV')  # 0xe265ed56
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.attack_bounce_considered_on_ground))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CameraTrackingJson", data)
        return cls(
            tracking_type=enums.TrackingType.from_json(json_data['tracking_type']),
            tracking_axis=enums.TrackingAxis.from_json(json_data['tracking_axis']),
            update_line_of_sight=json_data['update_line_of_sight'],
            use_bounds_for_non_players=json_data['use_bounds_for_non_players'],
            ignore_players_in_bounds=json_data['ignore_players_in_bounds'],
            attack_bounce_considered_on_ground=json_data['attack_bounce_considered_on_ground'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'tracking_type': self.tracking_type.to_json(),
            'tracking_axis': self.tracking_axis.to_json(),
            'update_line_of_sight': self.update_line_of_sight,
            'use_bounds_for_non_players': self.use_bounds_for_non_players,
            'ignore_players_in_bounds': self.ignore_players_in_bounds,
            'attack_bounce_considered_on_ground': self.attack_bounce_considered_on_ground,
        }


def _decode_tracking_type(data: typing.BinaryIO, property_size: int):
    return enums.TrackingType.from_stream(data)


def _decode_tracking_axis(data: typing.BinaryIO, property_size: int):
    return enums.TrackingAxis.from_stream(data)


def _decode_update_line_of_sight(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_bounds_for_non_players(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_players_in_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_attack_bounce_considered_on_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5bfed7db: ('tracking_type', _decode_tracking_type),
    0x2abd251: ('tracking_axis', _decode_tracking_axis),
    0xbbb489d0: ('update_line_of_sight', _decode_update_line_of_sight),
    0x7ebdd66c: ('use_bounds_for_non_players', _decode_use_bounds_for_non_players),
    0x8fa9689c: ('ignore_players_in_bounds', _decode_ignore_players_in_bounds),
    0xe265ed56: ('attack_bounce_considered_on_ground', _decode_attack_bounce_considered_on_ground),
}

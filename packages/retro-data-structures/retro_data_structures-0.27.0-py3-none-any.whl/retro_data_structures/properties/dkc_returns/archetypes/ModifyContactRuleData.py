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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class ModifyContactRuleDataJson(typing_extensions.TypedDict):
        number_of_alternate_rules: int
        contact_rules_alternate1: int
        contact_rules_alternate2: int
        contact_rules_alternate3: int
        contact_rules_alternate4: int
        contact_rules_alternate5: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xefa6fc75, 0x7992d8a1, 0xff06aa0f, 0x345a79aa, 0x295f4912, 0xe2039ab7)


@dataclasses.dataclass()
class ModifyContactRuleData(BaseProperty):
    number_of_alternate_rules: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xefa6fc75, original_name='NumberOfAlternateRules'
        ),
    })
    contact_rules_alternate1: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7992d8a1, original_name='ContactRulesAlternate1'
        ),
    })
    contact_rules_alternate2: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xff06aa0f, original_name='ContactRulesAlternate2'
        ),
    })
    contact_rules_alternate3: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x345a79aa, original_name='ContactRulesAlternate3'
        ),
    })
    contact_rules_alternate4: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x295f4912, original_name='ContactRulesAlternate4'
        ),
    })
    contact_rules_alternate5: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe2039ab7, original_name='ContactRulesAlternate5'
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
            _FAST_FORMAT = struct.Struct('>LHlLHQLHQLHQLHQLHQ')
    
        dec = _FAST_FORMAT.unpack(data.read(80))
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

        data.write(b'\xef\xa6\xfcu')  # 0xefa6fc75
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_alternate_rules))

        data.write(b'y\x92\xd8\xa1')  # 0x7992d8a1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules_alternate1))

        data.write(b'\xff\x06\xaa\x0f')  # 0xff06aa0f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules_alternate2))

        data.write(b'4Zy\xaa')  # 0x345a79aa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules_alternate3))

        data.write(b')_I\x12')  # 0x295f4912
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules_alternate4))

        data.write(b'\xe2\x03\x9a\xb7')  # 0xe2039ab7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules_alternate5))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ModifyContactRuleDataJson", data)
        return cls(
            number_of_alternate_rules=json_data['number_of_alternate_rules'],
            contact_rules_alternate1=json_data['contact_rules_alternate1'],
            contact_rules_alternate2=json_data['contact_rules_alternate2'],
            contact_rules_alternate3=json_data['contact_rules_alternate3'],
            contact_rules_alternate4=json_data['contact_rules_alternate4'],
            contact_rules_alternate5=json_data['contact_rules_alternate5'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'number_of_alternate_rules': self.number_of_alternate_rules,
            'contact_rules_alternate1': self.contact_rules_alternate1,
            'contact_rules_alternate2': self.contact_rules_alternate2,
            'contact_rules_alternate3': self.contact_rules_alternate3,
            'contact_rules_alternate4': self.contact_rules_alternate4,
            'contact_rules_alternate5': self.contact_rules_alternate5,
        }


def _decode_number_of_alternate_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_contact_rules_alternate1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_contact_rules_alternate2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_contact_rules_alternate3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_contact_rules_alternate4(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_contact_rules_alternate5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xefa6fc75: ('number_of_alternate_rules', _decode_number_of_alternate_rules),
    0x7992d8a1: ('contact_rules_alternate1', _decode_contact_rules_alternate1),
    0xff06aa0f: ('contact_rules_alternate2', _decode_contact_rules_alternate2),
    0x345a79aa: ('contact_rules_alternate3', _decode_contact_rules_alternate3),
    0x295f4912: ('contact_rules_alternate4', _decode_contact_rules_alternate4),
    0xe2039ab7: ('contact_rules_alternate5', _decode_contact_rules_alternate5),
}

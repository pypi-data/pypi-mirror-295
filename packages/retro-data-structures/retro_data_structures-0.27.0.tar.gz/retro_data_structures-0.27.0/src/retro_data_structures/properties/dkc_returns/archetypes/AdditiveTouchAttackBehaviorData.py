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
from retro_data_structures.properties.dkc_returns.archetypes.TouchAttackDirectionEnum import TouchAttackDirectionEnum

if typing.TYPE_CHECKING:
    class AdditiveTouchAttackBehaviorDataJson(typing_extensions.TypedDict):
        contact_top: json_util.JsonObject
        contact_bottom: json_util.JsonObject
        contact_front: json_util.JsonObject
        contact_back: json_util.JsonObject
    

@dataclasses.dataclass()
class AdditiveTouchAttackBehaviorData(BaseProperty):
    contact_top: TouchAttackDirectionEnum = dataclasses.field(default_factory=TouchAttackDirectionEnum, metadata={
        'reflection': FieldReflection[TouchAttackDirectionEnum](
            TouchAttackDirectionEnum, id=0xff0a98a3, original_name='ContactTop', from_json=TouchAttackDirectionEnum.from_json, to_json=TouchAttackDirectionEnum.to_json
        ),
    })
    contact_bottom: TouchAttackDirectionEnum = dataclasses.field(default_factory=TouchAttackDirectionEnum, metadata={
        'reflection': FieldReflection[TouchAttackDirectionEnum](
            TouchAttackDirectionEnum, id=0x0a62c650, original_name='ContactBottom', from_json=TouchAttackDirectionEnum.from_json, to_json=TouchAttackDirectionEnum.to_json
        ),
    })
    contact_front: TouchAttackDirectionEnum = dataclasses.field(default_factory=TouchAttackDirectionEnum, metadata={
        'reflection': FieldReflection[TouchAttackDirectionEnum](
            TouchAttackDirectionEnum, id=0x954e50d4, original_name='ContactFront', from_json=TouchAttackDirectionEnum.from_json, to_json=TouchAttackDirectionEnum.to_json
        ),
    })
    contact_back: TouchAttackDirectionEnum = dataclasses.field(default_factory=TouchAttackDirectionEnum, metadata={
        'reflection': FieldReflection[TouchAttackDirectionEnum](
            TouchAttackDirectionEnum, id=0x229d79fe, original_name='ContactBack', from_json=TouchAttackDirectionEnum.from_json, to_json=TouchAttackDirectionEnum.to_json
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
        if property_count != 4:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xff0a98a3
        contact_top = TouchAttackDirectionEnum.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0a62c650
        contact_bottom = TouchAttackDirectionEnum.from_stream(data, property_size, default_override={'attack_direction': enums.AttackDirection.Unknown2})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x954e50d4
        contact_front = TouchAttackDirectionEnum.from_stream(data, property_size, default_override={'attack_direction': enums.AttackDirection.Unknown5})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x229d79fe
        contact_back = TouchAttackDirectionEnum.from_stream(data, property_size, default_override={'attack_direction': enums.AttackDirection.Unknown6})
    
        return cls(contact_top, contact_bottom, contact_front, contact_back)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xff\n\x98\xa3')  # 0xff0a98a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_top.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\nb\xc6P')  # 0xa62c650
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_bottom.to_stream(data, default_override={'attack_direction': enums.AttackDirection.Unknown2})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95NP\xd4')  # 0x954e50d4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_front.to_stream(data, default_override={'attack_direction': enums.AttackDirection.Unknown5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'"\x9dy\xfe')  # 0x229d79fe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_back.to_stream(data, default_override={'attack_direction': enums.AttackDirection.Unknown6})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("AdditiveTouchAttackBehaviorDataJson", data)
        return cls(
            contact_top=TouchAttackDirectionEnum.from_json(json_data['contact_top']),
            contact_bottom=TouchAttackDirectionEnum.from_json(json_data['contact_bottom']),
            contact_front=TouchAttackDirectionEnum.from_json(json_data['contact_front']),
            contact_back=TouchAttackDirectionEnum.from_json(json_data['contact_back']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'contact_top': self.contact_top.to_json(),
            'contact_bottom': self.contact_bottom.to_json(),
            'contact_front': self.contact_front.to_json(),
            'contact_back': self.contact_back.to_json(),
        }


def _decode_contact_bottom(data: typing.BinaryIO, property_size: int):
    return TouchAttackDirectionEnum.from_stream(data, property_size, default_override={'attack_direction': enums.AttackDirection.Unknown2})


def _decode_contact_front(data: typing.BinaryIO, property_size: int):
    return TouchAttackDirectionEnum.from_stream(data, property_size, default_override={'attack_direction': enums.AttackDirection.Unknown5})


def _decode_contact_back(data: typing.BinaryIO, property_size: int):
    return TouchAttackDirectionEnum.from_stream(data, property_size, default_override={'attack_direction': enums.AttackDirection.Unknown6})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xff0a98a3: ('contact_top', TouchAttackDirectionEnum.from_stream),
    0xa62c650: ('contact_bottom', _decode_contact_bottom),
    0x954e50d4: ('contact_front', _decode_contact_front),
    0x229d79fe: ('contact_back', _decode_contact_back),
}

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
import retro_data_structures.enums.echoes as enums
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.Vector import Vector

if typing.TYPE_CHECKING:
    from retro_data_structures.asset_manager import AssetManager
    from retro_data_structures.base_resource import Dependency

    class TriggerInfoJson(typing_extensions.TypedDict):
        damage: json_util.JsonObject
        force_field: json_util.JsonValue
        flags_trigger: int
    

@dataclasses.dataclass()
class TriggerInfo(BaseProperty):
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0x337f9524, original_name='Damage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    force_field: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x20927e9b, original_name='ForceField', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    flags_trigger: enums.FlagsTrigger = dataclasses.field(default=enums.FlagsTrigger(30726), metadata={
        'reflection': FieldReflection[enums.FlagsTrigger](
            enums.FlagsTrigger, id=0x82859f46, original_name='FlagsTrigger', from_json=enums.FlagsTrigger.from_json, to_json=enums.FlagsTrigger.to_json
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        if property_count != 3:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x337f9524
        damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x20927e9b
        force_field = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82859f46
        flags_trigger = enums.FlagsTrigger.from_stream(data)
    
        return cls(damage, force_field, flags_trigger)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \x92~\x9b')  # 0x20927e9b
        data.write(b'\x00\x0c')  # size
        self.force_field.to_stream(data)

        data.write(b'\x82\x85\x9fF')  # 0x82859f46
        data.write(b'\x00\x04')  # size
        self.flags_trigger.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TriggerInfoJson", data)
        return cls(
            damage=DamageInfo.from_json(json_data['damage']),
            force_field=Vector.from_json(json_data['force_field']),
            flags_trigger=enums.FlagsTrigger.from_json(json_data['flags_trigger']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'damage': self.damage.to_json(),
            'force_field': self.force_field.to_json(),
            'flags_trigger': self.flags_trigger.to_json(),
        }

    def dependencies_for(self, asset_manager: AssetManager) -> typing.Iterator[Dependency]:
        for method, field_name, field_type in [
            (self.damage.dependencies_for, "damage", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TriggerInfo.{field_name} ({field_type}): {e}"
                )


def _decode_force_field(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_flags_trigger(data: typing.BinaryIO, property_size: int):
    return enums.FlagsTrigger.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x337f9524: ('damage', DamageInfo.from_stream),
    0x20927e9b: ('force_field', _decode_force_field),
    0x82859f46: ('flags_trigger', _decode_flags_trigger),
}

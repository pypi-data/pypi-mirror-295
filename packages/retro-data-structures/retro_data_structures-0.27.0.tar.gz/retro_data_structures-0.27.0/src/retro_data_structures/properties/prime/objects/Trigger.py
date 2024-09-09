# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.field_reflection import FieldReflection
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.core.Vector import Vector

if typing.TYPE_CHECKING:
    from retro_data_structures.asset_manager import AssetManager
    from retro_data_structures.base_resource import Dependency

    class TriggerJson(typing_extensions.TypedDict):
        name: str
        position: json_util.JsonValue
        scale: json_util.JsonValue
        unnamed: json_util.JsonObject
        force: json_util.JsonValue
        trigger_flags: int
        active: bool
        deactivate_on_entered: bool
        deactivate_on_exited: bool
    

@dataclasses.dataclass()
class Trigger(BaseObjectType):
    name: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x00000000, original_name='Name'
        ),
    })
    position: Vector = dataclasses.field(default_factory=Vector, metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x00000001, original_name='Position', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    scale: Vector = dataclasses.field(default_factory=Vector, metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x00000002, original_name='Scale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unnamed: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0x00000003, original_name=None, from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    force: Vector = dataclasses.field(default_factory=Vector, metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x00000004, original_name='Force', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    trigger_flags: enums.TriggerFlags = dataclasses.field(default=enums.TriggerFlags(0), metadata={
        'reflection': FieldReflection[enums.TriggerFlags](
            enums.TriggerFlags, id=0x00000005, original_name='Trigger Flags', from_json=enums.TriggerFlags.from_json, to_json=enums.TriggerFlags.to_json
        ),
    })
    active: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x00000006, original_name='Active'
        ),
    })
    deactivate_on_entered: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x00000007, original_name='Deactivate On Entered'
        ),
    })
    deactivate_on_exited: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x00000008, original_name='Deactivate On Exited'
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> str | None:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x4

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed = DamageInfo.from_stream(data, property_size)
        force = Vector.from_stream(data)
        trigger_flags = enums.TriggerFlags.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        deactivate_on_entered = struct.unpack('>?', data.read(1))[0]
        deactivate_on_exited = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, scale, unnamed, force, trigger_flags, active, deactivate_on_entered, deactivate_on_exited)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\t')  # 9 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed.to_stream(data)
        self.force.to_stream(data)
        self.trigger_flags.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>?', self.deactivate_on_entered))
        data.write(struct.pack('>?', self.deactivate_on_exited))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TriggerJson", data)
        return cls(
            name=json_data['name'],
            position=Vector.from_json(json_data['position']),
            scale=Vector.from_json(json_data['scale']),
            unnamed=DamageInfo.from_json(json_data['unnamed']),
            force=Vector.from_json(json_data['force']),
            trigger_flags=enums.TriggerFlags.from_json(json_data['trigger_flags']),
            active=json_data['active'],
            deactivate_on_entered=json_data['deactivate_on_entered'],
            deactivate_on_exited=json_data['deactivate_on_exited'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'unnamed': self.unnamed.to_json(),
            'force': self.force.to_json(),
            'trigger_flags': self.trigger_flags.to_json(),
            'active': self.active,
            'deactivate_on_entered': self.deactivate_on_entered,
            'deactivate_on_exited': self.deactivate_on_exited,
        }

    def dependencies_for(self, asset_manager: AssetManager) -> typing.Iterator[Dependency]:
        for method, field_name, field_type in [
            (self.unnamed.dependencies_for, "unnamed", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Trigger.{field_name} ({field_type}): {e}"
                )

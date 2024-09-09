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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.dkc_returns.archetypes.TriggerInfo import TriggerInfo

if typing.TYPE_CHECKING:
    class DamageableTriggerOrientatedJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        health: json_util.JsonObject
        vulnerability: json_util.JsonObject
        invulnerable: bool
        damage_originator: int
        trigger_properties: json_util.JsonObject
    

@dataclasses.dataclass()
class DamageableTriggerOrientated(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo, metadata={
        'reflection': FieldReflection[HealthInfo](
            HealthInfo, id=0xcf90d15e, original_name='Health', from_json=HealthInfo.from_json, to_json=HealthInfo.to_json
        ),
    })
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability, metadata={
        'reflection': FieldReflection[DamageVulnerability](
            DamageVulnerability, id=0x7b71ae90, original_name='Vulnerability', from_json=DamageVulnerability.from_json, to_json=DamageVulnerability.to_json
        ),
    })
    invulnerable: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6652bdd7, original_name='Invulnerable'
        ),
    })
    damage_originator: enums.DamageableTriggerEnum = dataclasses.field(default=enums.DamageableTriggerEnum.Unknown1, metadata={
        'reflection': FieldReflection[enums.DamageableTriggerEnum](
            enums.DamageableTriggerEnum, id=0x8b9d2123, original_name='DamageOriginator', from_json=enums.DamageableTriggerEnum.from_json, to_json=enums.DamageableTriggerEnum.to_json
        ),
    })
    trigger_properties: TriggerInfo = dataclasses.field(default_factory=TriggerInfo, metadata={
        'reflection': FieldReflection[TriggerInfo](
            TriggerInfo, id=0xbbfee93e, original_name='TriggerProperties', from_json=TriggerInfo.from_json, to_json=TriggerInfo.to_json
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> str | None:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DTRO'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 6:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcf90d15e
        health = HealthInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b71ae90
        vulnerability = DamageVulnerability.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6652bdd7
        invulnerable = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8b9d2123
        damage_originator = enums.DamageableTriggerEnum.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbfee93e
        trigger_properties = TriggerInfo.from_stream(data, property_size)
    
        return cls(editor_properties, health, vulnerability, invulnerable, damage_originator, trigger_properties)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'fR\xbd\xd7')  # 0x6652bdd7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.invulnerable))

        data.write(b'\x8b\x9d!#')  # 0x8b9d2123
        data.write(b'\x00\x04')  # size
        self.damage_originator.to_stream(data)

        data.write(b'\xbb\xfe\xe9>')  # 0xbbfee93e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.trigger_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("DamageableTriggerOrientatedJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            health=HealthInfo.from_json(json_data['health']),
            vulnerability=DamageVulnerability.from_json(json_data['vulnerability']),
            invulnerable=json_data['invulnerable'],
            damage_originator=enums.DamageableTriggerEnum.from_json(json_data['damage_originator']),
            trigger_properties=TriggerInfo.from_json(json_data['trigger_properties']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'invulnerable': self.invulnerable,
            'damage_originator': self.damage_originator.to_json(),
            'trigger_properties': self.trigger_properties.to_json(),
        }


def _decode_invulnerable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damage_originator(data: typing.BinaryIO, property_size: int):
    return enums.DamageableTriggerEnum.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xcf90d15e: ('health', HealthInfo.from_stream),
    0x7b71ae90: ('vulnerability', DamageVulnerability.from_stream),
    0x6652bdd7: ('invulnerable', _decode_invulnerable),
    0x8b9d2123: ('damage_originator', _decode_damage_originator),
    0xbbfee93e: ('trigger_properties', TriggerInfo.from_stream),
}

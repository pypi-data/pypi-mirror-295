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
from retro_data_structures.properties.dkc_returns.archetypes.CharacterGlueData import CharacterGlueData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCrushData import PlayerCrushData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerPeriodicAdditiveAnimationData import PlayerPeriodicAdditiveAnimationData
from retro_data_structures.properties.dkc_returns.archetypes.TandemBeam import TandemBeam
from retro_data_structures.properties.dkc_returns.archetypes.TrackObjectModuleData import TrackObjectModuleData

if typing.TYPE_CHECKING:
    class UnknownStruct140Json(typing_extensions.TypedDict):
        unknown: int
        periodic_additive_animation_data: json_util.JsonObject
        crush_data: json_util.JsonObject
        track_object_module_data: json_util.JsonObject
        character_glue: json_util.JsonObject
        tandem_beam: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct140(BaseProperty):
    unknown: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x94dd8979, original_name='Unknown'
        ),
    })
    periodic_additive_animation_data: PlayerPeriodicAdditiveAnimationData = dataclasses.field(default_factory=PlayerPeriodicAdditiveAnimationData, metadata={
        'reflection': FieldReflection[PlayerPeriodicAdditiveAnimationData](
            PlayerPeriodicAdditiveAnimationData, id=0x975dcef7, original_name='PeriodicAdditiveAnimationData', from_json=PlayerPeriodicAdditiveAnimationData.from_json, to_json=PlayerPeriodicAdditiveAnimationData.to_json
        ),
    })
    crush_data: PlayerCrushData = dataclasses.field(default_factory=PlayerCrushData, metadata={
        'reflection': FieldReflection[PlayerCrushData](
            PlayerCrushData, id=0x8abb25c4, original_name='CrushData', from_json=PlayerCrushData.from_json, to_json=PlayerCrushData.to_json
        ),
    })
    track_object_module_data: TrackObjectModuleData = dataclasses.field(default_factory=TrackObjectModuleData, metadata={
        'reflection': FieldReflection[TrackObjectModuleData](
            TrackObjectModuleData, id=0xf4d39593, original_name='TrackObjectModuleData', from_json=TrackObjectModuleData.from_json, to_json=TrackObjectModuleData.to_json
        ),
    })
    character_glue: CharacterGlueData = dataclasses.field(default_factory=CharacterGlueData, metadata={
        'reflection': FieldReflection[CharacterGlueData](
            CharacterGlueData, id=0x9d9ce325, original_name='CharacterGlue', from_json=CharacterGlueData.from_json, to_json=CharacterGlueData.to_json
        ),
    })
    tandem_beam: TandemBeam = dataclasses.field(default_factory=TandemBeam, metadata={
        'reflection': FieldReflection[TandemBeam](
            TandemBeam, id=0x34a979a6, original_name='TandemBeam', from_json=TandemBeam.from_json, to_json=TandemBeam.to_json
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
        assert property_id == 0x94dd8979
        unknown = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x975dcef7
        periodic_additive_animation_data = PlayerPeriodicAdditiveAnimationData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8abb25c4
        crush_data = PlayerCrushData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf4d39593
        track_object_module_data = TrackObjectModuleData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9d9ce325
        character_glue = CharacterGlueData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x34a979a6
        tandem_beam = TandemBeam.from_stream(data, property_size)
    
        return cls(unknown, periodic_additive_animation_data, crush_data, track_object_module_data, character_glue, tandem_beam)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x94\xdd\x89y')  # 0x94dd8979
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\x97]\xce\xf7')  # 0x975dcef7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.periodic_additive_animation_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8a\xbb%\xc4')  # 0x8abb25c4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.crush_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xd3\x95\x93')  # 0xf4d39593
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.track_object_module_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\x9c\xe3%')  # 0x9d9ce325
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_glue.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'4\xa9y\xa6')  # 0x34a979a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tandem_beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct140Json", data)
        return cls(
            unknown=json_data['unknown'],
            periodic_additive_animation_data=PlayerPeriodicAdditiveAnimationData.from_json(json_data['periodic_additive_animation_data']),
            crush_data=PlayerCrushData.from_json(json_data['crush_data']),
            track_object_module_data=TrackObjectModuleData.from_json(json_data['track_object_module_data']),
            character_glue=CharacterGlueData.from_json(json_data['character_glue']),
            tandem_beam=TandemBeam.from_json(json_data['tandem_beam']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'periodic_additive_animation_data': self.periodic_additive_animation_data.to_json(),
            'crush_data': self.crush_data.to_json(),
            'track_object_module_data': self.track_object_module_data.to_json(),
            'character_glue': self.character_glue.to_json(),
            'tandem_beam': self.tandem_beam.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x94dd8979: ('unknown', _decode_unknown),
    0x975dcef7: ('periodic_additive_animation_data', PlayerPeriodicAdditiveAnimationData.from_stream),
    0x8abb25c4: ('crush_data', PlayerCrushData.from_stream),
    0xf4d39593: ('track_object_module_data', TrackObjectModuleData.from_stream),
    0x9d9ce325: ('character_glue', CharacterGlueData.from_stream),
    0x34a979a6: ('tandem_beam', TandemBeam.from_stream),
}

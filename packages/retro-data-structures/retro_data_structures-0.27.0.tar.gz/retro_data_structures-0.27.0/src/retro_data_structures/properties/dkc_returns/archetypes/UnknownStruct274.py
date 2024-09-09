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
from retro_data_structures.properties.dkc_returns.archetypes.TrainTrackManagerStructA import TrainTrackManagerStructA

if typing.TYPE_CHECKING:
    class UnknownStruct274Json(typing_extensions.TypedDict):
        random_scheme: int
        sequence_count: int
        train_track_manager_struct_a_0xc101f47e: json_util.JsonObject
        train_track_manager_struct_a_0xac870724: json_util.JsonObject
        train_track_manager_struct_a_0x88055612: json_util.JsonObject
        train_track_manager_struct_a_0x778ae190: json_util.JsonObject
        train_track_manager_struct_a_0x5308b0a6: json_util.JsonObject
        train_track_manager_struct_a_0x3e8e43fc: json_util.JsonObject
        train_track_manager_struct_a_0x1a0c12ca: json_util.JsonObject
        train_track_manager_struct_a_0x1ae02ab9: json_util.JsonObject
        train_track_manager_struct_a_0x3e627b8f: json_util.JsonObject
        train_track_manager_struct_a_0x53e488d5: json_util.JsonObject
        train_track_manager_struct_a_0x7766d9e3: json_util.JsonObject
        train_track_manager_struct_a_0x88e96e61: json_util.JsonObject
        train_track_manager_struct_a_0xac6b3f57: json_util.JsonObject
        train_track_manager_struct_a_0xc1edcc0d: json_util.JsonObject
        train_track_manager_struct_a_0xe56f9d3b: json_util.JsonObject
        train_track_manager_struct_a_0xc035bceb: json_util.JsonObject
        train_track_manager_struct_a_0xe4b7eddd: json_util.JsonObject
        train_track_manager_struct_a_0x89311e87: json_util.JsonObject
        train_track_manager_struct_a_0xadb34fb1: json_util.JsonObject
        train_track_manager_struct_a_0x523cf833: json_util.JsonObject
        train_track_manager_struct_a_0x76bea905: json_util.JsonObject
        train_track_manager_struct_a_0x1b385a5f: json_util.JsonObject
        train_track_manager_struct_a_0x3fba0b69: json_util.JsonObject
        train_track_manager_struct_a_0x3f56331a: json_util.JsonObject
        train_track_manager_struct_a_0x1bd4622c: json_util.JsonObject
        train_track_manager_struct_a_0x76529176: json_util.JsonObject
        train_track_manager_struct_a_0x7e0ed299: json_util.JsonObject
        train_track_manager_struct_a_0x5a8c83af: json_util.JsonObject
        train_track_manager_struct_a_0x370a70f5: json_util.JsonObject
        train_track_manager_struct_a_0x138821c3: json_util.JsonObject
        train_track_manager_struct_a_0xec079641: json_util.JsonObject
        train_track_manager_struct_a_0xc885c777: json_util.JsonObject
        train_track_manager_struct_a_0xa503342d: json_util.JsonObject
        train_track_manager_struct_a_0x8181651b: json_util.JsonObject
        train_track_manager_struct_a_0x816d5d68: json_util.JsonObject
        train_track_manager_struct_a_0xa5ef0c5e: json_util.JsonObject
        train_track_manager_struct_a_0xf5ddec80: json_util.JsonObject
        train_track_manager_struct_a_0xd15fbdb6: json_util.JsonObject
        train_track_manager_struct_a_0xbcd94eec: json_util.JsonObject
        train_track_manager_struct_a_0x985b1fda: json_util.JsonObject
        train_track_manager_struct_a_0x67d4a858: json_util.JsonObject
        train_track_manager_struct_a_0x4356f96e: json_util.JsonObject
        train_track_manager_struct_a_0x2ed00a34: json_util.JsonObject
        train_track_manager_struct_a_0x0a525b02: json_util.JsonObject
        train_track_manager_struct_a_0x0abe6371: json_util.JsonObject
        train_track_manager_struct_a_0x2e3c3247: json_util.JsonObject
        train_track_manager_struct_a_0x3a43fb48: json_util.JsonObject
        train_track_manager_struct_a_0x1ec1aa7e: json_util.JsonObject
        train_track_manager_struct_a_0x73475924: json_util.JsonObject
        train_track_manager_struct_a_0x57c50812: json_util.JsonObject
        train_track_manager_struct_a_0xa84abf90: json_util.JsonObject
        train_track_manager_struct_a_0x8cc8eea6: json_util.JsonObject
        train_track_manager_struct_a_0xe14e1dfc: json_util.JsonObject
        train_track_manager_struct_a_0xc5cc4cca: json_util.JsonObject
        train_track_manager_struct_a_0xc52074b9: json_util.JsonObject
        train_track_manager_struct_a_0xe1a2258f: json_util.JsonObject
        train_track_manager_struct_a_0x390a96f3: json_util.JsonObject
        train_track_manager_struct_a_0x1d88c7c5: json_util.JsonObject
        train_track_manager_struct_a_0x700e349f: json_util.JsonObject
        train_track_manager_struct_a_0x548c65a9: json_util.JsonObject
        train_track_manager_struct_a_0xab03d22b: json_util.JsonObject
        train_track_manager_struct_a_0x8f81831d: json_util.JsonObject
        train_track_manager_struct_a_0xe2077047: json_util.JsonObject
        train_track_manager_struct_a_0xc6852171: json_util.JsonObject
        train_track_manager_struct_a_0xc6691902: json_util.JsonObject
        train_track_manager_struct_a_0xe2eb4834: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct274(BaseProperty):
    random_scheme: enums.RandomScheme = dataclasses.field(default=enums.RandomScheme.Unknown2, metadata={
        'reflection': FieldReflection[enums.RandomScheme](
            enums.RandomScheme, id=0xc8fd4813, original_name='RandomScheme', from_json=enums.RandomScheme.from_json, to_json=enums.RandomScheme.to_json
        ),
    })
    sequence_count: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x65eceb7a, original_name='SequenceCount'
        ),
    })
    train_track_manager_struct_a_0xc101f47e: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc101f47e, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xac870724: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xac870724, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x88055612: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x88055612, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x778ae190: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x778ae190, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x5308b0a6: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x5308b0a6, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x3e8e43fc: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x3e8e43fc, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x1a0c12ca: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x1a0c12ca, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x1ae02ab9: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x1ae02ab9, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x3e627b8f: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x3e627b8f, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x53e488d5: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x53e488d5, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x7766d9e3: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x7766d9e3, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x88e96e61: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x88e96e61, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xac6b3f57: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xac6b3f57, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc1edcc0d: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc1edcc0d, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xe56f9d3b: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xe56f9d3b, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc035bceb: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc035bceb, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xe4b7eddd: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xe4b7eddd, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x89311e87: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x89311e87, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xadb34fb1: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xadb34fb1, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x523cf833: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x523cf833, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x76bea905: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x76bea905, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x1b385a5f: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x1b385a5f, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x3fba0b69: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x3fba0b69, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x3f56331a: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x3f56331a, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x1bd4622c: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x1bd4622c, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x76529176: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x76529176, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x7e0ed299: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x7e0ed299, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x5a8c83af: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x5a8c83af, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x370a70f5: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x370a70f5, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x138821c3: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x138821c3, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xec079641: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xec079641, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc885c777: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc885c777, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xa503342d: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xa503342d, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x8181651b: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x8181651b, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x816d5d68: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x816d5d68, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xa5ef0c5e: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xa5ef0c5e, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xf5ddec80: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xf5ddec80, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xd15fbdb6: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xd15fbdb6, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xbcd94eec: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xbcd94eec, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x985b1fda: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x985b1fda, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x67d4a858: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x67d4a858, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x4356f96e: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x4356f96e, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x2ed00a34: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x2ed00a34, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x0a525b02: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x0a525b02, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x0abe6371: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x0abe6371, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x2e3c3247: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x2e3c3247, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x3a43fb48: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x3a43fb48, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x1ec1aa7e: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x1ec1aa7e, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x73475924: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x73475924, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x57c50812: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x57c50812, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xa84abf90: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xa84abf90, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x8cc8eea6: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x8cc8eea6, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xe14e1dfc: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xe14e1dfc, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc5cc4cca: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc5cc4cca, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc52074b9: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc52074b9, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xe1a2258f: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xe1a2258f, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x390a96f3: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x390a96f3, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x1d88c7c5: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x1d88c7c5, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x700e349f: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x700e349f, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x548c65a9: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x548c65a9, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xab03d22b: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xab03d22b, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0x8f81831d: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0x8f81831d, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xe2077047: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xe2077047, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc6852171: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc6852171, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xc6691902: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xc6691902, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
        ),
    })
    train_track_manager_struct_a_0xe2eb4834: TrainTrackManagerStructA = dataclasses.field(default_factory=TrainTrackManagerStructA, metadata={
        'reflection': FieldReflection[TrainTrackManagerStructA](
            TrainTrackManagerStructA, id=0xe2eb4834, original_name='TrainTrackManagerStructA', from_json=TrainTrackManagerStructA.from_json, to_json=TrainTrackManagerStructA.to_json
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
        if property_count != 68:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc8fd4813
        random_scheme = enums.RandomScheme.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x65eceb7a
        sequence_count = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc101f47e
        train_track_manager_struct_a_0xc101f47e = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xac870724
        train_track_manager_struct_a_0xac870724 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x88055612
        train_track_manager_struct_a_0x88055612 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x778ae190
        train_track_manager_struct_a_0x778ae190 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5308b0a6
        train_track_manager_struct_a_0x5308b0a6 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3e8e43fc
        train_track_manager_struct_a_0x3e8e43fc = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1a0c12ca
        train_track_manager_struct_a_0x1a0c12ca = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1ae02ab9
        train_track_manager_struct_a_0x1ae02ab9 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3e627b8f
        train_track_manager_struct_a_0x3e627b8f = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x53e488d5
        train_track_manager_struct_a_0x53e488d5 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7766d9e3
        train_track_manager_struct_a_0x7766d9e3 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x88e96e61
        train_track_manager_struct_a_0x88e96e61 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xac6b3f57
        train_track_manager_struct_a_0xac6b3f57 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc1edcc0d
        train_track_manager_struct_a_0xc1edcc0d = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe56f9d3b
        train_track_manager_struct_a_0xe56f9d3b = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc035bceb
        train_track_manager_struct_a_0xc035bceb = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe4b7eddd
        train_track_manager_struct_a_0xe4b7eddd = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x89311e87
        train_track_manager_struct_a_0x89311e87 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xadb34fb1
        train_track_manager_struct_a_0xadb34fb1 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x523cf833
        train_track_manager_struct_a_0x523cf833 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76bea905
        train_track_manager_struct_a_0x76bea905 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1b385a5f
        train_track_manager_struct_a_0x1b385a5f = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3fba0b69
        train_track_manager_struct_a_0x3fba0b69 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3f56331a
        train_track_manager_struct_a_0x3f56331a = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1bd4622c
        train_track_manager_struct_a_0x1bd4622c = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76529176
        train_track_manager_struct_a_0x76529176 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e0ed299
        train_track_manager_struct_a_0x7e0ed299 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5a8c83af
        train_track_manager_struct_a_0x5a8c83af = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x370a70f5
        train_track_manager_struct_a_0x370a70f5 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x138821c3
        train_track_manager_struct_a_0x138821c3 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xec079641
        train_track_manager_struct_a_0xec079641 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc885c777
        train_track_manager_struct_a_0xc885c777 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa503342d
        train_track_manager_struct_a_0xa503342d = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8181651b
        train_track_manager_struct_a_0x8181651b = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x816d5d68
        train_track_manager_struct_a_0x816d5d68 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa5ef0c5e
        train_track_manager_struct_a_0xa5ef0c5e = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5ddec80
        train_track_manager_struct_a_0xf5ddec80 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd15fbdb6
        train_track_manager_struct_a_0xd15fbdb6 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbcd94eec
        train_track_manager_struct_a_0xbcd94eec = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x985b1fda
        train_track_manager_struct_a_0x985b1fda = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x67d4a858
        train_track_manager_struct_a_0x67d4a858 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4356f96e
        train_track_manager_struct_a_0x4356f96e = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2ed00a34
        train_track_manager_struct_a_0x2ed00a34 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0a525b02
        train_track_manager_struct_a_0x0a525b02 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0abe6371
        train_track_manager_struct_a_0x0abe6371 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e3c3247
        train_track_manager_struct_a_0x2e3c3247 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a43fb48
        train_track_manager_struct_a_0x3a43fb48 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1ec1aa7e
        train_track_manager_struct_a_0x1ec1aa7e = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73475924
        train_track_manager_struct_a_0x73475924 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x57c50812
        train_track_manager_struct_a_0x57c50812 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa84abf90
        train_track_manager_struct_a_0xa84abf90 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8cc8eea6
        train_track_manager_struct_a_0x8cc8eea6 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe14e1dfc
        train_track_manager_struct_a_0xe14e1dfc = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc5cc4cca
        train_track_manager_struct_a_0xc5cc4cca = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc52074b9
        train_track_manager_struct_a_0xc52074b9 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe1a2258f
        train_track_manager_struct_a_0xe1a2258f = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x390a96f3
        train_track_manager_struct_a_0x390a96f3 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1d88c7c5
        train_track_manager_struct_a_0x1d88c7c5 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x700e349f
        train_track_manager_struct_a_0x700e349f = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x548c65a9
        train_track_manager_struct_a_0x548c65a9 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab03d22b
        train_track_manager_struct_a_0xab03d22b = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f81831d
        train_track_manager_struct_a_0x8f81831d = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2077047
        train_track_manager_struct_a_0xe2077047 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc6852171
        train_track_manager_struct_a_0xc6852171 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc6691902
        train_track_manager_struct_a_0xc6691902 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2eb4834
        train_track_manager_struct_a_0xe2eb4834 = TrainTrackManagerStructA.from_stream(data, property_size)
    
        return cls(random_scheme, sequence_count, train_track_manager_struct_a_0xc101f47e, train_track_manager_struct_a_0xac870724, train_track_manager_struct_a_0x88055612, train_track_manager_struct_a_0x778ae190, train_track_manager_struct_a_0x5308b0a6, train_track_manager_struct_a_0x3e8e43fc, train_track_manager_struct_a_0x1a0c12ca, train_track_manager_struct_a_0x1ae02ab9, train_track_manager_struct_a_0x3e627b8f, train_track_manager_struct_a_0x53e488d5, train_track_manager_struct_a_0x7766d9e3, train_track_manager_struct_a_0x88e96e61, train_track_manager_struct_a_0xac6b3f57, train_track_manager_struct_a_0xc1edcc0d, train_track_manager_struct_a_0xe56f9d3b, train_track_manager_struct_a_0xc035bceb, train_track_manager_struct_a_0xe4b7eddd, train_track_manager_struct_a_0x89311e87, train_track_manager_struct_a_0xadb34fb1, train_track_manager_struct_a_0x523cf833, train_track_manager_struct_a_0x76bea905, train_track_manager_struct_a_0x1b385a5f, train_track_manager_struct_a_0x3fba0b69, train_track_manager_struct_a_0x3f56331a, train_track_manager_struct_a_0x1bd4622c, train_track_manager_struct_a_0x76529176, train_track_manager_struct_a_0x7e0ed299, train_track_manager_struct_a_0x5a8c83af, train_track_manager_struct_a_0x370a70f5, train_track_manager_struct_a_0x138821c3, train_track_manager_struct_a_0xec079641, train_track_manager_struct_a_0xc885c777, train_track_manager_struct_a_0xa503342d, train_track_manager_struct_a_0x8181651b, train_track_manager_struct_a_0x816d5d68, train_track_manager_struct_a_0xa5ef0c5e, train_track_manager_struct_a_0xf5ddec80, train_track_manager_struct_a_0xd15fbdb6, train_track_manager_struct_a_0xbcd94eec, train_track_manager_struct_a_0x985b1fda, train_track_manager_struct_a_0x67d4a858, train_track_manager_struct_a_0x4356f96e, train_track_manager_struct_a_0x2ed00a34, train_track_manager_struct_a_0x0a525b02, train_track_manager_struct_a_0x0abe6371, train_track_manager_struct_a_0x2e3c3247, train_track_manager_struct_a_0x3a43fb48, train_track_manager_struct_a_0x1ec1aa7e, train_track_manager_struct_a_0x73475924, train_track_manager_struct_a_0x57c50812, train_track_manager_struct_a_0xa84abf90, train_track_manager_struct_a_0x8cc8eea6, train_track_manager_struct_a_0xe14e1dfc, train_track_manager_struct_a_0xc5cc4cca, train_track_manager_struct_a_0xc52074b9, train_track_manager_struct_a_0xe1a2258f, train_track_manager_struct_a_0x390a96f3, train_track_manager_struct_a_0x1d88c7c5, train_track_manager_struct_a_0x700e349f, train_track_manager_struct_a_0x548c65a9, train_track_manager_struct_a_0xab03d22b, train_track_manager_struct_a_0x8f81831d, train_track_manager_struct_a_0xe2077047, train_track_manager_struct_a_0xc6852171, train_track_manager_struct_a_0xc6691902, train_track_manager_struct_a_0xe2eb4834)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00D')  # 68 properties

        data.write(b'\xc8\xfdH\x13')  # 0xc8fd4813
        data.write(b'\x00\x04')  # size
        self.random_scheme.to_stream(data)

        data.write(b'e\xec\xebz')  # 0x65eceb7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sequence_count))

        data.write(b'\xc1\x01\xf4~')  # 0xc101f47e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc101f47e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xac\x87\x07$')  # 0xac870724
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xac870724.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\x05V\x12')  # 0x88055612
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x88055612.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\x8a\xe1\x90')  # 0x778ae190
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x778ae190.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S\x08\xb0\xa6')  # 0x5308b0a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x5308b0a6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\x8eC\xfc')  # 0x3e8e43fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x3e8e43fc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a\x0c\x12\xca')  # 0x1a0c12ca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x1a0c12ca.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a\xe0*\xb9')  # 0x1ae02ab9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x1ae02ab9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>b{\x8f')  # 0x3e627b8f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x3e627b8f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S\xe4\x88\xd5')  # 0x53e488d5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x53e488d5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'wf\xd9\xe3')  # 0x7766d9e3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x7766d9e3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\xe9na')  # 0x88e96e61
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x88e96e61.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xack?W')  # 0xac6b3f57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xac6b3f57.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1\xed\xcc\r')  # 0xc1edcc0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc1edcc0d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5o\x9d;')  # 0xe56f9d3b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xe56f9d3b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc05\xbc\xeb')  # 0xc035bceb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc035bceb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4\xb7\xed\xdd')  # 0xe4b7eddd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xe4b7eddd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x891\x1e\x87')  # 0x89311e87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x89311e87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\xb3O\xb1')  # 0xadb34fb1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xadb34fb1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'R<\xf83')  # 0x523cf833
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x523cf833.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xbe\xa9\x05')  # 0x76bea905
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x76bea905.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b8Z_')  # 0x1b385a5f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x1b385a5f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\xba\x0bi')  # 0x3fba0b69
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x3fba0b69.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?V3\x1a')  # 0x3f56331a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x3f56331a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\xd4b,')  # 0x1bd4622c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x1bd4622c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'vR\x91v')  # 0x76529176
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x76529176.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~\x0e\xd2\x99')  # 0x7e0ed299
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x7e0ed299.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Z\x8c\x83\xaf')  # 0x5a8c83af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x5a8c83af.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\np\xf5')  # 0x370a70f5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x370a70f5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\x88!\xc3')  # 0x138821c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x138821c3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec\x07\x96A')  # 0xec079641
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xec079641.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8\x85\xc7w')  # 0xc885c777
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc885c777.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\x034-')  # 0xa503342d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xa503342d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\x81e\x1b')  # 0x8181651b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x8181651b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81m]h')  # 0x816d5d68
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x816d5d68.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\xef\x0c^')  # 0xa5ef0c5e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xa5ef0c5e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\xdd\xec\x80')  # 0xf5ddec80
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xf5ddec80.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1_\xbd\xb6')  # 0xd15fbdb6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xd15fbdb6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\xd9N\xec')  # 0xbcd94eec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xbcd94eec.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98[\x1f\xda')  # 0x985b1fda
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x985b1fda.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xd4\xa8X')  # 0x67d4a858
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x67d4a858.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'CV\xf9n')  # 0x4356f96e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x4356f96e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.\xd0\n4')  # 0x2ed00a34
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x2ed00a34.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\nR[\x02')  # 0xa525b02
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x0a525b02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\n\xbecq')  # 0xabe6371
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x0abe6371.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.<2G')  # 0x2e3c3247
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x2e3c3247.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':C\xfbH')  # 0x3a43fb48
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x3a43fb48.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1e\xc1\xaa~')  # 0x1ec1aa7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x1ec1aa7e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'sGY$')  # 0x73475924
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x73475924.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'W\xc5\x08\x12')  # 0x57c50812
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x57c50812.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa8J\xbf\x90')  # 0xa84abf90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xa84abf90.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8c\xc8\xee\xa6')  # 0x8cc8eea6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x8cc8eea6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1N\x1d\xfc')  # 0xe14e1dfc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xe14e1dfc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\xccL\xca')  # 0xc5cc4cca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc5cc4cca.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5 t\xb9')  # 0xc52074b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc52074b9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\xa2%\x8f')  # 0xe1a2258f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xe1a2258f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9\n\x96\xf3')  # 0x390a96f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x390a96f3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\x88\xc7\xc5')  # 0x1d88c7c5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x1d88c7c5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'p\x0e4\x9f')  # 0x700e349f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x700e349f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T\x8ce\xa9')  # 0x548c65a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x548c65a9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab\x03\xd2+')  # 0xab03d22b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xab03d22b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8f\x81\x83\x1d')  # 0x8f81831d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0x8f81831d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\x07pG')  # 0xe2077047
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xe2077047.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x85!q')  # 0xc6852171
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc6852171.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6i\x19\x02')  # 0xc6691902
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xc6691902.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\xebH4')  # 0xe2eb4834
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.train_track_manager_struct_a_0xe2eb4834.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct274Json", data)
        return cls(
            random_scheme=enums.RandomScheme.from_json(json_data['random_scheme']),
            sequence_count=json_data['sequence_count'],
            train_track_manager_struct_a_0xc101f47e=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc101f47e']),
            train_track_manager_struct_a_0xac870724=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xac870724']),
            train_track_manager_struct_a_0x88055612=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x88055612']),
            train_track_manager_struct_a_0x778ae190=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x778ae190']),
            train_track_manager_struct_a_0x5308b0a6=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x5308b0a6']),
            train_track_manager_struct_a_0x3e8e43fc=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x3e8e43fc']),
            train_track_manager_struct_a_0x1a0c12ca=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x1a0c12ca']),
            train_track_manager_struct_a_0x1ae02ab9=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x1ae02ab9']),
            train_track_manager_struct_a_0x3e627b8f=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x3e627b8f']),
            train_track_manager_struct_a_0x53e488d5=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x53e488d5']),
            train_track_manager_struct_a_0x7766d9e3=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x7766d9e3']),
            train_track_manager_struct_a_0x88e96e61=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x88e96e61']),
            train_track_manager_struct_a_0xac6b3f57=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xac6b3f57']),
            train_track_manager_struct_a_0xc1edcc0d=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc1edcc0d']),
            train_track_manager_struct_a_0xe56f9d3b=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xe56f9d3b']),
            train_track_manager_struct_a_0xc035bceb=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc035bceb']),
            train_track_manager_struct_a_0xe4b7eddd=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xe4b7eddd']),
            train_track_manager_struct_a_0x89311e87=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x89311e87']),
            train_track_manager_struct_a_0xadb34fb1=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xadb34fb1']),
            train_track_manager_struct_a_0x523cf833=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x523cf833']),
            train_track_manager_struct_a_0x76bea905=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x76bea905']),
            train_track_manager_struct_a_0x1b385a5f=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x1b385a5f']),
            train_track_manager_struct_a_0x3fba0b69=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x3fba0b69']),
            train_track_manager_struct_a_0x3f56331a=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x3f56331a']),
            train_track_manager_struct_a_0x1bd4622c=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x1bd4622c']),
            train_track_manager_struct_a_0x76529176=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x76529176']),
            train_track_manager_struct_a_0x7e0ed299=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x7e0ed299']),
            train_track_manager_struct_a_0x5a8c83af=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x5a8c83af']),
            train_track_manager_struct_a_0x370a70f5=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x370a70f5']),
            train_track_manager_struct_a_0x138821c3=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x138821c3']),
            train_track_manager_struct_a_0xec079641=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xec079641']),
            train_track_manager_struct_a_0xc885c777=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc885c777']),
            train_track_manager_struct_a_0xa503342d=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xa503342d']),
            train_track_manager_struct_a_0x8181651b=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x8181651b']),
            train_track_manager_struct_a_0x816d5d68=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x816d5d68']),
            train_track_manager_struct_a_0xa5ef0c5e=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xa5ef0c5e']),
            train_track_manager_struct_a_0xf5ddec80=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xf5ddec80']),
            train_track_manager_struct_a_0xd15fbdb6=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xd15fbdb6']),
            train_track_manager_struct_a_0xbcd94eec=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xbcd94eec']),
            train_track_manager_struct_a_0x985b1fda=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x985b1fda']),
            train_track_manager_struct_a_0x67d4a858=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x67d4a858']),
            train_track_manager_struct_a_0x4356f96e=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x4356f96e']),
            train_track_manager_struct_a_0x2ed00a34=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x2ed00a34']),
            train_track_manager_struct_a_0x0a525b02=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x0a525b02']),
            train_track_manager_struct_a_0x0abe6371=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x0abe6371']),
            train_track_manager_struct_a_0x2e3c3247=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x2e3c3247']),
            train_track_manager_struct_a_0x3a43fb48=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x3a43fb48']),
            train_track_manager_struct_a_0x1ec1aa7e=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x1ec1aa7e']),
            train_track_manager_struct_a_0x73475924=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x73475924']),
            train_track_manager_struct_a_0x57c50812=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x57c50812']),
            train_track_manager_struct_a_0xa84abf90=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xa84abf90']),
            train_track_manager_struct_a_0x8cc8eea6=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x8cc8eea6']),
            train_track_manager_struct_a_0xe14e1dfc=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xe14e1dfc']),
            train_track_manager_struct_a_0xc5cc4cca=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc5cc4cca']),
            train_track_manager_struct_a_0xc52074b9=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc52074b9']),
            train_track_manager_struct_a_0xe1a2258f=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xe1a2258f']),
            train_track_manager_struct_a_0x390a96f3=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x390a96f3']),
            train_track_manager_struct_a_0x1d88c7c5=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x1d88c7c5']),
            train_track_manager_struct_a_0x700e349f=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x700e349f']),
            train_track_manager_struct_a_0x548c65a9=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x548c65a9']),
            train_track_manager_struct_a_0xab03d22b=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xab03d22b']),
            train_track_manager_struct_a_0x8f81831d=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0x8f81831d']),
            train_track_manager_struct_a_0xe2077047=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xe2077047']),
            train_track_manager_struct_a_0xc6852171=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc6852171']),
            train_track_manager_struct_a_0xc6691902=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xc6691902']),
            train_track_manager_struct_a_0xe2eb4834=TrainTrackManagerStructA.from_json(json_data['train_track_manager_struct_a_0xe2eb4834']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'random_scheme': self.random_scheme.to_json(),
            'sequence_count': self.sequence_count,
            'train_track_manager_struct_a_0xc101f47e': self.train_track_manager_struct_a_0xc101f47e.to_json(),
            'train_track_manager_struct_a_0xac870724': self.train_track_manager_struct_a_0xac870724.to_json(),
            'train_track_manager_struct_a_0x88055612': self.train_track_manager_struct_a_0x88055612.to_json(),
            'train_track_manager_struct_a_0x778ae190': self.train_track_manager_struct_a_0x778ae190.to_json(),
            'train_track_manager_struct_a_0x5308b0a6': self.train_track_manager_struct_a_0x5308b0a6.to_json(),
            'train_track_manager_struct_a_0x3e8e43fc': self.train_track_manager_struct_a_0x3e8e43fc.to_json(),
            'train_track_manager_struct_a_0x1a0c12ca': self.train_track_manager_struct_a_0x1a0c12ca.to_json(),
            'train_track_manager_struct_a_0x1ae02ab9': self.train_track_manager_struct_a_0x1ae02ab9.to_json(),
            'train_track_manager_struct_a_0x3e627b8f': self.train_track_manager_struct_a_0x3e627b8f.to_json(),
            'train_track_manager_struct_a_0x53e488d5': self.train_track_manager_struct_a_0x53e488d5.to_json(),
            'train_track_manager_struct_a_0x7766d9e3': self.train_track_manager_struct_a_0x7766d9e3.to_json(),
            'train_track_manager_struct_a_0x88e96e61': self.train_track_manager_struct_a_0x88e96e61.to_json(),
            'train_track_manager_struct_a_0xac6b3f57': self.train_track_manager_struct_a_0xac6b3f57.to_json(),
            'train_track_manager_struct_a_0xc1edcc0d': self.train_track_manager_struct_a_0xc1edcc0d.to_json(),
            'train_track_manager_struct_a_0xe56f9d3b': self.train_track_manager_struct_a_0xe56f9d3b.to_json(),
            'train_track_manager_struct_a_0xc035bceb': self.train_track_manager_struct_a_0xc035bceb.to_json(),
            'train_track_manager_struct_a_0xe4b7eddd': self.train_track_manager_struct_a_0xe4b7eddd.to_json(),
            'train_track_manager_struct_a_0x89311e87': self.train_track_manager_struct_a_0x89311e87.to_json(),
            'train_track_manager_struct_a_0xadb34fb1': self.train_track_manager_struct_a_0xadb34fb1.to_json(),
            'train_track_manager_struct_a_0x523cf833': self.train_track_manager_struct_a_0x523cf833.to_json(),
            'train_track_manager_struct_a_0x76bea905': self.train_track_manager_struct_a_0x76bea905.to_json(),
            'train_track_manager_struct_a_0x1b385a5f': self.train_track_manager_struct_a_0x1b385a5f.to_json(),
            'train_track_manager_struct_a_0x3fba0b69': self.train_track_manager_struct_a_0x3fba0b69.to_json(),
            'train_track_manager_struct_a_0x3f56331a': self.train_track_manager_struct_a_0x3f56331a.to_json(),
            'train_track_manager_struct_a_0x1bd4622c': self.train_track_manager_struct_a_0x1bd4622c.to_json(),
            'train_track_manager_struct_a_0x76529176': self.train_track_manager_struct_a_0x76529176.to_json(),
            'train_track_manager_struct_a_0x7e0ed299': self.train_track_manager_struct_a_0x7e0ed299.to_json(),
            'train_track_manager_struct_a_0x5a8c83af': self.train_track_manager_struct_a_0x5a8c83af.to_json(),
            'train_track_manager_struct_a_0x370a70f5': self.train_track_manager_struct_a_0x370a70f5.to_json(),
            'train_track_manager_struct_a_0x138821c3': self.train_track_manager_struct_a_0x138821c3.to_json(),
            'train_track_manager_struct_a_0xec079641': self.train_track_manager_struct_a_0xec079641.to_json(),
            'train_track_manager_struct_a_0xc885c777': self.train_track_manager_struct_a_0xc885c777.to_json(),
            'train_track_manager_struct_a_0xa503342d': self.train_track_manager_struct_a_0xa503342d.to_json(),
            'train_track_manager_struct_a_0x8181651b': self.train_track_manager_struct_a_0x8181651b.to_json(),
            'train_track_manager_struct_a_0x816d5d68': self.train_track_manager_struct_a_0x816d5d68.to_json(),
            'train_track_manager_struct_a_0xa5ef0c5e': self.train_track_manager_struct_a_0xa5ef0c5e.to_json(),
            'train_track_manager_struct_a_0xf5ddec80': self.train_track_manager_struct_a_0xf5ddec80.to_json(),
            'train_track_manager_struct_a_0xd15fbdb6': self.train_track_manager_struct_a_0xd15fbdb6.to_json(),
            'train_track_manager_struct_a_0xbcd94eec': self.train_track_manager_struct_a_0xbcd94eec.to_json(),
            'train_track_manager_struct_a_0x985b1fda': self.train_track_manager_struct_a_0x985b1fda.to_json(),
            'train_track_manager_struct_a_0x67d4a858': self.train_track_manager_struct_a_0x67d4a858.to_json(),
            'train_track_manager_struct_a_0x4356f96e': self.train_track_manager_struct_a_0x4356f96e.to_json(),
            'train_track_manager_struct_a_0x2ed00a34': self.train_track_manager_struct_a_0x2ed00a34.to_json(),
            'train_track_manager_struct_a_0x0a525b02': self.train_track_manager_struct_a_0x0a525b02.to_json(),
            'train_track_manager_struct_a_0x0abe6371': self.train_track_manager_struct_a_0x0abe6371.to_json(),
            'train_track_manager_struct_a_0x2e3c3247': self.train_track_manager_struct_a_0x2e3c3247.to_json(),
            'train_track_manager_struct_a_0x3a43fb48': self.train_track_manager_struct_a_0x3a43fb48.to_json(),
            'train_track_manager_struct_a_0x1ec1aa7e': self.train_track_manager_struct_a_0x1ec1aa7e.to_json(),
            'train_track_manager_struct_a_0x73475924': self.train_track_manager_struct_a_0x73475924.to_json(),
            'train_track_manager_struct_a_0x57c50812': self.train_track_manager_struct_a_0x57c50812.to_json(),
            'train_track_manager_struct_a_0xa84abf90': self.train_track_manager_struct_a_0xa84abf90.to_json(),
            'train_track_manager_struct_a_0x8cc8eea6': self.train_track_manager_struct_a_0x8cc8eea6.to_json(),
            'train_track_manager_struct_a_0xe14e1dfc': self.train_track_manager_struct_a_0xe14e1dfc.to_json(),
            'train_track_manager_struct_a_0xc5cc4cca': self.train_track_manager_struct_a_0xc5cc4cca.to_json(),
            'train_track_manager_struct_a_0xc52074b9': self.train_track_manager_struct_a_0xc52074b9.to_json(),
            'train_track_manager_struct_a_0xe1a2258f': self.train_track_manager_struct_a_0xe1a2258f.to_json(),
            'train_track_manager_struct_a_0x390a96f3': self.train_track_manager_struct_a_0x390a96f3.to_json(),
            'train_track_manager_struct_a_0x1d88c7c5': self.train_track_manager_struct_a_0x1d88c7c5.to_json(),
            'train_track_manager_struct_a_0x700e349f': self.train_track_manager_struct_a_0x700e349f.to_json(),
            'train_track_manager_struct_a_0x548c65a9': self.train_track_manager_struct_a_0x548c65a9.to_json(),
            'train_track_manager_struct_a_0xab03d22b': self.train_track_manager_struct_a_0xab03d22b.to_json(),
            'train_track_manager_struct_a_0x8f81831d': self.train_track_manager_struct_a_0x8f81831d.to_json(),
            'train_track_manager_struct_a_0xe2077047': self.train_track_manager_struct_a_0xe2077047.to_json(),
            'train_track_manager_struct_a_0xc6852171': self.train_track_manager_struct_a_0xc6852171.to_json(),
            'train_track_manager_struct_a_0xc6691902': self.train_track_manager_struct_a_0xc6691902.to_json(),
            'train_track_manager_struct_a_0xe2eb4834': self.train_track_manager_struct_a_0xe2eb4834.to_json(),
        }


def _decode_random_scheme(data: typing.BinaryIO, property_size: int):
    return enums.RandomScheme.from_stream(data)


def _decode_sequence_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc8fd4813: ('random_scheme', _decode_random_scheme),
    0x65eceb7a: ('sequence_count', _decode_sequence_count),
    0xc101f47e: ('train_track_manager_struct_a_0xc101f47e', TrainTrackManagerStructA.from_stream),
    0xac870724: ('train_track_manager_struct_a_0xac870724', TrainTrackManagerStructA.from_stream),
    0x88055612: ('train_track_manager_struct_a_0x88055612', TrainTrackManagerStructA.from_stream),
    0x778ae190: ('train_track_manager_struct_a_0x778ae190', TrainTrackManagerStructA.from_stream),
    0x5308b0a6: ('train_track_manager_struct_a_0x5308b0a6', TrainTrackManagerStructA.from_stream),
    0x3e8e43fc: ('train_track_manager_struct_a_0x3e8e43fc', TrainTrackManagerStructA.from_stream),
    0x1a0c12ca: ('train_track_manager_struct_a_0x1a0c12ca', TrainTrackManagerStructA.from_stream),
    0x1ae02ab9: ('train_track_manager_struct_a_0x1ae02ab9', TrainTrackManagerStructA.from_stream),
    0x3e627b8f: ('train_track_manager_struct_a_0x3e627b8f', TrainTrackManagerStructA.from_stream),
    0x53e488d5: ('train_track_manager_struct_a_0x53e488d5', TrainTrackManagerStructA.from_stream),
    0x7766d9e3: ('train_track_manager_struct_a_0x7766d9e3', TrainTrackManagerStructA.from_stream),
    0x88e96e61: ('train_track_manager_struct_a_0x88e96e61', TrainTrackManagerStructA.from_stream),
    0xac6b3f57: ('train_track_manager_struct_a_0xac6b3f57', TrainTrackManagerStructA.from_stream),
    0xc1edcc0d: ('train_track_manager_struct_a_0xc1edcc0d', TrainTrackManagerStructA.from_stream),
    0xe56f9d3b: ('train_track_manager_struct_a_0xe56f9d3b', TrainTrackManagerStructA.from_stream),
    0xc035bceb: ('train_track_manager_struct_a_0xc035bceb', TrainTrackManagerStructA.from_stream),
    0xe4b7eddd: ('train_track_manager_struct_a_0xe4b7eddd', TrainTrackManagerStructA.from_stream),
    0x89311e87: ('train_track_manager_struct_a_0x89311e87', TrainTrackManagerStructA.from_stream),
    0xadb34fb1: ('train_track_manager_struct_a_0xadb34fb1', TrainTrackManagerStructA.from_stream),
    0x523cf833: ('train_track_manager_struct_a_0x523cf833', TrainTrackManagerStructA.from_stream),
    0x76bea905: ('train_track_manager_struct_a_0x76bea905', TrainTrackManagerStructA.from_stream),
    0x1b385a5f: ('train_track_manager_struct_a_0x1b385a5f', TrainTrackManagerStructA.from_stream),
    0x3fba0b69: ('train_track_manager_struct_a_0x3fba0b69', TrainTrackManagerStructA.from_stream),
    0x3f56331a: ('train_track_manager_struct_a_0x3f56331a', TrainTrackManagerStructA.from_stream),
    0x1bd4622c: ('train_track_manager_struct_a_0x1bd4622c', TrainTrackManagerStructA.from_stream),
    0x76529176: ('train_track_manager_struct_a_0x76529176', TrainTrackManagerStructA.from_stream),
    0x7e0ed299: ('train_track_manager_struct_a_0x7e0ed299', TrainTrackManagerStructA.from_stream),
    0x5a8c83af: ('train_track_manager_struct_a_0x5a8c83af', TrainTrackManagerStructA.from_stream),
    0x370a70f5: ('train_track_manager_struct_a_0x370a70f5', TrainTrackManagerStructA.from_stream),
    0x138821c3: ('train_track_manager_struct_a_0x138821c3', TrainTrackManagerStructA.from_stream),
    0xec079641: ('train_track_manager_struct_a_0xec079641', TrainTrackManagerStructA.from_stream),
    0xc885c777: ('train_track_manager_struct_a_0xc885c777', TrainTrackManagerStructA.from_stream),
    0xa503342d: ('train_track_manager_struct_a_0xa503342d', TrainTrackManagerStructA.from_stream),
    0x8181651b: ('train_track_manager_struct_a_0x8181651b', TrainTrackManagerStructA.from_stream),
    0x816d5d68: ('train_track_manager_struct_a_0x816d5d68', TrainTrackManagerStructA.from_stream),
    0xa5ef0c5e: ('train_track_manager_struct_a_0xa5ef0c5e', TrainTrackManagerStructA.from_stream),
    0xf5ddec80: ('train_track_manager_struct_a_0xf5ddec80', TrainTrackManagerStructA.from_stream),
    0xd15fbdb6: ('train_track_manager_struct_a_0xd15fbdb6', TrainTrackManagerStructA.from_stream),
    0xbcd94eec: ('train_track_manager_struct_a_0xbcd94eec', TrainTrackManagerStructA.from_stream),
    0x985b1fda: ('train_track_manager_struct_a_0x985b1fda', TrainTrackManagerStructA.from_stream),
    0x67d4a858: ('train_track_manager_struct_a_0x67d4a858', TrainTrackManagerStructA.from_stream),
    0x4356f96e: ('train_track_manager_struct_a_0x4356f96e', TrainTrackManagerStructA.from_stream),
    0x2ed00a34: ('train_track_manager_struct_a_0x2ed00a34', TrainTrackManagerStructA.from_stream),
    0xa525b02: ('train_track_manager_struct_a_0x0a525b02', TrainTrackManagerStructA.from_stream),
    0xabe6371: ('train_track_manager_struct_a_0x0abe6371', TrainTrackManagerStructA.from_stream),
    0x2e3c3247: ('train_track_manager_struct_a_0x2e3c3247', TrainTrackManagerStructA.from_stream),
    0x3a43fb48: ('train_track_manager_struct_a_0x3a43fb48', TrainTrackManagerStructA.from_stream),
    0x1ec1aa7e: ('train_track_manager_struct_a_0x1ec1aa7e', TrainTrackManagerStructA.from_stream),
    0x73475924: ('train_track_manager_struct_a_0x73475924', TrainTrackManagerStructA.from_stream),
    0x57c50812: ('train_track_manager_struct_a_0x57c50812', TrainTrackManagerStructA.from_stream),
    0xa84abf90: ('train_track_manager_struct_a_0xa84abf90', TrainTrackManagerStructA.from_stream),
    0x8cc8eea6: ('train_track_manager_struct_a_0x8cc8eea6', TrainTrackManagerStructA.from_stream),
    0xe14e1dfc: ('train_track_manager_struct_a_0xe14e1dfc', TrainTrackManagerStructA.from_stream),
    0xc5cc4cca: ('train_track_manager_struct_a_0xc5cc4cca', TrainTrackManagerStructA.from_stream),
    0xc52074b9: ('train_track_manager_struct_a_0xc52074b9', TrainTrackManagerStructA.from_stream),
    0xe1a2258f: ('train_track_manager_struct_a_0xe1a2258f', TrainTrackManagerStructA.from_stream),
    0x390a96f3: ('train_track_manager_struct_a_0x390a96f3', TrainTrackManagerStructA.from_stream),
    0x1d88c7c5: ('train_track_manager_struct_a_0x1d88c7c5', TrainTrackManagerStructA.from_stream),
    0x700e349f: ('train_track_manager_struct_a_0x700e349f', TrainTrackManagerStructA.from_stream),
    0x548c65a9: ('train_track_manager_struct_a_0x548c65a9', TrainTrackManagerStructA.from_stream),
    0xab03d22b: ('train_track_manager_struct_a_0xab03d22b', TrainTrackManagerStructA.from_stream),
    0x8f81831d: ('train_track_manager_struct_a_0x8f81831d', TrainTrackManagerStructA.from_stream),
    0xe2077047: ('train_track_manager_struct_a_0xe2077047', TrainTrackManagerStructA.from_stream),
    0xc6852171: ('train_track_manager_struct_a_0xc6852171', TrainTrackManagerStructA.from_stream),
    0xc6691902: ('train_track_manager_struct_a_0xc6691902', TrainTrackManagerStructA.from_stream),
    0xe2eb4834: ('train_track_manager_struct_a_0xe2eb4834', TrainTrackManagerStructA.from_stream),
}

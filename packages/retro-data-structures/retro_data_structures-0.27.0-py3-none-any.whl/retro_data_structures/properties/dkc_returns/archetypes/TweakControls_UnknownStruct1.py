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
from retro_data_structures.properties.dkc_returns.archetypes.MapControls import MapControls
from retro_data_structures.properties.dkc_returns.archetypes.MiscControls import MiscControls
from retro_data_structures.properties.dkc_returns.archetypes.TweakControls_UnknownStruct2 import TweakControls_UnknownStruct2
from retro_data_structures.properties.dkc_returns.archetypes.TweakControls_UnknownStruct3 import TweakControls_UnknownStruct3

if typing.TYPE_CHECKING:
    class TweakControls_UnknownStruct1Json(typing_extensions.TypedDict):
        unknown: json_util.JsonObject
        map: json_util.JsonObject
        misc: json_util.JsonObject
        debug: json_util.JsonObject
    

@dataclasses.dataclass()
class TweakControls_UnknownStruct1(BaseProperty):
    unknown: TweakControls_UnknownStruct2 = dataclasses.field(default_factory=TweakControls_UnknownStruct2, metadata={
        'reflection': FieldReflection[TweakControls_UnknownStruct2](
            TweakControls_UnknownStruct2, id=0x4bd8ecb9, original_name='Unknown', from_json=TweakControls_UnknownStruct2.from_json, to_json=TweakControls_UnknownStruct2.to_json
        ),
    })
    map: MapControls = dataclasses.field(default_factory=MapControls, metadata={
        'reflection': FieldReflection[MapControls](
            MapControls, id=0x9acb4ace, original_name='Map', from_json=MapControls.from_json, to_json=MapControls.to_json
        ),
    })
    misc: MiscControls = dataclasses.field(default_factory=MiscControls, metadata={
        'reflection': FieldReflection[MiscControls](
            MiscControls, id=0xbe77ded2, original_name='Misc', from_json=MiscControls.from_json, to_json=MiscControls.to_json
        ),
    })
    debug: TweakControls_UnknownStruct3 = dataclasses.field(default_factory=TweakControls_UnknownStruct3, metadata={
        'reflection': FieldReflection[TweakControls_UnknownStruct3](
            TweakControls_UnknownStruct3, id=0x47069911, original_name='Debug', from_json=TweakControls_UnknownStruct3.from_json, to_json=TweakControls_UnknownStruct3.to_json
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
        assert property_id == 0x4bd8ecb9
        unknown = TweakControls_UnknownStruct2.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9acb4ace
        map = MapControls.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbe77ded2
        misc = MiscControls.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47069911
        debug = TweakControls_UnknownStruct3.from_stream(data, property_size)
    
        return cls(unknown, map, misc, debug)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'K\xd8\xec\xb9')  # 0x4bd8ecb9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a\xcbJ\xce')  # 0x9acb4ace
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.map.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbew\xde\xd2')  # 0xbe77ded2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.misc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G\x06\x99\x11')  # 0x47069911
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.debug.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TweakControls_UnknownStruct1Json", data)
        return cls(
            unknown=TweakControls_UnknownStruct2.from_json(json_data['unknown']),
            map=MapControls.from_json(json_data['map']),
            misc=MiscControls.from_json(json_data['misc']),
            debug=TweakControls_UnknownStruct3.from_json(json_data['debug']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown.to_json(),
            'map': self.map.to_json(),
            'misc': self.misc.to_json(),
            'debug': self.debug.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4bd8ecb9: ('unknown', TweakControls_UnknownStruct2.from_stream),
    0x9acb4ace: ('map', MapControls.from_stream),
    0xbe77ded2: ('misc', MiscControls.from_stream),
    0x47069911: ('debug', TweakControls_UnknownStruct3.from_stream),
}

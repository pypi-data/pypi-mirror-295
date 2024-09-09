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
from retro_data_structures.properties.dkc_returns.archetypes.FramingRules import FramingRules
from retro_data_structures.properties.dkc_returns.archetypes.ZoomBehaviorData import ZoomBehaviorData

if typing.TYPE_CHECKING:
    class CameraFramingJson(typing_extensions.TypedDict):
        framing_rules: json_util.JsonObject
        zoom_behavior: json_util.JsonObject
    

@dataclasses.dataclass()
class CameraFraming(BaseProperty):
    framing_rules: FramingRules = dataclasses.field(default_factory=FramingRules, metadata={
        'reflection': FieldReflection[FramingRules](
            FramingRules, id=0xc79aa0c6, original_name='FramingRules', from_json=FramingRules.from_json, to_json=FramingRules.to_json
        ),
    })
    zoom_behavior: ZoomBehaviorData = dataclasses.field(default_factory=ZoomBehaviorData, metadata={
        'reflection': FieldReflection[ZoomBehaviorData](
            ZoomBehaviorData, id=0x62243011, original_name='ZoomBehavior', from_json=ZoomBehaviorData.from_json, to_json=ZoomBehaviorData.to_json
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
        if property_count != 2:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc79aa0c6
        framing_rules = FramingRules.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x62243011
        zoom_behavior = ZoomBehaviorData.from_stream(data, property_size)
    
        return cls(framing_rules, zoom_behavior)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xc7\x9a\xa0\xc6')  # 0xc79aa0c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.framing_rules.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'b$0\x11')  # 0x62243011
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.zoom_behavior.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("CameraFramingJson", data)
        return cls(
            framing_rules=FramingRules.from_json(json_data['framing_rules']),
            zoom_behavior=ZoomBehaviorData.from_json(json_data['zoom_behavior']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'framing_rules': self.framing_rules.to_json(),
            'zoom_behavior': self.zoom_behavior.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc79aa0c6: ('framing_rules', FramingRules.from_stream),
    0x62243011: ('zoom_behavior', ZoomBehaviorData.from_stream),
}

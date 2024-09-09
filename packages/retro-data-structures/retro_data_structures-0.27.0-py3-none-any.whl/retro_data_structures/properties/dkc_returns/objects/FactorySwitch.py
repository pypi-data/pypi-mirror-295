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
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.RotationSplines import RotationSplines
from retro_data_structures.properties.dkc_returns.archetypes.TranslationSplines import TranslationSplines
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class FactorySwitchJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        case_model: int
        indicator_model: int
        switch_state: bool
        switch_delay: float
        rotation_controls: json_util.JsonObject
        translation_control: json_util.JsonObject
        toggle_sound: int
        reset_sound: int
        unknown_0x25c9c68f: bool
        unknown_0x10e79562: json_util.JsonValue
        unknown_0x7357fbac: bool
        actor_information: json_util.JsonObject
    

@dataclasses.dataclass()
class FactorySwitch(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    case_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6ca453b1, original_name='CaseModel'
        ),
    })
    indicator_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb6d34cbe, original_name='IndicatorModel'
        ),
    })
    switch_state: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x66e64eba, original_name='SwitchState'
        ),
    })
    switch_delay: float = dataclasses.field(default=0.6000000238418579, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8a1fd661, original_name='SwitchDelay'
        ),
    })
    rotation_controls: RotationSplines = dataclasses.field(default_factory=RotationSplines, metadata={
        'reflection': FieldReflection[RotationSplines](
            RotationSplines, id=0xefe4ea57, original_name='RotationControls', from_json=RotationSplines.from_json, to_json=RotationSplines.to_json
        ),
    })
    translation_control: TranslationSplines = dataclasses.field(default_factory=TranslationSplines, metadata={
        'reflection': FieldReflection[TranslationSplines](
            TranslationSplines, id=0x692267ea, original_name='TranslationControl', from_json=TranslationSplines.from_json, to_json=TranslationSplines.to_json
        ),
    })
    toggle_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x36f96f54, original_name='ToggleSound'
        ),
    })
    reset_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': [], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x465159a3, original_name='ResetSound'
        ),
    })
    unknown_0x25c9c68f: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x25c9c68f, original_name='Unknown'
        ),
    })
    unknown_0x10e79562: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x10e79562, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    unknown_0x7357fbac: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7357fbac, original_name='Unknown'
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
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
        return 'FSWC'

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
        if property_count != 13:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6ca453b1
        case_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb6d34cbe
        indicator_model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x66e64eba
        switch_state = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8a1fd661
        switch_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xefe4ea57
        rotation_controls = RotationSplines.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x692267ea
        translation_control = TranslationSplines.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36f96f54
        toggle_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x465159a3
        reset_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x25c9c68f
        unknown_0x25c9c68f = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x10e79562
        unknown_0x10e79562 = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7357fbac
        unknown_0x7357fbac = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        return cls(editor_properties, case_model, indicator_model, switch_state, switch_delay, rotation_controls, translation_control, toggle_sound, reset_sound, unknown_0x25c9c68f, unknown_0x10e79562, unknown_0x7357fbac, actor_information)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\xa4S\xb1')  # 0x6ca453b1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.case_model))

        data.write(b'\xb6\xd3L\xbe')  # 0xb6d34cbe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.indicator_model))

        data.write(b'f\xe6N\xba')  # 0x66e64eba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.switch_state))

        data.write(b'\x8a\x1f\xd6a')  # 0x8a1fd661
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.switch_delay))

        data.write(b'\xef\xe4\xeaW')  # 0xefe4ea57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotation_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i"g\xea')  # 0x692267ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.translation_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xf9oT')  # 0x36f96f54
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.toggle_sound))

        data.write(b'FQY\xa3')  # 0x465159a3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.reset_sound))

        data.write(b'%\xc9\xc6\x8f')  # 0x25c9c68f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x25c9c68f))

        data.write(b'\x10\xe7\x95b')  # 0x10e79562
        data.write(b'\x00\x0c')  # size
        self.unknown_0x10e79562.to_stream(data)

        data.write(b'sW\xfb\xac')  # 0x7357fbac
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7357fbac))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
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
        json_data = typing.cast("FactorySwitchJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            case_model=json_data['case_model'],
            indicator_model=json_data['indicator_model'],
            switch_state=json_data['switch_state'],
            switch_delay=json_data['switch_delay'],
            rotation_controls=RotationSplines.from_json(json_data['rotation_controls']),
            translation_control=TranslationSplines.from_json(json_data['translation_control']),
            toggle_sound=json_data['toggle_sound'],
            reset_sound=json_data['reset_sound'],
            unknown_0x25c9c68f=json_data['unknown_0x25c9c68f'],
            unknown_0x10e79562=Vector.from_json(json_data['unknown_0x10e79562']),
            unknown_0x7357fbac=json_data['unknown_0x7357fbac'],
            actor_information=ActorParameters.from_json(json_data['actor_information']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'case_model': self.case_model,
            'indicator_model': self.indicator_model,
            'switch_state': self.switch_state,
            'switch_delay': self.switch_delay,
            'rotation_controls': self.rotation_controls.to_json(),
            'translation_control': self.translation_control.to_json(),
            'toggle_sound': self.toggle_sound,
            'reset_sound': self.reset_sound,
            'unknown_0x25c9c68f': self.unknown_0x25c9c68f,
            'unknown_0x10e79562': self.unknown_0x10e79562.to_json(),
            'unknown_0x7357fbac': self.unknown_0x7357fbac,
            'actor_information': self.actor_information.to_json(),
        }


def _decode_case_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_indicator_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_switch_state(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_switch_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_toggle_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_reset_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x25c9c68f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x10e79562(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x7357fbac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x6ca453b1: ('case_model', _decode_case_model),
    0xb6d34cbe: ('indicator_model', _decode_indicator_model),
    0x66e64eba: ('switch_state', _decode_switch_state),
    0x8a1fd661: ('switch_delay', _decode_switch_delay),
    0xefe4ea57: ('rotation_controls', RotationSplines.from_stream),
    0x692267ea: ('translation_control', TranslationSplines.from_stream),
    0x36f96f54: ('toggle_sound', _decode_toggle_sound),
    0x465159a3: ('reset_sound', _decode_reset_sound),
    0x25c9c68f: ('unknown_0x25c9c68f', _decode_unknown_0x25c9c68f),
    0x10e79562: ('unknown_0x10e79562', _decode_unknown_0x10e79562),
    0x7357fbac: ('unknown_0x7357fbac', _decode_unknown_0x7357fbac),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct277 import UnknownStruct277
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class TutorialJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        actor_parameters: json_util.JsonObject
        unknown_struct6: json_util.JsonObject
        unknown_struct277: json_util.JsonObject
        offset: json_util.JsonValue
        activation_distance: float
        activation_delay: float
        sound_show_tutorial: int
        sound_hide_tutorial: int
        ignore_player_detection: bool
    

@dataclasses.dataclass()
class Tutorial(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    actor_parameters: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0xd29c031d, original_name='ActorParameters', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    unknown_struct6: PlayerType = dataclasses.field(default_factory=PlayerType, metadata={
        'reflection': FieldReflection[PlayerType](
            PlayerType, id=0x56abb3b8, original_name='UnknownStruct6', from_json=PlayerType.from_json, to_json=PlayerType.to_json
        ),
    })
    unknown_struct277: UnknownStruct277 = dataclasses.field(default_factory=UnknownStruct277, metadata={
        'reflection': FieldReflection[UnknownStruct277](
            UnknownStruct277, id=0x76aa6d55, original_name='UnknownStruct277', from_json=UnknownStruct277.from_json, to_json=UnknownStruct277.to_json
        ),
    })
    offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x46477064, original_name='Offset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    activation_distance: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf90a4fe9, original_name='ActivationDistance'
        ),
    })
    activation_delay: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe585f166, original_name='ActivationDelay'
        ),
    })
    sound_show_tutorial: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x446307a9, original_name='Sound_ShowTutorial'
        ),
    })
    sound_hide_tutorial: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x11f84560, original_name='Sound_HideTutorial'
        ),
    })
    ignore_player_detection: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x14ceff80, original_name='IgnorePlayerDetection'
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
        return 'TUTR'

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
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd29c031d
        actor_parameters = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x56abb3b8
        unknown_struct6 = PlayerType.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76aa6d55
        unknown_struct277 = UnknownStruct277.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46477064
        offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf90a4fe9
        activation_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe585f166
        activation_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x446307a9
        sound_show_tutorial = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x11f84560
        sound_hide_tutorial = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x14ceff80
        ignore_player_detection = struct.unpack('>?', data.read(1))[0]
    
        return cls(editor_properties, actor_parameters, unknown_struct6, unknown_struct277, offset, activation_distance, activation_delay, sound_show_tutorial, sound_hide_tutorial, ignore_player_detection)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\n')  # 10 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x9c\x03\x1d')  # 0xd29c031d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\xab\xb3\xb8')  # 0x56abb3b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xaamU')  # 0x76aa6d55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct277.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'FGpd')  # 0x46477064
        data.write(b'\x00\x0c')  # size
        self.offset.to_stream(data)

        data.write(b'\xf9\nO\xe9')  # 0xf90a4fe9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_distance))

        data.write(b'\xe5\x85\xf1f')  # 0xe585f166
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_delay))

        data.write(b'Dc\x07\xa9')  # 0x446307a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_show_tutorial))

        data.write(b'\x11\xf8E`')  # 0x11f84560
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_hide_tutorial))

        data.write(b'\x14\xce\xff\x80')  # 0x14ceff80
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_player_detection))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("TutorialJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            actor_parameters=ActorParameters.from_json(json_data['actor_parameters']),
            unknown_struct6=PlayerType.from_json(json_data['unknown_struct6']),
            unknown_struct277=UnknownStruct277.from_json(json_data['unknown_struct277']),
            offset=Vector.from_json(json_data['offset']),
            activation_distance=json_data['activation_distance'],
            activation_delay=json_data['activation_delay'],
            sound_show_tutorial=json_data['sound_show_tutorial'],
            sound_hide_tutorial=json_data['sound_hide_tutorial'],
            ignore_player_detection=json_data['ignore_player_detection'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_parameters': self.actor_parameters.to_json(),
            'unknown_struct6': self.unknown_struct6.to_json(),
            'unknown_struct277': self.unknown_struct277.to_json(),
            'offset': self.offset.to_json(),
            'activation_distance': self.activation_distance,
            'activation_delay': self.activation_delay,
            'sound_show_tutorial': self.sound_show_tutorial,
            'sound_hide_tutorial': self.sound_hide_tutorial,
            'ignore_player_detection': self.ignore_player_detection,
        }


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_activation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activation_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_show_tutorial(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_hide_tutorial(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ignore_player_detection(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xd29c031d: ('actor_parameters', ActorParameters.from_stream),
    0x56abb3b8: ('unknown_struct6', PlayerType.from_stream),
    0x76aa6d55: ('unknown_struct277', UnknownStruct277.from_stream),
    0x46477064: ('offset', _decode_offset),
    0xf90a4fe9: ('activation_distance', _decode_activation_distance),
    0xe585f166: ('activation_delay', _decode_activation_delay),
    0x446307a9: ('sound_show_tutorial', _decode_sound_show_tutorial),
    0x11f84560: ('sound_hide_tutorial', _decode_sound_hide_tutorial),
    0x14ceff80: ('ignore_player_detection', _decode_ignore_player_detection),
}

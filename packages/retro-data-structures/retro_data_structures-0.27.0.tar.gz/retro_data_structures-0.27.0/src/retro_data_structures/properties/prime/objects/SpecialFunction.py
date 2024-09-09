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
from retro_data_structures.properties.prime.archetypes.LayerSwitch import LayerSwitch
from retro_data_structures.properties.prime.core.Vector import Vector

if typing.TYPE_CHECKING:
    from retro_data_structures.asset_manager import AssetManager
    from retro_data_structures.base_resource import Dependency

    class SpecialFunctionJson(typing_extensions.TypedDict):
        name: str
        position: json_util.JsonValue
        rotation: json_util.JsonValue
        function: int
        unknown_1: str
        unknown_2: float
        unknown_3: float
        unknown_4: float
        unnamed_0x00000008: json_util.JsonObject
        unnamed_0x00000009: int
        active: bool
        unknown_5: float
        used_by_spinner_controller_1: int
        used_by_spinner_controller_2: int
        used_by_spinner_controller_3: int
    

@dataclasses.dataclass()
class SpecialFunction(BaseObjectType):
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
    rotation: Vector = dataclasses.field(default_factory=Vector, metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x00000002, original_name='Rotation', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    function: enums.Function = dataclasses.field(default=enums.Function.Function0, metadata={
        'reflection': FieldReflection[enums.Function](
            enums.Function, id=0x00000003, original_name='Function', from_json=enums.Function.from_json, to_json=enums.Function.to_json
        ),
    })
    unknown_1: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x00000004, original_name='Unknown 1'
        ),
    })
    unknown_2: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x00000005, original_name='Unknown 2'
        ),
    })
    unknown_3: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x00000006, original_name='Unknown 3'
        ),
    })
    unknown_4: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x00000007, original_name='Unknown 4'
        ),
    })
    unnamed_0x00000008: LayerSwitch = dataclasses.field(default_factory=LayerSwitch, metadata={
        'reflection': FieldReflection[LayerSwitch](
            LayerSwitch, id=0x00000008, original_name=None, from_json=LayerSwitch.from_json, to_json=LayerSwitch.to_json
        ),
    })
    unnamed_0x00000009: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam, metadata={
        'reflection': FieldReflection[enums.PlayerItem](
            enums.PlayerItem, id=0x00000009, original_name=None, from_json=enums.PlayerItem.from_json, to_json=enums.PlayerItem.to_json
        ),
    })
    active: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x0000000a, original_name='Active'
        ),
    })
    unknown_5: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0000000b, original_name='Unknown 5'
        ),
    })
    used_by_spinner_controller_1: int = dataclasses.field(default=0, metadata={
        'sound': True, 'reflection': FieldReflection[int](
            int, id=0x0000000c, original_name='Used by SpinnerController 1'
        ),
    })
    used_by_spinner_controller_2: int = dataclasses.field(default=0, metadata={
        'sound': True, 'reflection': FieldReflection[int](
            int, id=0x0000000d, original_name='Used by SpinnerController 2'
        ),
    })
    used_by_spinner_controller_3: int = dataclasses.field(default=0, metadata={
        'sound': True, 'reflection': FieldReflection[int](
            int, id=0x0000000e, original_name='Used by SpinnerController 3'
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
        return 0x3A

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        function = enums.Function.from_stream(data)
        unknown_1 = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000008 = LayerSwitch.from_stream(data, property_size)
        unnamed_0x00000009 = enums.PlayerItem.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        used_by_spinner_controller_1 = struct.unpack('>l', data.read(4))[0]
        used_by_spinner_controller_2 = struct.unpack('>l', data.read(4))[0]
        used_by_spinner_controller_3 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, rotation, function, unknown_1, unknown_2, unknown_3, unknown_4, unnamed_0x00000008, unnamed_0x00000009, active, unknown_5, used_by_spinner_controller_1, used_by_spinner_controller_2, used_by_spinner_controller_3)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0f')  # 15 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.function.to_stream(data)
        data.write(self.unknown_1.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        self.unnamed_0x00000008.to_stream(data)
        self.unnamed_0x00000009.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>l', self.used_by_spinner_controller_1))
        data.write(struct.pack('>l', self.used_by_spinner_controller_2))
        data.write(struct.pack('>l', self.used_by_spinner_controller_3))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SpecialFunctionJson", data)
        return cls(
            name=json_data['name'],
            position=Vector.from_json(json_data['position']),
            rotation=Vector.from_json(json_data['rotation']),
            function=enums.Function.from_json(json_data['function']),
            unknown_1=json_data['unknown_1'],
            unknown_2=json_data['unknown_2'],
            unknown_3=json_data['unknown_3'],
            unknown_4=json_data['unknown_4'],
            unnamed_0x00000008=LayerSwitch.from_json(json_data['unnamed_0x00000008']),
            unnamed_0x00000009=enums.PlayerItem.from_json(json_data['unnamed_0x00000009']),
            active=json_data['active'],
            unknown_5=json_data['unknown_5'],
            used_by_spinner_controller_1=json_data['used_by_spinner_controller_1'],
            used_by_spinner_controller_2=json_data['used_by_spinner_controller_2'],
            used_by_spinner_controller_3=json_data['used_by_spinner_controller_3'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'function': self.function.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'active': self.active,
            'unknown_5': self.unknown_5,
            'used_by_spinner_controller_1': self.used_by_spinner_controller_1,
            'used_by_spinner_controller_2': self.used_by_spinner_controller_2,
            'used_by_spinner_controller_3': self.used_by_spinner_controller_3,
        }

    def _dependencies_for_used_by_spinner_controller_1(self, asset_manager: AssetManager) -> typing.Iterator[Dependency]:
        yield from asset_manager.get_audio_group_dependency(self.used_by_spinner_controller_1)

    def _dependencies_for_used_by_spinner_controller_2(self, asset_manager: AssetManager) -> typing.Iterator[Dependency]:
        yield from asset_manager.get_audio_group_dependency(self.used_by_spinner_controller_2)

    def _dependencies_for_used_by_spinner_controller_3(self, asset_manager: AssetManager) -> typing.Iterator[Dependency]:
        yield from asset_manager.get_audio_group_dependency(self.used_by_spinner_controller_3)

    def dependencies_for(self, asset_manager: AssetManager) -> typing.Iterator[Dependency]:
        for method, field_name, field_type in [
            (self.unnamed_0x00000008.dependencies_for, "unnamed_0x00000008", "LayerSwitch"),
            (self._dependencies_for_used_by_spinner_controller_1, "used_by_spinner_controller_1", "int"),
            (self._dependencies_for_used_by_spinner_controller_2, "used_by_spinner_controller_2", "int"),
            (self._dependencies_for_used_by_spinner_controller_3, "used_by_spinner_controller_3", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpecialFunction.{field_name} ({field_type}): {e}"
                )

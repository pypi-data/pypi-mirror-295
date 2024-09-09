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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct254 import UnknownStruct254
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct255 import UnknownStruct255
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct257 import UnknownStruct257
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct258 import UnknownStruct258
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct259Json(typing_extensions.TypedDict):
        snap_to_spline: bool
        gravity: float
        unknown_0xee382651: float
        unknown_0x46b65220: float
        unknown_0xab417b5d: float
        unknown_0x0f4cb02a: float
        unknown_0x396bedd2: float
        unknown_0xe564f7b4: float
        unknown_0x8699ac03: float
        unknown_0x663174bc: float
        ground_pound_window: float
        ground_pound_relapse_multiplier: float
        unknown_0xcdeaba73: float
        grid_size: float
        grid_count: int
        unknown_0x2144c2e2: float
        unknown_0xc9292d7b: int
        unknown_0x12cbcdb4: bool
        render_push_amount: float
        unknown_0xcb065ea2: bool
        additive_state_machine: int
        unknown_0x06435aff: int
        unknown_0xb073b311: int
        unknown_0x719345cf: int
        spike_move_speed: float
        unknown_0x0483a338: int
        unknown_struct254: json_util.JsonObject
        unknown_struct255: json_util.JsonObject
        unknown_struct257: json_util.JsonObject
        unknown_struct258: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct259(BaseProperty):
    snap_to_spline: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x26ecb939, original_name='SnapToSpline'
        ),
    })
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    unknown_0xee382651: float = dataclasses.field(default=0.30000001192092896, metadata={
        'reflection': FieldReflection[float](
            float, id=0xee382651, original_name='Unknown'
        ),
    })
    unknown_0x46b65220: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x46b65220, original_name='Unknown'
        ),
    })
    unknown_0xab417b5d: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xab417b5d, original_name='Unknown'
        ),
    })
    unknown_0x0f4cb02a: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0f4cb02a, original_name='Unknown'
        ),
    })
    unknown_0x396bedd2: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x396bedd2, original_name='Unknown'
        ),
    })
    unknown_0xe564f7b4: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe564f7b4, original_name='Unknown'
        ),
    })
    unknown_0x8699ac03: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8699ac03, original_name='Unknown'
        ),
    })
    unknown_0x663174bc: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x663174bc, original_name='Unknown'
        ),
    })
    ground_pound_window: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x68d787b4, original_name='GroundPoundWindow'
        ),
    })
    ground_pound_relapse_multiplier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x686e030b, original_name='GroundPoundRelapseMultiplier'
        ),
    })
    unknown_0xcdeaba73: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcdeaba73, original_name='Unknown'
        ),
    })
    grid_size: float = dataclasses.field(default=2.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x904c4375, original_name='GridSize'
        ),
    })
    grid_count: int = dataclasses.field(default=12, metadata={
        'reflection': FieldReflection[int](
            int, id=0xe2aeebfb, original_name='GridCount'
        ),
    })
    unknown_0x2144c2e2: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2144c2e2, original_name='Unknown'
        ),
    })
    unknown_0xc9292d7b: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xc9292d7b, original_name='Unknown'
        ),
    })
    unknown_0x12cbcdb4: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x12cbcdb4, original_name='Unknown'
        ),
    })
    render_push_amount: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf496803d, original_name='RenderPushAmount'
        ),
    })
    unknown_0xcb065ea2: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcb065ea2, original_name='Unknown'
        ),
    })
    additive_state_machine: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FSMC'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3a9808cf, original_name='AdditiveStateMachine'
        ),
    })
    unknown_0x06435aff: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x06435aff, original_name='Unknown'
        ),
    })
    unknown_0xb073b311: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb073b311, original_name='Unknown'
        ),
    })
    unknown_0x719345cf: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x719345cf, original_name='Unknown'
        ),
    })
    spike_move_speed: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5b203cba, original_name='SpikeMoveSpeed'
        ),
    })
    unknown_0x0483a338: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x0483a338, original_name='Unknown'
        ),
    })
    unknown_struct254: UnknownStruct254 = dataclasses.field(default_factory=UnknownStruct254, metadata={
        'reflection': FieldReflection[UnknownStruct254](
            UnknownStruct254, id=0xe0dcfbbe, original_name='UnknownStruct254', from_json=UnknownStruct254.from_json, to_json=UnknownStruct254.to_json
        ),
    })
    unknown_struct255: UnknownStruct255 = dataclasses.field(default_factory=UnknownStruct255, metadata={
        'reflection': FieldReflection[UnknownStruct255](
            UnknownStruct255, id=0x2540a671, original_name='UnknownStruct255', from_json=UnknownStruct255.from_json, to_json=UnknownStruct255.to_json
        ),
    })
    unknown_struct257: UnknownStruct257 = dataclasses.field(default_factory=UnknownStruct257, metadata={
        'reflection': FieldReflection[UnknownStruct257](
            UnknownStruct257, id=0xaac2f8da, original_name='UnknownStruct257', from_json=UnknownStruct257.from_json, to_json=UnknownStruct257.to_json
        ),
    })
    unknown_struct258: UnknownStruct258 = dataclasses.field(default_factory=UnknownStruct258, metadata={
        'reflection': FieldReflection[UnknownStruct258](
            UnknownStruct258, id=0x17c3e3ec, original_name='UnknownStruct258', from_json=UnknownStruct258.from_json, to_json=UnknownStruct258.to_json
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
        if property_count != 30:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26ecb939
        snap_to_spline = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xee382651
        unknown_0xee382651 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46b65220
        unknown_0x46b65220 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab417b5d
        unknown_0xab417b5d = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0f4cb02a
        unknown_0x0f4cb02a = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x396bedd2
        unknown_0x396bedd2 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe564f7b4
        unknown_0xe564f7b4 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8699ac03
        unknown_0x8699ac03 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x663174bc
        unknown_0x663174bc = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68d787b4
        ground_pound_window = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x686e030b
        ground_pound_relapse_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcdeaba73
        unknown_0xcdeaba73 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x904c4375
        grid_size = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe2aeebfb
        grid_count = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2144c2e2
        unknown_0x2144c2e2 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc9292d7b
        unknown_0xc9292d7b = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x12cbcdb4
        unknown_0x12cbcdb4 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf496803d
        render_push_amount = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcb065ea2
        unknown_0xcb065ea2 = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a9808cf
        additive_state_machine = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x06435aff
        unknown_0x06435aff = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb073b311
        unknown_0xb073b311 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x719345cf
        unknown_0x719345cf = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5b203cba
        spike_move_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0483a338
        unknown_0x0483a338 = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe0dcfbbe
        unknown_struct254 = UnknownStruct254.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2540a671
        unknown_struct255 = UnknownStruct255.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaac2f8da
        unknown_struct257 = UnknownStruct257.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x17c3e3ec
        unknown_struct258 = UnknownStruct258.from_stream(data, property_size)
    
        return cls(snap_to_spline, gravity, unknown_0xee382651, unknown_0x46b65220, unknown_0xab417b5d, unknown_0x0f4cb02a, unknown_0x396bedd2, unknown_0xe564f7b4, unknown_0x8699ac03, unknown_0x663174bc, ground_pound_window, ground_pound_relapse_multiplier, unknown_0xcdeaba73, grid_size, grid_count, unknown_0x2144c2e2, unknown_0xc9292d7b, unknown_0x12cbcdb4, render_push_amount, unknown_0xcb065ea2, additive_state_machine, unknown_0x06435aff, unknown_0xb073b311, unknown_0x719345cf, spike_move_speed, unknown_0x0483a338, unknown_struct254, unknown_struct255, unknown_struct257, unknown_struct258)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1e')  # 30 properties

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xee8&Q')  # 0xee382651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xee382651))

        data.write(b'F\xb6R ')  # 0x46b65220
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x46b65220))

        data.write(b'\xabA{]')  # 0xab417b5d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xab417b5d))

        data.write(b'\x0fL\xb0*')  # 0xf4cb02a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0f4cb02a))

        data.write(b'9k\xed\xd2')  # 0x396bedd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x396bedd2))

        data.write(b'\xe5d\xf7\xb4')  # 0xe564f7b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe564f7b4))

        data.write(b'\x86\x99\xac\x03')  # 0x8699ac03
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8699ac03))

        data.write(b'f1t\xbc')  # 0x663174bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x663174bc))

        data.write(b'h\xd7\x87\xb4')  # 0x68d787b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_window))

        data.write(b'hn\x03\x0b')  # 0x686e030b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_relapse_multiplier))

        data.write(b'\xcd\xea\xbas')  # 0xcdeaba73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcdeaba73))

        data.write(b'\x90LCu')  # 0x904c4375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grid_size))

        data.write(b'\xe2\xae\xeb\xfb')  # 0xe2aeebfb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grid_count))

        data.write(b'!D\xc2\xe2')  # 0x2144c2e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2144c2e2))

        data.write(b'\xc9)-{')  # 0xc9292d7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc9292d7b))

        data.write(b'\x12\xcb\xcd\xb4')  # 0x12cbcdb4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x12cbcdb4))

        data.write(b'\xf4\x96\x80=')  # 0xf496803d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.render_push_amount))

        data.write(b'\xcb\x06^\xa2')  # 0xcb065ea2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcb065ea2))

        data.write(b':\x98\x08\xcf')  # 0x3a9808cf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.additive_state_machine))

        data.write(b'\x06CZ\xff')  # 0x6435aff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x06435aff))

        data.write(b'\xb0s\xb3\x11')  # 0xb073b311
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb073b311))

        data.write(b'q\x93E\xcf')  # 0x719345cf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x719345cf))

        data.write(b'[ <\xba')  # 0x5b203cba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spike_move_speed))

        data.write(b'\x04\x83\xa38')  # 0x483a338
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x0483a338))

        data.write(b'\xe0\xdc\xfb\xbe')  # 0xe0dcfbbe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct254.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%@\xa6q')  # 0x2540a671
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct255.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\xc2\xf8\xda')  # 0xaac2f8da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct257.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xc3\xe3\xec')  # 0x17c3e3ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct258.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct259Json", data)
        return cls(
            snap_to_spline=json_data['snap_to_spline'],
            gravity=json_data['gravity'],
            unknown_0xee382651=json_data['unknown_0xee382651'],
            unknown_0x46b65220=json_data['unknown_0x46b65220'],
            unknown_0xab417b5d=json_data['unknown_0xab417b5d'],
            unknown_0x0f4cb02a=json_data['unknown_0x0f4cb02a'],
            unknown_0x396bedd2=json_data['unknown_0x396bedd2'],
            unknown_0xe564f7b4=json_data['unknown_0xe564f7b4'],
            unknown_0x8699ac03=json_data['unknown_0x8699ac03'],
            unknown_0x663174bc=json_data['unknown_0x663174bc'],
            ground_pound_window=json_data['ground_pound_window'],
            ground_pound_relapse_multiplier=json_data['ground_pound_relapse_multiplier'],
            unknown_0xcdeaba73=json_data['unknown_0xcdeaba73'],
            grid_size=json_data['grid_size'],
            grid_count=json_data['grid_count'],
            unknown_0x2144c2e2=json_data['unknown_0x2144c2e2'],
            unknown_0xc9292d7b=json_data['unknown_0xc9292d7b'],
            unknown_0x12cbcdb4=json_data['unknown_0x12cbcdb4'],
            render_push_amount=json_data['render_push_amount'],
            unknown_0xcb065ea2=json_data['unknown_0xcb065ea2'],
            additive_state_machine=json_data['additive_state_machine'],
            unknown_0x06435aff=json_data['unknown_0x06435aff'],
            unknown_0xb073b311=json_data['unknown_0xb073b311'],
            unknown_0x719345cf=json_data['unknown_0x719345cf'],
            spike_move_speed=json_data['spike_move_speed'],
            unknown_0x0483a338=json_data['unknown_0x0483a338'],
            unknown_struct254=UnknownStruct254.from_json(json_data['unknown_struct254']),
            unknown_struct255=UnknownStruct255.from_json(json_data['unknown_struct255']),
            unknown_struct257=UnknownStruct257.from_json(json_data['unknown_struct257']),
            unknown_struct258=UnknownStruct258.from_json(json_data['unknown_struct258']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'snap_to_spline': self.snap_to_spline,
            'gravity': self.gravity,
            'unknown_0xee382651': self.unknown_0xee382651,
            'unknown_0x46b65220': self.unknown_0x46b65220,
            'unknown_0xab417b5d': self.unknown_0xab417b5d,
            'unknown_0x0f4cb02a': self.unknown_0x0f4cb02a,
            'unknown_0x396bedd2': self.unknown_0x396bedd2,
            'unknown_0xe564f7b4': self.unknown_0xe564f7b4,
            'unknown_0x8699ac03': self.unknown_0x8699ac03,
            'unknown_0x663174bc': self.unknown_0x663174bc,
            'ground_pound_window': self.ground_pound_window,
            'ground_pound_relapse_multiplier': self.ground_pound_relapse_multiplier,
            'unknown_0xcdeaba73': self.unknown_0xcdeaba73,
            'grid_size': self.grid_size,
            'grid_count': self.grid_count,
            'unknown_0x2144c2e2': self.unknown_0x2144c2e2,
            'unknown_0xc9292d7b': self.unknown_0xc9292d7b,
            'unknown_0x12cbcdb4': self.unknown_0x12cbcdb4,
            'render_push_amount': self.render_push_amount,
            'unknown_0xcb065ea2': self.unknown_0xcb065ea2,
            'additive_state_machine': self.additive_state_machine,
            'unknown_0x06435aff': self.unknown_0x06435aff,
            'unknown_0xb073b311': self.unknown_0xb073b311,
            'unknown_0x719345cf': self.unknown_0x719345cf,
            'spike_move_speed': self.spike_move_speed,
            'unknown_0x0483a338': self.unknown_0x0483a338,
            'unknown_struct254': self.unknown_struct254.to_json(),
            'unknown_struct255': self.unknown_struct255.to_json(),
            'unknown_struct257': self.unknown_struct257.to_json(),
            'unknown_struct258': self.unknown_struct258.to_json(),
        }


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xee382651(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x46b65220(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xab417b5d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0f4cb02a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x396bedd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe564f7b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8699ac03(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x663174bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_relapse_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcdeaba73(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grid_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grid_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2144c2e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc9292d7b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x12cbcdb4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_push_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcb065ea2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_additive_state_machine(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x06435aff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb073b311(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x719345cf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spike_move_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0483a338(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xee382651: ('unknown_0xee382651', _decode_unknown_0xee382651),
    0x46b65220: ('unknown_0x46b65220', _decode_unknown_0x46b65220),
    0xab417b5d: ('unknown_0xab417b5d', _decode_unknown_0xab417b5d),
    0xf4cb02a: ('unknown_0x0f4cb02a', _decode_unknown_0x0f4cb02a),
    0x396bedd2: ('unknown_0x396bedd2', _decode_unknown_0x396bedd2),
    0xe564f7b4: ('unknown_0xe564f7b4', _decode_unknown_0xe564f7b4),
    0x8699ac03: ('unknown_0x8699ac03', _decode_unknown_0x8699ac03),
    0x663174bc: ('unknown_0x663174bc', _decode_unknown_0x663174bc),
    0x68d787b4: ('ground_pound_window', _decode_ground_pound_window),
    0x686e030b: ('ground_pound_relapse_multiplier', _decode_ground_pound_relapse_multiplier),
    0xcdeaba73: ('unknown_0xcdeaba73', _decode_unknown_0xcdeaba73),
    0x904c4375: ('grid_size', _decode_grid_size),
    0xe2aeebfb: ('grid_count', _decode_grid_count),
    0x2144c2e2: ('unknown_0x2144c2e2', _decode_unknown_0x2144c2e2),
    0xc9292d7b: ('unknown_0xc9292d7b', _decode_unknown_0xc9292d7b),
    0x12cbcdb4: ('unknown_0x12cbcdb4', _decode_unknown_0x12cbcdb4),
    0xf496803d: ('render_push_amount', _decode_render_push_amount),
    0xcb065ea2: ('unknown_0xcb065ea2', _decode_unknown_0xcb065ea2),
    0x3a9808cf: ('additive_state_machine', _decode_additive_state_machine),
    0x6435aff: ('unknown_0x06435aff', _decode_unknown_0x06435aff),
    0xb073b311: ('unknown_0xb073b311', _decode_unknown_0xb073b311),
    0x719345cf: ('unknown_0x719345cf', _decode_unknown_0x719345cf),
    0x5b203cba: ('spike_move_speed', _decode_spike_move_speed),
    0x483a338: ('unknown_0x0483a338', _decode_unknown_0x0483a338),
    0xe0dcfbbe: ('unknown_struct254', UnknownStruct254.from_stream),
    0x2540a671: ('unknown_struct255', UnknownStruct255.from_stream),
    0xaac2f8da: ('unknown_struct257', UnknownStruct257.from_stream),
    0x17c3e3ec: ('unknown_struct258', UnknownStruct258.from_stream),
}

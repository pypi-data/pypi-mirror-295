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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class SwingLineBehaviorDataJson(typing_extensions.TypedDict):
        attach_to_line_locator_name: str
        line_end_point_locator_name: str
        swing_line_additive_length: float
        swing_line_dist_backwards: float
        swing_line_type: int
        swing_line_max_angle: float
        swing_line_length: float
        time_apex_to_apex: float
        start_position_time_scale: float
        orient_creature_with_line: bool
        jettison_line_scale_speed: float
        death_line_action: int
        curve_line_additive_scale: float
        curve_line_ramp_in_speed: float
        curve_line_ramp_out_speed: float
        curve_line_depart_apex_angle_to_ramp_in: float
        curve_line_approach_apex_angle_to_ramp_out: float
        curve_line_middle: bool
        dwell_dist_from_anchor: float
        dwell_time: float
        climb_down_distance: float
        climb_down_speed: float
        drop_at_line_end: bool
        drop_to_ground_rule: int
        hang_around_time: float
        climb_up_speed: float
        end_of_line_jiggle_scale: float
    

@dataclasses.dataclass()
class SwingLineBehaviorData(BaseProperty):
    attach_to_line_locator_name: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xa13a2bf2, original_name='AttachToLineLocatorName'
        ),
    })
    line_end_point_locator_name: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xf9edcf89, original_name='LineEndPointLocatorName'
        ),
    })
    swing_line_additive_length: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x589c9074, original_name='SwingLineAdditiveLength'
        ),
    })
    swing_line_dist_backwards: float = dataclasses.field(default=0.44999998807907104, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8563ee2a, original_name='SwingLineDistBackwards'
        ),
    })
    swing_line_type: enums.SwingLineType = dataclasses.field(default=enums.SwingLineType.Unknown1, metadata={
        'reflection': FieldReflection[enums.SwingLineType](
            enums.SwingLineType, id=0x1734f891, original_name='SwingLineType', from_json=enums.SwingLineType.from_json, to_json=enums.SwingLineType.to_json
        ),
    })
    swing_line_max_angle: float = dataclasses.field(default=60.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc02efbe3, original_name='SwingLineMaxAngle'
        ),
    })
    swing_line_length: float = dataclasses.field(default=2.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xee890a28, original_name='SwingLineLength'
        ),
    })
    time_apex_to_apex: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbbe1271e, original_name='TimeApexToApex'
        ),
    })
    start_position_time_scale: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf613102d, original_name='StartPositionTimeScale'
        ),
    })
    orient_creature_with_line: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x35ba52b1, original_name='OrientCreatureWithLine'
        ),
    })
    jettison_line_scale_speed: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe35ed218, original_name='JettisonLineScaleSpeed'
        ),
    })
    death_line_action: enums.DeathLineAction = dataclasses.field(default=enums.DeathLineAction.Unknown1, metadata={
        'reflection': FieldReflection[enums.DeathLineAction](
            enums.DeathLineAction, id=0x2037e511, original_name='DeathLineAction', from_json=enums.DeathLineAction.from_json, to_json=enums.DeathLineAction.to_json
        ),
    })
    curve_line_additive_scale: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x29640a2d, original_name='CurveLineAdditiveScale'
        ),
    })
    curve_line_ramp_in_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8468beb1, original_name='CurveLineRampInSpeed'
        ),
    })
    curve_line_ramp_out_speed: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x55ee3bf9, original_name='CurveLineRampOutSpeed'
        ),
    })
    curve_line_depart_apex_angle_to_ramp_in: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf8b1d183, original_name='CurveLineDepartApexAngleToRampIn'
        ),
    })
    curve_line_approach_apex_angle_to_ramp_out: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe127b113, original_name='CurveLineApproachApexAngleToRampOut'
        ),
    })
    curve_line_middle: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x43ca4653, original_name='CurveLineMiddle'
        ),
    })
    dwell_dist_from_anchor: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb37c9890, original_name='DwellDistFromAnchor'
        ),
    })
    dwell_time: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcdf7ceb9, original_name='DwellTime'
        ),
    })
    climb_down_distance: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe9084c1f, original_name='ClimbDownDistance'
        ),
    })
    climb_down_speed: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa47a7037, original_name='ClimbDownSpeed'
        ),
    })
    drop_at_line_end: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3aa64111, original_name='DropAtLineEnd'
        ),
    })
    drop_to_ground_rule: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4fa9f7c2, original_name='DropToGroundRule'
        ),
    })
    hang_around_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf5bee58e, original_name='HangAroundTime'
        ),
    })
    climb_up_speed: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe27604be, original_name='ClimbUpSpeed'
        ),
    })
    end_of_line_jiggle_scale: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xafe00ef0, original_name='EndOfLineJiggleScale'
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
        if property_count != 27:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa13a2bf2
        attach_to_line_locator_name = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf9edcf89
        line_end_point_locator_name = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x589c9074
        swing_line_additive_length = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8563ee2a
        swing_line_dist_backwards = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1734f891
        swing_line_type = enums.SwingLineType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc02efbe3
        swing_line_max_angle = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xee890a28
        swing_line_length = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbe1271e
        time_apex_to_apex = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf613102d
        start_position_time_scale = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x35ba52b1
        orient_creature_with_line = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe35ed218
        jettison_line_scale_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2037e511
        death_line_action = enums.DeathLineAction.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x29640a2d
        curve_line_additive_scale = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8468beb1
        curve_line_ramp_in_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x55ee3bf9
        curve_line_ramp_out_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf8b1d183
        curve_line_depart_apex_angle_to_ramp_in = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe127b113
        curve_line_approach_apex_angle_to_ramp_out = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43ca4653
        curve_line_middle = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb37c9890
        dwell_dist_from_anchor = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcdf7ceb9
        dwell_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9084c1f
        climb_down_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa47a7037
        climb_down_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3aa64111
        drop_at_line_end = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4fa9f7c2
        drop_to_ground_rule = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5bee58e
        hang_around_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe27604be
        climb_up_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xafe00ef0
        end_of_line_jiggle_scale = struct.unpack('>f', data.read(4))[0]
    
        return cls(attach_to_line_locator_name, line_end_point_locator_name, swing_line_additive_length, swing_line_dist_backwards, swing_line_type, swing_line_max_angle, swing_line_length, time_apex_to_apex, start_position_time_scale, orient_creature_with_line, jettison_line_scale_speed, death_line_action, curve_line_additive_scale, curve_line_ramp_in_speed, curve_line_ramp_out_speed, curve_line_depart_apex_angle_to_ramp_in, curve_line_approach_apex_angle_to_ramp_out, curve_line_middle, dwell_dist_from_anchor, dwell_time, climb_down_distance, climb_down_speed, drop_at_line_end, drop_to_ground_rule, hang_around_time, climb_up_speed, end_of_line_jiggle_scale)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'\xa1:+\xf2')  # 0xa13a2bf2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.attach_to_line_locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xed\xcf\x89')  # 0xf9edcf89
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.line_end_point_locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x9c\x90t')  # 0x589c9074
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_additive_length))

        data.write(b'\x85c\xee*')  # 0x8563ee2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_dist_backwards))

        data.write(b'\x174\xf8\x91')  # 0x1734f891
        data.write(b'\x00\x04')  # size
        self.swing_line_type.to_stream(data)

        data.write(b'\xc0.\xfb\xe3')  # 0xc02efbe3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_max_angle))

        data.write(b'\xee\x89\n(')  # 0xee890a28
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_length))

        data.write(b"\xbb\xe1'\x1e")  # 0xbbe1271e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_apex_to_apex))

        data.write(b'\xf6\x13\x10-')  # 0xf613102d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_position_time_scale))

        data.write(b'5\xbaR\xb1')  # 0x35ba52b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.orient_creature_with_line))

        data.write(b'\xe3^\xd2\x18')  # 0xe35ed218
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jettison_line_scale_speed))

        data.write(b' 7\xe5\x11')  # 0x2037e511
        data.write(b'\x00\x04')  # size
        self.death_line_action.to_stream(data)

        data.write(b')d\n-')  # 0x29640a2d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_additive_scale))

        data.write(b'\x84h\xbe\xb1')  # 0x8468beb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_ramp_in_speed))

        data.write(b'U\xee;\xf9')  # 0x55ee3bf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_ramp_out_speed))

        data.write(b'\xf8\xb1\xd1\x83')  # 0xf8b1d183
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_depart_apex_angle_to_ramp_in))

        data.write(b"\xe1'\xb1\x13")  # 0xe127b113
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_approach_apex_angle_to_ramp_out))

        data.write(b'C\xcaFS')  # 0x43ca4653
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.curve_line_middle))

        data.write(b'\xb3|\x98\x90')  # 0xb37c9890
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dwell_dist_from_anchor))

        data.write(b'\xcd\xf7\xce\xb9')  # 0xcdf7ceb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dwell_time))

        data.write(b'\xe9\x08L\x1f')  # 0xe9084c1f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_down_distance))

        data.write(b'\xa4zp7')  # 0xa47a7037
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_down_speed))

        data.write(b':\xa6A\x11')  # 0x3aa64111
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.drop_at_line_end))

        data.write(b'O\xa9\xf7\xc2')  # 0x4fa9f7c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.drop_to_ground_rule))

        data.write(b'\xf5\xbe\xe5\x8e')  # 0xf5bee58e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hang_around_time))

        data.write(b'\xe2v\x04\xbe')  # 0xe27604be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_up_speed))

        data.write(b'\xaf\xe0\x0e\xf0')  # 0xafe00ef0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.end_of_line_jiggle_scale))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SwingLineBehaviorDataJson", data)
        return cls(
            attach_to_line_locator_name=json_data['attach_to_line_locator_name'],
            line_end_point_locator_name=json_data['line_end_point_locator_name'],
            swing_line_additive_length=json_data['swing_line_additive_length'],
            swing_line_dist_backwards=json_data['swing_line_dist_backwards'],
            swing_line_type=enums.SwingLineType.from_json(json_data['swing_line_type']),
            swing_line_max_angle=json_data['swing_line_max_angle'],
            swing_line_length=json_data['swing_line_length'],
            time_apex_to_apex=json_data['time_apex_to_apex'],
            start_position_time_scale=json_data['start_position_time_scale'],
            orient_creature_with_line=json_data['orient_creature_with_line'],
            jettison_line_scale_speed=json_data['jettison_line_scale_speed'],
            death_line_action=enums.DeathLineAction.from_json(json_data['death_line_action']),
            curve_line_additive_scale=json_data['curve_line_additive_scale'],
            curve_line_ramp_in_speed=json_data['curve_line_ramp_in_speed'],
            curve_line_ramp_out_speed=json_data['curve_line_ramp_out_speed'],
            curve_line_depart_apex_angle_to_ramp_in=json_data['curve_line_depart_apex_angle_to_ramp_in'],
            curve_line_approach_apex_angle_to_ramp_out=json_data['curve_line_approach_apex_angle_to_ramp_out'],
            curve_line_middle=json_data['curve_line_middle'],
            dwell_dist_from_anchor=json_data['dwell_dist_from_anchor'],
            dwell_time=json_data['dwell_time'],
            climb_down_distance=json_data['climb_down_distance'],
            climb_down_speed=json_data['climb_down_speed'],
            drop_at_line_end=json_data['drop_at_line_end'],
            drop_to_ground_rule=json_data['drop_to_ground_rule'],
            hang_around_time=json_data['hang_around_time'],
            climb_up_speed=json_data['climb_up_speed'],
            end_of_line_jiggle_scale=json_data['end_of_line_jiggle_scale'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attach_to_line_locator_name': self.attach_to_line_locator_name,
            'line_end_point_locator_name': self.line_end_point_locator_name,
            'swing_line_additive_length': self.swing_line_additive_length,
            'swing_line_dist_backwards': self.swing_line_dist_backwards,
            'swing_line_type': self.swing_line_type.to_json(),
            'swing_line_max_angle': self.swing_line_max_angle,
            'swing_line_length': self.swing_line_length,
            'time_apex_to_apex': self.time_apex_to_apex,
            'start_position_time_scale': self.start_position_time_scale,
            'orient_creature_with_line': self.orient_creature_with_line,
            'jettison_line_scale_speed': self.jettison_line_scale_speed,
            'death_line_action': self.death_line_action.to_json(),
            'curve_line_additive_scale': self.curve_line_additive_scale,
            'curve_line_ramp_in_speed': self.curve_line_ramp_in_speed,
            'curve_line_ramp_out_speed': self.curve_line_ramp_out_speed,
            'curve_line_depart_apex_angle_to_ramp_in': self.curve_line_depart_apex_angle_to_ramp_in,
            'curve_line_approach_apex_angle_to_ramp_out': self.curve_line_approach_apex_angle_to_ramp_out,
            'curve_line_middle': self.curve_line_middle,
            'dwell_dist_from_anchor': self.dwell_dist_from_anchor,
            'dwell_time': self.dwell_time,
            'climb_down_distance': self.climb_down_distance,
            'climb_down_speed': self.climb_down_speed,
            'drop_at_line_end': self.drop_at_line_end,
            'drop_to_ground_rule': self.drop_to_ground_rule,
            'hang_around_time': self.hang_around_time,
            'climb_up_speed': self.climb_up_speed,
            'end_of_line_jiggle_scale': self.end_of_line_jiggle_scale,
        }


def _decode_attach_to_line_locator_name(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_line_end_point_locator_name(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_swing_line_additive_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_line_dist_backwards(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_line_type(data: typing.BinaryIO, property_size: int):
    return enums.SwingLineType.from_stream(data)


def _decode_swing_line_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_line_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_apex_to_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_position_time_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_orient_creature_with_line(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_jettison_line_scale_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_line_action(data: typing.BinaryIO, property_size: int):
    return enums.DeathLineAction.from_stream(data)


def _decode_curve_line_additive_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_ramp_in_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_ramp_out_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_depart_apex_angle_to_ramp_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_approach_apex_angle_to_ramp_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_middle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_dwell_dist_from_anchor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dwell_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_down_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_down_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_at_line_end(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_drop_to_ground_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hang_around_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_up_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_end_of_line_jiggle_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa13a2bf2: ('attach_to_line_locator_name', _decode_attach_to_line_locator_name),
    0xf9edcf89: ('line_end_point_locator_name', _decode_line_end_point_locator_name),
    0x589c9074: ('swing_line_additive_length', _decode_swing_line_additive_length),
    0x8563ee2a: ('swing_line_dist_backwards', _decode_swing_line_dist_backwards),
    0x1734f891: ('swing_line_type', _decode_swing_line_type),
    0xc02efbe3: ('swing_line_max_angle', _decode_swing_line_max_angle),
    0xee890a28: ('swing_line_length', _decode_swing_line_length),
    0xbbe1271e: ('time_apex_to_apex', _decode_time_apex_to_apex),
    0xf613102d: ('start_position_time_scale', _decode_start_position_time_scale),
    0x35ba52b1: ('orient_creature_with_line', _decode_orient_creature_with_line),
    0xe35ed218: ('jettison_line_scale_speed', _decode_jettison_line_scale_speed),
    0x2037e511: ('death_line_action', _decode_death_line_action),
    0x29640a2d: ('curve_line_additive_scale', _decode_curve_line_additive_scale),
    0x8468beb1: ('curve_line_ramp_in_speed', _decode_curve_line_ramp_in_speed),
    0x55ee3bf9: ('curve_line_ramp_out_speed', _decode_curve_line_ramp_out_speed),
    0xf8b1d183: ('curve_line_depart_apex_angle_to_ramp_in', _decode_curve_line_depart_apex_angle_to_ramp_in),
    0xe127b113: ('curve_line_approach_apex_angle_to_ramp_out', _decode_curve_line_approach_apex_angle_to_ramp_out),
    0x43ca4653: ('curve_line_middle', _decode_curve_line_middle),
    0xb37c9890: ('dwell_dist_from_anchor', _decode_dwell_dist_from_anchor),
    0xcdf7ceb9: ('dwell_time', _decode_dwell_time),
    0xe9084c1f: ('climb_down_distance', _decode_climb_down_distance),
    0xa47a7037: ('climb_down_speed', _decode_climb_down_speed),
    0x3aa64111: ('drop_at_line_end', _decode_drop_at_line_end),
    0x4fa9f7c2: ('drop_to_ground_rule', _decode_drop_to_ground_rule),
    0xf5bee58e: ('hang_around_time', _decode_hang_around_time),
    0xe27604be: ('climb_up_speed', _decode_climb_up_speed),
    0xafe00ef0: ('end_of_line_jiggle_scale', _decode_end_of_line_jiggle_scale),
}

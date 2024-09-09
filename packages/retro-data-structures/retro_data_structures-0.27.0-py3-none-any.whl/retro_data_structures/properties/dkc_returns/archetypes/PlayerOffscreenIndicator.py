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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerOffscreenIndicatorIconData import PlayerOffscreenIndicatorIconData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerOffscreenIndicatorTextData import PlayerOffscreenIndicatorTextData
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class PlayerOffscreenIndicatorJson(typing_extensions.TypedDict):
        offscreen_time_til_render: float
        offscreen_time_til_notify: float
        max_time_to_render: int
        max_time_to_sound_alert: int
        offscreen_timer_tick_sound: int
        offscreen_timer_alert_sound: int
        text: json_util.JsonObject
        icon: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerOffscreenIndicator(BaseProperty):
    offscreen_time_til_render: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0ccf3adf, original_name='OffscreenTimeTilRender'
        ),
    })
    offscreen_time_til_notify: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x46c5cb7a, original_name='OffscreenTimeTilNotify'
        ),
    })
    max_time_to_render: int = dataclasses.field(default=5, metadata={
        'reflection': FieldReflection[int](
            int, id=0x4988b02b, original_name='MaxTimeToRender'
        ),
    })
    max_time_to_sound_alert: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x47a8818b, original_name='MaxTimeToSoundAlert'
        ),
    })
    offscreen_timer_tick_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x17bf00f0, original_name='OffscreenTimerTickSound'
        ),
    })
    offscreen_timer_alert_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4868549d, original_name='OffscreenTimerAlertSound'
        ),
    })
    text: PlayerOffscreenIndicatorTextData = dataclasses.field(default_factory=PlayerOffscreenIndicatorTextData, metadata={
        'reflection': FieldReflection[PlayerOffscreenIndicatorTextData](
            PlayerOffscreenIndicatorTextData, id=0xa5b20d17, original_name='Text', from_json=PlayerOffscreenIndicatorTextData.from_json, to_json=PlayerOffscreenIndicatorTextData.to_json
        ),
    })
    icon: PlayerOffscreenIndicatorIconData = dataclasses.field(default_factory=PlayerOffscreenIndicatorIconData, metadata={
        'reflection': FieldReflection[PlayerOffscreenIndicatorIconData](
            PlayerOffscreenIndicatorIconData, id=0xe7bb8978, original_name='Icon', from_json=PlayerOffscreenIndicatorIconData.from_json, to_json=PlayerOffscreenIndicatorIconData.to_json
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
        if property_count != 8:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0ccf3adf
        offscreen_time_til_render = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46c5cb7a
        offscreen_time_til_notify = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4988b02b
        max_time_to_render = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47a8818b
        max_time_to_sound_alert = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x17bf00f0
        offscreen_timer_tick_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4868549d
        offscreen_timer_alert_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa5b20d17
        text = PlayerOffscreenIndicatorTextData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe7bb8978
        icon = PlayerOffscreenIndicatorIconData.from_stream(data, property_size)
    
        return cls(offscreen_time_til_render, offscreen_time_til_notify, max_time_to_render, max_time_to_sound_alert, offscreen_timer_tick_sound, offscreen_timer_alert_sound, text, icon)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x0c\xcf:\xdf')  # 0xccf3adf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.offscreen_time_til_render))

        data.write(b'F\xc5\xcbz')  # 0x46c5cb7a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.offscreen_time_til_notify))

        data.write(b'I\x88\xb0+')  # 0x4988b02b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_time_to_render))

        data.write(b'G\xa8\x81\x8b')  # 0x47a8818b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_time_to_sound_alert))

        data.write(b'\x17\xbf\x00\xf0')  # 0x17bf00f0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.offscreen_timer_tick_sound))

        data.write(b'HhT\x9d')  # 0x4868549d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.offscreen_timer_alert_sound))

        data.write(b'\xa5\xb2\r\x17')  # 0xa5b20d17
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.text.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xbb\x89x')  # 0xe7bb8978
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.icon.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerOffscreenIndicatorJson", data)
        return cls(
            offscreen_time_til_render=json_data['offscreen_time_til_render'],
            offscreen_time_til_notify=json_data['offscreen_time_til_notify'],
            max_time_to_render=json_data['max_time_to_render'],
            max_time_to_sound_alert=json_data['max_time_to_sound_alert'],
            offscreen_timer_tick_sound=json_data['offscreen_timer_tick_sound'],
            offscreen_timer_alert_sound=json_data['offscreen_timer_alert_sound'],
            text=PlayerOffscreenIndicatorTextData.from_json(json_data['text']),
            icon=PlayerOffscreenIndicatorIconData.from_json(json_data['icon']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'offscreen_time_til_render': self.offscreen_time_til_render,
            'offscreen_time_til_notify': self.offscreen_time_til_notify,
            'max_time_to_render': self.max_time_to_render,
            'max_time_to_sound_alert': self.max_time_to_sound_alert,
            'offscreen_timer_tick_sound': self.offscreen_timer_tick_sound,
            'offscreen_timer_alert_sound': self.offscreen_timer_alert_sound,
            'text': self.text.to_json(),
            'icon': self.icon.to_json(),
        }


def _decode_offscreen_time_til_render(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_offscreen_time_til_notify(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_time_to_render(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_time_to_sound_alert(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_offscreen_timer_tick_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_offscreen_timer_alert_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xccf3adf: ('offscreen_time_til_render', _decode_offscreen_time_til_render),
    0x46c5cb7a: ('offscreen_time_til_notify', _decode_offscreen_time_til_notify),
    0x4988b02b: ('max_time_to_render', _decode_max_time_to_render),
    0x47a8818b: ('max_time_to_sound_alert', _decode_max_time_to_sound_alert),
    0x17bf00f0: ('offscreen_timer_tick_sound', _decode_offscreen_timer_tick_sound),
    0x4868549d: ('offscreen_timer_alert_sound', _decode_offscreen_timer_alert_sound),
    0xa5b20d17: ('text', PlayerOffscreenIndicatorTextData.from_stream),
    0xe7bb8978: ('icon', PlayerOffscreenIndicatorIconData.from_stream),
}

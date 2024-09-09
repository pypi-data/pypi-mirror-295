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
from retro_data_structures.properties.dkc_returns.archetypes.PlayerType import PlayerType
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class PlayerCommonDataJson(typing_extensions.TypedDict):
        player: int
        anim_scale: float
        character_type: json_util.JsonObject
        ledge_assist_step_up_height: float
        gravity: float
        terminal_velocity: float
        invulnerable_time: float
        invulnerable_blink_time: float
        damage_knock_back_input_disable_time: float
        respawn_render_push_amount: float
        use_terrain_alignment: bool
        allow_collision_with_mine_cart_tracks: bool
        allow_death_delete: bool
        respawn_sound: int
        respawn_effect: int
    

@dataclasses.dataclass()
class PlayerCommonData(BaseProperty):
    player: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x96f89702, original_name='Player'
        ),
    })
    anim_scale: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1878fa08, original_name='AnimScale'
        ),
    })
    character_type: PlayerType = dataclasses.field(default_factory=PlayerType, metadata={
        'reflection': FieldReflection[PlayerType](
            PlayerType, id=0x013e35fb, original_name='CharacterType', from_json=PlayerType.from_json, to_json=PlayerType.to_json
        ),
    })
    ledge_assist_step_up_height: float = dataclasses.field(default=0.949999988079071, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa21fb5ce, original_name='LedgeAssistStepUpHeight'
        ),
    })
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    terminal_velocity: float = dataclasses.field(default=35.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xab9566a2, original_name='TerminalVelocity'
        ),
    })
    invulnerable_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xac015a47, original_name='InvulnerableTime'
        ),
    })
    invulnerable_blink_time: float = dataclasses.field(default=0.125, metadata={
        'reflection': FieldReflection[float](
            float, id=0x48be7880, original_name='InvulnerableBlinkTime'
        ),
    })
    damage_knock_back_input_disable_time: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9743637b, original_name='DamageKnockBackInputDisableTime'
        ),
    })
    respawn_render_push_amount: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb198e731, original_name='RespawnRenderPushAmount'
        ),
    })
    use_terrain_alignment: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6117e78f, original_name='UseTerrainAlignment'
        ),
    })
    allow_collision_with_mine_cart_tracks: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x917b5ad5, original_name='AllowCollisionWithMineCartTracks'
        ),
    })
    allow_death_delete: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7b363100, original_name='AllowDeathDelete'
        ),
    })
    respawn_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2e50dcec, original_name='RespawnSound'
        ),
    })
    respawn_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4b65999c, original_name='RespawnEffect'
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
        if property_count != 15:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x96f89702
        player = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1878fa08
        anim_scale = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x013e35fb
        character_type = PlayerType.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa21fb5ce
        ledge_assist_step_up_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab9566a2
        terminal_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xac015a47
        invulnerable_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x48be7880
        invulnerable_blink_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9743637b
        damage_knock_back_input_disable_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb198e731
        respawn_render_push_amount = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6117e78f
        use_terrain_alignment = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x917b5ad5
        allow_collision_with_mine_cart_tracks = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b363100
        allow_death_delete = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e50dcec
        respawn_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4b65999c
        respawn_effect = struct.unpack(">Q", data.read(8))[0]
    
        return cls(player, anim_scale, character_type, ledge_assist_step_up_height, gravity, terminal_velocity, invulnerable_time, invulnerable_blink_time, damage_knock_back_input_disable_time, respawn_render_push_amount, use_terrain_alignment, allow_collision_with_mine_cart_tracks, allow_death_delete, respawn_sound, respawn_effect)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x96\xf8\x97\x02')  # 0x96f89702
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.player))

        data.write(b'\x18x\xfa\x08')  # 0x1878fa08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anim_scale))

        data.write(b'\x01>5\xfb')  # 0x13e35fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\x1f\xb5\xce')  # 0xa21fb5ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ledge_assist_step_up_height))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xab\x95f\xa2')  # 0xab9566a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terminal_velocity))

        data.write(b'\xac\x01ZG')  # 0xac015a47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.invulnerable_time))

        data.write(b'H\xbex\x80')  # 0x48be7880
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.invulnerable_blink_time))

        data.write(b'\x97Cc{')  # 0x9743637b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_knock_back_input_disable_time))

        data.write(b'\xb1\x98\xe71')  # 0xb198e731
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_render_push_amount))

        data.write(b'a\x17\xe7\x8f')  # 0x6117e78f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_terrain_alignment))

        data.write(b'\x91{Z\xd5')  # 0x917b5ad5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_collision_with_mine_cart_tracks))

        data.write(b'{61\x00')  # 0x7b363100
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_death_delete))

        data.write(b'.P\xdc\xec')  # 0x2e50dcec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.respawn_sound))

        data.write(b'Ke\x99\x9c')  # 0x4b65999c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.respawn_effect))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerCommonDataJson", data)
        return cls(
            player=json_data['player'],
            anim_scale=json_data['anim_scale'],
            character_type=PlayerType.from_json(json_data['character_type']),
            ledge_assist_step_up_height=json_data['ledge_assist_step_up_height'],
            gravity=json_data['gravity'],
            terminal_velocity=json_data['terminal_velocity'],
            invulnerable_time=json_data['invulnerable_time'],
            invulnerable_blink_time=json_data['invulnerable_blink_time'],
            damage_knock_back_input_disable_time=json_data['damage_knock_back_input_disable_time'],
            respawn_render_push_amount=json_data['respawn_render_push_amount'],
            use_terrain_alignment=json_data['use_terrain_alignment'],
            allow_collision_with_mine_cart_tracks=json_data['allow_collision_with_mine_cart_tracks'],
            allow_death_delete=json_data['allow_death_delete'],
            respawn_sound=json_data['respawn_sound'],
            respawn_effect=json_data['respawn_effect'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'player': self.player,
            'anim_scale': self.anim_scale,
            'character_type': self.character_type.to_json(),
            'ledge_assist_step_up_height': self.ledge_assist_step_up_height,
            'gravity': self.gravity,
            'terminal_velocity': self.terminal_velocity,
            'invulnerable_time': self.invulnerable_time,
            'invulnerable_blink_time': self.invulnerable_blink_time,
            'damage_knock_back_input_disable_time': self.damage_knock_back_input_disable_time,
            'respawn_render_push_amount': self.respawn_render_push_amount,
            'use_terrain_alignment': self.use_terrain_alignment,
            'allow_collision_with_mine_cart_tracks': self.allow_collision_with_mine_cart_tracks,
            'allow_death_delete': self.allow_death_delete,
            'respawn_sound': self.respawn_sound,
            'respawn_effect': self.respawn_effect,
        }


def _decode_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_anim_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ledge_assist_step_up_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terminal_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_invulnerable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_invulnerable_blink_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_knock_back_input_disable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_respawn_render_push_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_terrain_alignment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_collision_with_mine_cart_tracks(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_death_delete(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_respawn_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_respawn_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x96f89702: ('player', _decode_player),
    0x1878fa08: ('anim_scale', _decode_anim_scale),
    0x13e35fb: ('character_type', PlayerType.from_stream),
    0xa21fb5ce: ('ledge_assist_step_up_height', _decode_ledge_assist_step_up_height),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xab9566a2: ('terminal_velocity', _decode_terminal_velocity),
    0xac015a47: ('invulnerable_time', _decode_invulnerable_time),
    0x48be7880: ('invulnerable_blink_time', _decode_invulnerable_blink_time),
    0x9743637b: ('damage_knock_back_input_disable_time', _decode_damage_knock_back_input_disable_time),
    0xb198e731: ('respawn_render_push_amount', _decode_respawn_render_push_amount),
    0x6117e78f: ('use_terrain_alignment', _decode_use_terrain_alignment),
    0x917b5ad5: ('allow_collision_with_mine_cart_tracks', _decode_allow_collision_with_mine_cart_tracks),
    0x7b363100: ('allow_death_delete', _decode_allow_death_delete),
    0x2e50dcec: ('respawn_sound', _decode_respawn_sound),
    0x4b65999c: ('respawn_effect', _decode_respawn_effect),
}

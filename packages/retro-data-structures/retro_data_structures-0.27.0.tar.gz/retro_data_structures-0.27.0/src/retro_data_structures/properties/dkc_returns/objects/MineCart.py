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
from retro_data_structures.properties.dkc_returns.archetypes.MineCartData import MineCartData
from retro_data_structures.properties.dkc_returns.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.dkc_returns.archetypes.PlayerCommonData import PlayerCommonData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerJumpData import PlayerJumpData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountData import PlayerMountData
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMountRiderList import PlayerMountRiderList
from retro_data_structures.properties.dkc_returns.archetypes.PlayerMultiKillRewardData import PlayerMultiKillRewardData
from retro_data_structures.properties.dkc_returns.archetypes.ShadowData import ShadowData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct import UnknownStruct

if typing.TYPE_CHECKING:
    class MineCartJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        patterned: json_util.JsonObject
        shadow_data: json_util.JsonObject
        actor_information: json_util.JsonObject
        unknown_struct: json_util.JsonObject
        common: json_util.JsonObject
        jump_data: json_util.JsonObject
        multi_kill_reward_data: json_util.JsonObject
        mount_data: json_util.JsonObject
        rider_list_data: json_util.JsonObject
        mine_cart_data: json_util.JsonObject
    

@dataclasses.dataclass()
class MineCart(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef, metadata={
        'reflection': FieldReflection[PatternedAITypedef](
            PatternedAITypedef, id=0xb3774750, original_name='Patterned', from_json=PatternedAITypedef.from_json, to_json=PatternedAITypedef.to_json
        ),
    })
    shadow_data: ShadowData = dataclasses.field(default_factory=ShadowData, metadata={
        'reflection': FieldReflection[ShadowData](
            ShadowData, id=0xbf81c83e, original_name='ShadowData', from_json=ShadowData.from_json, to_json=ShadowData.to_json
        ),
    })
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters, metadata={
        'reflection': FieldReflection[ActorParameters](
            ActorParameters, id=0x7e397fed, original_name='ActorInformation', from_json=ActorParameters.from_json, to_json=ActorParameters.to_json
        ),
    })
    unknown_struct: UnknownStruct = dataclasses.field(default_factory=UnknownStruct, metadata={
        'reflection': FieldReflection[UnknownStruct](
            UnknownStruct, id=0x0063f638, original_name='UnknownStruct', from_json=UnknownStruct.from_json, to_json=UnknownStruct.to_json
        ),
    })
    common: PlayerCommonData = dataclasses.field(default_factory=PlayerCommonData, metadata={
        'reflection': FieldReflection[PlayerCommonData](
            PlayerCommonData, id=0x3c38498d, original_name='Common', from_json=PlayerCommonData.from_json, to_json=PlayerCommonData.to_json
        ),
    })
    jump_data: PlayerJumpData = dataclasses.field(default_factory=PlayerJumpData, metadata={
        'reflection': FieldReflection[PlayerJumpData](
            PlayerJumpData, id=0xf07bec6d, original_name='JumpData', from_json=PlayerJumpData.from_json, to_json=PlayerJumpData.to_json
        ),
    })
    multi_kill_reward_data: PlayerMultiKillRewardData = dataclasses.field(default_factory=PlayerMultiKillRewardData, metadata={
        'reflection': FieldReflection[PlayerMultiKillRewardData](
            PlayerMultiKillRewardData, id=0x98efc863, original_name='MultiKillRewardData', from_json=PlayerMultiKillRewardData.from_json, to_json=PlayerMultiKillRewardData.to_json
        ),
    })
    mount_data: PlayerMountData = dataclasses.field(default_factory=PlayerMountData, metadata={
        'reflection': FieldReflection[PlayerMountData](
            PlayerMountData, id=0x978e5bd8, original_name='MountData', from_json=PlayerMountData.from_json, to_json=PlayerMountData.to_json
        ),
    })
    rider_list_data: PlayerMountRiderList = dataclasses.field(default_factory=PlayerMountRiderList, metadata={
        'reflection': FieldReflection[PlayerMountRiderList](
            PlayerMountRiderList, id=0x7f681411, original_name='RiderListData', from_json=PlayerMountRiderList.from_json, to_json=PlayerMountRiderList.to_json
        ),
    })
    mine_cart_data: MineCartData = dataclasses.field(default_factory=MineCartData, metadata={
        'reflection': FieldReflection[MineCartData](
            MineCartData, id=0xd7326912, original_name='MineCartData', from_json=MineCartData.from_json, to_json=MineCartData.to_json
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
        return 'CART'

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
        if property_count != 11:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb3774750
        patterned = PatternedAITypedef.from_stream(data, property_size, default_override={'collision_radius': 0.699999988079071, 'collision_height': 1.0})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf81c83e
        shadow_data = ShadowData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e397fed
        actor_information = ActorParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0063f638
        unknown_struct = UnknownStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3c38498d
        common = PlayerCommonData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf07bec6d
        jump_data = PlayerJumpData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x98efc863
        multi_kill_reward_data = PlayerMultiKillRewardData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x978e5bd8
        mount_data = PlayerMountData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7f681411
        rider_list_data = PlayerMountRiderList.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd7326912
        mine_cart_data = MineCartData.from_stream(data, property_size)
    
        return cls(editor_properties, patterned, shadow_data, actor_information, unknown_struct, common, jump_data, multi_kill_reward_data, mount_data, rider_list_data, mine_cart_data)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'collision_radius': 0.699999988079071, 'collision_height': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x81\xc8>')  # 0xbf81c83e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shadow_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00c\xf68')  # 0x63f638
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<8I\x8d')  # 0x3c38498d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.common.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0{\xecm')  # 0xf07bec6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xef\xc8c')  # 0x98efc863
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.multi_kill_reward_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\x8e[\xd8')  # 0x978e5bd8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mount_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7fh\x14\x11')  # 0x7f681411
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rider_list_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd72i\x12')  # 0xd7326912
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mine_cart_data.to_stream(data)
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
        json_data = typing.cast("MineCartJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            patterned=PatternedAITypedef.from_json(json_data['patterned']),
            shadow_data=ShadowData.from_json(json_data['shadow_data']),
            actor_information=ActorParameters.from_json(json_data['actor_information']),
            unknown_struct=UnknownStruct.from_json(json_data['unknown_struct']),
            common=PlayerCommonData.from_json(json_data['common']),
            jump_data=PlayerJumpData.from_json(json_data['jump_data']),
            multi_kill_reward_data=PlayerMultiKillRewardData.from_json(json_data['multi_kill_reward_data']),
            mount_data=PlayerMountData.from_json(json_data['mount_data']),
            rider_list_data=PlayerMountRiderList.from_json(json_data['rider_list_data']),
            mine_cart_data=MineCartData.from_json(json_data['mine_cart_data']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'shadow_data': self.shadow_data.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_struct': self.unknown_struct.to_json(),
            'common': self.common.to_json(),
            'jump_data': self.jump_data.to_json(),
            'multi_kill_reward_data': self.multi_kill_reward_data.to_json(),
            'mount_data': self.mount_data.to_json(),
            'rider_list_data': self.rider_list_data.to_json(),
            'mine_cart_data': self.mine_cart_data.to_json(),
        }


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'collision_radius': 0.699999988079071, 'collision_height': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xb3774750: ('patterned', _decode_patterned),
    0xbf81c83e: ('shadow_data', ShadowData.from_stream),
    0x7e397fed: ('actor_information', ActorParameters.from_stream),
    0x63f638: ('unknown_struct', UnknownStruct.from_stream),
    0x3c38498d: ('common', PlayerCommonData.from_stream),
    0xf07bec6d: ('jump_data', PlayerJumpData.from_stream),
    0x98efc863: ('multi_kill_reward_data', PlayerMultiKillRewardData.from_stream),
    0x978e5bd8: ('mount_data', PlayerMountData.from_stream),
    0x7f681411: ('rider_list_data', PlayerMountRiderList.from_stream),
    0xd7326912: ('mine_cart_data', MineCartData.from_stream),
}

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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class PickupDataJson(typing_extensions.TypedDict):
        item_to_give: int
        capacity_increase: int
        item_percentage_increase: int
        amount: int
        unknown_0x39262bce: int
        respawn_time: float
        lifetime: float
        fadetime: float
        fade_out_time: float
        activation_delay: float
        unknown_0x059fefc5: float
        flying_pickup_speed: float
        flying_pickup_target_scale: json_util.JsonValue
        flying_pickup_model: int
        flying_pickup_effect: int
        pickup_effect: int
        touched_sound_effect: int
        caud: int
        unknown_0xdb5b110d: int
        unknown_0x5dcf63a3: int
        unknown_0x9693b006: int
        ghost_touched_sound_effect: int
        unknown_0x2cf86398: int
        unknown_0x93d41865: int
        unknown_0x15406acb: int
        unknown_0xde1cb96e: int
        texture_set: int
        auto_spin: bool
        blink_out: bool
        unknown_0x69539dfc: bool
        can_render_sort: bool
        unknown_0x4ddc1327: bool
        render_in_foreground: bool
        pickup_delay: float
        unknown_0xe722238d: bool
        unknown_0xfc7cfe9b: bool
        unknown_0xea3675c5: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xa02ef0c4, 0x28c71b54, 0x165ab069, 0x94af1445, 0x39262bce, 0xf7fbaaa5, 0x32dc67f6, 0x56e3ceef, 0x7c269ebc, 0xe585f166, 0x59fefc5, 0x4cd4343a, 0x2f5456a7, 0xed398efb, 0xe1cb9ec7, 0xa9fe872a, 0x371cd734, 0xaa125f90, 0xdb5b110d, 0x5dcf63a3, 0x9693b006, 0x1e093b02, 0x2cf86398, 0x93d41865, 0x15406acb, 0xde1cb96e, 0x6b40acef, 0x961c0d17, 0xa755eb02, 0x69539dfc, 0x85cea266, 0x4ddc1327, 0xa6aa06d5, 0xbc96214f, 0xe722238d, 0xfc7cfe9b, 0xea3675c5)


@dataclasses.dataclass()
class PickupData(BaseProperty):
    item_to_give: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana, metadata={
        'reflection': FieldReflection[enums.PlayerItem](
            enums.PlayerItem, id=0xa02ef0c4, original_name='ItemToGive', from_json=enums.PlayerItem.from_json, to_json=enums.PlayerItem.to_json
        ),
    })
    capacity_increase: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x28c71b54, original_name='CapacityIncrease'
        ),
    })
    item_percentage_increase: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x165ab069, original_name='ItemPercentageIncrease'
        ),
    })
    amount: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x94af1445, original_name='Amount'
        ),
    })
    unknown_0x39262bce: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x39262bce, original_name='Unknown'
        ),
    })
    respawn_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf7fbaaa5, original_name='RespawnTime'
        ),
    })
    lifetime: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x32dc67f6, original_name='Lifetime'
        ),
    })
    fadetime: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x56e3ceef, original_name='Fadetime'
        ),
    })
    fade_out_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7c269ebc, original_name='FadeOutTime'
        ),
    })
    activation_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe585f166, original_name='ActivationDelay'
        ),
    })
    unknown_0x059fefc5: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x059fefc5, original_name='Unknown'
        ),
    })
    flying_pickup_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4cd4343a, original_name='FlyingPickupSpeed'
        ),
    })
    flying_pickup_target_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x2f5456a7, original_name='FlyingPickupTargetScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    flying_pickup_model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xed398efb, original_name='FlyingPickupModel'
        ),
    })
    flying_pickup_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe1cb9ec7, original_name='FlyingPickupEffect'
        ),
    })
    pickup_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa9fe872a, original_name='PickupEffect'
        ),
    })
    touched_sound_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x371cd734, original_name='TouchedSoundEffect'
        ),
    })
    caud: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xaa125f90, original_name='CAUD'
        ),
    })
    unknown_0xdb5b110d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xdb5b110d, original_name='Unknown'
        ),
    })
    unknown_0x5dcf63a3: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5dcf63a3, original_name='Unknown'
        ),
    })
    unknown_0x9693b006: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x9693b006, original_name='Unknown'
        ),
    })
    ghost_touched_sound_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1e093b02, original_name='GhostTouchedSoundEffect'
        ),
    })
    unknown_0x2cf86398: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2cf86398, original_name='Unknown'
        ),
    })
    unknown_0x93d41865: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x93d41865, original_name='Unknown'
        ),
    })
    unknown_0x15406acb: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x15406acb, original_name='Unknown'
        ),
    })
    unknown_0xde1cb96e: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xde1cb96e, original_name='Unknown'
        ),
    })
    texture_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6b40acef, original_name='TextureSet'
        ),
    })
    auto_spin: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x961c0d17, original_name='AutoSpin'
        ),
    })
    blink_out: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa755eb02, original_name='BlinkOut'
        ),
    })
    unknown_0x69539dfc: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x69539dfc, original_name='Unknown'
        ),
    })
    can_render_sort: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x85cea266, original_name='CanRenderSort'
        ),
    })
    unknown_0x4ddc1327: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4ddc1327, original_name='Unknown'
        ),
    })
    render_in_foreground: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa6aa06d5, original_name='RenderInForeground'
        ),
    })
    pickup_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbc96214f, original_name='PickupDelay'
        ),
    })
    unknown_0xe722238d: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe722238d, original_name='Unknown'
        ),
    })
    unknown_0xfc7cfe9b: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xfc7cfe9b, original_name='Unknown'
        ),
    })
    unknown_0xea3675c5: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xea3675c5, original_name='Unknown'
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
        if property_count != 37:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHLLHlLHlLHlLHlLHfLHfLHfLHfLHfLHfLHfLHfffLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHlLH?LH?LH?LH?LH?LH?LHfLH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(403))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[41], dec[44], dec[47], dec[50], dec[53], dec[56], dec[59], dec[62], dec[65], dec[68], dec[71], dec[74], dec[77], dec[80], dec[83], dec[86], dec[89], dec[92], dec[95], dec[98], dec[101], dec[104], dec[107], dec[110]) == _FAST_IDS
        return cls(
            enums.PlayerItem(dec[2]),
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
            dec[29],
            dec[32],
            dec[35],
            Vector(*dec[38:41]),
            dec[43],
            dec[46],
            dec[49],
            dec[52],
            dec[55],
            dec[58],
            dec[61],
            dec[64],
            dec[67],
            dec[70],
            dec[73],
            dec[76],
            dec[79],
            dec[82],
            dec[85],
            dec[88],
            dec[91],
            dec[94],
            dec[97],
            dec[100],
            dec[103],
            dec[106],
            dec[109],
            dec[112],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00%')  # 37 properties

        data.write(b'\xa0.\xf0\xc4')  # 0xa02ef0c4
        data.write(b'\x00\x04')  # size
        self.item_to_give.to_stream(data)

        data.write(b'(\xc7\x1bT')  # 0x28c71b54
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.capacity_increase))

        data.write(b'\x16Z\xb0i')  # 0x165ab069
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.item_percentage_increase))

        data.write(b'\x94\xaf\x14E')  # 0x94af1445
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.amount))

        data.write(b'9&+\xce')  # 0x39262bce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x39262bce))

        data.write(b'\xf7\xfb\xaa\xa5')  # 0xf7fbaaa5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_time))

        data.write(b'2\xdcg\xf6')  # 0x32dc67f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lifetime))

        data.write(b'V\xe3\xce\xef')  # 0x56e3ceef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fadetime))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xe5\x85\xf1f')  # 0xe585f166
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_delay))

        data.write(b'\x05\x9f\xef\xc5')  # 0x59fefc5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x059fefc5))

        data.write(b'L\xd44:')  # 0x4cd4343a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flying_pickup_speed))

        data.write(b'/TV\xa7')  # 0x2f5456a7
        data.write(b'\x00\x0c')  # size
        self.flying_pickup_target_scale.to_stream(data)

        data.write(b'\xed9\x8e\xfb')  # 0xed398efb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flying_pickup_model))

        data.write(b'\xe1\xcb\x9e\xc7')  # 0xe1cb9ec7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flying_pickup_effect))

        data.write(b'\xa9\xfe\x87*')  # 0xa9fe872a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pickup_effect))

        data.write(b'7\x1c\xd74')  # 0x371cd734
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.touched_sound_effect))

        data.write(b'\xaa\x12_\x90')  # 0xaa125f90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xdb[\x11\r')  # 0xdb5b110d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xdb5b110d))

        data.write(b']\xcfc\xa3')  # 0x5dcf63a3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x5dcf63a3))

        data.write(b'\x96\x93\xb0\x06')  # 0x9693b006
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x9693b006))

        data.write(b'\x1e\t;\x02')  # 0x1e093b02
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ghost_touched_sound_effect))

        data.write(b',\xf8c\x98')  # 0x2cf86398
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x2cf86398))

        data.write(b'\x93\xd4\x18e')  # 0x93d41865
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x93d41865))

        data.write(b'\x15@j\xcb')  # 0x15406acb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x15406acb))

        data.write(b'\xde\x1c\xb9n')  # 0xde1cb96e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xde1cb96e))

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'\x96\x1c\r\x17')  # 0x961c0d17
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_spin))

        data.write(b'\xa7U\xeb\x02')  # 0xa755eb02
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.blink_out))

        data.write(b'iS\x9d\xfc')  # 0x69539dfc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x69539dfc))

        data.write(b'\x85\xce\xa2f')  # 0x85cea266
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_render_sort))

        data.write(b"M\xdc\x13'")  # 0x4ddc1327
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4ddc1327))

        data.write(b'\xa6\xaa\x06\xd5')  # 0xa6aa06d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_in_foreground))

        data.write(b'\xbc\x96!O')  # 0xbc96214f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pickup_delay))

        data.write(b'\xe7"#\x8d')  # 0xe722238d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xe722238d))

        data.write(b'\xfc|\xfe\x9b')  # 0xfc7cfe9b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xfc7cfe9b))

        data.write(b'\xea6u\xc5')  # 0xea3675c5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xea3675c5))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PickupDataJson", data)
        return cls(
            item_to_give=enums.PlayerItem.from_json(json_data['item_to_give']),
            capacity_increase=json_data['capacity_increase'],
            item_percentage_increase=json_data['item_percentage_increase'],
            amount=json_data['amount'],
            unknown_0x39262bce=json_data['unknown_0x39262bce'],
            respawn_time=json_data['respawn_time'],
            lifetime=json_data['lifetime'],
            fadetime=json_data['fadetime'],
            fade_out_time=json_data['fade_out_time'],
            activation_delay=json_data['activation_delay'],
            unknown_0x059fefc5=json_data['unknown_0x059fefc5'],
            flying_pickup_speed=json_data['flying_pickup_speed'],
            flying_pickup_target_scale=Vector.from_json(json_data['flying_pickup_target_scale']),
            flying_pickup_model=json_data['flying_pickup_model'],
            flying_pickup_effect=json_data['flying_pickup_effect'],
            pickup_effect=json_data['pickup_effect'],
            touched_sound_effect=json_data['touched_sound_effect'],
            caud=json_data['caud'],
            unknown_0xdb5b110d=json_data['unknown_0xdb5b110d'],
            unknown_0x5dcf63a3=json_data['unknown_0x5dcf63a3'],
            unknown_0x9693b006=json_data['unknown_0x9693b006'],
            ghost_touched_sound_effect=json_data['ghost_touched_sound_effect'],
            unknown_0x2cf86398=json_data['unknown_0x2cf86398'],
            unknown_0x93d41865=json_data['unknown_0x93d41865'],
            unknown_0x15406acb=json_data['unknown_0x15406acb'],
            unknown_0xde1cb96e=json_data['unknown_0xde1cb96e'],
            texture_set=json_data['texture_set'],
            auto_spin=json_data['auto_spin'],
            blink_out=json_data['blink_out'],
            unknown_0x69539dfc=json_data['unknown_0x69539dfc'],
            can_render_sort=json_data['can_render_sort'],
            unknown_0x4ddc1327=json_data['unknown_0x4ddc1327'],
            render_in_foreground=json_data['render_in_foreground'],
            pickup_delay=json_data['pickup_delay'],
            unknown_0xe722238d=json_data['unknown_0xe722238d'],
            unknown_0xfc7cfe9b=json_data['unknown_0xfc7cfe9b'],
            unknown_0xea3675c5=json_data['unknown_0xea3675c5'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'item_to_give': self.item_to_give.to_json(),
            'capacity_increase': self.capacity_increase,
            'item_percentage_increase': self.item_percentage_increase,
            'amount': self.amount,
            'unknown_0x39262bce': self.unknown_0x39262bce,
            'respawn_time': self.respawn_time,
            'lifetime': self.lifetime,
            'fadetime': self.fadetime,
            'fade_out_time': self.fade_out_time,
            'activation_delay': self.activation_delay,
            'unknown_0x059fefc5': self.unknown_0x059fefc5,
            'flying_pickup_speed': self.flying_pickup_speed,
            'flying_pickup_target_scale': self.flying_pickup_target_scale.to_json(),
            'flying_pickup_model': self.flying_pickup_model,
            'flying_pickup_effect': self.flying_pickup_effect,
            'pickup_effect': self.pickup_effect,
            'touched_sound_effect': self.touched_sound_effect,
            'caud': self.caud,
            'unknown_0xdb5b110d': self.unknown_0xdb5b110d,
            'unknown_0x5dcf63a3': self.unknown_0x5dcf63a3,
            'unknown_0x9693b006': self.unknown_0x9693b006,
            'ghost_touched_sound_effect': self.ghost_touched_sound_effect,
            'unknown_0x2cf86398': self.unknown_0x2cf86398,
            'unknown_0x93d41865': self.unknown_0x93d41865,
            'unknown_0x15406acb': self.unknown_0x15406acb,
            'unknown_0xde1cb96e': self.unknown_0xde1cb96e,
            'texture_set': self.texture_set,
            'auto_spin': self.auto_spin,
            'blink_out': self.blink_out,
            'unknown_0x69539dfc': self.unknown_0x69539dfc,
            'can_render_sort': self.can_render_sort,
            'unknown_0x4ddc1327': self.unknown_0x4ddc1327,
            'render_in_foreground': self.render_in_foreground,
            'pickup_delay': self.pickup_delay,
            'unknown_0xe722238d': self.unknown_0xe722238d,
            'unknown_0xfc7cfe9b': self.unknown_0xfc7cfe9b,
            'unknown_0xea3675c5': self.unknown_0xea3675c5,
        }


def _decode_item_to_give(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_capacity_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_item_percentage_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x39262bce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_respawn_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fadetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activation_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x059fefc5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flying_pickup_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flying_pickup_target_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_flying_pickup_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flying_pickup_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_pickup_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_touched_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xdb5b110d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x5dcf63a3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x9693b006(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ghost_touched_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x2cf86398(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x93d41865(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x15406acb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xde1cb96e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_auto_spin(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_blink_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x69539dfc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_render_sort(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4ddc1327(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_in_foreground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pickup_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe722238d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xfc7cfe9b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xea3675c5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa02ef0c4: ('item_to_give', _decode_item_to_give),
    0x28c71b54: ('capacity_increase', _decode_capacity_increase),
    0x165ab069: ('item_percentage_increase', _decode_item_percentage_increase),
    0x94af1445: ('amount', _decode_amount),
    0x39262bce: ('unknown_0x39262bce', _decode_unknown_0x39262bce),
    0xf7fbaaa5: ('respawn_time', _decode_respawn_time),
    0x32dc67f6: ('lifetime', _decode_lifetime),
    0x56e3ceef: ('fadetime', _decode_fadetime),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xe585f166: ('activation_delay', _decode_activation_delay),
    0x59fefc5: ('unknown_0x059fefc5', _decode_unknown_0x059fefc5),
    0x4cd4343a: ('flying_pickup_speed', _decode_flying_pickup_speed),
    0x2f5456a7: ('flying_pickup_target_scale', _decode_flying_pickup_target_scale),
    0xed398efb: ('flying_pickup_model', _decode_flying_pickup_model),
    0xe1cb9ec7: ('flying_pickup_effect', _decode_flying_pickup_effect),
    0xa9fe872a: ('pickup_effect', _decode_pickup_effect),
    0x371cd734: ('touched_sound_effect', _decode_touched_sound_effect),
    0xaa125f90: ('caud', _decode_caud),
    0xdb5b110d: ('unknown_0xdb5b110d', _decode_unknown_0xdb5b110d),
    0x5dcf63a3: ('unknown_0x5dcf63a3', _decode_unknown_0x5dcf63a3),
    0x9693b006: ('unknown_0x9693b006', _decode_unknown_0x9693b006),
    0x1e093b02: ('ghost_touched_sound_effect', _decode_ghost_touched_sound_effect),
    0x2cf86398: ('unknown_0x2cf86398', _decode_unknown_0x2cf86398),
    0x93d41865: ('unknown_0x93d41865', _decode_unknown_0x93d41865),
    0x15406acb: ('unknown_0x15406acb', _decode_unknown_0x15406acb),
    0xde1cb96e: ('unknown_0xde1cb96e', _decode_unknown_0xde1cb96e),
    0x6b40acef: ('texture_set', _decode_texture_set),
    0x961c0d17: ('auto_spin', _decode_auto_spin),
    0xa755eb02: ('blink_out', _decode_blink_out),
    0x69539dfc: ('unknown_0x69539dfc', _decode_unknown_0x69539dfc),
    0x85cea266: ('can_render_sort', _decode_can_render_sort),
    0x4ddc1327: ('unknown_0x4ddc1327', _decode_unknown_0x4ddc1327),
    0xa6aa06d5: ('render_in_foreground', _decode_render_in_foreground),
    0xbc96214f: ('pickup_delay', _decode_pickup_delay),
    0xe722238d: ('unknown_0xe722238d', _decode_unknown_0xe722238d),
    0xfc7cfe9b: ('unknown_0xfc7cfe9b', _decode_unknown_0xfc7cfe9b),
    0xea3675c5: ('unknown_0xea3675c5', _decode_unknown_0xea3675c5),
}

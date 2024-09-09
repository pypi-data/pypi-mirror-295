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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct175Json(typing_extensions.TypedDict):
        gui_frame: int
        unknown_struct27: json_util.JsonObject
        title: int
        file: int
        empty: int
        back: int
        back_core: int
        copy: int
        erase: int
        copy_button_sound: int
        erase_button_sound: int
        copy_sound: int
        erase_sound: int
        unknown_0x7666757e: int
        unknown_0x59743f72: int
        unknown_0xabc95500: int
        unknown_0xfe60dcdf: int
        confirm_erase: int
        unknown_0x3a127e2d: int
        confirm_copy: int
        unknown_0xa03d67df: int
        unknown_0xfe4cb2bc: int
        unknown_0xaade9068: int
        unknown_0xf14d911d: int
        unknown_0xaedbcc3d: int
        area_characters: int
        level_characters: int
        unknown_0x6af2a9fb: int
        unknown_struct28: json_util.JsonObject
        text_background: int
    

@dataclasses.dataclass()
class UnknownStruct175(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27, metadata={
        'reflection': FieldReflection[UnknownStruct27](
            UnknownStruct27, id=0x73e2819b, original_name='UnknownStruct27', from_json=UnknownStruct27.from_json, to_json=UnknownStruct27.to_json
        ),
    })
    title: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa4f20c17, original_name='Title'
        ),
    })
    file: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xab783f75, original_name='File'
        ),
    })
    empty: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x951da97e, original_name='Empty'
        ),
    })
    back: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe9336455, original_name='Back'
        ),
    })
    back_core: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x770bcd3b, original_name='BackCore'
        ),
    })
    copy: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf3ea47e7, original_name='Copy'
        ),
    })
    erase: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe7c6e905, original_name='Erase'
        ),
    })
    copy_button_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7ac5b370, original_name='CopyButtonSound'
        ),
    })
    erase_button_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x2e39dd12, original_name='EraseButtonSound'
        ),
    })
    copy_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x22128d84, original_name='CopySound'
        ),
    })
    erase_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc24b1fdc, original_name='EraseSound'
        ),
    })
    unknown_0x7666757e: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7666757e, original_name='Unknown'
        ),
    })
    unknown_0x59743f72: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x59743f72, original_name='Unknown'
        ),
    })
    unknown_0xabc95500: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xabc95500, original_name='Unknown'
        ),
    })
    unknown_0xfe60dcdf: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xfe60dcdf, original_name='Unknown'
        ),
    })
    confirm_erase: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x75d129e8, original_name='ConfirmErase'
        ),
    })
    unknown_0x3a127e2d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x3a127e2d, original_name='Unknown'
        ),
    })
    confirm_copy: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x36a4312b, original_name='ConfirmCopy'
        ),
    })
    unknown_0xa03d67df: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa03d67df, original_name='Unknown'
        ),
    })
    unknown_0xfe4cb2bc: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xfe4cb2bc, original_name='Unknown'
        ),
    })
    unknown_0xaade9068: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xaade9068, original_name='Unknown'
        ),
    })
    unknown_0xf14d911d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf14d911d, original_name='Unknown'
        ),
    })
    unknown_0xaedbcc3d: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xaedbcc3d, original_name='Unknown'
        ),
    })
    area_characters: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb0d747b5, original_name='AreaCharacters'
        ),
    })
    level_characters: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4eca6603, original_name='LevelCharacters'
        ),
    })
    unknown_0x6af2a9fb: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x6af2a9fb, original_name='Unknown'
        ),
    })
    unknown_struct28: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28, metadata={
        'reflection': FieldReflection[UnknownStruct28](
            UnknownStruct28, id=0x5365cf39, original_name='UnknownStruct28', from_json=UnknownStruct28.from_json, to_json=UnknownStruct28.to_json
        ),
    })
    text_background: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['TXTR'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe119319b, original_name='TextBackground'
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
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x73e2819b
        unknown_struct27 = UnknownStruct27.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa4f20c17
        title = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xab783f75
        file = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x951da97e
        empty = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9336455
        back = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x770bcd3b
        back_core = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf3ea47e7
        copy = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe7c6e905
        erase = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7ac5b370
        copy_button_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e39dd12
        erase_button_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x22128d84
        copy_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc24b1fdc
        erase_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7666757e
        unknown_0x7666757e = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59743f72
        unknown_0x59743f72 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xabc95500
        unknown_0xabc95500 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe60dcdf
        unknown_0xfe60dcdf = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x75d129e8
        confirm_erase = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3a127e2d
        unknown_0x3a127e2d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x36a4312b
        confirm_copy = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa03d67df
        unknown_0xa03d67df = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfe4cb2bc
        unknown_0xfe4cb2bc = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaade9068
        unknown_0xaade9068 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf14d911d
        unknown_0xf14d911d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaedbcc3d
        unknown_0xaedbcc3d = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0d747b5
        area_characters = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4eca6603
        level_characters = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6af2a9fb
        unknown_0x6af2a9fb = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5365cf39
        unknown_struct28 = UnknownStruct28.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe119319b
        text_background = struct.unpack(">Q", data.read(8))[0]
    
        return cls(gui_frame, unknown_struct27, title, file, empty, back, back_core, copy, erase, copy_button_sound, erase_button_sound, copy_sound, erase_sound, unknown_0x7666757e, unknown_0x59743f72, unknown_0xabc95500, unknown_0xfe60dcdf, confirm_erase, unknown_0x3a127e2d, confirm_copy, unknown_0xa03d67df, unknown_0xfe4cb2bc, unknown_0xaade9068, unknown_0xf14d911d, unknown_0xaedbcc3d, area_characters, level_characters, unknown_0x6af2a9fb, unknown_struct28, text_background)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x1e')  # 30 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\xabx?u')  # 0xab783f75
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.file))

        data.write(b'\x95\x1d\xa9~')  # 0x951da97e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.empty))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\xf3\xeaG\xe7')  # 0xf3ea47e7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.copy))

        data.write(b'\xe7\xc6\xe9\x05')  # 0xe7c6e905
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.erase))

        data.write(b'z\xc5\xb3p')  # 0x7ac5b370
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.copy_button_sound))

        data.write(b'.9\xdd\x12')  # 0x2e39dd12
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.erase_button_sound))

        data.write(b'"\x12\x8d\x84')  # 0x22128d84
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.copy_sound))

        data.write(b'\xc2K\x1f\xdc')  # 0xc24b1fdc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.erase_sound))

        data.write(b'vfu~')  # 0x7666757e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x7666757e))

        data.write(b'Yt?r')  # 0x59743f72
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x59743f72))

        data.write(b'\xab\xc9U\x00')  # 0xabc95500
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xabc95500))

        data.write(b'\xfe`\xdc\xdf')  # 0xfe60dcdf
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xfe60dcdf))

        data.write(b'u\xd1)\xe8')  # 0x75d129e8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.confirm_erase))

        data.write(b':\x12~-')  # 0x3a127e2d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x3a127e2d))

        data.write(b'6\xa41+')  # 0x36a4312b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.confirm_copy))

        data.write(b'\xa0=g\xdf')  # 0xa03d67df
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xa03d67df))

        data.write(b'\xfeL\xb2\xbc')  # 0xfe4cb2bc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xfe4cb2bc))

        data.write(b'\xaa\xde\x90h')  # 0xaade9068
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xaade9068))

        data.write(b'\xf1M\x91\x1d')  # 0xf14d911d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xf14d911d))

        data.write(b'\xae\xdb\xcc=')  # 0xaedbcc3d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xaedbcc3d))

        data.write(b'\xb0\xd7G\xb5')  # 0xb0d747b5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.area_characters))

        data.write(b'N\xcaf\x03')  # 0x4eca6603
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.level_characters))

        data.write(b'j\xf2\xa9\xfb')  # 0x6af2a9fb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x6af2a9fb))

        data.write(b'Se\xcf9')  # 0x5365cf39
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct175Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            unknown_struct27=UnknownStruct27.from_json(json_data['unknown_struct27']),
            title=json_data['title'],
            file=json_data['file'],
            empty=json_data['empty'],
            back=json_data['back'],
            back_core=json_data['back_core'],
            copy=json_data['copy'],
            erase=json_data['erase'],
            copy_button_sound=json_data['copy_button_sound'],
            erase_button_sound=json_data['erase_button_sound'],
            copy_sound=json_data['copy_sound'],
            erase_sound=json_data['erase_sound'],
            unknown_0x7666757e=json_data['unknown_0x7666757e'],
            unknown_0x59743f72=json_data['unknown_0x59743f72'],
            unknown_0xabc95500=json_data['unknown_0xabc95500'],
            unknown_0xfe60dcdf=json_data['unknown_0xfe60dcdf'],
            confirm_erase=json_data['confirm_erase'],
            unknown_0x3a127e2d=json_data['unknown_0x3a127e2d'],
            confirm_copy=json_data['confirm_copy'],
            unknown_0xa03d67df=json_data['unknown_0xa03d67df'],
            unknown_0xfe4cb2bc=json_data['unknown_0xfe4cb2bc'],
            unknown_0xaade9068=json_data['unknown_0xaade9068'],
            unknown_0xf14d911d=json_data['unknown_0xf14d911d'],
            unknown_0xaedbcc3d=json_data['unknown_0xaedbcc3d'],
            area_characters=json_data['area_characters'],
            level_characters=json_data['level_characters'],
            unknown_0x6af2a9fb=json_data['unknown_0x6af2a9fb'],
            unknown_struct28=UnknownStruct28.from_json(json_data['unknown_struct28']),
            text_background=json_data['text_background'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'title': self.title,
            'file': self.file,
            'empty': self.empty,
            'back': self.back,
            'back_core': self.back_core,
            'copy': self.copy,
            'erase': self.erase,
            'copy_button_sound': self.copy_button_sound,
            'erase_button_sound': self.erase_button_sound,
            'copy_sound': self.copy_sound,
            'erase_sound': self.erase_sound,
            'unknown_0x7666757e': self.unknown_0x7666757e,
            'unknown_0x59743f72': self.unknown_0x59743f72,
            'unknown_0xabc95500': self.unknown_0xabc95500,
            'unknown_0xfe60dcdf': self.unknown_0xfe60dcdf,
            'confirm_erase': self.confirm_erase,
            'unknown_0x3a127e2d': self.unknown_0x3a127e2d,
            'confirm_copy': self.confirm_copy,
            'unknown_0xa03d67df': self.unknown_0xa03d67df,
            'unknown_0xfe4cb2bc': self.unknown_0xfe4cb2bc,
            'unknown_0xaade9068': self.unknown_0xaade9068,
            'unknown_0xf14d911d': self.unknown_0xf14d911d,
            'unknown_0xaedbcc3d': self.unknown_0xaedbcc3d,
            'area_characters': self.area_characters,
            'level_characters': self.level_characters,
            'unknown_0x6af2a9fb': self.unknown_0x6af2a9fb,
            'unknown_struct28': self.unknown_struct28.to_json(),
            'text_background': self.text_background,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_file(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_empty(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_copy(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_erase(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_copy_button_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_erase_button_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_copy_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_erase_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x7666757e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x59743f72(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xabc95500(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xfe60dcdf(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_confirm_erase(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x3a127e2d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_confirm_copy(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xa03d67df(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xfe4cb2bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xaade9068(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xf14d911d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xaedbcc3d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_area_characters(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_level_characters(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x6af2a9fb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', UnknownStruct27.from_stream),
    0xa4f20c17: ('title', _decode_title),
    0xab783f75: ('file', _decode_file),
    0x951da97e: ('empty', _decode_empty),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0xf3ea47e7: ('copy', _decode_copy),
    0xe7c6e905: ('erase', _decode_erase),
    0x7ac5b370: ('copy_button_sound', _decode_copy_button_sound),
    0x2e39dd12: ('erase_button_sound', _decode_erase_button_sound),
    0x22128d84: ('copy_sound', _decode_copy_sound),
    0xc24b1fdc: ('erase_sound', _decode_erase_sound),
    0x7666757e: ('unknown_0x7666757e', _decode_unknown_0x7666757e),
    0x59743f72: ('unknown_0x59743f72', _decode_unknown_0x59743f72),
    0xabc95500: ('unknown_0xabc95500', _decode_unknown_0xabc95500),
    0xfe60dcdf: ('unknown_0xfe60dcdf', _decode_unknown_0xfe60dcdf),
    0x75d129e8: ('confirm_erase', _decode_confirm_erase),
    0x3a127e2d: ('unknown_0x3a127e2d', _decode_unknown_0x3a127e2d),
    0x36a4312b: ('confirm_copy', _decode_confirm_copy),
    0xa03d67df: ('unknown_0xa03d67df', _decode_unknown_0xa03d67df),
    0xfe4cb2bc: ('unknown_0xfe4cb2bc', _decode_unknown_0xfe4cb2bc),
    0xaade9068: ('unknown_0xaade9068', _decode_unknown_0xaade9068),
    0xf14d911d: ('unknown_0xf14d911d', _decode_unknown_0xf14d911d),
    0xaedbcc3d: ('unknown_0xaedbcc3d', _decode_unknown_0xaedbcc3d),
    0xb0d747b5: ('area_characters', _decode_area_characters),
    0x4eca6603: ('level_characters', _decode_level_characters),
    0x6af2a9fb: ('unknown_0x6af2a9fb', _decode_unknown_0x6af2a9fb),
    0x5365cf39: ('unknown_struct28', UnknownStruct28.from_stream),
    0xe119319b: ('text_background', _decode_text_background),
}

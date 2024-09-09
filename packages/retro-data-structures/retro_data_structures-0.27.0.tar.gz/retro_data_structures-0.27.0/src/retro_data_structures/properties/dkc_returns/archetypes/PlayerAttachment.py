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
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters

if typing.TYPE_CHECKING:
    class PlayerAttachmentJson(typing_extensions.TypedDict):
        attachment_model: json_util.JsonObject
        attachment_locator: str
        unknown: bool
    

@dataclasses.dataclass()
class PlayerAttachment(BaseProperty):
    attachment_model: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0x520ebb68, original_name='AttachmentModel', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    attachment_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xe856fc2b, original_name='AttachmentLocator'
        ),
    })
    unknown: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x2662929f, original_name='Unknown'
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
        if property_count != 3:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x520ebb68
        attachment_model = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe856fc2b
        attachment_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2662929f
        unknown = struct.unpack('>?', data.read(1))[0]
    
        return cls(attachment_model, attachment_locator, unknown)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'R\x0e\xbbh')  # 0x520ebb68
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment_model.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe8V\xfc+')  # 0xe856fc2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.attachment_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&b\x92\x9f')  # 0x2662929f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerAttachmentJson", data)
        return cls(
            attachment_model=AnimationParameters.from_json(json_data['attachment_model']),
            attachment_locator=json_data['attachment_locator'],
            unknown=json_data['unknown'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attachment_model': self.attachment_model.to_json(),
            'attachment_locator': self.attachment_locator,
            'unknown': self.unknown,
        }


def _decode_attachment_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x520ebb68: ('attachment_model', AnimationParameters.from_stream),
    0xe856fc2b: ('attachment_locator', _decode_attachment_locator),
    0x2662929f: ('unknown', _decode_unknown),
}

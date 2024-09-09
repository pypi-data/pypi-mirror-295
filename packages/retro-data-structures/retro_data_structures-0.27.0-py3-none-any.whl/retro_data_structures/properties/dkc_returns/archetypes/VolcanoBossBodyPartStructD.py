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

if typing.TYPE_CHECKING:
    class VolcanoBossBodyPartStructDJson(typing_extensions.TypedDict):
        unknown_0x0f099933: int
        unknown_0xe8a3c283: str
    

@dataclasses.dataclass()
class VolcanoBossBodyPartStructD(BaseProperty):
    unknown_0x0f099933: enums.Unknown = dataclasses.field(default=enums.Unknown.Unknown7, metadata={
        'reflection': FieldReflection[enums.Unknown](
            enums.Unknown, id=0x0f099933, original_name='Unknown', from_json=enums.Unknown.from_json, to_json=enums.Unknown.to_json
        ),
    })
    unknown_0xe8a3c283: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xe8a3c283, original_name='Unknown'
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
        if property_count != 2:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0f099933
        unknown_0x0f099933 = enums.Unknown.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe8a3c283
        unknown_0xe8a3c283 = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(unknown_0x0f099933, unknown_0xe8a3c283)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x0f\t\x993')  # 0xf099933
        data.write(b'\x00\x04')  # size
        self.unknown_0x0f099933.to_stream(data)

        data.write(b'\xe8\xa3\xc2\x83')  # 0xe8a3c283
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xe8a3c283.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("VolcanoBossBodyPartStructDJson", data)
        return cls(
            unknown_0x0f099933=enums.Unknown.from_json(json_data['unknown_0x0f099933']),
            unknown_0xe8a3c283=json_data['unknown_0xe8a3c283'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x0f099933': self.unknown_0x0f099933.to_json(),
            'unknown_0xe8a3c283': self.unknown_0xe8a3c283,
        }


def _decode_unknown_0x0f099933(data: typing.BinaryIO, property_size: int):
    return enums.Unknown.from_stream(data)


def _decode_unknown_0xe8a3c283(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf099933: ('unknown_0x0f099933', _decode_unknown_0x0f099933),
    0xe8a3c283: ('unknown_0xe8a3c283', _decode_unknown_0xe8a3c283),
}

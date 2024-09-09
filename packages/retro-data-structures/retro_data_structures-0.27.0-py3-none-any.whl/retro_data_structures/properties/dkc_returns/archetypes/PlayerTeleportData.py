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
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence

if typing.TYPE_CHECKING:
    class PlayerTeleportDataJson(typing_extensions.TypedDict):
        teleport_to_locator: str
        teleport_render_push_amount: float
        teleport_method: json_util.JsonObject
    

@dataclasses.dataclass()
class PlayerTeleportData(BaseProperty):
    teleport_to_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xa6ab8644, original_name='TeleportToLocator'
        ),
    })
    teleport_render_push_amount: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4a3bceb4, original_name='TeleportRenderPushAmount'
        ),
    })
    teleport_method: Convergence = dataclasses.field(default_factory=Convergence, metadata={
        'reflection': FieldReflection[Convergence](
            Convergence, id=0xa0647df6, original_name='TeleportMethod', from_json=Convergence.from_json, to_json=Convergence.to_json
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
        assert property_id == 0xa6ab8644
        teleport_to_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4a3bceb4
        teleport_render_push_amount = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa0647df6
        teleport_method = Convergence.from_stream(data, property_size)
    
        return cls(teleport_to_locator, teleport_render_push_amount, teleport_method)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xa6\xab\x86D')  # 0xa6ab8644
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.teleport_to_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J;\xce\xb4')  # 0x4a3bceb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.teleport_render_push_amount))

        data.write(b'\xa0d}\xf6')  # 0xa0647df6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.teleport_method.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerTeleportDataJson", data)
        return cls(
            teleport_to_locator=json_data['teleport_to_locator'],
            teleport_render_push_amount=json_data['teleport_render_push_amount'],
            teleport_method=Convergence.from_json(json_data['teleport_method']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'teleport_to_locator': self.teleport_to_locator,
            'teleport_render_push_amount': self.teleport_render_push_amount,
            'teleport_method': self.teleport_method.to_json(),
        }


def _decode_teleport_to_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_teleport_render_push_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa6ab8644: ('teleport_to_locator', _decode_teleport_to_locator),
    0x4a3bceb4: ('teleport_render_push_amount', _decode_teleport_render_push_amount),
    0xa0647df6: ('teleport_method', Convergence.from_stream),
}

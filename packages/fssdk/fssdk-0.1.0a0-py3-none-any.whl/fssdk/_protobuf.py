from google.protobuf.internal.encoder import _VarintBytes

from ._cli import CLI
from .protobuf import flipper_pb2

class Protobuf:
    _cli: CLI = None
    _seq: int = 0

    def __init__(self, cli: CLI):
        self._cli = cli

    def send(self, data, command: str, has_next: bool = None, seq: int = None) -> int:
        message = flipper_pb2.Main()

        if seq is None:
            self._seq += 1
            message.command_id = self._seq
        else:
            message.command_id = seq

        message.command_status = flipper_pb2.CommandStatus.Value('OK')

        if has_next:
            message.has_next = has_next

        getattr(message, command).CopyFrom(data)

        size = message.ByteSize()
        raw_data = bytearray(
            _VarintBytes(size) + message.SerializeToString()
        )

        self._cli.write(raw_data)

        return message.command_id

    def send_and_read_answer(self, data, command: str, has_next: bool = False, seq: int = None) -> flipper_pb2.Main:
        command_id = self.send(data, command, has_next, seq)
        
        return self.read_answer(command_id)

    def read_answer(self, seq: int = None) -> flipper_pb2.Main:
        command_id = self._seq if seq is None else seq

        while True:
            data = self.read_any()

            if data.command_id == command_id:
                return data

    def read_any(self) -> flipper_pb2.Main:
        length = self._read_varint_32()
        raw_data = self._cli.read(length)

        data = flipper_pb2.Main()

        data.ParseFromString(raw_data)

        return data

    def _read_varint_32(self) -> int:
        MASK = (1 << 32) - 1

        result = 0
        shift = 0

        while True:
            raw_data = self._cli.read(1)

            data = int.from_bytes(raw_data, byteorder='little', signed=False)
            result |= (data & 0x7F) << shift

            if not data & 0x80:
                result &= MASK
                result = int(result)

                return result
            shift += 7

            if shift >= 64:
                raise Varint32Exception('Too many bytes when decoding varint.')

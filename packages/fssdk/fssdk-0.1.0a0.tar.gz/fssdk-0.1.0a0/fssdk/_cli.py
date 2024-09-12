import serial


class CLI:
    _TERMINAL_IDENTIFIER: bytes = b'>:'
    _CTRL_C: bytes = b'\x03'

    _conn: serial.Serial = None

    def __init__(self, port: str):
        self._conn = serial.Serial(
            port=port,
            baudrate=230400,
            bytesize=serial.EIGHTBITS,
            timeout=1,
            stopbits=serial.STOPBITS_ONE)

        self.read_until_terminal()

        self._conn.timeout = None
    
    def __del__(self):
        self._conn.close()

    def read(self, size: int) -> bytes:
        return self._conn.read(size)
    
    def write(self, data: bytes) -> None:
        return self._conn.write(data)
    
    def write_data(self, data: str|bytes) -> None:
        raw_data: bytes  = data if isinstance(data, bytes) else data.encode()

        self._conn.write(raw_data)
        self._conn.readline()

    def write_command(self, command: str) -> None:
        data: str = f'{command}\r'.encode()

        self._conn.write(data)
        self._conn.readline()

    def read_until_terminal(self) -> str:
        return self._conn \
            .read_until(self._TERMINAL_IDENTIFIER) \
            .rstrip(self._TERMINAL_IDENTIFIER) \
            .rstrip() \
            .decode()
    
    def send_ctrl_c(self) -> None:
        self._conn.write(self._CTRL_C)

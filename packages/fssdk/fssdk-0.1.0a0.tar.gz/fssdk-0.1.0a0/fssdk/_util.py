from hashlib import file_digest

from serial.tools import list_ports

from ._cli import CLI


def resolve_port(portname: str = 'auto') -> str | None:
    if portname != 'auto':
        return portname
    
    ports = list_ports.grep('flip_')
    flippers = list(ports)

    if len(flippers) == 1:
        flipper = flippers[0]
        
        return flipper.device
    
    return None


def upload_file(cli: CLI, source: str, target: str) -> None:
    cli.write_command(f'storage md5 {target}')

    checksum = cli.read_until_terminal()

    with open(source, 'rb') as fp:
        digest = file_digest(fp, 'md5')
    
    print(checksum)
    print(digest.hexdigest())

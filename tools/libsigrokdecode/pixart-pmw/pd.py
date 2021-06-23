import enum

import sigrokdecode as srd

__all__ = ['Decoder']


class RegisterOperation(enum.Enum):
    READ = enum.auto()
    WRITE = enum.auto()


class Decoder(srd.Decoder):
    api_version = 3
    id = 'pixart-pmw'
    name = 'PixArt PMW'
    license = 'gplv2+'
    longname = 'PixArt PMW protocol over SPI'
    desc = (
            'Decoder for protocol used to communicate '
            'with PixArt PMW chips over SPI'
    )
    inputs = ['spi']
    outputs = []
    annotations = (
        ('command', 'Command'),
        ('reply', 'Reply'),
    )
    annotation_rows = (
        ('command', 'Command', (0, )),
        ('reply', 'Reply', (1, )),
    )

    def __init__(self):
        self.reset()

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def reset(self):
        pass

    def decode(self, startsample, endsample, data):
        ptype, command_data, reply_data = data

        if ptype != 'TRANSFER':
            return

        if not command_data:
            return

        first_byte = command_data[0].val
        command_type = RegisterOperation.WRITE if first_byte & 0x80 else RegisterOperation.READ
        register_num = first_byte & ~0x80

        command_end = endsample
        if command_type == RegisterOperation.READ:
            message = 'Read register {:02X}'.format(register_num)
            if len(command_data) > 1:
                command_end = command_data[1].ss
        elif command_type == RegisterOperation.WRITE:
            message = 'Write register {:02X}: {}'.format(
                register_num, format_transfer_data(command_data[1:]))
        self.put(startsample, command_end, self.out_ann, [0, [message]])

        if command_type == RegisterOperation.READ:
            reply_start = startsample
            if len(reply_data) > 1:
                reply_start = reply_data[1].ss
            self.put(reply_start, endsample, self.out_ann,
                     [1, [format_transfer_data(reply_data[1:])]])


def format_transfer_data(data):
    return ' '.join(['{:02X}'.format(val.val) for val in data])

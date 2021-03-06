#!/usr/bin/env python3

import argparse
import os
import struct
import sys
from pathlib import Path

def print_preamble(output_file, from_string):
    print(f'\
/*\r\n\
 * File automatically generated by: {Path(__file__).name}\r\n\
 * From binary: {from_string}\r\n\
 */\r\n\
\n\
#pragma once\r\n\
\n', file=output_file, end='')


def print_array(output_file, name, byte_array):
    print(f'static const uint8_t {name}[] = ', file=output_file, end='{\r\n\t')

    num_bytes = sum(1 for byte in byte_array)

    for i in range(num_bytes):
        if (i + 1) == num_bytes:
            print(f'0x{byte_array[i]:02X}', file=output_file, end='};\r\n')
        elif (i + 1) % 16 == 0:
            print(f'0x{byte_array[i]:02X},', file=output_file, end='\r\n\t')
        else:
            print(f'0x{byte_array[i]:02X}, ', file=output_file, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Format binary file to C header')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file.')
    parser.add_argument('binary', metavar='binary.bin', type=str,
                        help='binary to parse.')
    args = parser.parse_args()

    if not args.binary or not os.path.exists(args.binary):
        print(f'{args.binary} doesn\'t exist', file=sys.stderr)
        exit(1)

    try:
        binary = open(args.binary, 'rb')
    except PermissionError as e:
        print(f'can\'t open {args.binary}: {str(e)}', file=sys.stderr)
        exit(1)

    if args.output:
        output_file = args.output
    else:
        output_file = Path(args.binary).stem + '.h'

    try:
        output = open(output_file, 'wt')
    except PermissionError as e:
        print(f'can\'t open {output_file}: {str(e)}', file=sys.stderr)
        exit(1)

    num_bytes = os.path.getsize(args.binary)
    binary_bytes = bytearray(binary.read(num_bytes))

    print_preamble(output, Path(args.binary).name)
    print_array(output, Path(args.binary).stem, binary_bytes)

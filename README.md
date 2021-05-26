# sensor-blobs

Mouse optical sensors proprietary firmware blobs

format:

`vendor_device_version.bin`

*version may be omited

## tools

in [tools](tools/) you may find useful scripts to work with these blobs.

### bin2header

bin2headers takes in a binary and creates a usefull C header file with the contents.

```
usage: bin2header.py [-h] [-o OUTPUT] binary.bin

Format binary file to C header

positional arguments:
  binary.bin            binary to parse.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file.
```

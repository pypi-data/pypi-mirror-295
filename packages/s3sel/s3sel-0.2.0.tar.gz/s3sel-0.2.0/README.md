# s3sel

A small tool for simple management of multiple .s3cfg files.
By default runs in ui mode if no arguments are provided.

Running `s3sel -h` will get you started.

Usage as of v0.2.0:
```
usage: s3sel [-h] [-a] [-l] [-v] [-d] [-s] [-c] [name]

positional arguments:
  name

options:
  -h, --help         show this help message and exit
  -a, --add-current  add your current .s3cfg to s3sel store
  -l, --list-all     show all configs present in s3sel store
  -v, --verbose      enable verbose output
  -d, --delete       delete config from s3sel store by specified name
  -s, --switch       switch your current .s3cfg to config with specified name
  -c, --check        check if your current .s3cfg is already stored

```

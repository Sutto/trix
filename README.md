# Trix!

Written by Darcy Laycock.

This was written for the CITS4211 AI Project in 2013.

## Running this code

With a copy of the code, to run it you must invoke the program in bin/
from the top level directory. On a unix-based OS this is done via ./bin/trix,
on windows (I assume) via python3.exe bin/trix - Note that this codebase is
only compatible with Python 3.

Usage is as such:

```bash
./bin/trix [options] [input-file] [output-file]
```

For example,

```bash
./bin/trix test/in test/out
```

Will read the pieces in from test/in and print them out to test/out

To specify a custom board width, use -w (defaulting to 11), and a custom buffer
size (defaulting to 1), use -b.

E.G:

```bash
./bin/trix -w 10 -b 3 test/in test/out
```

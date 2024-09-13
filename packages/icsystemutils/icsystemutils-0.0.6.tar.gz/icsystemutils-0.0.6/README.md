`icsystemutils` is a Python package with some low-level utilities for interacting with real system resources (cpu, gpu, network etc).

It is maintained by the Irish Centre for High End Computing (ICHEC), mostly as a dependency of high-level packages and tools used to support ICHEC research and workflows.

# Examples #

Although this is mostly intended to be a library, some example uses to build CLI apps are shown below.

## Get CPU info ##

This reads the CPU info on Linux/Mac via system apis and returns the result as json.

``` shell
icsystemutils read_cpu
```

# License #

This project is Copyright of the Irish Centre for High End Computing. You can use it under the terms of the GPLv3+, which further details in the included LICENSE file.

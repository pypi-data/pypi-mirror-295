# PyMake

PyMake is a simple, Python-based build system designed to simplify the process of compiling and running C++ projects. It provides an intuitive API for configuring your build process and executing compiled programs.

## Features

- Easy-to-use Python API for build configuration
- Support for multiple source files and directories
- Include directory management
- Macro definitions
- Library linking and path configuration
- Compiler, linker, assembler, and preprocessor flag customization
- Verbose output option for debugging
- Flexible output directory setting
- Run compiled programs with custom arguments and environment variables

## Installation

To install PyMake, you can use pip:

```bash
pip install git+https://github.com/fresh-milkshake/pymake.git
```

## Usage

Here's a simple example to get you started:

```python
from pymake import *

add_sources_directory("src")
add_includes_directory("inc")

set_verbose(True)

build(compiler="g++")
run()
```

This script will compile all the source files in the `src` directory, link them into an executable, and then run the executable.

## Documentation

For more details on the API and its usage, please refer to the [documentation](docs.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
"""
PyMake is a simple, Python-based build system designed to simplify the process of compiling and running C++ projects. It provides an intuitive API for configuring your build process and executing compiled programs.
"""

import os
import subprocess
import pathlib
from typing import List, Optional


__version__ = "0.1.0"


class CompilerConfig:
    def __init__(self):
        self.source_files: List[pathlib.Path] = []
        self.include_directories: List[pathlib.Path] = []
        self.defines: List[str] = []
        self.library_paths: List[pathlib.Path] = []
        self.libraries: List[str] = []
        self.compiler_flags: List[str] = []
        self.linker_flags: List[str] = []
        self.assembler_flags: List[str] = []
        self.preprocessor_flags: List[str] = []
        self.output_directory: pathlib.Path = pathlib.Path(".")
        self.extra_args: List[str] = []
        self.verbose: bool = False
        self.compile_error: bool = False

    def clear(self):
        self.source_files.clear()
        self.include_directories.clear()
        self.defines.clear()
        self.library_paths.clear()
        self.libraries.clear()
        self.compiler_flags.clear()
        self.linker_flags.clear()
        self.assembler_flags.clear()
        self.preprocessor_flags.clear()
        self.output_directory = pathlib.Path(".")
        self.extra_args.clear()
        self.verbose = False
        self.compile_error = False


_compiler_config = CompilerConfig()


def add_source_file(*file_names: str):
    """
    Adds one or more source files for compilation.

    Args:
        file_names (str): Names of the source files.
    """
    _compiler_config.source_files.extend(
        pathlib.Path(file_name) for file_name in file_names
    )


def add_sources_directory(*directories: str):
    """
    Adds one or more source directories for compilation.

    Args:
        directories (str): Paths to the source directories.
    """
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                _compiler_config.source_files.append(pathlib.Path(root, file))


def add_includes_directory(*directories: str):
    """
    Adds one or more include directories for compilation.

    Args:
        directories (str): Paths to the include directories.
    """
    _compiler_config.include_directories.extend(
        pathlib.Path(directory) for directory in directories
    )


def define(*macros: str):
    """
    Defines one or more macros for compilation.

    Args:
        macros (str): Names of the macros.
    """
    _compiler_config.defines.extend(macro for macro in macros)


def add_library_path(*paths: str):
    """
    Adds one or more library search paths.

    Args:
        paths (str): Paths to the libraries.
    """
    _compiler_config.library_paths.extend(pathlib.Path(path) for path in paths)


def link_library(*library_names: str):
    """
    Links one or more libraries by name.

    Args:
        library_names (str): Names of the libraries.
    """
    _compiler_config.libraries.extend(library_name for library_name in library_names)


def add_compiler_flag(*flags: str):
    """
    Adds one or more compiler-specific flags.

    Args:
        flags (str): Compiler flags.
    """
    _compiler_config.compiler_flags.extend(flag for flag in flags)


def add_linker_flag(*flags: str):
    """
    Adds one or more linker-specific flags.

    Args:
        flags (str): Linker flags.
    """
    _compiler_config.linker_flags.extend(flag for flag in flags)


def add_assembler_flag(*flags: str):
    """
    Adds one or more assembler-specific flags.

    Args:
        flags (str): Assembler flags.
    """
    _compiler_config.assembler_flags.extend(flag for flag in flags)


def add_preprocessor_flag(*flags: str):
    """
    Adds one or more preprocessor-specific flags.

    Args:
        flags (str): Preprocessor flags.
    """
    _compiler_config.preprocessor_flags.extend(flag for flag in flags)


def set_output_directory(directory: str):
    """
    Sets the output directory for the compiled binary.

    Args:
        directory (str): Directory where the output will be placed.
    """
    _compiler_config.output_directory = pathlib.Path(directory)


def add_extra_arg(*args: str):
    """
    Adds one or more extra arguments to the compiler command.

    Args:
        args (str): Extra arguments.
    """
    _compiler_config.extra_args.extend(arg for arg in args)


def set_verbose(verbose: bool):
    """
    Enables or disables verbose output.

    Args:
        verbose (bool): If True, enables verbose output.
    """
    _compiler_config.verbose = verbose


def build(
    output_file: str = "output",
    compiler: str = "g++",
    flags: Optional[List[str]] = None,
    compile_only: bool = False,
    assembly_only: bool = False,
    preprocess_only: bool = False,
):
    """
    Compiles the program.

    Args:
        output_file (str): Name of the output file.
        compiler (str): Compiler to use.
        flags (list): List of additional compiler flags.
        compile_only (bool): If True, compile and assemble but do not link.
        assembly_only (bool): If True, compile only but do not assemble or link.
        preprocess_only (bool): If True, preprocess only, do not compile, assemble or link.
    """
    flags = flags or []

    if not _compiler_config.output_directory.exists():
        os.makedirs(_compiler_config.output_directory)

    output_path = _compiler_config.output_directory / output_file
    compile_command = [
        compiler,
        "-o",
        str(output_path),
    ]

    if preprocess_only:
        compile_command.append("-E")
    elif assembly_only:
        compile_command.append("-S")
    elif compile_only:
        compile_command.append("-c")
    compile_command.extend(str(file) for file in _compiler_config.source_files)
    compile_command.extend(
        f"-I{directory}" for directory in _compiler_config.include_directories
    )
    compile_command.extend(f"-D{macro}" for macro in _compiler_config.defines)
    compile_command.extend(f"-L{path}" for path in _compiler_config.library_paths)
    compile_command.extend(f"-l{lib}" for lib in _compiler_config.libraries)
    compile_command.extend(_compiler_config.compiler_flags)
    compile_command.extend(flags)
    compile_command.extend(f"-Wl,{flag}" for flag in _compiler_config.linker_flags)
    compile_command.extend(f"-Wa,{flag}" for flag in _compiler_config.assembler_flags)
    compile_command.extend(
        f"-Wp,{flag}" for flag in _compiler_config.preprocessor_flags
    )
    compile_command.extend(_compiler_config.extra_args)

    if _compiler_config.verbose:
        print(f"Compile command: {' '.join(compile_command)}")

    result = subprocess.run(
        compile_command, shell=False, capture_output=True, text=True
    )

    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr, end="")
        _compiler_config.compile_error = True
    else:
        print("Compilation succeeded.")
        if _compiler_config.verbose:
            print(result.stdout, end="")


def run(
    output_file: str = "output.exe",
    args: Optional[List[str]] = None,
    env: Optional[dict] = None,
):
    """
    Runs the compiled program.

    Args:
        output_file (str): Name of the output file.
        args (list, optional): List of arguments to pass to the program.
        env (dict, optional): Dictionary of environment variables to set for the program.
    """
    if _compiler_config.compile_error:
        print("Compilation failed. Exiting.")
        return

    output_path = _compiler_config.output_directory / output_file
    command = [str(output_path)]

    if args:
        command.extend(args)

    print(f"Running '{output_path}'...\n--- Output ---")
    result = subprocess.run(
        command, shell=False, capture_output=True, text=True, env=env
    )
    print(result.stderr, result.stdout, sep="\n")
    print("--- End of output ---\nReturn code:", result.returncode)

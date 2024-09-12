import os
import typing
from pathlib import Path

import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

SETUP_DIR = Path(__file__).resolve().parent
SRC_DIR = SETUP_DIR / "src"


def scan_files_in_dir(
        directory: Path,
        fileext: typing.Union[str, typing.Iterable[str]],
        recursive: bool = False
) -> typing.List[Path]:
    if isinstance(fileext, str):
        fileext = [fileext]

    files = []
    for _ext in fileext:
        if not _ext.startswith("."):
            _ext = "." + _ext
        if recursive:
            file_gen = directory.rglob(f"*{_ext}")
        else:
            file_gen = directory.glob(f"*{_ext}")
        files += list(file_gen)
    return files


def make_extension(src_path: Path, *args, **kwargs) -> Extension:
    ext_rel_path = src_path.relative_to(SRC_DIR)
    ext_name = str(ext_rel_path.with_suffix("")).replace(os.path.sep, ".")
    return Extension(
        ext_name,
        [str(src_path.relative_to(SETUP_DIR))],
        *args,
        **kwargs
    )


CY_EXTS = True
src_files = scan_files_in_dir(SRC_DIR, ".pyx", recursive=True)
if not src_files:
    src_files = scan_files_in_dir(SRC_DIR, [".c", ".cpp"], recursive=True)
    CY_EXTS = False

np_include_dir = numpy.get_include()
extensions = [
    make_extension(
        src_file,
        include_dirs=[np_include_dir],
        extra_compile_args=["-O3", "-Wall"]
    ) for src_file in src_files
]
if CY_EXTS:
    extensions = cythonize(extensions)

setup(
    ext_modules=extensions
)

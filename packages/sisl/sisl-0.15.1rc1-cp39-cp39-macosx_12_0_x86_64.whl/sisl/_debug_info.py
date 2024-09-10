# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Debug information for the tools required
_cython_build_version = """Cython version 3.0.11"""
_numpy_build_version = """2.0.2"""

_cc = """/Applications/Xcode_14.2.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"""
_cc_version = """14.0.0.14000029"""
_cflags = """-O3 -DNDEBUG"""

_fc = """/usr/local/bin/gfortran"""
_fc_version = """11.5.0"""
_fflags = """-O3"""

_definitions = """NPY_NO_DEPRECATED_API=NPY_1_20_API_VERSION CYTHON_NO_PYINIT_EXPORT=1"""

_cmake_args = [
    ("CMAKE_BUILD_TYPE", """Release"""),
    ("WITH_FORTRAN", """ON"""),
    ("F2PY_REPORT_ON_ARRAY_COPY", """10"""),
    ("WITH_F2PY_REPORT_COPY", """OFF"""),
    ("WITH_F2PY_REPORT_EXIT", """OFF"""),
    ("WITH_COVERAGE", """OFF"""),
    ("WITH_LINE_DIRECTIVES", """OFF"""),
    ("WITH_ANNOTATE", """OFF"""),
    ("WITH_GDB", """OFF"""),
    ("NO_COMPILATION", """"""),
]


def print_debug_info():
    import importlib
    from pathlib import Path
    import sys

    print("[sys]")
    print(sys.version)

    # We import it like this to ensure there are no import errors
    # with sisl, this might be problematic, however, it should at least
    # provide consistent information
    import sisl._version as sisl_version

    fmt = "{0:30s}{1}"

    print("[sisl]")
    print(fmt.format("version", sisl_version.__version__))
    path = Path(sisl_version.__file__)
    print(fmt.format("path", str((path / "..").resolve())))

    def print_attr(module, attr: str = ""):
        attr_val = None
        try:
            mod = importlib.import_module(module)
            if attr:
                attr_val = getattr(mod, attr)
                print(fmt.format(module, attr_val))
        except BaseException as e:
            print(fmt.format(module, "not found"))
            print(fmt.format("", str(e)))

        return attr_val

    # regardless of whether it is on, or not, we try to import fortran extension
    print_attr("sisl.io.siesta._siesta")

    print(fmt.format("CC", _cc))
    print(fmt.format("CFLAGS", _cflags))
    print(fmt.format("C version", _cc_version))
    print(fmt.format("FC", _fc))
    print(fmt.format("FFLAGS", _fflags))
    print(fmt.format("FC version", _fc_version))
    print(fmt.format("cython build version", _cython_build_version))
    print(fmt.format("numpy build version", _numpy_build_version))

    print("[sisl.definitions]")
    for df in _definitions.split():
        try:
            name, value = df.split("=", 1)
            print(fmt.format(name, value))
        except ValueError:
            print(fmt.format(df, ""))

    print("[sisl.cmake_args]")
    for d, v in _cmake_args:
        print(fmt.format(d, v))

    print("[sisl.env]")
    from sisl._environ import SISL_ENVIRON, get_environ_variable

    for envvar in SISL_ENVIRON:
        print(fmt.format(envvar, get_environ_variable(envvar)))

    print("[runtime]")

    pip_install = []
    conda_install = []
    for pip, conda, mod in (
        ("numpy", "numpy", "numpy"),
        ("scipy", "scipy", "scipy"),
        ("xarray", "xarray", "xarray"),
        ("netCDF4", "netCDF4", "netCDF4"),
        ("pandas", "pandas", "pandas"),
        ("matplotlib", "matplotlib", "matplotlib"),
        ("dill", "dill", "dill"),
        ("pathos", "pathos", "pathos"),
        ("scikit-image", "scikit-image", "skimage"),
        ("plotly", "plotly", "plotly"),
        ("ase", "ase", "ase"),
        ("pymatgen", "pymatgen", "pymatgen"),
    ):
        attr = print_attr(mod, "__version__")
        if attr is not None:
            pip_install.append(f"{pip}=={attr}")
            conda_install.append(f"{conda}=={attr}")

    print("[install]")
    print(fmt.format("pip", " ".join(pip_install)))
    print(fmt.format("conda", " ".join(conda_install)))

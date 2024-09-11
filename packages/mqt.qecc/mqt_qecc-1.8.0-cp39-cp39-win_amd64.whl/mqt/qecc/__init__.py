"""MQT QECC library.

This file is part of the MQT QECC library released under the MIT license.
See README.md or go to https://github.com/cda-tum/qecc for more information.
"""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_8_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_qecc.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-mqt_qecc-1.8.0')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-mqt_qecc-1.8.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.c_void_p
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_8_1()
del _delvewheel_patch_1_8_1
# end delvewheel patch

from ._version import version as __version__
from .analog_information_decoding.simulators.analog_tannergraph_decoding import AnalogTannergraphDecoder, AtdSimulator
from .analog_information_decoding.simulators.quasi_single_shot_v2 import QssSimulator
from .codes import CSSCode, StabilizerCode
from .pyqecc import (
    Code,
    Decoder,
    DecodingResult,
    DecodingResultStatus,
    DecodingRunInformation,
    GrowthVariant,
    UFDecoder,
    UFHeuristic,
    apply_ecc,
    sample_iid_pauli_err,
)

__all__ = [
    "AnalogTannergraphDecoder",
    "AtdSimulator",
    "CSSCode",
    "Code",
    "Decoder",
    "DecodingResult",
    "DecodingResultStatus",
    "DecodingRunInformation",
    "GrowthVariant",
    "QssSimulator",
    "StabilizerCode",
    "UFDecoder",
    "UFHeuristic",
    "__version__",
    "apply_ecc",
    "sample_iid_pauli_err",
]

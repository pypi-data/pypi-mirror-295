"""MQT QECC library.

This file is part of the MQT QECC library released under the MIT license.
See README.md or go to https://github.com/cda-tum/qecc for more information.
"""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_8_1():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_qecc.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


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

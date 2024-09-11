from __future__ import annotations

import enum
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

_PKG_NAME: str = Path(__file__).parent.stem

VERSION = "2024.739139.0"

__version__ = VERSION

DATA_DIR: Path = Path.home() / _PKG_NAME
"""
Defines a subdirectory named for this package in the user's home path.

If the subdirectory doesn't exist, it is created on package invocation.
"""
if not DATA_DIR.is_dir():
    DATA_DIR.mkdir(parents=False)

np.set_printoptions(precision=18)


type ArrayINT = NDArray[np.intp]
type ArrayFloat = NDArray[np.half | np.single | np.double]


type ArrayBoolean = NDArray[np.bool_]

type ArrayDouble = NDArray[np.double]
type ArrayBIGINT = NDArray[np.int64]

DEFAULT_REC_RATE = 0.85


@enum.unique
class RECForm(enum.StrEnum):
    """For derivation of recapture ratio from market shares."""

    INOUT = "inside-out"
    OUTIN = "outside-in"
    FIXED = "proportional"


@enum.unique
class UPPAggrSelector(enum.StrEnum):
    """
    Aggregator for GUPPI and diversion ratio estimates.

    """

    AVG = "average"
    CPA = "cross-product-share weighted average"
    CPD = "cross-product-share weighted distance"
    CPG = "cross-product-share weighted geometric mean"
    DIS = "symmetrically-weighted distance"
    GMN = "geometric mean"
    MAX = "max"
    MIN = "min"
    OSA = "own-share weighted average"
    OSD = "own-share weighted distance"
    OSG = "own-share weighted geometric mean"

"""
Methods to format and print summary statistics on merger enforcement patterns.

"""

import enum
from collections.abc import Mapping

import numpy as np
from scipy.interpolate import interp1d  # type: ignore

from .. import VERSION, ArrayBIGINT  # noqa: TID252
from ..core import ftc_merger_investigations_data as fid  # noqa: TID252
from . import INVResolution

__version__ = VERSION


@enum.unique
class IndustryGroup(enum.StrEnum):
    ALL = "All Markets"
    GRO = "Grocery Markets"
    OIL = "Oil Markets"
    CHM = "Chemical Markets"
    PHM = "Pharmaceuticals Markets"
    HOS = "Hospital Markets"
    EDS = "Electronically-Controlled Devices and Systems Markets"
    BRD = "Branded Consumer Goods Markets"
    OTH = '"Other" Markets'
    IIC = "Industries in Common"


@enum.unique
class OtherEvidence(enum.StrEnum):
    UR = "Unrestricted on additional evidence"
    HD = "Hot Documents Identified"
    HN = "No Hot Documents Identified"
    HU = "No Evidence on Hot Documents"
    CN = "No Strong Customer Complaints"
    CS = "Strong Customer Complaints"
    CU = "No Evidence on Customer Complaints"
    ED = "Entry Difficult"
    EE = "Entry Easy"
    NE = "No Entry Evidence"


@enum.unique
class StatsGrpSelector(enum.StrEnum):
    FC = "ByFirmCount"
    HD = "ByHHIandDelta"
    DL = "ByDelta"
    ZN = "ByConcZone"


@enum.unique
class StatsReturnSelector(enum.StrEnum):
    CNT = "count"
    RPT = "rate, point"
    RIN = "rate, interval"


@enum.unique
class SortSelector(enum.StrEnum):
    UCH = "unchanged"
    REV = "reversed"


# Parameters and functions to interpolate selected HHI and ΔHHI values
#   recorded in fractions to ranges of values in points on the HHI scale
HHI_DELTA_KNOTS = np.array(
    [0, 100, 200, 300, 500, 800, 1200, 2500, 5001], dtype=np.int64
)
HHI_POST_ZONE_KNOTS = np.array([0, 1800, 2400, 10001], dtype=np.int64)
hhi_delta_ranger, hhi_zone_post_ranger = (
    interp1d(_f / 1e4, _f, kind="previous", assume_sorted=True)
    for _f in (HHI_DELTA_KNOTS, HHI_POST_ZONE_KNOTS)
)


HMG_PRESUMPTION_ZONE_MAP = {
    HHI_POST_ZONE_KNOTS[0]: {
        HHI_DELTA_KNOTS[0]: (0, 0, 0),
        HHI_DELTA_KNOTS[1]: (0, 0, 0),
        HHI_DELTA_KNOTS[2]: (0, 0, 0),
    },
    HHI_POST_ZONE_KNOTS[1]: {
        HHI_DELTA_KNOTS[0]: (0, 1, 1),
        HHI_DELTA_KNOTS[1]: (1, 1, 2),
        HHI_DELTA_KNOTS[2]: (1, 1, 2),
    },
    HHI_POST_ZONE_KNOTS[2]: {
        HHI_DELTA_KNOTS[0]: (0, 2, 1),
        HHI_DELTA_KNOTS[1]: (1, 2, 3),
        HHI_DELTA_KNOTS[2]: (2, 2, 4),
    },
}

ZONE_VALS = np.unique(
    np.vstack([
        tuple(HMG_PRESUMPTION_ZONE_MAP[_k].values()) for _k in HMG_PRESUMPTION_ZONE_MAP
    ]),
    axis=0,
)

ZONE_STRINGS = {
    0: R"Green Zone (Safeharbor)",
    1: R"Yellow Zone",
    2: R"Red Zone (SLC Presumption)",
    fid.TTL_KEY: "TOTAL",
}
ZONE_DETAIL_STRINGS_HHI = {
    0: Rf"HHI < {HHI_POST_ZONE_KNOTS[1]} pts.",
    1: R"HHI ∈ [{}, {}) pts. and ".format(*HHI_POST_ZONE_KNOTS[1:3]),
    2: Rf"HHI ⩾ {HHI_POST_ZONE_KNOTS[2]} pts. and ",
}
ZONE_DETAIL_STRINGS_DELTA = {
    0: "",
    1: Rf"ΔHHI < {HHI_DELTA_KNOTS[1]} pts.",
    2: Rf"ΔHHI ⩾ {HHI_DELTA_KNOTS[1]} pts.}}",
    3: R"ΔHHI ∈ [{}, {}) pts.".format(*HHI_DELTA_KNOTS[1:3]),
    4: Rf"ΔHHI ⩾ {HHI_DELTA_KNOTS[2]} pts.",
}


def enf_cnts_obs_by_group(
    _invdata_array_dict: Mapping[str, Mapping[str, Mapping[str, fid.INVTableData]]],
    _study_period: str,
    _table_ind_grp: IndustryGroup,
    _table_evid_cond: OtherEvidence,
    _stats_group: StatsGrpSelector,
    _enf_spec: INVResolution,
    /,
) -> ArrayBIGINT:
    if _stats_group == StatsGrpSelector.HD:
        raise ValueError(
            f"Clearance/enforcement statistics, '{_stats_group}' not valied here."
        )

    match _stats_group:
        case StatsGrpSelector.FC:
            _cnts_func = enf_cnts_byfirmcount
            _cnts_listing_func = enf_cnts_obs_byfirmcount
        case StatsGrpSelector.DL:
            _cnts_func = enf_cnts_bydelta
            _cnts_listing_func = enf_cnts_obs_byhhianddelta
        case StatsGrpSelector.ZN:
            _cnts_func = enf_cnts_byconczone
            _cnts_listing_func = enf_cnts_obs_byhhianddelta

    return _cnts_func(
        _cnts_listing_func(
            _invdata_array_dict,
            _study_period,
            _table_ind_grp,
            _table_evid_cond,
            _enf_spec,
        )
    )


def enf_cnts_obs_byfirmcount(
    _data_array_dict: Mapping[str, Mapping[str, Mapping[str, fid.INVTableData]]],
    _data_period: str = "1996-2003",
    _table_ind_group: IndustryGroup = IndustryGroup.ALL,
    _table_evid_cond: OtherEvidence = OtherEvidence.UR,
    _enf_spec: INVResolution = INVResolution.CLRN,
    /,
) -> ArrayBIGINT:
    if _data_period not in _data_array_dict:
        raise ValueError(
            f"Invalid value of data period, {f'"{_data_period}"'}."
            f"Must be one of, {tuple(_data_array_dict.keys())!r}."
        )

    _data_array_dict_sub = _data_array_dict[_data_period][fid.TABLE_TYPES[1]]

    _table_no = table_no_lku(_data_array_dict_sub, _table_ind_group, _table_evid_cond)

    _cnts_array = _data_array_dict_sub[_table_no].data_array

    _ndim_in = 1
    _stats_kept_indxs = []
    match _enf_spec:
        case INVResolution.CLRN:
            _stats_kept_indxs = [-1, -2]
        case INVResolution.ENFT:
            _stats_kept_indxs = [-1, -3]
        case INVResolution.BOTH:
            _stats_kept_indxs = [-1, -3, -2]

    return np.column_stack([
        _cnts_array[:, :_ndim_in],
        _cnts_array[:, _stats_kept_indxs],
    ])


def enf_cnts_obs_byhhianddelta(
    _data_array_dict: Mapping[str, Mapping[str, Mapping[str, fid.INVTableData]]],
    _data_period: str = "1996-2003",
    _table_ind_group: IndustryGroup = IndustryGroup.ALL,
    _table_evid_cond: OtherEvidence = OtherEvidence.UR,
    _enf_spec: INVResolution = INVResolution.CLRN,
    /,
) -> ArrayBIGINT:
    if _data_period not in _data_array_dict:
        raise ValueError(
            f"Invalid value of data period, {f'"{_data_period}"'}."
            f"Must be one of, {tuple(_data_array_dict.keys())!r}."
        )

    _data_array_dict_sub = _data_array_dict[_data_period][fid.TABLE_TYPES[0]]

    _table_no = table_no_lku(_data_array_dict_sub, _table_ind_group, _table_evid_cond)

    _cnts_array = _data_array_dict_sub[_table_no].data_array

    _ndim_in = 2
    _stats_kept_indxs = []
    match _enf_spec:
        case INVResolution.CLRN:
            _stats_kept_indxs = [-1, -2]
        case INVResolution.ENFT:
            _stats_kept_indxs = [-1, -3]
        case INVResolution.BOTH:
            _stats_kept_indxs = [-1, -3, -2]

    return np.column_stack([
        _cnts_array[:, :_ndim_in],
        _cnts_array[:, _stats_kept_indxs],
    ])


def table_no_lku(
    _data_array_dict_sub: Mapping[str, fid.INVTableData],
    _table_ind_group: IndustryGroup = IndustryGroup.ALL,
    _table_evid_cond: OtherEvidence = OtherEvidence.UR,
    /,
) -> str:
    if _table_ind_group not in (
        _igl := [_data_array_dict_sub[_v].industry_group for _v in _data_array_dict_sub]
    ):
        raise ValueError(
            f"Invalid value for industry group, {f'"{_table_ind_group}"'}."
            f"Must be one of {_igl!r}"
        )

    _tno = next(
        _t
        for _t in _data_array_dict_sub
        if all((
            _data_array_dict_sub[_t].industry_group == _table_ind_group,
            _data_array_dict_sub[_t].additional_evidence == _table_evid_cond,
        ))
    )

    return _tno


def enf_cnts_byfirmcount(_cnts_array: ArrayBIGINT, /) -> ArrayBIGINT:
    _ndim_in = 1
    return np.vstack([
        np.concatenate([
            (f,),
            np.einsum("ij->j", _cnts_array[_cnts_array[:, 0] == f][:, _ndim_in:]),
        ])
        for f in np.unique(_cnts_array[:, 0])
    ])


def enf_cnts_bydelta(_cnts_array: ArrayBIGINT, /) -> ArrayBIGINT:
    _ndim_in = 2
    return np.vstack([
        np.concatenate([
            (f,),
            np.einsum("ij->j", _cnts_array[_cnts_array[:, 1] == f][:, _ndim_in:]),
        ])
        for f in HHI_DELTA_KNOTS[:-1]
    ])


def enf_cnts_byconczone(_cnts_array: ArrayBIGINT, /) -> ArrayBIGINT:
    # Prepare to tag clearance stats by presumption zone
    _hhi_zone_post_ranged = hhi_zone_post_ranger(_cnts_array[:, 0] / 1e4)
    _hhi_delta_ranged = hhi_delta_ranger(_cnts_array[:, 1] / 1e4)

    # Step 1: Tag and agg. from HHI-post and Delta to zone triple
    # NOTE: Although you could just map and not (partially) aggregate in this step,
    # the mapped array is a copy, and is larger without partial aggregation, so
    # aggregation reduces the footprint of this step in memory. Although this point
    # is more relevant for generated than observed data, using the same coding pattern
    # in both cases does make life easier
    _ndim_in = 2
    _nkeys = 3
    _cnts_byhhipostanddelta = -1 * np.ones(
        _nkeys + _cnts_array.shape[1] - _ndim_in, dtype=np.int64
    )
    _cnts_byconczone = -1 * np.ones_like(_cnts_byhhipostanddelta)
    for _hhi_zone_post_lim in HHI_POST_ZONE_KNOTS[:-1]:
        _level_test = _hhi_zone_post_ranged == _hhi_zone_post_lim

        for _hhi_zone_delta_lim in HHI_DELTA_KNOTS[:3]:
            _delta_test = (
                (_hhi_delta_ranged >= _hhi_zone_delta_lim)
                if _hhi_zone_delta_lim == HHI_DELTA_KNOTS[2]
                else (_hhi_delta_ranged == _hhi_zone_delta_lim)
            )

            _zone_val = HMG_PRESUMPTION_ZONE_MAP[_hhi_zone_post_lim][
                _hhi_zone_delta_lim
            ]

            _conc_test = _level_test & _delta_test

            _cnts_byhhipostanddelta = np.vstack((
                _cnts_byhhipostanddelta,
                np.array(
                    (
                        *_zone_val,
                        *np.einsum("ij->j", _cnts_array[:, _ndim_in:][_conc_test]),
                    ),
                    dtype=np.int64,
                ),
            ))
    _cnts_byhhipostanddelta = _cnts_byhhipostanddelta[1:]

    for _zone_val in ZONE_VALS:
        # Logical-and of multiple vectors:
        _hhi_zone_test = (
            1
            * np.column_stack([
                _cnts_byhhipostanddelta[:, _idx] == _val
                for _idx, _val in enumerate(_zone_val)
            ])
        ).prod(axis=1) == 1

        _cnts_byconczone = np.vstack((
            _cnts_byconczone,
            np.concatenate(
                (
                    _zone_val,
                    np.einsum(
                        "ij->j", _cnts_byhhipostanddelta[_hhi_zone_test][:, _nkeys:]
                    ),
                ),
                dtype=np.int64,
            ),
        ))

    return _cnts_byconczone[1:]


if __name__ == "__main__":
    print(
        "This module provides methods to aggregate statistics on merger enforcement patterns for reporting."
    )

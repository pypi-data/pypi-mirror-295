from rapidfuzz.fuzz import (
    ratio as _ratio,
    partial_ratio as _partial_ratio,
    token_set_ratio as _token_set_ratio,
    token_sort_ratio as _token_sort_ratio,
    partial_token_set_ratio as _partial_token_set_ratio,
    partial_token_sort_ratio as _partial_token_sort_ratio,
    WRatio as _WRatio,
    QRatio as _QRatio,
)

from . import utils

def _rapidfuzz_scorer(scorer, s1, s2, force_ascii, full_process):
    if full_process:
        if s1 is None or s2 is None:
            return 0

        s1 = utils.full_process(s1, force_ascii=force_ascii)
        s2 = utils.full_process(s2, force_ascii=force_ascii)

    return int(round(scorer(s1, s2)))


def ratio(s1, s2):
    return _rapidfuzz_scorer(_ratio, s1, s2, False, False)


def partial_ratio(s1, s2):
    return _rapidfuzz_scorer(_partial_ratio, s1, s2, False, False)

def token_sort_ratio(s1, s2, force_ascii=True, full_process=True):
    return _rapidfuzz_scorer(_token_sort_ratio, s1, s2, force_ascii, full_process)


def partial_token_sort_ratio(s1, s2, force_ascii=True, full_process=True):
    return _rapidfuzz_scorer(
        _partial_token_sort_ratio, s1, s2, force_ascii, full_process
    )


def token_set_ratio(s1, s2, force_ascii=True, full_process=True):
    return _rapidfuzz_scorer(_token_set_ratio, s1, s2, force_ascii, full_process)


def partial_token_set_ratio(s1, s2, force_ascii=True, full_process=True):
    return _rapidfuzz_scorer(
        _partial_token_set_ratio, s1, s2, force_ascii, full_process
    )

def QRatio(s1, s2, force_ascii=True, full_process=True):
    return _rapidfuzz_scorer(_QRatio, s1, s2, force_ascii, full_process)


def UQRatio(s1, s2, full_process=True):
    return QRatio(s1, s2, force_ascii=False, full_process=full_process)


# w is for weighted
def WRatio(s1, s2, force_ascii=True, full_process=True):
    return _rapidfuzz_scorer(_WRatio, s1, s2, force_ascii, full_process)


def UWRatio(s1, s2, full_process=True):
    return WRatio(s1, s2, force_ascii=False, full_process=full_process)

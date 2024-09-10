from . import match
from . import utils
import logging
from rapidfuzz import fuzz as rfuzz
from rapidfuzz import process as rprocess
from functools import partial

_logger = logging.getLogger(__name__)

default_scorer = match.WRatio
default_processor = utils.full_process


def _get_processor(processor, scorer):
    if scorer not in (match.WRatio, match.QRatio,
                      match.token_set_ratio, match.token_sort_ratio,
                      match.partial_token_set_ratio, match.partial_token_sort_ratio,
                      match.UWRatio, match.UQRatio):
        return processor

    force_ascii = scorer not in [match.UWRatio, match.UQRatio]
    pre_processor = partial(utils.full_process, force_ascii=force_ascii)

    if not processor or processor == utils.full_process:
        return pre_processor

    def wrapper(s):
        return pre_processor(processor(s))

    return wrapper

_scorer_lowering = {
    match.ratio: rfuzz.ratio,
    match.partial_ratio: rfuzz.partial_ratio,
    match.token_set_ratio: rfuzz.token_set_ratio,
    match.token_sort_ratio: rfuzz.token_sort_ratio,
    match.partial_token_set_ratio: rfuzz.partial_token_set_ratio,
    match.partial_token_sort_ratio: rfuzz.partial_token_sort_ratio,
    match.WRatio: rfuzz.WRatio,
    match.QRatio: rfuzz.QRatio,
    match.UWRatio: rfuzz.WRatio,
    match.UQRatio: rfuzz.QRatio,
}


def _get_scorer(scorer):
    def wrapper(s1, s2, score_cutoff=0):
        return scorer(s1, s2)

    return _scorer_lowering.get(scorer, wrapper)


def _preprocess_query(query, processor):
    processed_query = processor(query) if processor else query
    if len(processed_query) == 0:
        _logger.warning("Applied processor reduces input query to empty string, "
                        "all comparisons will have score 0. "
                        f"[Query: \'{query}\']")

    return processed_query


def extractWithoutOrder(query, choices, processor=default_processor, scorer=default_scorer, score_cutoff=0):
    is_mapping = hasattr(choices, "items")
    is_lowered = scorer in _scorer_lowering

    query = _preprocess_query(query, processor)
    it = rprocess.extract_iter(
        query, choices,
        processor=_get_processor(processor, scorer),
        scorer=_get_scorer(scorer),
        score_cutoff=score_cutoff
    )

    for choice, score, key in it:
        if is_lowered:
            score = int(round(score))

        yield (choice, score, key) if is_mapping else (choice, score)


def extract(query, choices, processor=default_processor, scorer=default_scorer, limit=5):
    return extractBests(query, choices, processor=processor, scorer=scorer, limit=limit)


def extractBests(query, choices, processor=default_processor, scorer=default_scorer, score_cutoff=0, limit=5):
    is_mapping = hasattr(choices, "items")
    is_lowered = scorer in _scorer_lowering

    query = _preprocess_query(query, processor)
    results = rprocess.extract(
        query, choices,
        processor=_get_processor(processor, scorer),
        scorer=_get_scorer(scorer),
        score_cutoff=score_cutoff,
        limit=limit
    )

    for i, (choice, score, key) in enumerate(results):
        if is_lowered:
            score = int(round(score))

        results[i] = (choice, score, key) if is_mapping else (choice, score)

    return results


def extractOne(query, choices, processor=default_processor, scorer=default_scorer, score_cutoff=0):
    is_mapping = hasattr(choices, "items")
    is_lowered = scorer in _scorer_lowering

    query = _preprocess_query(query, processor)
    res = rprocess.extractOne(
        query, choices,
        processor=_get_processor(processor, scorer),
        scorer=_get_scorer(scorer),
        score_cutoff=score_cutoff
    )

    if res is None:
        return res

    choice, score, key = res

    if is_lowered:
        score = int(round(score))

    return (choice, score, key) if is_mapping else (choice, score)


def dedupe(contains_dupes, threshold=70, scorer=match.token_set_ratio):
    deduped = set()
    for item in contains_dupes:
        matches = extractBests(item, contains_dupes, scorer=scorer, score_cutoff=threshold, limit=None)
        deduped.add(max(matches, key=lambda x: (len(x[0]), x[0]))[0])

    return list(deduped) if len(deduped) != len(contains_dupes) else contains_dupes

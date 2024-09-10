from rapidfuzz.utils import default_process as _default_process

translation_table = {i: None for i in range(128, 256)}


def ascii_only(s):
    return s.translate(translation_table)


def full_process(s, force_ascii=False):
    if force_ascii:
        s = ascii_only(str(s))
    return _default_process(s)

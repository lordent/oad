import collections


def dict_merge(d1, d2):
    d = dict(**d1)
    for k, v in d2.items():
        if (k in d and isinstance(d[k], dict)
                and isinstance(d2[k], collections.Mapping)):
            d[k] = dict_merge(d[k], d2[k])
        elif k in d and isinstance(d[k], list):
            d[k] = d[k] + v
        else:
            d[k] = d2[k]
    return d

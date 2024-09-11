import numpy as np


def flatten_list(lst):
    """
    this is the fastest
    """
    out = []
    for sublist in lst:
        out.extend(sublist)
    return out


def make_mask(size, idx_true=None):
    """
    Creates a boolean mask from a list of indices.

    :param size: The total size of the array.
    :param idx_true: A list of indices to be returned as True in the mask.
    :return: A boolean mask array of the specified size.
    """
    if idx_true is None:
        idx_true = list(range(size))

    mask = np.zeros(size, dtype=bool)
    mask[idx_true] = True
    return mask


def sort_by(list_to_sort, list_to_sort_by, descend=True):
    """
    sort one list by another list
    :param list list_to_sort:
    :param list list_to_sort_by:
    :param bool descend:
    :return list sorted_list:
    """

    sorted_lists = [
        (cid, did) for did, cid in sorted(zip(list_to_sort_by, list_to_sort))
    ]
    if descend:
        sorted_lists = sorted_lists[::-1]
    ordered = np.array(sorted_lists)[:, 0]
    ordered_by = np.array(sorted_lists)[:, 1]

    return list(ordered), list(ordered_by)


def rewrite_array_as_list_for_plotting(array):
    """function for restructuring data so it can be plotted more efficiently by matplotlib. Converts the input array
        into a list of lines separated by None values. NOTE: this means that all lines are together represented as a single
        line. Using this data structure to plot will, therefore, reduce the extent to which individual lines can be accessed
        by matplotlib.

    ==================   ==================
    line number              data
    ==================   ==================
    0                    1.8, 1.2, 1.6, 0.7
    1                    0.8, 1.2, 1.5, 0.9
    ==================   ==================

    will become

    ==================   ============================================
    line number              data
    ==================   ============================================
    0                    1.8, 1.2, 1.6, 0.7, None, 0.8, 1.2, 1.5, 0.9
    ==================   ============================================

    :param array array: the data you wish to plot
    :return x: the data as one None-separated line
    :return y: a list of indices to plot alongside
    """

    y = []
    x = []
    for item in array:
        y.extend(list(item))
        y.append(None)
        x.extend(list(range(len(item))))
        x.append(None)
    return x, y



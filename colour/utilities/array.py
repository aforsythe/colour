#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Array Utilities
===============

Defines array utilities objects.
"""

from __future__ import division, unicode_literals

import numpy as np

from colour.utilities import CaseInsensitiveMapping, is_iterable

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013 - 2015 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['as_array',
           'as_numeric',
           'as_stack',
           'as_shape',
           'closest',
           'normalise',
           'steps',
           'is_uniform',
           'row_as_diagonal']


def as_array(x, shape=None, data_type=np.float_):
    """
    Converts given :math:`x` variable to *ndarray*.

    Parameters
    ----------
    x : object
        Variable to convert.
    shape : tuple, optional
        *ndarray* shape.
    data_type : dtype, optional
        *ndarray* data type.

    Returns
    -------
    ndarray
        :math:`x` variable converted to *ndarray*.

    Examples
    --------
    >>> as_array(1)
    array([ 1.])
    """

    array = (np.asarray(x, dtype=data_type)
             if is_iterable(x) else
             np.asarray((x,), dtype=data_type))

    if shape is not None:
        array = array.reshape(shape)

    return array


def as_numeric(x):
    """
    Converts given :math:`x` variable to *numeric*. In the event where
    :math:`x` cannot be converted, it is passed as is.

    Parameters
    ----------
    x : object
        Variable to convert.

    Returns
    -------
    ndarray
        :math:`x` variable converted to *numeric*.

    See Also
    --------
    as_array, as_stack, as_shape

    Examples
    --------
    >>> as_numeric(np.array([1]))
    1.0
    >>> as_numeric(np.arange(10))
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    """

    try:
        return float(x)
    except TypeError as error:
        return x


def as_stack(x, direction='Depth', squeeze=True, shape=None):
    """
    Converts given :math:`x` variable to a stack with given direction. The
    stack can be squeezed so that single-dimensional entries from the resulting
    *ndarray* shape are removed. It is also possible to pass an arbitrary
    compatible shape for the final resulting *ndarray* shape.

    Parameters
    ----------
    x : object
        Variable to convert.
    direction : unicode, optional
        {'Depth', 'D', 'Horizontal', 'H', 'Vertical', 'V', 'Ignore', 'I'}
        Stack direction.
    squeeze : bool, optional
        Squeeze resulting *ndarray*.
    shape : array_like, optional
        Arbitrary compatible shape for the final resulting *ndarray*.

    Returns
    -------
    ndarray
        :math:`x` variable converted to a stack.

    See Also
    --------
    as_array, as_numeric, as_shape

    Examples
    --------
    Using various depth directions:

    >>> x = np.array([[1, 2, 3], [4, 5, 6]])
    >>> as_stack(x)
    array([[1, 4],
           [2, 5],
           [3, 6]])
    >>> as_stack(x, 'Depth')
    array([[1, 4],
           [2, 5],
           [3, 6]])
    >>> as_stack(x, 'Horizontal')
    array([1, 2, 3, 4, 5, 6])
    >>> as_stack(x, 'Vertical')
    array([[1, 2, 3],
           [4, 5, 6]])

    Squeezing single-dimensional entries:

    >>> x = np.array([[[1, 2, 3], [4, 5, 6]]])
    >>> as_stack(x)
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> as_stack(x, squeeze=False)
    array([[[1],
            [2],
            [3]],
    <BLANKLINE>
           [[4],
            [5],
            [6]]])

    Altering the shape of the resulting *ndarray*:

    >>> x = np.array([[1, 2, 3], [4, 5, 6]])
    >>> as_stack(x)
    array([[1, 4],
           [2, 5],
           [3, 6]])
    >>> as_stack(x, shape=(2, 3))
    array([[1, 4, 2],
           [5, 3, 6]])
    """

    methods = CaseInsensitiveMapping(
        {'Depth': np.dstack,
         'D': np.dstack,
         'Horizontal': np.hstack,
         'H': np.hstack,
         'Vertical': np.vstack,
         'V': np.vstack,
         'Ignore': lambda x: x,
         'I': lambda x: x})

    x = methods.get(direction)(x)

    if squeeze:
        x = np.squeeze(x)

    if shape is not None:
        x = x.reshape(shape)

    return x


def as_shape(x):
    """
    Returns the shape of given :math:`x`. In the event where :math:`x` shape
    cannot be retrieved because the object is not a *ndarray* sub-class, *None*
    is returned.

    Parameters
    ----------
    x : object
        Variable to retrieve the shape of.

    Returns
    -------
    tuple or None
        Shape of :math:`x` variable if any.

    See Also
    --------
    as_array, as_numeric, as_stack

    Examples
    --------
    >>> as_shape(np.array([1, 2, 3]))
    (3,)
    >>> as_shape(1)
    """

    try:
        return x.shape
    except AttributeError:
        return None


def closest(y, x):
    """
    Returns closest :math:`y` variable element to reference :math:`x` variable.

    Parameters
    ----------
    y : array_like
        Variable to search for the closest element.
    x : numeric
        Reference variable.

    Returns
    -------
    numeric
        Closest :math:`y` variable element.

    Examples
    --------
    >>> y = np.array([24.31357115, 63.62396289, 55.71528816, 62.70988028, 46.84480573, 25.40026416])  # noqa
    >>> closest(y, 63)
    62.70988028
    """

    return y[(np.abs(np.array(y) - x)).argmin()]


def normalise(x, factor=1, clip=True):
    """
    Normalises given *array_like* :math:`x` variable values and optionally clip
    them between.

    Parameters
    ----------
    x : array_like
        :math:`x` variable to normalise.
    factor : numeric, optional
        Normalization factor
    clip : bool, optional
        Clip values between in domain [0, 'factor'].

    Returns
    -------
    ndarray
        Normalised :math:`x` variable.

    Examples
    --------
    >>> x = np.array([0.48224885, 0.31651974, 0.22070513])
    >>> normalise(x)  # doctest: +ELLIPSIS
    array([ 1.        ,  0.6563411...,  0.4576581...])
    """

    x = as_array(x)
    maximum = np.max(x)
    x *= (1 / maximum) * factor
    return np.clip(x, 0, factor) if clip else x


def steps(distribution):
    """
    Returns the steps of given distribution.

    Parameters
    ----------
    distribution : array_like
        Distribution to retrieve the steps.

    Returns
    -------
    tuple
        Distribution steps.

    Examples
    --------
    Uniformly spaced variable:

    >>> y = np.array([1, 2, 3, 4, 5])
    >>> steps(y)
    (1,)

    Non-uniformly spaced variable:

    >>> y = np.array([1, 2, 3, 4, 8])
    >>> steps(y)
    (1, 4)
    """

    return tuple(set([distribution[i + 1] - distribution[i]
                      for i in range(len(distribution) - 1)]))


def is_uniform(distribution):
    """
    Returns if given distribution is uniform.

    Parameters
    ----------
    distribution : array_like
        Distribution to check for uniformity.

    Returns
    -------
    bool
        Is distribution uniform.

    Examples
    --------
    Uniformly spaced variable:

    >>> y = np.array([1, 2, 3, 4, 5])
    >>> is_uniform(y)
    True

    Non-uniformly spaced variable:

    >>> y = np.array([1, 2, 3.1415, 4, 5])
    >>> is_uniform(y)
    False
    """

    return True if len(steps(distribution)) == 1 else False


def row_as_diagonal(a):
    """
    Returns the per row diagonal matrices of the given array.

    Parameters
    ----------
    a : array_like
        Array to perform the diagonal matrices computation.

    Returns
    -------
    ndarray

    References
    ----------
    .. [1]  Castro, S. (2014). Numpy: Fastest way of computing diagonal for
            each row of a 2d array. Retrieved August 22, 2014, from
            http://stackoverflow.com/questions/26511401/numpy-fastest-way-of-computing-diagonal-for-each-row-of-a-2d-array/26517247#26517247  # noqa

    Examples
    --------
    >>> a = np.array([[0.25891593, 0.07299478, 0.36586996],
    ...               [0.30851087, 0.37131459, 0.16274825],
    ...               [0.71061831, 0.67718718, 0.09562581],
    ...               [0.71588836, 0.76772047, 0.15476079],
    ...               [0.92985142, 0.22263399, 0.88027331]])
    >>> row_as_diagonal(a)
    array([[[ 0.25891593,  0.        ,  0.        ],
            [ 0.        ,  0.07299478,  0.        ],
            [ 0.        ,  0.        ,  0.36586996]],
    <BLANKLINE>
           [[ 0.30851087,  0.        ,  0.        ],
            [ 0.        ,  0.37131459,  0.        ],
            [ 0.        ,  0.        ,  0.16274825]],
    <BLANKLINE>
           [[ 0.71061831,  0.        ,  0.        ],
            [ 0.        ,  0.67718718,  0.        ],
            [ 0.        ,  0.        ,  0.09562581]],
    <BLANKLINE>
           [[ 0.71588836,  0.        ,  0.        ],
            [ 0.        ,  0.76772047,  0.        ],
            [ 0.        ,  0.        ,  0.15476079]],
    <BLANKLINE>
           [[ 0.92985142,  0.        ,  0.        ],
            [ 0.        ,  0.22263399,  0.        ],
            [ 0.        ,  0.        ,  0.88027331]]])
    """

    rd = np.zeros((a.shape[0], a.shape[1], a.shape[1]))
    diagonal = np.arange(a.shape[1])
    rd[:, diagonal, diagonal] = a

    return rd


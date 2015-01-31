#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common Constants
================

Defines common constants objects that don't belong to any specific category.
"""

from __future__ import division, unicode_literals

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013 - 2015 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['FLOATING_POINT_NUMBER_PATTERN',
           'INTEGER_THRESHOLD']

FLOATING_POINT_NUMBER_PATTERN = '[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
"""
Floating point number regex matching pattern.

FLOATING_POINT_NUMBER_PATTERN : unicode
"""

INTEGER_THRESHOLD = 0.001
"""
Integer threshold value.

INTEGER_THRESHOLD : numeric
"""
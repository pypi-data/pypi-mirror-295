# -*- coding: utf-8 -*-
"""
    pip_services4_commons.exec.IParameterized
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for parameterized components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC

from ..exec.Parameters import Parameters


class IParameterized(ABC):
    """
    Interface for components that require execution parameters.
    """

    def set_parameters(self, parameters: Parameters):
        """
        Sets execution parameters.

        :param parameters: execution parameters.
        """
        raise NotImplementedError('Method from interface definition')

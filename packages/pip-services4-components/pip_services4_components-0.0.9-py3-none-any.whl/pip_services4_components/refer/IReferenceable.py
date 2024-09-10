# -*- coding: utf-8 -*-
"""
    pip_services4_commons.refer.IReferenceable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for referenceable components.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC

from ..refer import IReferences


class IReferenceable(ABC):
    """
    Interface for components that depends on obj components.
    If component requires explicit notification to unset references
    it shall additionally implement :class:`IUnreferenceable <pip_services4_compoents.refer.IUnreferenceable.IUnreferenceable>` interface.

    Example:

    .. code-block:: python
    
        class MyController(IReferenceable):
            _persistence = None

            def set_references(self, references):
                self._persistence = references.get_one_required(Descriptor("mygroup", "persistence", "*", "*", "1.0"))
    """

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        raise NotImplementedError('Method from interface definition')

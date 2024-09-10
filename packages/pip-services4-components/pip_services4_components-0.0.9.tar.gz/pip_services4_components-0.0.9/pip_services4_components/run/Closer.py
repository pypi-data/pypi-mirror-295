# -*- coding: utf-8 -*-
"""
    pip_services4_commons.exec.Closer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Closer component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Any, List, Optional

from pip_services4_components.context.IContext import IContext

from .IClosable import IClosable


class Closer:
    """
    Helper class that closes previously opened components.
    """

    @staticmethod
    def close_one(context: Optional[IContext], component: Any):
        """
        Closes specific component.

        To be closed components must implement :class:`IClosable <pip_services4_components.run.IClosable.IClosable>` interface.
        If they don't the call to this method has no effect.

        :param context: (optional) transaction id to trace execution through call chain.

        :param component: the component that is to be closed.
        """
        if isinstance(component, IClosable):
            component.close(context)

    @staticmethod
    def close(context: Optional[IContext], components: List[Any]):
        """
        Closes multiple components.

        To be closed components must implement :class:`IClosable <pip_services4_components.run.IClosable.IClosable>` interface.
        If they don't the call to this method has no effect.

        :param context: (optional) transaction id to trace execution through call chain.

        :param components: the list of components that are to be closed.
        """
        if components is None:
            return

        for component in components:
            Closer.close_one(context, component)

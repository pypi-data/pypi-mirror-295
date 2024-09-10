# -*- coding: utf-8 -*-
"""
    pip_services4_commons.config.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Contains the implementation of the config design pattern.
    The :class:`IConfigurable <pip_services4_components.config.IConfigurable.IConfigurable>` configurable interface
    contains just one method - "configure", which takes ConfigParams as a parameter (extends StringValueMap class).
    If any object needs to be configurable, we implement this interface
    and parse the ConfigParams that the method received.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [
    'IConfigurable', 'IReconfigurable', 'ConfigParams',
    'NameResolver', 'OptionsResolver'
]

from .ConfigParams import ConfigParams
from .IConfigurable import IConfigurable
from .IReconfigurable import IReconfigurable
from .NameResolver import NameResolver
from .OptionsResolver import OptionsResolver

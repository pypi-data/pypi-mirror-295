#!/usr/bin/env python3
"""


See EOF for license/metadata/notes as applicable
"""

##-- builtin imports
from __future__ import annotations

# import abc
import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import types
import weakref
# from copy import deepcopy
# from dataclasses import InitVar, dataclass, field
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable, Generator)
from uuid import UUID, uuid1

##-- end builtin imports

##-- lib imports
# import more_itertools as mitz
# from boltons import
##-- end lib imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

from jgdv.enums.util import EnumBuilder_m, FlagsBuilder_m

class TaskStateEnum(EnumBuilder_m, enum.Enum):
    """
      Enumeration of the different states a task can be in.
    """
    TEARDOWN        = enum.auto()
    SUCCESS         = enum.auto()
    FAILED          = enum.auto()
    HALTED          = enum.auto()
    WAIT            = enum.auto()
    READY           = enum.auto()
    RUNNING         = enum.auto()
    EXISTS          = enum.auto()
    INIT            = enum.auto()

    DEFINED         = enum.auto()
    DECLARED        = enum.auto()
    ARTIFACT        = enum.auto()

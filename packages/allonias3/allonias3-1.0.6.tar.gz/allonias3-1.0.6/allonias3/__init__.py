from __future__ import annotations

import logging

import dill  # nosec

logger = logging.getLogger("allonias3")

# Monckey patch to allow loading a pickled class even if some modules are
# missing

_old_find_class = dill._dill.Unpickler.find_class  # noqa: SLF001


class DummyObject:
    def __init__(self, *args, **kwargs):
        pass


def _custom_find_class(*args, **kwargs):
    try:
        return _old_find_class(*args, **kwargs)
    except ModuleNotFoundError as e:
        logger.warning(
            f"Could not unpickle the object correctly : {e}. It might not be "
            f"usabe."
        )
        return DummyObject


dill._dill.Unpickler.find_class = _custom_find_class  # noqa: SLF001

from .configs import Configs  # noqa: E402
from .s3_path import S3Path  # noqa: E402

__all__ = ["S3Path", "Configs"]

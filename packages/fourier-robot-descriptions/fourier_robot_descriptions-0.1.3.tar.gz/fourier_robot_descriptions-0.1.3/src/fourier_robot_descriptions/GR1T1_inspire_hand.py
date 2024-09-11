"""GR1T2 description."""

from os import getenv as _getenv
from os import path as _path

from ._cache import clone_to_cache as _clone_to_cache

REPOSITORY_PATH: str = _clone_to_cache(
    "fourier_grx_descriptions",
    commit=_getenv("ROBOT_DESCRIPTION_COMMIT", None),
)

PACKAGE_PATH: str = _path.join(REPOSITORY_PATH, "GRX/GR1/GR1T1/URDF")

URDF_PATH: str = _path.join(PACKAGE_PATH, "urdf", "GR1T1_inspire_hand.urdf")

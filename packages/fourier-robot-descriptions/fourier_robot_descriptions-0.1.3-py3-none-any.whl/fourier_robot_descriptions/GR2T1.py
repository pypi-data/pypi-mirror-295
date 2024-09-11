"""GR1T2 description."""

from os import getenv as _getenv
from os import path as _path

from ._cache import clone_to_cache as _clone_to_cache

REPOSITORY_PATH: str = _clone_to_cache(
    "fourier_grx_descriptions_private",
    commit=_getenv("ROBOT_DESCRIPTION_COMMIT", None),
)

PACKAGE_PATH: str = _path.join(REPOSITORY_PATH, "GRX/GR2/GR2T1/URDF/GR2T1")

URDF_PATH: str = _path.join(PACKAGE_PATH, "urdf", "robot.urdf")

import pytest

from h2lib._h2lib import H2Lib
from h2lib_tests.test_files import tfp

from .test_write_htc import write_dtu10mw_only_tower


def test_init_static_solver(write_dtu10mw_only_tower):
    with H2Lib() as h2:
        # Load a basic model.
        model_path = tfp + "DTU_10_MW/"
        h2.init("htc/DTU_10MW_RWT_only_tower.htc", model_path)

        # First execution is fine.
        h2.init_static_solver()

        # The next should give an error.
        with pytest.raises(RuntimeError, match="STATIC_SOLVER_ALREADY_INITIALIZED"):
            h2.init_static_solver()

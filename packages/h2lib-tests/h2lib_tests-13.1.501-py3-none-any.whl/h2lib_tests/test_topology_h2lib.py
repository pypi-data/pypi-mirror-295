from h2lib._h2lib import H2Lib

from numpy import testing as npt
from h2lib_tests.test_files import tfp
import numpy as np
import pytest
from .test_write_htc import (
    write_dtu10mw_only_tower,
    write_dtu10mw_only_tower_rotated,
    write_dtu10mw_only_tower_encrypted
)


@pytest.fixture(scope="module")
def h2_dtu_10mw_only_tower(write_dtu10mw_only_tower):
    h2 = H2Lib(suppress_output=True)
    model_path = f"{tfp}DTU_10_MW/"
    htc_path = "htc/DTU_10MW_RWT_only_tower.htc"
    h2.init(htc_path=htc_path, model_path=model_path)
    yield h2
    h2.close()


@pytest.fixture(scope="module")
def h2_dtu_10mw_only_tower_rotated(write_dtu10mw_only_tower_rotated):
    h2 = H2Lib(suppress_output=True)
    model_path = f"{tfp}DTU_10_MW/"
    htc_path = "htc/DTU_10MW_RWT_only_tower_rotated.htc"
    h2.init(htc_path=htc_path, model_path=model_path)
    yield h2
    h2.close()


@pytest.fixture(scope="module")
def h2_dtu_10mw_only_tower_encrypted(write_dtu10mw_only_tower_encrypted):
    h2 = H2Lib(suppress_output=True)
    model_path = f"{tfp}DTU_10_MW/"
    htc_path = "htc/DTU_10MW_RWT_only_tower_encrypted.htc"
    h2.init(htc_path=htc_path, model_path=model_path)
    yield h2
    h2.close()


def test_number_of_bodies_and_constraints(
    h2_dtu_10mw_only_tower,
):
    nbdy, ncst = h2_dtu_10mw_only_tower.get_number_of_bodies_and_constraints()
    assert nbdy == 3
    assert ncst == 9


def test_number_of_bodies_and_constraints_encrypted(
    h2_dtu_10mw_only_tower_encrypted,
):
    with pytest.raises(RuntimeError, match="STRUCTURE_IS_CONFIDENTIAL"):
        h2_dtu_10mw_only_tower_encrypted.get_number_of_bodies_and_constraints()


def test_get_number_of_elements(h2_dtu_10mw_only_tower):
    nelem = h2_dtu_10mw_only_tower.get_number_of_elements()
    npt.assert_array_equal(nelem, np.array([3, 3, 4]))


def test_get_number_of_elements_encrypted(
    h2_dtu_10mw_only_tower_encrypted,
):
    # This test is not really needed, since the check for confidential structure
    # is already done by test_number_of_bodies_and_constraints_encrypted().
    with pytest.raises(RuntimeError, match="STRUCTURE_IS_CONFIDENTIAL"):
        h2_dtu_10mw_only_tower_encrypted.get_number_of_elements()


def test_get_timoshenko_location(
    h2_dtu_10mw_only_tower,
):
    # Test first element.
    l, r1, r12, tes = h2_dtu_10mw_only_tower.get_timoshenko_location(ibdy=0, ielem=0)
    assert l - 11.5 < 1e-14
    npt.assert_array_equal(r1, np.array([0.0, 0.0, 0]))
    npt.assert_array_almost_equal_nulp(r12, np.array([0.0, 0.0, -11.5]))
    npt.assert_array_equal(
        tes,
        np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]]),
    )

    # Test last element.
    l, r1, r12, tes = h2_dtu_10mw_only_tower.get_timoshenko_location(ibdy=2, ielem=3)
    assert l - 12.13 < 1e-14
    npt.assert_array_almost_equal_nulp(r1, np.array([0.0, 0.0, -34.5]))
    npt.assert_array_almost_equal_nulp(r12, np.array([0.0, 0.0, -12.13]), nulp=3)
    npt.assert_array_equal(
        tes,
        np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]]),
    )


def test_get_timoshenko_location_body_does_not_exist(
    h2_dtu_10mw_only_tower,
):
    with pytest.raises(IndexError, match="BODY_DOES_NOT_EXIST"):
        h2_dtu_10mw_only_tower.get_timoshenko_location(ibdy=1000, ielem=0)


def test_get_timoshenko_location_element_does_not_exist(
    h2_dtu_10mw_only_tower,
):
    with pytest.raises(IndexError, match="ELEMENT_DOES_NOT_EXIST"):
        h2_dtu_10mw_only_tower.get_timoshenko_location(ibdy=0, ielem=1000)


def test_get_timoshenko_location_encrypted(
    h2_dtu_10mw_only_tower_encrypted,
):
    with pytest.raises(RuntimeError, match="STRUCTURE_IS_CONFIDENTIAL"):
        h2_dtu_10mw_only_tower_encrypted.get_timoshenko_location(ibdy=0, ielem=0)


def test_get_body_rotation_tensor_1(h2_dtu_10mw_only_tower):
    amat = h2_dtu_10mw_only_tower.get_body_rotation_tensor(ibdy=0)
    npt.assert_array_equal(amat, np.eye(3))


def test_get_body_rotation_tensor_2(
    h2_dtu_10mw_only_tower_rotated, write_dtu10mw_only_tower_rotated
):
    amat = h2_dtu_10mw_only_tower_rotated.get_body_rotation_tensor(ibdy=0)
    _, alpha = write_dtu10mw_only_tower_rotated
    alpha_rad = np.deg2rad(alpha)
    sa = np.sin(alpha_rad)
    ca = np.cos(alpha_rad)
    npt.assert_array_almost_equal_nulp(
        amat, np.array([[1.0, 0.0, 0.0], [0.0, ca, -sa], [0.0, sa, ca]])
    )


def test_get_body_rotation_tensor_body_does_not_exist(h2_dtu_10mw_only_tower):
    with pytest.raises(IndexError, match="BODY_DOES_NOT_EXIST"):
        h2_dtu_10mw_only_tower.get_body_rotation_tensor(ibdy=1000)


def test_get_body_rotation_tensor_encrypted(h2_dtu_10mw_only_tower_encrypted):
    with pytest.raises(RuntimeError, match="STRUCTURE_IS_CONFIDENTIAL"):
        h2_dtu_10mw_only_tower_encrypted.get_body_rotation_tensor(ibdy=0)

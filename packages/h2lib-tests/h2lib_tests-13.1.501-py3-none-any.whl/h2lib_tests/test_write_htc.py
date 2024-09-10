import pytest
from wetb.hawc2.htc_file import HTCFile
from h2lib_tests.test_files import tfp


@pytest.fixture(scope="module")
def write_dtu10mw_only_tower():
    # Start from DTU_10MW_RWT and delete everything except the tower.
    htc = HTCFile(tfp + "DTU_10_MW/htc/DTU_10MW_RWT.htc")
    htc.set_name("DTU_10MW_RWT_only_tower")
    for key1 in htc["new_htc_structure"].keys():
        if key1.startswith("main_body"):
            if "tower" not in htc["new_htc_structure"][key1]["name"].values:
                htc["new_htc_structure"][key1].delete()
        if key1 == "orientation":
            for key2 in htc["new_htc_structure"]["orientation"].keys():
                if key2.startswith("relative"):
                    htc["new_htc_structure"]["orientation"][key2].delete()
        if key1 == "constraint":
            for key2 in htc["new_htc_structure"]["constraint"].keys():
                if key2 != "fix0":
                    htc["new_htc_structure"]["constraint"][key2].delete()
    htc["wind"].delete()
    htc["aerodrag"].delete()
    htc["aero"].delete()
    htc["dll"].delete()
    htc["output"].delete()
    # Reduce simulation time.
    htc.simulation.time_stop = 10.0
    # Change number of bodies in the tower.
    htc.new_htc_structure.main_body.nbodies = 3
    # Save the new file.
    htc.save()
    return htc


@pytest.fixture(scope="module")
def write_dtu10mw_only_tower_rotated(write_dtu10mw_only_tower):
    # Start from the DTU_10MW_RWT_only_tower and rotate the tower.
    htc = write_dtu10mw_only_tower.copy()
    htc.set_name("DTU_10MW_RWT_only_tower_rotated")
    alpha = 30.0
    htc.new_htc_structure.orientation.base.body_eulerang = [
        alpha,
        0.0,
        0.0,
    ]
    htc.save()
    return (htc, alpha)


@pytest.fixture(scope="module")
def write_dtu10mw_only_tower_encrypted(write_dtu10mw_only_tower):
    # Start from the DTU_10MW_RWT_only_tower and then encrypt the tower.
    htc = write_dtu10mw_only_tower.copy()
    htc.set_name("DTU_10MW_RWT_only_tower_encrypted")
    # Only the tower is left.
    htc.new_htc_structure.main_body.timoschenko_input.filename = "./data/DTU_10MW_RWT_Tower_st.dat.v3.enc"
    htc.save()

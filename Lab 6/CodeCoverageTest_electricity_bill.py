import pytest

from electricity_bill import energy_charge, late_fee, subsidy


def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200


def test_paid_on_time():
    assert late_fee(500, 0) == 0


def test_energy_charge_boundaries_and_connections():
    assert energy_charge(0, "domestic") == 50
    assert energy_charge(99, "domestic") == 347
    assert energy_charge(100, "domestic") == 350
    assert energy_charge(101, "domestic") == 355
    assert energy_charge(299, "domestic") == 1345
    assert energy_charge(300, "domestic") == 1350
    assert energy_charge(301, "domestic") == 1358
    assert energy_charge(100, "commercial") == 750
    assert energy_charge(301, "commercial") == 2766


def test_energy_charge_rejects_invalid_input():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(10, "industrial")
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")


def test_late_fee_boundaries_and_surcharge():
    assert late_fee(500, -1) == 0
    assert late_fee(500, 1) == 50
    assert late_fee(500, 15) == 50
    assert late_fee(500, 16) == 100
    assert late_fee(2000, 16) == 100
    assert late_fee(2500, 16) == 225


def test_subsidy_combinations():
    assert subsidy(101, False, False) == 0
    assert subsidy(100, True, False) == 50
    assert subsidy(100, False, False) == 0
    assert subsidy(100, True, True) == 150
    assert subsidy(300, False, True) == 100
    assert subsidy(301, False, True) == 0
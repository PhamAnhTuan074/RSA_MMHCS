from core.factor_demo import (
    factor_n_demo,
    fast_mod_exp,
    fast_mod_exp_detailed_steps,
)


def test_tc06_fast_mod_exp():
    assert fast_mod_exp(72, 17, 3233) == pow(72, 17, 3233)


def test_tc07_factor_n():
    result = factor_n_demo(3233)
    assert result["success"]
    assert {result["p"], result["q"]} == {53, 61}


def test_detailed_fast_power_example_from_source_document():
    rows = fast_mod_exp_detailed_steps(4, 3, 33)
    assert rows[-1]["k sau bước"] == "Kết quả cuối = 31"
    assert rows[0]["b bước sau"] == "1"


def test_medium_example_from_source_document():
    assert fast_mod_exp(123, 19, 14933) == 3621
    assert fast_mod_exp(3621, 13915, 14933) == 123
